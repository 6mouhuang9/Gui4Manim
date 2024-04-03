#接下来该处理VGroup以及transform相关的了
#这个，transform类型的如何实现呢？
#VGroup与Transform的联系紧密吗？    
#之前最常用的是ReplacementTransformm,其实Transform与ReplacementTransform差不多
#这个，相似点在于都是同时出现多个动画对象
#之前的数据结构能不能用？有序号，有参数，那么首先确定要用VGroup，然后依次设定方法与参数，最后放在置于VGroup中，然后就能使用VGroup相关的各种范例，说实话，我突然感觉没什么意义，感觉只要加一个transform方法就行
#哦对，还有一个生成函数图形的那个方法，也就是输入函数的方法ParameticFunction，输入函数顺便再与latex转换一下
#是否需要另外搞一个transform_object_params,倒是可以说实话，不过不用多，先搞处理代码的部分吧

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
        # 如果有错误（例如，解析错误），返回原始字符串
        # 这是一个简单的错误处理，可能需要根据具体需要进行调整
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
        
        #这里是我打错了，不过之后的中文化也能这么处理
        #if obj_type == "Mathtex":
        #   obj_type = "MathTex"  # 调整名称以匹配Manim类名

        
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
    
    # 添加变换动画的代码
    # 假设我们知道哪些对象要进行变换
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
