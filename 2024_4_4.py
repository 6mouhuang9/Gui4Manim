import json
import subprocess
def generate_manimce_code(data):
    code = "from manim import *\n\n"
    code += "class MyScene(Scene):\n"
    code += "    def construct(self):\n"
    code += "        plane = NumberPlane()\n"
    code += "        self.add(plane)\n"

    for obj_data in data:
        obj_index = obj_data["index"]
        obj_type = obj_data["type"]
        obj_params = obj_data["params"]

        code += f"        object{obj_index} = {obj_type}("
        for param, value in obj_params.items():
            if param == "text":  # 检查参数是否为文本类型
                value = f'"{value}"'  # 如果是，添加双引号
            code += f"{param}={value}, "
        code = code[:-2]  # 移除最后的逗号和空格
        code += ")\n"

        for anim_index, anim_data in obj_data["animations"].items():
            anim_effect = anim_data["effect"]
            anim_params = anim_data["params"]

            code += f"        self.play({anim_effect}(object{obj_index}, "
            for param, value in anim_params.items():
                code += f"{param}={value}, "
            code = code[:-2]  # 移除最后的逗号和空格
            code += "))\n"

    return code

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

json_data = load_json_file('animations_data.json')
manim_code = generate_manimce_code(json_data)

# 生成manim代码文件
with open("manim_code_4_4.py", "w") as f:
    f.write(manim_code)
subprocess.run(["manim", "-pql", "manim_code_4_4.py", "MyScene"])

#来，咱们明确一下，manim中输入坐标的具体形式到底是什么
#arrow = Arrow3D(
#           start=np.array([0, 0, 0]),
#           end=np.array([2, 2, 2]),
#           resolution=8
#        )

#        p1 = [0,0,0]
#        p2 = [1,2,0]
#        brace = BraceBetweenPoints(p1,p2)

#        dot_1 = Dot3D(point=axes.coords_to_point(0, 0, 1), color=RED)
#        dot_2 = Dot3D(point=axes.coords_to_point(2, 0, 0), radius=0.1, color=BLUE)
#        dot_3 = Dot3D(point=[0, 0, 0], radius=0.1, color=ORANGE)

#        point = Point(location=[0.63, 0.37, 0])

#       arrow3d_1 = Arrow3D(start=(1.0, 2.0, 3.0), end=(-3.0, -2.0, -1.0), thickness=0.02, color="YELLOW")

#可以看出，坐标可以是np.array[_,_,_],也可以是[_,_,_]，也可以是(_,_,_)，但唯独不能是纯数字 _,_,_
#那就处理一下，能不能用tuple加(),或者用list加[]?