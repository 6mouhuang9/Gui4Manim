import tkinter as tk
from tkinter import ttk, simpledialog

OBJECTS_PARAMS = {
    #triangle存疑，因为manimce中只有关键字参数，没有提到过顶点
    "Circle": {
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "color": {"default": "BLUE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Square": {
        "side_length": {"default": 2, "type": float, "validation": "positive"},
        "fill_color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Rectangle": {
        "width": {"default": 4, "type": float, "validation": "positive"},
        "height": {"default": 2, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    #这...
    "Triangle": {
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
        #你这个validation有个球的意义，判断都用不着，再说了，谁家坐标规定用整数？
    "Polygon": {
        "sides": {"default": 5, "type": int, "validation": "positive_integer"},
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Line": {
        "start": {"default": [0, 0, 0], "type": "list", "validation": None},
        "end": {"default": [1, 1, 1], "type": "list", "validation": None},
        #这个有起点和终点了，用不着
        #"position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
        #Arrow用不了，一會改成vector
    "NumberLine": {
        "x_range": {"default": [0, 10, 1], "type": "list"},
        "length": {"default": 10, "type": float, "validation": "positive"},
        #挺抽象的，给坐标轴加位置
        #"position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Sector": {
        "outer_radius": {"default": 1, "type": float, "validation": "positive"},
        "inner_radius": {"default": 0, "type": float, "validation": "non_negative"},
        "angle": {"default": 60, "type": float, "validation": "angle"},
        "start_angle": {"default": 0, "type": float, "validation": "angle"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Dot": {
        "point": {"default": [0, 0, 0], "type": "list", "validation": None},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        #"position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Arc": {
        "start_angle": {"default": 0, "type": float, "validation": "angle"},
        "angle": {"default": 3.14, "type": float, "validation": "angle"},
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Star": {
        "n": {"default": 5, "type": int, "validation": "positive_integer"},
        "outer_radius": {"default": 2, "type": float, "validation": "positive"},
        "inner_radius": {"default": 1, "type": float, "validation": "positive"},
        "density": {"default": 2, "type": int, "validation": "positive_integer"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },

    "Annulus": {
        "inner_radius": {"default": 1, "type": float, "validation": "positive"},
        "outer_radius": {"default": 2, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "RegularPolygram": {
        "n": {"default": 5, "type": int, "validation": "positive_integer"},
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "start_angle": {"default": 0, "type": float, "validation": "angle"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "RegularPolygon": {
        "n": {"default": 6, "type": int, "validation": "positive_integer"},
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "start_angle": {"default": 0, "type": float, "validation": "angle"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Ellipse": {
        "width": {"default": 4, "type": float, "validation": "positive"},
        "height": {"default": 2, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "AnnularSector": {
        "inner_radius": {"default": 1, "type": float, "validation": "positive"},
        "outer_radius": {"default": 2, "type": float, "validation": "positive"},
        "angle": {"default": "PI/2", "type": "str"},  # Modified to str for PI/2
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "BraceBetweenPoints": {
        "point_1": {"default": [0, 0, 0], "type": "list", "validation": None},
        "point_2": {"default": [1, 1, 1], "type": "list", "validation": None},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "RoundRectangle": {
        "corner_radius": {"default": 0.5, "type": float, "validation": "positive"},
        "width": {"default": 4, "type": float, "validation": "positive"},
        "height": {"default": 2, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "MathTex": {
        "tex_string": {"default": r"\text{Manim}", "type": str, "validation": None},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Tex": {
        "tex_string": {"default": r"\text{Manim}", "type": str, "validation": None},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Text": {
        "text": {"default": "Manim", "type": str, "validation": None},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Polyhedron": {
        "vertex_coords": {"default": [], "type": "list", "is_coordinate_list": True, "validation": None},
        "faces_list": {"default": [], "type": "list", "is_coordinate_list": True, "validation": None},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Icosahedron": {
        "edge_length": {"default": 1, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Octahedron": {
        "edge_length": {"default": 1, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Tetrahedron": {
        "edge_length": {"default": 1, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },
    "Dodecahedron": {
        "edge_length": {"default": 1, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": None},
    },

    #surface没有必要
    "Sphere": {
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "resolution": {"default": (24, 24), "type": "tuple", "validation": "resolution"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Torus": {
        "major_radius": {"default": 3, "type": float, "validation": "positive"},
        "minor_radius": {"default": 1, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Cone": {
        "base_radius": {"default": 1, "type": float, "validation": "positive"},
        "height": {"default": 2, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"},
        "resolution": {"default": 24, "type": int, "validation": "positive_integer"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Cylinder": {
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "height": {"default": 2, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 0.5, "type": float, "validation": "non_negative"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Dot3D": {
        "point": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},
        "radius": {"default": 0.1, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Line3D": {
        "start": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
        "end": {"default": [1, 1, 1], "type": "list", "validation": "coordinates"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},
        "stroke_width": {"default": 0.04, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Arrow3D": {
        "start": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
        "end": {"default": [1, 1, 1], "type": "list", "validation": "coordinates"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},
        "stroke_width": {"default": 0.04, "type": float, "validation": "positive"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },

    "Cross": {
        "length": {"default": 1, "type": float, "validation": "positive"},
        "stroke_width": {"default": 0.1, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Cube": {
        "side_length": {"default": 1, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Prism": {
        "dimensions": {"default": [3, 2, 1], "type": "list"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "ArcPolygon": {
        "vertices": {"default": [(0, 0), (1, 0), (1, 1)], "type": "list", "is_coordinate_list": True},
        "radius": {"default": 1, "type": float, "validation": "positive"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "fill_opacity": {"default": 1.0, "type": float, "validation": "non_negative"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "ArrowVectorField": {
        "func": {"default": None, "type": callable},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "StreamLines": {
        "func": {"default": None, "type": callable},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "BraceBetweenPoints": {
        "point_1": {"default": [0, 0, 0], "type": "list"},
        "point_2": {"default": [0, 0, 0], "type": "list"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "Elbow": {
        "width": {"default": 1, "type": float},
        "angle": {"default": 0, "type": float},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "point": {
        "location": {"default": [0, 0, 0], "type": "list"},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },
    "PointCloudDot": {
        "center": {"default": [0, 0, 0], "type": "list"},
        "radius": {"default": 1, "type": float},
        "color": {"default": "WHITE", "type": str, "validation": "color"},
        "position": {"default": [0, 0, 0], "type": "list", "validation": "coordinates"},
    },

    #有时候感觉cutout更像animations
}

animation_params_options = {
    "FadeIn": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "FadeOut": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "Rotate": {"angle": {"default": 3.14, "type": float, "validation": "positive"}, "run_time": {"default": 2, "type": float, "validation": "positive"}},
    "AddTextLetterByLetter": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "AddTextWordByWord":{"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "Circumscribe": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "ShowCreationThenFadeOut": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "Broadcast": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "Flash": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "ShowPassingFlashWithThinningStrokeWidth": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "FadeToColor": {"run_time": {"default": 2, "type": float, "validation": "positive"},    "color": {"default": "WHITE", "type": str, "validation": "color"},},
    "ScaleInPlace": {"run_time": {"default": 2, "type": float, "validation": "positive"},
    "*arg": {"default": 2, "type": float, "validation": "positive"}},
    "ShrinkToCenter": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "ApplyWave": {"run_time": {"default": 2, "type": float, "validation": "positive"},      "direction": {"default": [0,0,0], "type": "list", "validation": "position"},
    "time_width ": {"default": 1, "type": float, "validation": "positive"}},
    #同伦类型论（homotopy type theory，缩写 HoTT）是一套旨在于同伦论的大框架下构建内涵类型论语义的理论，尤指Quillen模型范畴和弱分解系统。
    "Homotopy": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "ComplexHomotopy": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "DrawBorderThenFill": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "Create": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    "Uncreate": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    #这又是个什么玩意
    "ShowPartial": {"run_time": {"default": 2, "type": float, "validation": "positive"}},
    
    "MaintainPositionRelativeTo": {"run_time": {"default": 2, "type": float, "validation": "positive"}},


    
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

def create_object_config(root, obj_id, OBJECTS_PARAMS, animation_params_options):
    object_frame = ttk.LabelFrame(root, text=f"对象 {obj_id}")
    object_frame.pack(fill='x', expand=True, padx=10, pady=5)

    object_type_var = tk.StringVar(value=list(OBJECTS_PARAMS.keys())[0])
    object_type_menu = ttk.OptionMenu(object_frame, object_type_var, *OBJECTS_PARAMS.keys())
    object_type_menu.pack(side=tk.LEFT)

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

    animations_config_container = ttk.Frame(object_frame)
    animations_config_container.pack(fill='both', expand=True)

    def confirm_animation_config():
        for widget in animations_config_container.winfo_children():
            widget.destroy()
        try:
            animation_count = int(animation_count_entry.get())
            create_animation_config(animations_config_container, animation_count, animation_params_options)
        except ValueError:
            print("请输入有效的动画数量")

    confirm_btn = ttk.Button(object_frame, text="确认动画数量", command=confirm_animation_config)
    confirm_btn.pack(side=tk.LEFT)


def collect_object_params(object_count, OBJECTS_PARAMS, animation_params_options):
    root = tk.Tk()
    root.title("对象参数")

    for i in range(1, object_count + 1):
        create_object_config(root, i, OBJECTS_PARAMS, animation_params_options)

    ttk.Button(root, text="提交", command=root.destroy).pack(pady=20)
    root.mainloop()

def create_animation_config(frame, animation_count,animation_params_options):
    """动态生成动画配置界面"""
    for i in range(animation_count):
        animation_frame = ttk.Frame(frame)
        animation_frame.pack(fill='x', expand=True, padx=5, pady=5)
        
        # 动画类型选择
        animation_type_var = tk.StringVar(value=list(animation_params_options.keys())[0])
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

        animation_type_var.trace_add("write", lambda *args, var=animation_type_var, parent_frame=animation_frame: on_animation_type_change(var, parent_frame))
        on_animation_type_change(animation_type_var, animation_frame)  # 初始化参数输入区域s

object_count = simpledialog.askinteger("输入", "请输入对象的数量:", minvalue=1)
if object_count:
    collect_object_params(object_count,OBJECTS_PARAMS,animation_params_options)
