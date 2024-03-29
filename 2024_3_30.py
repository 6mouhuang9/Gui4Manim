import subprocess


def generate_manim_code(animation_data):
    manim_code = ""

    # 导入所需模块
    manim_code += "from manim import *\n\n"

    # 生成场景类和构造函数
    manim_code += "class MyScene(Scene):\n"
    manim_code += "    def construct(self):\n"

    # 生成动画对象的代码
    for obj_name, obj_data in objects_data.items():
    # 获取对象类型和参数
        obj_type = obj_data["type"]
        obj_params = obj_data["parameters"]
        
        # 生成对象的代码
        obj_code = f"      {obj_name} = {obj_type}("
        obj_code += ", ".join([f"{key}={value}" for key, value in obj_params.items()])
        obj_code += ")\n"
        manim_code += obj_code
    
        # 生成对象动画的代码
        for anim_data in obj_data["animations"]:
            anim_type = anim_data["type"]
            anim_params = anim_data.get("parameters", {})
            #这里并不需要单独把run_time摘出来
            anim_code = f"      self.play({anim_type}({obj_name}, "
            anim_code += ",".join([f"{key}={value}" for key, value in anim_params.items()])
            anim_code += f"))\n"
            manim_code += anim_code

    return manim_code

# 示例数据
objects_data = {
    "object1": {
        "type": "Circle",
        "parameters": {
            "radius": 1,
            "color": "BLUE"
        },
        "animations": [
            {
                "type": "FadeIn",
                "parameters": {
                    "run_time": 1
                }
            },
            {
                "type": "Rotate",
                "parameters": {
                    "angle": 90,
                    "run_time": 2
                }
            }
        ]
    },
    "object2": {
        "type": "Square",
        "parameters": {
            "side_length": 2,
            "color": "RED"
        },
        "animations": [
            {
                "type": "Create",
                "parameters": {
                    "run_time": 1
                }
            }
        ]
    }
}


# 生成Manim代码
manim_code = generate_manim_code(objects_data)
print(manim_code)

# 生成manim代码文件
with open("manim_code.py", "w") as f:
    f.write(manim_code)

# 运行manim代码
subprocess.run(["manim", "-pql", "manim_code.py", "MyScene"])