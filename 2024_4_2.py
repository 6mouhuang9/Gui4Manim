from ast import Tuple
import json
import os
import numpy as np


OBJECTS_PARAMS = {
    "Circle": {
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "color": {"default": "BLUE", "type": str, "validation": "color"}
    },
    "Square": {
        "side_length": {"default": 2, "type": float, "validation": "positive"},  # 正方形的边长
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 正方形的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"}  # 正方形的不透明度
    },
    "Rectangle": {
        "width": {"default": 4, "type": float, "validation": "positive"},  # 矩形的宽度
        "height": {"default": 2, "type": float, "validation": "positive"},  # 矩形的高度
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 矩形的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"}  # 矩形的不透明度
    },
    #triangle存疑，因为manimce中只有关键字参数，没有提到过顶点
    "Triangle": {
        "point1": {"default": [-1, -1, 0], "type": "list", "validation": None},  # 第一个顶点的坐标
        "point2": {"default": [1, -1, 0], "type": "list", "validation": None},   # 第二个顶点的坐标
        "point3": {"default": [0, 1, 0], "type": "list", "validation": None},    # 第三个顶点的坐标
        "color": {"default": "WHITE", "type": str, "validation": "color"},        # 三角形的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"}  # 三角形的不透明度
    },
    "Polygon": {
        "sides": {"default": 5, "type": int, "validation": "positive_integer"},
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "color": {"default": "YELLOW", "type": str, "validation": "color"}
    },
    "Line": {
        "start": {"default": [0,0,0], "type": "list", "validation": "position"},
        "end": {"default": [0,0,0], "type": "list", "validation": "position"},
        "color": {"default": "WHITE", "type": "list", "validation": "color"}
    },
    "Arrow": {
        "stroke_width": {"default": 6, "type": float, "validation": "positive"},
        "buff": {"default": 0.25, "type": float, "validation": "non_negative"},
        "max_tip_length_to_length_ratio": {"default": 0.25, "type": float, "validation": "non_negative"},
        "max_stroke_width_to_length_ratio": {"default": 5, "type": float, "validation": "positive"}
        # 对于 *args 和 **kwargs，通常我们不在此处处理，但如果有特定的常用参数可以考虑添加
    },
    "NumberLine": {
        "x_range": {"default": [0, 10, 1], "type": "list"},  # 示例：开始，结束，步长
        "length": {"default": 10, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "include_numbers": {"default": True, "type": bool},
        "label_direction": {"default": "UP", "type": str, "validation": "direction"},
        "unit_size": {"default": 1, "type": float, "validation": "positive"},
        # 更多参数...
    },
    "Sector": {
        "outer_radius": {"default": 1, "type": float, "validation": "positive"},
        "inner_radius": {"default": 0, "type": float, "validation": "non_negative"},
        "angle": {"default": 60, "type": float, "validation": "angle"},
        "start_angle": {"default": 0, "type": float, "validation": "angle"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "stroke_width": {"default": 6, "type": float, "validation": "positive"},
        "fill_opacity": {"default": 0.5, "type": float, "validation": "fill_opacity"},
        # 更多参数...
    },
    "Dot":{
        "point": {"default": [0, 0, 0], "type": "list", "validation": None},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
    },
    "Arc": {
        "start_angle": {"default": 0, "type": float, "validation": "angle"},
        "angle": {"default": 3.14, "type": float, "validation": "angle"},  # 默认以弧度表示半圆
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        # 根据需要添加其他参数
    },
    "Ellipse": {
        "width": {"default": 4, "type": float, "validation": "positive"},
        "height": {"default": 2, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        # 可能的其他参数，例如边框粗细、样式等
    },
    "Annulus": {
        "inner_radius": {"default": 1, "type": float, "validation": "positive"},
        "outer_radius": {"default": 2, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        # 如果有需要，可以添加其他参数，例如角度等
    },
    "RegularPolygram": {
        "n": {"default": 5, "type": int, "validation": "positive_integer"},  # 边数或顶点数
        "radius": {"default": 1, "type": float, "validation": "positive"},  # 外接圆半径
        "start_angle": {"default": 0, "type": float, "validation": "angle"},  # 起始角度
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 边框颜色
        "fill_color": {"default": "BLUE", "type": str, "validation": "color"},  # 填充颜色
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"}  # 填充不透明度
    },
    "RegularPolygon": {
        "n": {"default": 6, "type": int, "validation": "positive_integer"},  # 边数或顶点数
        "radius": {"default": 1, "type": float, "validation": "positive"},  # 外接圆半径
        "start_angle": {"default": 0, "type": float, "validation": "angle"},  # 起始角度
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 边框颜色
        "fill_color": {"default": "BLUE", "type": str, "validation": "color"},  # 填充颜色
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"}  # 填充不透明度
    },
    "Star": {
        "n": {"default": 5, "type": int, "validation": "positive_integer"},  # 星形的尖角数量
        "outer_radius": {"default": 2, "type": float, "validation": "positive"},  # 星形的外半径
        "inner_radius": {"default": 1, "type": float, "validation": "positive"},  # 星形的内半径，通常小于外半径
        "density": {"default": 2, "type": int, "validation": "positive_integer"},  # 用于定义星形密度的参数，通常是2
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 星形的边框颜色
        "fill_color": {"default": "YELLOW", "type": str, "validation": "color"},  # 星形的填充颜色
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"}  # 填充不透明度
    },
    "Rectangle": {
        "width": {"default": 4, "type": float, "validation": "positive"},  # 矩形的宽度
        "height": {"default": 2, "type": float, "validation": "positive"},  # 矩形的高度
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 矩形的边框颜色
        "fill_color": {"default": "BLUE", "type": str, "validation": "color"},  # 矩形的填充颜色
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"}  # 填充不透明度
    },
    #surface没有必要
    "Sphere": {
        "radius": {"default": 1, "type": float, "validation": "positive"},  # 球体的半径
        "resolution": {"default": (24, 24), "type": "tuple", "validation": "resolution"},  # 球体的分辨率，表示(u, v)方向的分段数
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 球体的颜色
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"}  # 球体的不透明度
    },
    "Torus": {
        "major_radius": {"default": 3, "type": float, "validation": "positive"},  # 圆环的大半径，即圆环中心到管道中心的距离
        "minor_radius": {"default": 1, "type": float, "validation": "positive"},  # 圆环的小半径，即管道的半径
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 圆环的颜色
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"},  # 圆环的不透明度
    },
    "Cone": {
        "base_radius": {"default": 1, "type": float, "validation": "positive"},  # 圆锥的底面半径
        "height": {"default": 2, "type": float, "validation": "positive"},  # 圆锥的高度
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 圆锥的颜色
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"},  # 圆锥的不透明度
        "resolution": {"default": 24, "type": int, "validation": "positive_integer"}  # 圆锥的分辨率，表示底面圆的分段数
    },
    "Cylinder": {
        "radius": {"default": 1, "type": float, "validation": "positive"},  # 圆柱的底面半径
        "height": {"default": 2, "type": float, "validation": "positive"},  # 圆柱的高度
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 圆柱的颜色
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"},  # 圆柱的不透明度
    },
    "Dot3D": {
        "point": {"default": [0, 0, 0], "type": "list", "validation": None},  # 3D点的位置
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 点的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},  # 点的不透明度
        "radius": {"default": 0.1, "type": float, "validation": "positive"}  # 点的半径
    },
    "Line3D": {
        "start": {"default": [0, 0, 0], "type": "list", "validation": None},  # 线段的起点位置
        "end": {"default": [1, 1, 1], "type": "list"},  # 线段的终点位置
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 线段的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},  # 线段的不透明度
        "stroke_width": {"default": 0.04, "type": float, "validation": "positive"}  # 线段的线宽
    },
    "Arrow3D": {
        "start": {"default": [0, 0, 0], "type": "list", "validation": None},  # 箭头的起点位置
        "end": {"default": [1, 1, 1], "type": "list", "validation": None},  # 箭头的终点位置
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 箭头的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},  # 箭头的不透明度
        "stroke_width": {"default": 0.04, "type": float, "validation": "positive"},  # 箭头线段的线宽
    },
    "Cross": {
        "length": {"default": 1, "type": float, "validation": "positive"},  # 十字形的线段长度
        "stroke_width": {"default": 0.1, "type": float, "validation": "positive"},  # 十字形的线宽
        "color": {"default": "WHITE", "type": str, "validation": "color"},  # 十字形的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"}  # 十字形的不透明度
    },
    "Cube": {
        "side_length": {"default": 1, "type": float, "validation": "positive"},  # 立方体的边长
        "color": {"default": "WHITE", "type": str, "validation": "color"},        # 立方体的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"}  # 立方体的不透明度
    },
    "Prism": {
        "dimensions": {"default": [3, 2, 1], "type": "list", "validation": None},  # 棱柱的尺寸
        "color": {"default": "WHITE", "type": str, "validation": "color"},        # 棱柱的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"}  # 棱柱的不透明度
    },
    "ArcPolygon": {
        "vertices": {"default": [(0, 0), (1, 0), (1, 1)], "type": "list", "is_coordinate_list": True,"validation": None},  # 多边形的顶点坐标
        "radius": {"default": 1, "type": float, "validation": "positive"},                    # 弧线的半径
        "color": {"default": "WHITE", "type": str, "validation": "color"},                     # 多边形的颜色
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"}               # 多边形的不透明度
    },
    #Math和Tex目前都搞不了，之後單獨處理
    "Text": {
        "text": {"default": r"\text{Manim}", "type": str, "validation": None},  # LaTeX 文本内容
        "color": {"default": "WHITE", "type": str, "validation": "color"},             # 颜色
        "alignment": {"default": "LEFT", "type": str, "validation": "alignment"}         # 对齐方式
    },
    "Polyhedron": {
        "vertex_coords": {"default": [], "type": "list", "is_coordinate_list": True,"validation": None},          # 多面体的顶点坐标列表
        "faces_list": {"default": [], "type": "list","is_coordinate_list": True, "validation": None},             # 多面体的面列表
    },
    "Icosahedron": {
        "edge_length": {"default": 1, "type": float, "validation": "positive"},   # 二十面体的边长
        # 其他可能的关键字参数...
    },
    "Octahedron": {
        "edge_length": {"default": 1, "type": float, "validation": "positive"},   # 八面体的边长
        # 其他可能的关键字参数...
    },
    "Tetrahedron": {
        "edge_length": {"default": 1, "type": float, "validation": "positive"},   # 四面体的边长
        # 其他可能的关键字参数...
    },
    "Dodecahedron": {
        "edge_length": {"default": 1, "type": float, "validation": "positive"},   # 十二面体的边长
        # 其他可能的关键字参数...
    },
    "ArrowVectorField": {
        "func": {"default": None, "type": callable, "validation": None},   # 流函数
        # 删了不少，用球不着
    },
    "StreamLines": {
        "func": {"default": None, "type": callable, "validation": None},           # 流函数
        #同上
    },
    "BraceBetweenPoints": {
        "point_1": {"default": None, "type": "list", "validation": None},        # 起始点
        "point_2": {"default": None, "type": "list", "validation": None},        # 结束点
        #"label_text": {"default": '', "type": str, "validation": None},            # 文本(压根就没这个参数吧)
        # 其他可能的关键字参数...
        #对于输入坐标的情况该怎么搞
    },
    #我不打算处理NumberLine，都使用默认版本
    #同理，PolarPlane也是这样
    #同理，ComplexLine也是这样
    #ThreeDAxes以及视角则默认交给那几个3D图形
}

# 定义动画效果及其参数

animation_params_options = {
    "FadeIn": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "FadeOut": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "Rotate": {"angle": {"default": 3.14, "type": float, "validation": "positive"}, "run_time": {"default": 2, "type": float, "validation": "positive"}},
    # 根据需要添加更多动画效果...
}

def convert_numpy_to_list(data):
    if isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, dict):
        return {key: convert_numpy_to_list(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_to_list(item) for item in data]
    else:
        return data

def get_user_choice(options, prompt):
    """让用户从提供的选项中做出选择，并返回选择的项目。"""
    print(prompt)
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    while True:
        choice = input("请选择一个选项 (输入编号): ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        else:
            print("无效选择，请重试。")

def collect_params(params_definitions):
    """根据参数定义收集用户输入的参数值。"""
    params = {}
    for param, definition in params_definitions.items():
        default = definition.get('default')
        param_type = definition.get('type')
        
        prompt = f"请输入 {param}"
        if default is not None:
            prompt += f" (默认: {default})"
        prompt += ": "

        # 检查参数是否预期为坐标列表
        if definition.get('is_coordinate_list', False):
            print(f"{prompt} 请输入多个坐标，每个坐标用逗号分隔，并用分号分隔不同的坐标。例如: 0,0; 1,1; 2,2")
            user_input = input()
            if user_input:
                # 处理用户输入的坐标，将字符串转换为坐标列表
                try:
                    # 分割不同的坐标，然后进一步分割每个坐标的x,y值
                    #value = [list(map(float, coord.strip().split(','))) for coord in user_input.split(';')]
                    value = [[float(coord.strip()) for coord in point.split(',')] for point in user_input.split(';')]
                except ValueError:
                    print("输入格式错误，请按正确的格式输入多个坐标。")
                    value = default
            else:
                value = default
        else:
            user_input = input(prompt)
            # 处理其他类型的参数...
            if user_input:
                try:
                    if param_type == "int":
                        value = int(user_input)
                    elif param_type == "float":
                        value = float(user_input)
                    elif param_type == "bool":
                        value = user_input.lower() in ['true', '1', 't', 'y', 'yes']
                    #elif param_type == "str" or param_type == "list":
                    elif param_type == "str":
                        value = f'{user_input}'
                    elif param_type == "list":
                        value = np.array([float(item) for item in user_input.split(',')])
                        value = convert_numpy_to_list(value)
                    else:
                        value = user_input
                except ValueError:
                    print("输入格式错误。")
                    value = default
            else:
                value = default

        params[param] = value
    return params


def collect_animations(animation_effects, animation_params_options):
    animations = {}
    num_effects = int(input("这个动画对象需要几个动画效果? "))
    for j in range(1, num_effects + 1):
        print(f"\n配置动画效果 #{j}")
        chosen_effect = get_user_choice(animation_effects, "选择一个动画效果:")
        effect_params_definitions = animation_params_options[chosen_effect]
        
        # 在这里调用 collect_params 以收集动画效果的参数，包括坐标
        effect_params = collect_params(effect_params_definitions)
        
        animations[j] = {"effect": chosen_effect, "params": effect_params}
    return animations

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


def main():
    animations_data = []

    # 从OBJECTS_PARAMS动态获取对象类型和参数选项
    object_types = list(OBJECTS_PARAMS.keys())
    # 动态获取动画效果类型
    animation_effects = list(animation_params_options.keys())

    num_objects = int(input("你想创建多少个动画对象? "))
    for i in range(num_objects):
        print(f"\n配置动画对象 #{i + 1}")
        chosen_type = get_user_choice(object_types, "选择动画对象类型:")
        params_definitions = OBJECTS_PARAMS[chosen_type]
        params = collect_params(params_definitions)
        
        # 使用collect_animations函数收集动画效果
        animations = collect_animations(animation_effects, animation_params_options)

        animations_data.append({
            "index": i + 1,
            "type": chosen_type,
            "params": params,
            "animations": animations
        })

    print("\n最终的动画数据结构: ")
    for item in animations_data:
        print(item)

    print('\n')
    print(animations_data)

    filename = "animations_data.json"
    write_data_to_json_file(filename, animations_data)

if __name__ == "__main__":
    main()


