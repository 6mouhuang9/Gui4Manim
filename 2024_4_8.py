
import json
import subprocess
from sympy import latex,sympify

def convert_to_latex(tex_string):
    #利用 sympy 将包含数学表达式的字符串转换为 LaTeX 格式。
    try:
        # 尝试将给定字符串解析为 sympy 表达式
        expr = sympify(tex_string)
        # 将 sympy 表达式转换为 LaTeX
        latex_expr = latex(expr)
        return latex_expr
    except Exception as e:
        print(f"转换为 LaTeX 时出错：{e}")
        return tex_string

def generate_transform_code(data):
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
                converted_latex = convert_to_latex(value)
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
    
    for i in range(0, len(object_names) - 1, 2):
        source_obj = object_names[i]
        target_obj = object_names[i + 1]
        code += f"        self.play(Transform({source_obj}, {target_obj}), run_time = 5)\n"
        code += "        self.wait(3)\n"
    
    return code

def generate_replacementtransform_code(data):
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
        
        #这里是我打错了，不过之后的中文化也能这么处理
        #if obj_type == "Mathtex":
        #   obj_type = "MathTex"  # 调整名称以匹配Manim类名

        # 生成对象的创建代码
        params_code = []
        for key, value in params.items():
            if key == "tex_string":
                # 特殊处理tex_string参数,将 tex_string 转换为 LaTeX 格式
                converted_latex = convert_to_latex(value)
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
    # 假设我们知道哪些对象要进行变换
    for i in range(0, len(object_names) - 1, 2):
        source_obj = object_names[i]
        target_obj = object_names[i + 1]
        code += f"        self.play(ReplacementTransform({source_obj}, {target_obj}), run_time = 5)\n"
        code += "        self.wait(3)\n"
    
    return code

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

json_data = load_json_file('transform_data.json')
manim_code = generate_transform_code(json_data)

# 生成manim代码文件
with open("manim_code_4_8.py", "w") as f:
    f.write(manim_code)
subprocess.run(["manim", "-pql", "manim_code_4_8.py", "MyScene"])
