import tkinter as tk
from tkinter import ttk, simpledialog
import os
import json
from transform_objects_params_final import TRANSFORM_OBJECTS_PARAMS
import json
import subprocess
from sympy import latex, sympify

class TransformAnimationConfigurator:

    def __init__(self, TRANSFORM_OBJECTS_PARAMS):
        self.TRANSFORM_OBJECTS_PARAMS = TRANSFORM_OBJECTS_PARAMS
        self.objects = []
        self.object_count = 0
        self.root = None
        self.manim_script_path = "manim_code_4_8.py"
        self.json_file_path = 'transform_data.json'

    def run(self):
        self.object_count = simpledialog.askinteger("输入", "请输入对象的数量:", minvalue=1)
        if self.object_count:
            self.root = tk.Tk()
            self.root.title("对象参数")
            for i in range(1, self.object_count + 1):
                self.create_object_config(i)

            submit_button = ttk.Button(self.root, text="获取参数并生成动画", command=self.generate_data)
            submit_button.pack(pady=20)
            self.root.mainloop()

    def write_data_to_json_file(self, filename, data):
        """将数据写入JSON文件，如果文件不存在则创建"""
        # 检查文件是否存在，如果不存在则创建
        if not os.path.exists(filename):
            print(f"文件 '{filename}' 不存在，将被创建。")
        else:
            print(f"文件 '{filename}' 已存在，将被覆盖。")
        
        # 写入数据到JSON文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"数据已成功写入到文件: {filename}")
        
    def update_params(self, frame, object_type):
        # 清除旧的参数输入字段
        for widget in frame.winfo_children():
            widget.destroy()

        # 获取选定对象类型的参数
        params = self.TRANSFORM_OBJECTS_PARAMS[object_type]

        # 为每个参数创建标签和输入框
        for param, info in params.items():
            ttk.Label(frame, text=f"{param}:").pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.insert(0, str(info['default']))
            entry.pack(side=tk.LEFT)
            entry.param_name = param  # 将参数名称作为属性添加到Entry组件

    def create_object_config(self, obj_id):
        object_frame = ttk.LabelFrame(self.root, text=f"对象 {obj_id}")
        object_frame.pack(fill='x', expand=True, padx=10, pady=5)

        # 对象类型选择
        object_type_var = tk.StringVar(value=list(self.TRANSFORM_OBJECTS_PARAMS.keys())[0])
        object_type_menu = ttk.OptionMenu(object_frame, object_type_var, *self.TRANSFORM_OBJECTS_PARAMS.keys())
        object_type_menu.pack(side=tk.LEFT)

        # 将StringVar存储为对象帧的属性
        object_frame.object_type_var = object_type_var

        # 参数配置区域
        params_frame = ttk.Frame(object_frame)
        params_frame.pack(fill='x', expand=True, padx=10, pady=5)
        self.update_params(params_frame, object_type_var.get())

        # 当对象类型改变时更新参数配置
        object_type_var.trace_add("write", lambda *args, var=object_type_var, frame=params_frame: self.update_params(frame, var.get()))
    
    def collect_object_params(self):
        self.root = tk.Tk()
        self.root.title("对象参数")
        self.objects = []

        for i in range(1, self.object_count + 1):
            self.create_object_config(i)

        submit_button = ttk.Button(self.root, text="提交", command=self.generate_data)
        submit_button.pack(pady=20)
        
        self.root.mainloop()
    
    def generate_data(self):
            object_frames = [child for child in self.root.winfo_children() if isinstance(child, ttk.LabelFrame)]
            for object_frame in object_frames:
                object_info = {
                    "index": object_frames.index(object_frame) + 1,
                    "type": object_frame.object_type_var.get(),  # 直接从属性中获取
                    "params": {},
                }

                # 收集参数
                params_frame = next((child for child in object_frame.winfo_children() if isinstance(child, ttk.Frame)), None)
                if params_frame:
                    for widget in params_frame.winfo_children():
                        if isinstance(widget, ttk.Entry):
                            param_name = widget.param_name  # 直接从Entry对象获取参数名称
                            object_info["params"][param_name] = widget.get()


                self.objects.append(object_info)

            # 处理收集到的数据，例如打印或保存
            print(self.objects)  # 或者其他处理方式
            #将数据存储到json文件中
            filename = "transform_data.json"
            self.write_data_to_json_file(filename, self.objects)
            self.create_manim_script()
            self.root.destroy()

    def convert_to_latex(self, tex_string):
        try:
            # 检测等号，如果存在，分别处理等号两边的表达式
            if '=' in tex_string:
                left_side, right_side = tex_string.split('=', 1)  # 分割等式
                left_expr = sympify(left_side.strip())  # 处理左侧表达式
                right_expr = sympify(right_side.strip())  # 处理右侧表达式
                latex_expr = latex(left_expr) + " = " + latex(right_expr)  # 转换为 LaTeX
            else:
                # 没有等号的情况，直接转换
                expr = sympify(tex_string)
                latex_expr = latex(expr)

            return latex_expr
        except Exception as e:
            print(f"转换为 LaTeX 时出错：{e}")
            return tex_string
    
    def generate_transform_code(self,data):
        code = "from manim import *\n\n"
        code += "class MyScene(Scene):\n"
        code += "    def construct(self):\n"
        code += "        plane = NumberPlane()\n"
        code += "        self.add(plane)\n"
        
        # 存储所有创建的对象代码以及它们的变量名
        objects_code = []
        object_names = []

        # 遍历数据结构中的每个对象，并生成Manim代码
        for obj in data:
            index = obj["index"]
            obj_type = obj["type"]
            params = obj["params"]
            
            # 根据类型生成对象的构造代码
            obj_name = f"object{index}"
            object_names.append(obj_name)
            
            params_code = []
            for key, value in params.items():
                if key == "tex_string":
                    # 特殊处理tex_string参数
                    converted_latex = self.convert_to_latex(value)
                    params_code.append(f'r"{converted_latex}"')
                elif key == "text":
                    # 特殊处理text参数
                    params_code.append(f'{key}=r"{value}"')
                elif key != "position":
                    params_code.append(f'{key}={value}')

            creation_code = f"{obj_name} = {obj_type}({', '.join(params_code)})\n"
            
            # 如果存在位置参数，则添加移动到指定位置的代码
            if "position" in params:
                position = params["position"]
                creation_code += f"        {obj_name}.move_to({position})\n"
            
            objects_code.append(creation_code)
        
        # 添加对象创建代码到总代码中
        for obj_code in objects_code:
            code += f"        {obj_code}"
        
        # 添加变换动画的代码
        for i in range(0, len(object_names) - 1, 2):
            source_obj = object_names[i]
            target_obj = object_names[i + 1]
            code += f"        self.play(Transform({source_obj}, {target_obj}), run_time = 5)\n"
            code += "        self.wait(3)\n"
        
        return code
        
    
    def load_json_file(self):
        # 方法实现 - 加载JSON文件
        with open(self.json_file_path, 'r') as file:
            json_data = json.load(file)
        return json_data
    
    def create_manim_script(self):
        # 方法实现 - 创建Manim脚本并执行
        json_data = self.load_json_file()
        manim_code = self.generate_transform_code(json_data)
        with open(self.manim_script_path, "w") as f:
            f.write(manim_code)
        subprocess.run(["manim", "-pql", self.manim_script_path, "MyScene"])

#configurator = TransformAnimationConfigurator(TRANSFORM_OBJECTS_PARAMS)
#configurator.run()