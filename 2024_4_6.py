import tkinter as tk
from tkinter import ttk, simpledialog

OBJECTS_PARAMS = {
    "Circle": {
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "color": {"default": "BLUE", "type": str, "validation": "color"}
    },
    "Square": {
        "side_length": {"default": 2, "type": float, "validation": "positive"},  # 正方形的边长
    },
    "Rectangle": {
        "width": {"default": 4, "type": float, "validation": "positive"},  # 矩形的宽度
        "height": {"default": 2, "type": float, "validation": "positive"},  # 矩形的高度
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
    },
    "Line": {
        "start": {"default": [0,0,0], "type": "list", "validation": "position"},
        "end": {"default": [0,0,0], "type": "list", "validation": "position"},
    },
    #Arrow用不了，一會改成vector
    "NumberLine": {
        "x_range": {"default": [0, 10, 1], "type": "list"},  # 示例：开始，结束，步长
        "length": {"default": 10, "type": float, "validation": "positive"},
        # 更多参数...
    },
    "Sector": {
        "outer_radius": {"default": 1, "type": float, "validation": "positive"},
        "inner_radius": {"default": 0, "type": float, "validation": "non_negative"},
        "angle": {"default": 60, "type": float, "validation": "angle"},
        "start_angle": {"default": 0, "type": float, "validation": "angle"},
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
        # 根据需要添加其他参数
    },
    "Ellipse": {
        "width": {"default": 4, "type": float, "validation": "positive"},
        "height": {"default": 2, "type": float, "validation": "positive"},
        # 可能的其他参数，例如边框粗细、样式等
    },
    "Annulus": {
        "inner_radius": {"default": 1, "type": float, "validation": "positive"},
        "outer_radius": {"default": 2, "type": float, "validation": "positive"},
        # 如果有需要，可以添加其他参数，例如角度等
    },
    "RegularPolygram": {
        "n": {"default": 5, "type": int, "validation": "positive_integer"},  # 边数或顶点数
        "radius": {"default": 1, "type": float, "validation": "positive"},  # 外接圆半径
        "start_angle": {"default": 0, "type": float, "validation": "angle"},  # 起始角度
    },
    "RegularPolygon": {
        "n": {"default": 6, "type": int, "validation": "positive_integer"},  # 边数或顶点数
        "radius": {"default": 1, "type": float, "validation": "positive"},  # 外接圆半径
        "start_angle": {"default": 0, "type": float, "validation": "angle"},  # 起始角度
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
    }
}

animation_params_options = {
    "FadeIn": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "FadeOut": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "Rotate": {"angle": {"default": 3.14, "type": float, "validation": "positive"}, "run_time": {"default": 2, "type": float, "validation": "positive"}},
    # 根据需要添加更多动画效果...
}

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

def collect_object_params(object_count):
    root = tk.Tk()
    root.title("对象参数")

    for i in range(object_count):
        object_frame = ttk.Frame(root)
        object_frame.pack(fill='x', expand=True, padx=10, pady=5)

        object_type_var = tk.StringVar(value=list(OBJECTS_PARAMS.keys())[0])
        object_type_menu = ttk.OptionMenu(object_frame, object_type_var, *OBJECTS_PARAMS.keys())
        object_type_menu.pack(side=tk.LEFT)

        params_frame = ttk.Frame(object_frame)
        params_frame.pack(fill='x', expand=True, padx=10, pady=5)

        def on_object_type_change(var=object_type_var, frame=params_frame, current_var=object_type_var.get()):
            update_params(frame, var.get())

        object_type_var.trace_add("write", lambda *args, var=object_type_var, frame=params_frame: on_object_type_change(var, frame))

        # 初始化参数输入区域
        update_params(params_frame, object_type_var.get())

    ttk.Button(root, text="提交", command=root.destroy).pack(pady=20)
    root.mainloop()


object_count = simpledialog.askinteger("输入", "请输入对象的数量:", minvalue=1)
if object_count:
    collect_object_params(object_count)
