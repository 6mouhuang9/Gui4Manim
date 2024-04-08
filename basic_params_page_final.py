import tkinter as tk
from tkinter import ttk, simpledialog
import os
import json
from object_params_final import OBJECTS_PARAMS,animation_params_options

#对于基本动画对象与动画类型参数的获取页面

def update_params(frame, object_type):
    # 清除旧的参数输入字段
    for widget in frame.winfo_children():
        widget.destroy()

    params = OBJECTS_PARAMS[object_type]
    for param, info in params.items():
        ttk.Label(frame, text=f"{param}:").pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.insert(0, str(info['default']))
        entry.pack(side=tk.LEFT)
        entry.param_name = param  # 将参数名称作为属性添加到Entry组件

def create_object_config(root, obj_id, OBJECTS_PARAMS, animation_params_options):
    object_frame = ttk.LabelFrame(root, text=f"对象 {obj_id}")
    object_frame.pack(fill='x', expand=True, padx=10, pady=5)

    object_type_var = tk.StringVar(value=list(OBJECTS_PARAMS.keys())[0])
    object_type_menu = ttk.OptionMenu(object_frame, object_type_var, *OBJECTS_PARAMS.keys())
    object_type_menu.pack(side=tk.LEFT)

    # 将StringVar存储为对象帧的属性
    object_frame.object_type_var = object_type_var

    params_frame = ttk.Frame(object_frame)
    params_frame.pack(fill='x', expand=True, padx=10, pady=5)
    update_params(params_frame, object_type_var.get())

    def on_object_type_change(var=object_type_var, frame=params_frame, current_var=object_type_var.get()):
            update_params(frame, var.get())
    
    object_type_var.trace_add("write", lambda *args, var=object_type_var, frame=params_frame: on_object_type_change(var, frame))

    # 初始化参数输入区域
    update_params(params_frame, object_type_var.get())

    ttk.Label(object_frame, text="动画数量:").pack(side=tk.LEFT)
    animation_count_entry = ttk.Entry(object_frame, width=3)
    animation_count_entry.pack(side=tk.LEFT)

    animations_config_container = ttk.Frame(object_frame, name='animations_container')
    animations_config_container.pack(fill='both', expand=True)

    def confirm_animation_config():
        print("确认动画数量被点击")  # 调试信息
        for widget in animations_config_container.winfo_children():
            widget.destroy()
        try:
            animation_count = int(animation_count_entry.get())
            create_animation_config(animations_config_container, animation_count, animation_params_options)
        except ValueError:
            print("请输入有效的动画数量")
        

    confirm_btn = ttk.Button(object_frame, text="确认动画数量", command=confirm_animation_config)
    confirm_btn.pack(side=tk.LEFT)

def create_animation_config(frame, animation_count,animation_params_options):
    """动态生成动画配置界面"""
    for i in range(animation_count):
        animation_frame = ttk.Frame(frame)
        animation_frame.pack(fill='x', expand=True, padx=5, pady=5)
        
        # 动画类型选择
        animation_type_var = tk.StringVar(value=list(animation_params_options.keys())[0])
        animation_frame.animation_type_var = animation_type_var  # 将变量存储为框架的属性
        ttk.Label(animation_frame, text="动画类型:").pack(side=tk.LEFT)
        ttk.OptionMenu(animation_frame, animation_type_var, animation_type_var.get(), *animation_params_options.keys()).pack(side=tk.LEFT)
        
        # 根据所选动画类型动态生成参数输入框
        def on_animation_type_change(var=animation_type_var, parent_frame=animation_frame):
            # 清除旧的参数输入字段
            for widget in parent_frame.winfo_children()[2:]:  # 保留前两个Widget（标签和下拉菜单）
                widget.destroy()
                
            animation_params = animation_params_options[var.get()]
            for param, info in animation_params.items():
                ttk.Label(parent_frame, text=f"{param}:").pack(side=tk.LEFT)
                entry = ttk.Entry(parent_frame)
                entry.insert(0, str(info['default']))
                entry.pack(side=tk.LEFT)
                entry.param_name = param  # 将参数名称作为属性添加

        animation_type_var.trace_add("write", lambda *args, var=animation_type_var, parent_frame=animation_frame: on_animation_type_change(var, parent_frame))
        on_animation_type_change(animation_type_var, animation_frame)  # 初始化参数输入区域s
        print(f"{animation_count}个动画配置已添加到容器中")  # 调试信息

def collect_object_params(object_count, OBJECTS_PARAMS, animation_params_options):
    root = tk.Tk()
    root.title("对象参数")
    objects = []

    for i in range(1, object_count + 1):
        create_object_config(root, i, OBJECTS_PARAMS, animation_params_options)

    


    def generate_data():
        object_frames = [child for child in root.winfo_children() if isinstance(child, ttk.LabelFrame)]
        for object_frame in object_frames:
            object_info = {
                "index": object_frames.index(object_frame) + 1,
                "type": object_frame.object_type_var.get(),  # 直接从属性中获取
                "params": {},
                "animations": {}
            }

            # 收集参数
            params_frame = next((child for child in object_frame.winfo_children() if isinstance(child, ttk.Frame)), None)
            if params_frame:
                for widget in params_frame.winfo_children():
                    if isinstance(widget, ttk.Entry):
                        param_name = widget.param_name  # 直接从Entry对象获取参数名称
                        object_info["params"][param_name] = widget.get()

            # 收集动画配置
            animations_container = next((child for child in object_frame.winfo_children() if isinstance(child, ttk.Frame) and child.winfo_name() == 'animations_container'), None)

            if animations_container:
                for i, animation_frame in enumerate(animations_container.winfo_children(), start=1):
                    if hasattr(animation_frame, 'animation_type_var'):
                        animation_type_var = animation_frame.animation_type_var
                        animation_info = {"effect": animation_type_var.get(), "params": {}}

                        for widget in animation_frame.winfo_children():
                            if isinstance(widget, ttk.Entry):
                                param_name = widget.param_name  # 直接从Entry对象获取参数名称
                                animation_info["params"][param_name] = widget.get()


                        object_info["animations"][i] = animation_info
                    else:
                        print(f"Animation frame {i} does not have 'animation_type_var' attribute.")

            else :
                print("不存在animations_container")

            # 将当前对象的信息添加到总列表中
            objects.append(object_info)

        # 打印到终端
        print(objects) 
        #将数据存储到json文件中
        filename = "gui_data.json"
        write_data_to_json_file(filename, objects)
        root.destroy()
    
    
    ttk.Button(root, text="提交", command=generate_data).pack(pady=20)
    root.mainloop()

def write_data_to_json_file(filename, data):
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


object_count = simpledialog.askinteger("输入", "请输入对象的数量:", minvalue=1)
if object_count:
    collect_object_params(object_count,OBJECTS_PARAMS,animation_params_options)


