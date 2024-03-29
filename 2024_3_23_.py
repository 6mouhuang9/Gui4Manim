import tkinter as tk
import tkinter as ttk
from manim import *
import subprocess
import uuid

#Mobjects:Arrow,Vector，NumberLine,Sector,Ellipse,Polygram,Polygon,RegulaiPolygram,RegularPolygon,Sphere,Torus,Cone,Cylinder,Dot3D,Line3D,Arrow3D,Cross
#艹，才发现arrow和vector一定程度上长得一样
class ArrowCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 输入箭头的数量
        self.num_arrows_label = tk.Label(self.master, text="要生成几个箭头?")
        self.num_arrows_label.pack()
        self.num_arrows_entry = tk.Entry(self.master)
        self.num_arrows_entry.pack()

        # 确认箭头的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_arrows = int(self.num_arrows_entry.get())

        # 移除上一个界面的控件
        self.num_arrows_label.pack_forget()
        self.num_arrows_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入箭头特征的控件
        self.create_arrow_input_widgets()
    
    def create_arrow_input_widgets(self):
        self.arrow_widgets = []

        for i in range(self.num_arrows):
            arrow_frame = tk.Frame(self.master)
            arrow_frame.pack(pady=5)

            start_label = tk.Label(arrow_frame, text=f"箭头{i + 1}的起点坐标(x, y, z):")
            start_label.pack(side="left")

            start_entry = tk.Entry(arrow_frame)
            start_entry.pack(side="left")

            end_label = tk.Label(arrow_frame, text=f"箭头{i + 1}的终点坐标(x, y, z):")
            end_label.pack(side="left")

            end_entry = tk.Entry(arrow_frame)
            end_entry.pack(side="left")

            self.arrow_widgets.append((start_entry, end_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析箭头起点和终点坐标字符串为数组
        arrows = []
        for start_entry, end_entry in self.arrow_widgets:
            start_str = start_entry.get()
            end_str = end_entry.get()
            start = np.array([float(x) for x in start_str.split(',')])
            end = np.array([float(x) for x in end_str.split(',')])
            arrows.append((start, end))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *
class {class_name}(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
"""

        for i, (start, end) in enumerate(arrows):
            manim_code += f"""
        # 创建箭头对象
        arrow{i+1} = Arrow(start={tuple(start)}, end={tuple(end)})

        # 添加箭头对象到场景中
        self.add(arrow{i+1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class VectorCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):

        #输入向量的数量
        self.num_vectors_label = tk.Label(self.master, text="要生成几个向量?")
        self.num_vectors_label.pack()
        self.num_vectors_entry = tk.Entry(self.master)
        self.num_vectors_entry.pack()

        #确认向量的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):

        self.num_vectors = int(self.num_vectors_entry.get())

        # 移除上一个界面的控件
        self.num_vectors_label.pack_forget()
        self.num_vectors_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入向量特征的控件
        self.create_vector_input_widgets()
    
    def create_vector_input_widgets(self):
        self.vector_widgets = []

        for i in range(self.num_vectors):
            vector_frame = ttk.Frame(self.master)
            vector_frame.pack(pady=5)

            vector_label = tk.Label(vector_frame, text=f"向量{i + 1}的坐标(x, y, z):")
            vector_label.pack(side="left")

            vector_entry = tk.Entry(vector_frame)
            vector_entry.pack(side="left")

            self.vector_widgets.append(vector_entry)

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()


    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析方向字符串为数组
        vectors = []
        for widget in self.vector_widgets:
            vector_str = widget.get()
            vector = np.array([float(x) for x in vector_str.split(',')])
            vectors.append(vector)

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *
class {class_name}(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
"""

        for i, vector in enumerate(vectors):
            manim_code += f"""
        # 创建向量对象
        vector{i+1} = Vector({tuple(vector)})

        # 添加向量对象到场景中
        self.add(vector{i+1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class NumberLinesCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_lines_label = tk.Label(self.master, text="要生成几条数轴:")
        self.num_lines_label.pack()
        self.num_lines_entry = tk.Entry(self.master)
        self.num_lines_entry.pack()

        # 添加按钮用于确认输入数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_lines = int(self.num_lines_entry.get())

        # 移除上一个界面的控件
        self.num_lines_label.pack_forget()
        self.num_lines_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入数轴特征的控件
        self.create_number_line_input_widgets()

    def create_number_line_input_widgets(self):
        self.number_line_widgets = []

        for i in range(self.num_lines):
            line_frame = tk.Frame(self.master)
            line_frame.pack(pady=10)

            x_range_label = tk.Label(line_frame, text=f"数轴{i + 1}的X范围:")
            x_range_label.pack(side="left")

            x_range_entry = tk.Entry(line_frame)
            x_range_entry.pack(side="left")

            length_label = tk.Label(line_frame, text="长度:")
            length_label.pack(side="left")

            length_entry = tk.Entry(line_frame)
            length_entry.pack(side="left")


            self.number_line_widgets.append((x_range_entry, length_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=15, width=80)
        self.code_text.pack()

    def generate_manim_code(self):
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, line_widgets in enumerate(self.number_line_widgets, 1):
            x_range = line_widgets[0].get()
            length = line_widgets[1].get()

            manim_code += f"""
        number_line_{i} = NumberLine(
            x_range=[{x_range}],
            length={length},
            include_numbers=True,
        )
        self.add(number_line_{i})
"""

        manim_code += "\n        self.wait()\n"

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class SectorCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_sectors_label = tk.Label(self.master, text="要生成几个扇形?")
        self.num_sectors_label.pack()
        self.num_sectors_entry = tk.Entry(self.master)
        self.num_sectors_entry.pack()

        #确认扇形数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_sectors = int(self.num_sectors_entry.get())

        # 移除上一个界面的控件
        self.num_sectors_label.pack_forget()
        self.num_sectors_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入扇形特征的控件
        self.create_sector_input_widgets()

    def create_sector_input_widgets(self):
        self.sector_widgets = []

        for i in range(self.num_sectors):
            sector_frame = tk.Frame(self.master)
            sector_frame.pack(pady=5)

            # 输入外半径
            outer_radius_label = tk.Label(sector_frame, text=f"扇形{i + 1}的外半径:")
            outer_radius_label.pack(side="left")
            outer_radius_entry = tk.Entry(sector_frame)
            outer_radius_entry.pack(side="left")

            # 输入内半径
            inner_radius_label = tk.Label(sector_frame, text=f"扇形{i + 1}的内半径:")
            inner_radius_label.pack(side="left")
            inner_radius_entry = tk.Entry(sector_frame)
            inner_radius_entry.pack(side="left")

            # 输入位置参数
            position_label = tk.Label(sector_frame, text=f"扇形{i + 1}的位置 (x, y, z):")
            position_label.pack(side="left")
            position_entry = tk.Entry(sector_frame)
            position_entry.pack(side="left")

            self.sector_widgets.append((outer_radius_entry, inner_radius_entry, position_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析扇形参数
        sectors = []
        for outer_radius_entry, inner_radius_entry, position_entry in self.sector_widgets:
            outer_radius = float(outer_radius_entry.get())
            inner_radius = float(inner_radius_entry.get())
            position = tuple(map(float, position_entry.get().split(',')))
            sectors.append((outer_radius, inner_radius, position))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, (outer_radius, inner_radius, position) in enumerate(sectors):
            manim_code += f"""
        # 创建扇形对象
        sector{i + 1} = Sector(outer_radius={outer_radius}, inner_radius={inner_radius})

        # 设置扇形对象位置
        sector{i + 1}.move_to({position})

        # 添加扇形对象到场景中
        self.add(sector{i + 1})

        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class EllipseCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_ellipses_label = tk.Label(self.master, text="要生成几个椭圆?")
        self.num_ellipses_label.pack()
        self.num_ellipses_entry = tk.Entry(self.master)
        self.num_ellipses_entry.pack()

        # 确认椭圆数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_ellipses = int(self.num_ellipses_entry.get())

        # 移除上一个界面的控件
        self.num_ellipses_label.pack_forget()
        self.num_ellipses_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入椭圆特征的控件
        self.create_ellipse_input_widgets()

    def create_ellipse_input_widgets(self):
        self.ellipse_widgets = []

        for i in range(self.num_ellipses):
            ellipse_frame = tk.Frame(self.master)
            ellipse_frame.pack(pady=5)

            # 输入长轴长度
            major_axis_label = tk.Label(ellipse_frame, text=f"椭圆{i + 1}的长轴长度:")
            major_axis_label.pack(side="left")
            major_axis_entry = tk.Entry(ellipse_frame)
            major_axis_entry.pack(side="left")

            # 输入短轴长度
            minor_axis_label = tk.Label(ellipse_frame, text=f"椭圆{i + 1}的短轴长度:")
            minor_axis_label.pack(side="left")
            minor_axis_entry = tk.Entry(ellipse_frame)
            minor_axis_entry.pack(side="left")

            # 输入偏移量
            shift_x_label = tk.Label(ellipse_frame, text=f"椭圆{i + 1}的X偏移:")
            shift_x_label.pack(side="left")
            shift_x_entry = tk.Entry(ellipse_frame)
            shift_x_entry.pack(side="left")

            shift_y_label = tk.Label(ellipse_frame, text=f"椭圆{i + 1}的Y偏移:")
            shift_y_label.pack(side="left")
            shift_y_entry = tk.Entry(ellipse_frame)
            shift_y_entry.pack(side="left")

            self.ellipse_widgets.append((major_axis_entry, minor_axis_entry, shift_x_entry, shift_y_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析椭圆参数
        ellipses = []
        for major_axis_entry, minor_axis_entry, shift_x_entry, shift_y_entry in self.ellipse_widgets:
            major_axis = float(major_axis_entry.get())
            minor_axis = float(minor_axis_entry.get())
            shift_x = float(shift_x_entry.get())
            shift_y = float(shift_y_entry.get())
            ellipses.append((major_axis, minor_axis, shift_x, shift_y))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
"""

        for i, (major_axis, minor_axis, shift_x, shift_y) in enumerate(ellipses):
            manim_code += f"""
        # 创建椭圆对象
        ellipse{i + 1} = Ellipse(width={2 * major_axis}, height={2 * minor_axis}).shift({shift_x} * RIGHT, {shift_y} * UP)

        # 添加椭圆对象到场景中
        self.add(ellipse{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class PolygramCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim Polygram 代码生成器")
        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入顶点坐标
        self.vertices_label = tk.Label(self.master, text="输入顶点坐标（每行一个）:")
        self.vertices_label.pack()
        self.vertices_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.vertices_text.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        vertices_str = self.vertices_text.get("1.0", tk.END).strip()
        vertices_lines = vertices_str.split("\n")

        # 解析顶点坐标
        vertices = []
        for line in vertices_lines:
            coords = line.split(",")
            vertex = [float(coord) for coord in coords]
            vertices.append(vertex)

        # 生成 Manim 代码
        class_name = "MyPolygramScene"
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        polygram = Polygram({vertices})
        self.add(polygram)
"""

        # 显示生成的代码
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

         # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class PolygonCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim Polygon 代码生成器")
        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入多边形数量
        self.num_polygons_label = tk.Label(self.master, text="要生成几个多边形?")
        self.num_polygons_label.pack()
        self.num_polygons_entry = tk.Entry(self.master)
        self.num_polygons_entry.pack()

        # 添加确认按钮
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_polygons = int(self.num_polygons_entry.get())

        # 移除上一个界面的控件
        self.num_polygons_label.pack_forget()
        self.num_polygons_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入多边形特征的控件
        self.create_polygon_input_widgets()

    def create_polygon_input_widgets(self):
        self.polygon_widgets = []

        for i in range(self.num_polygons):
            polygon_frame = tk.Frame(self.master)
            polygon_frame.pack(pady=5)

            # 输入多边形的位置偏移
            shift_x_label = tk.Label(polygon_frame, text=f"多边形{i + 1}的X偏移:")
            shift_x_label.pack(side="left")
            shift_x_entry = tk.Entry(polygon_frame)
            shift_x_entry.pack(side="left")

            shift_y_label = tk.Label(polygon_frame, text=f"多边形{i + 1}的Y偏移:")
            shift_y_label.pack(side="left")
            shift_y_entry = tk.Entry(polygon_frame)
            shift_y_entry.pack(side="left")

            # 输入多边形的顶点坐标
            vertices_label = tk.Label(polygon_frame, text=f"输入多边形{i + 1}的顶点坐标（每行一个）:")
            vertices_label.pack()
            vertices_text = tk.Text(polygon_frame, wrap="word", height=5, width=50)
            vertices_text.pack()

            self.polygon_widgets.append((shift_x_entry, shift_y_entry, vertices_text))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=15, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 生成 Manim 代码
        class_name = "MyPolygonsScene"
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, (shift_x_entry, shift_y_entry, vertices_text) in enumerate(self.polygon_widgets):
            # 获取输入框的值
            shift_x = float(shift_x_entry.get())
            shift_y = float(shift_y_entry.get())
            vertices_str = vertices_text.get("1.0", tk.END).strip()
            vertices_lines = vertices_str.split("\n")

            # 解析顶点坐标
            vertices = []
            for line in vertices_lines:
                coords = line.split(",")
                vertex = [float(coord) for coord in coords]
                vertices.append(tuple(vertex))

            # 生成多边形对象
            polygon_code = f"""
        # 创建多边形对象
        polygon{i + 1} = Polygon(*{vertices}).shift({shift_x} * RIGHT + {shift_y} * UP)

        # 添加多边形对象到场景中
        self.add(polygon{i + 1})
        self.wait(3)
"""
            manim_code += polygon_code

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class RegularPolygramCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim RegularPolygram 代码生成器")
        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入多边形数量
        self.num_polygrams_label = tk.Label(self.master, text="要生成尖几个多边形?")
        self.num_polygrams_label.pack()
        self.num_polygrams_entry = tk.Entry(self.master)
        self.num_polygrams_entry.pack()

        # 添加确认按钮
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_polygrams = int(self.num_polygrams_entry.get())

        # 移除上一个界面的控件
        self.num_polygrams_label.pack_forget()
        self.num_polygrams_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入多边形特征的控件
        self.create_polygram_input_widgets()

    def create_polygram_input_widgets(self):
        self.polygram_widgets = []

        for i in range(self.num_polygrams):
            polygram_frame = tk.Frame(self.master)
            polygram_frame.pack(pady=5)

            # 输入多边形的顶点数量
            num_vertices_label = tk.Label(polygram_frame, text=f"尖多边形{i + 1}的顶点数量:")
            num_vertices_label.pack(side="left")
            num_vertices_entry = tk.Entry(polygram_frame)
            num_vertices_entry.pack(side="left")

            # 输入多边形的半径
            radius_label = tk.Label(polygram_frame, text=f"尖多边形{i + 1}的半径:")
            radius_label.pack(side="left")
            radius_entry = tk.Entry(polygram_frame)
            radius_entry.pack(side="left")

            # 输入多边形的位置偏移
            shift_x_label = tk.Label(polygram_frame, text=f"尖多边形{i + 1}的X偏移:")
            shift_x_label.pack(side="left")
            shift_x_entry = tk.Entry(polygram_frame)
            shift_x_entry.pack(side="left")

            shift_y_label = tk.Label(polygram_frame, text=f"尖多边形{i + 1}的Y偏移:")
            shift_y_label.pack(side="left")
            shift_y_entry = tk.Entry(polygram_frame)
            shift_y_entry.pack(side="left")

            self.polygram_widgets.append((num_vertices_entry, radius_entry, shift_x_entry, shift_y_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyPolygramScene"
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
"""
        for i, (num_vertices_entry, radius_entry, shift_x_entry, shift_y_entry) in enumerate(self.polygram_widgets):
            num_vertices = int(num_vertices_entry.get())
            radius = float(radius_entry.get())
            shift_x = float(shift_x_entry.get())
            shift_y = float(shift_y_entry.get())
            manim_code+=f"""
        # 生成 RegularPolygram 对象的代码
        repolygram = RegularPolygram(num_vertices={num_vertices}, radius={radius}).shift({shift_x} * RIGHT + {shift_y} * UP)
        self.add(repolygram)
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class RegularPolygonCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_polygons_label = tk.Label(self.master, text="要生成几个正多边形?")
        self.num_polygons_label.pack()
        self.num_polygons_entry = tk.Entry(self.master)
        self.num_polygons_entry.pack()

        # 确认多边形数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_polygons = int(self.num_polygons_entry.get())

        # 移除上一个界面的控件
        self.num_polygons_label.pack_forget()
        self.num_polygons_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入多边形特征的控件
        self.create_polygon_input_widgets()

    def create_polygon_input_widgets(self):
        self.polygon_widgets = []

        for i in range(self.num_polygons):
            polygon_frame = tk.Frame(self.master)
            polygon_frame.pack(pady=5)

            # 输入多边形顶点数量
            num_vertices_label = tk.Label(polygon_frame, text=f"正多边形{i + 1}的顶点数量:")
            num_vertices_label.pack(side="left")
            num_vertices_entry = tk.Entry(polygon_frame)
            num_vertices_entry.pack(side="left")

            # 输入多边形半径
            radius_label = tk.Label(polygon_frame, text=f"正多边形{i + 1}的半径:")
            radius_label.pack(side="left")
            radius_entry = tk.Entry(polygon_frame)
            radius_entry.pack(side="left")

            # 输入多边形位置偏移
            shift_x_label = tk.Label(polygon_frame, text=f"正多边形{i + 1}的X偏移:")
            shift_x_label.pack(side="left")
            shift_x_entry = tk.Entry(polygon_frame)
            shift_x_entry.pack(side="left")

            shift_y_label = tk.Label(polygon_frame, text=f"正多边形{i + 1}的Y偏移:")
            shift_y_label.pack(side="left")
            shift_y_entry = tk.Entry(polygon_frame)
            shift_y_entry.pack(side="left")

            self.polygon_widgets.append((num_vertices_entry, radius_entry, shift_x_entry, shift_y_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析多边形参数
        polygons = []
        for num_vertices_entry, radius_entry, shift_x_entry, shift_y_entry in self.polygon_widgets:
            num_vertices = int(num_vertices_entry.get())
            radius = float(radius_entry.get())
            shift_x = float(shift_x_entry.get())
            shift_y = float(shift_y_entry.get())
            polygons.append((num_vertices, radius, shift_x, shift_y))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
"""

        for i, (num_vertices, radius, shift_x, shift_y) in enumerate(polygons):
            manim_code += f"""
        # 创建多边形对象
        polygon{i + 1} = RegularPolygon(n={num_vertices}, radius={radius}).shift({shift_x} * RIGHT + {shift_y} * UP)

        # 添加多边形对象到场景中
        self.add(polygon{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class SphereCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_spheres_label = tk.Label(self.master, text="要生成几个球体?")
        self.num_spheres_label.pack()
        self.num_spheres_entry = tk.Entry(self.master)
        self.num_spheres_entry.pack()

        # 确认球体数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_spheres = int(self.num_spheres_entry.get())

        # 移除上一个界面的控件
        self.num_spheres_label.pack_forget()
        self.num_spheres_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入球体特征的控件
        self.create_sphere_input_widgets()

    def create_sphere_input_widgets(self):
        self.sphere_widgets = []

        for i in range(self.num_spheres):
            sphere_frame = tk.Frame(self.master)
            sphere_frame.pack(pady=5)

            # 输入半径
            radius_label = tk.Label(sphere_frame, text=f"球体{i + 1}的半径:")
            radius_label.pack(side="left")
            radius_entry = tk.Entry(sphere_frame)
            radius_entry.pack(side="left")

            # 输入位置
            center_label = tk.Label(sphere_frame, text=f"球体{i + 1}的中心位置(x, y, z):")
            center_label.pack(side="left")
            center_entry = tk.Entry(sphere_frame)
            center_entry.pack(side="left")

            self.sphere_widgets.append((radius_entry, center_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析球体参数
        spheres = []
        for radius_entry, center_entry in self.sphere_widgets:
            radius = float(radius_entry.get())
            center = tuple(map(float, center_entry.get().split(',')))
            spheres.append((radius, center))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        axes = ThreeDAxes()
        self.add(axes)
"""

        for i, (radius, center) in enumerate(spheres):
            manim_code += f"""
        # 创建球体对象
        sphere{i + 1} = Sphere(radius={radius}).move_to({center})

        # 添加球体对象到场景中
        self.add(sphere{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class TorusCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_tori_label = tk.Label(self.master, text="要生成几个环面?")
        self.num_tori_label.pack()
        self.num_tori_entry = tk.Entry(self.master)
        self.num_tori_entry.pack()

        # 确认环面数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_tori = int(self.num_tori_entry.get())

        # 移除上一个界面的控件
        self.num_tori_label.pack_forget()
        self.num_tori_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入环面特征的控件
        self.create_torus_input_widgets()

    def create_torus_input_widgets(self):
        self.torus_widgets = []

        for i in range(self.num_tori):
            torus_frame = tk.Frame(self.master)
            torus_frame.pack(pady=5)

            #环面的参数
            major_radius_label = tk.Label(torus_frame, text=f"环面{i + 1}的主半径:")
            major_radius_label.pack(side="left")
            major_radius_entry = tk.Entry(torus_frame)
            major_radius_entry.pack(side="left")

            minor_radius_label = tk.Label(torus_frame, text=f"环面{i + 1}的次半径:")
            minor_radius_label.pack(side="left")
            minor_radius_entry = tk.Entry(torus_frame)
            minor_radius_entry.pack(side="left")

            # 输入位置
            center_label = tk.Label(torus_frame, text=f"环面{i + 1}的中心位置(x, y, z):")
            center_label.pack(side="left")
            center_entry = tk.Entry(torus_frame)
            center_entry.pack(side="left")

            self.torus_widgets.append((major_radius_entry, minor_radius_entry, center_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析环面参数
        tori = []
        for major_radius_entry, minor_radius_entry, center_entry in self.torus_widgets:
            major_radius = float(major_radius_entry.get())
            minor_radius = float(minor_radius_entry.get())
            center = tuple(map(float, center_entry.get().split(',')))
            tori.append((major_radius, minor_radius, center))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        axes = ThreeDAxes()
        self.add(axes)
"""
        for i, (major_radius, minor_radius, center) in enumerate(tori):
            manim_code += f"""
        # 创建环面对象
        torus{i + 1} = Torus(major_radius={major_radius}, minor_radius={minor_radius}).move_to({center})

        # 添加环面对象到场景中
        self.add(torus{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class ConeCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_cones_label = tk.Label(self.master, text="要生成几个圆锥?")
        self.num_cones_label.pack()
        self.num_cones_entry = tk.Entry(self.master)
        self.num_cones_entry.pack()

        # 确认圆锥数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_cones = int(self.num_cones_entry.get())

        # 移除上一个界面的控件
        self.num_cones_label.pack_forget()
        self.num_cones_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入圆锥特征的控件
        self.create_cone_input_widgets()

    def create_cone_input_widgets(self):
        self.cone_widgets = []

        for i in range(self.num_cones):
            cone_frame = tk.Frame(self.master)
            cone_frame.pack(pady=5)

            # 圆锥的参数
            base_radius_label = tk.Label(cone_frame, text=f"圆锥{i + 1}的底面半径:")
            base_radius_label.pack(side="left")
            base_radius_entry = tk.Entry(cone_frame)
            base_radius_entry.pack(side="left")

            height_label = tk.Label(cone_frame, text=f"圆锥{i + 1}的高度:")
            height_label.pack(side="left")
            height_entry = tk.Entry(cone_frame)
            height_entry.pack(side="left")

            # 输入位置
            center_label = tk.Label(cone_frame, text=f"圆锥{i + 1}的中心位置(x, y, z):")
            center_label.pack(side="left")
            center_entry = tk.Entry(cone_frame)
            center_entry.pack(side="left")

            self.cone_widgets.append((base_radius_entry, height_entry, center_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析圆锥参数
        cones = []
        for base_radius_entry, height_entry, center_entry in self.cone_widgets:
            base_radius = float(base_radius_entry.get())
            height = float(height_entry.get())
            center = tuple(map(float, center_entry.get().split(',')))
            cones.append((base_radius, height, center))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        axes = ThreeDAxes()
        self.add(axes)
"""
        for i, (base_radius, height, center) in enumerate(cones):
            manim_code += f"""
        # 创建圆锥对象
        cone{i + 1} = Cone(base_radius={base_radius}, height={height}).move_to({center})

        # 添加圆锥对象到场景中
        self.add(cone{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class CylinderCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_cylinders_label = tk.Label(self.master, text="要生成几个圆柱?")
        self.num_cylinders_label.pack()
        self.num_cylinders_entry = tk.Entry(self.master)
        self.num_cylinders_entry.pack()

        # 确认圆柱数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_cylinders = int(self.num_cylinders_entry.get())

        # 移除上一个界面的控件
        self.num_cylinders_label.pack_forget()
        self.num_cylinders_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入圆柱特征的控件
        self.create_cylinder_input_widgets()

    def create_cylinder_input_widgets(self):
        self.cylinder_widgets = []

        for i in range(self.num_cylinders):
            cylinder_frame = tk.Frame(self.master)
            cylinder_frame.pack(pady=5)

            # 圆柱的参数
            radius_label = tk.Label(cylinder_frame, text=f"圆柱{i + 1}的底面半径:")
            radius_label.pack(side="left")
            radius_entry = tk.Entry(cylinder_frame)
            radius_entry.pack(side="left")

            height_label = tk.Label(cylinder_frame, text=f"圆柱{i + 1}的高度:")
            height_label.pack(side="left")
            height_entry = tk.Entry(cylinder_frame)
            height_entry.pack(side="left")

            # 输入位置
            center_label = tk.Label(cylinder_frame, text=f"圆柱{i + 1}的中心位置(x, y, z):")
            center_label.pack(side="left")
            center_entry = tk.Entry(cylinder_frame)
            center_entry.pack(side="left")

            self.cylinder_widgets.append((radius_entry, height_entry, center_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析圆柱参数
        cylinders = []
        for radius_entry, height_entry, center_entry in self.cylinder_widgets:
            radius = float(radius_entry.get())
            height = float(height_entry.get())
            center = tuple(map(float, center_entry.get().split(',')))
            cylinders.append((radius, height, center))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        axes = ThreeDAxes()
        self.add(axes)
"""
        for i, (radius, height, center) in enumerate(cylinders):
            manim_code += f"""
        # 创建圆柱对象
        cylinder{i + 1} = Cylinder(radius={radius}, height={height}).move_to({center})

        # 添加圆柱对象到场景中
        self.add(cylinder{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class Dot3DCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")
        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_dots_label = tk.Label(self.master, text="要生成几个三维点?")
        self.num_dots_label.pack()
        self.num_dots_entry = tk.Entry(self.master)
        self.num_dots_entry.pack()

        # 确认点的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_dots = int(self.num_dots_entry.get())

        # 移除上一个界面的控件
        self.num_dots_label.pack_forget()
        self.num_dots_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入点特征的控件
        self.create_dot_input_widgets()

    def create_dot_input_widgets(self):
        self.dot_widgets = []

        for i in range(self.num_dots):
            dot_frame = tk.Frame(self.master)
            dot_frame.pack(pady=5)

            # 输入位置
            position_label = tk.Label(dot_frame, text=f"点{i + 1}的位置(x, y, z):")
            position_label.pack(side="left")
            position_entry = tk.Entry(dot_frame)
            position_entry.pack(side="left")

            # 输入半径
            radius_label = tk.Label(dot_frame, text=f"点{i + 1}的半径:")
            radius_label.pack(side="left")
            radius_entry = tk.Entry(dot_frame)
            radius_entry.pack(side="left")

            self.dot_widgets.append((position_entry, radius_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析点参数
        dots = []
        for position_entry, radius_entry in self.dot_widgets:
            position = tuple(map(float, position_entry.get().split(',')))
            radius = float(radius_entry.get())
            dots.append((position, radius))
            print(position)

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes()
        self.add(axes)
"""
        for i, (position, radius) in enumerate(dots):
            manim_code += f"""
        # 创建三维点对象
        dot3d_{i + 1} = Dot3D(point=axes.coords_to_point{position}, radius={radius}, color="BLUE")

        # 添加三维点对象到场景中
        self.add(dot3d_{i + 1})
        self.wait(1)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class Line3DCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")
        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_lines_label = tk.Label(self.master, text="要生成几条三维线条?")
        self.num_lines_label.pack()
        self.num_lines_entry = tk.Entry(self.master)
        self.num_lines_entry.pack()

        # 确认线条的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_lines = int(self.num_lines_entry.get())

        # 移除上一个界面的控件
        self.num_lines_label.pack_forget()
        self.num_lines_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入线条特征的控件
        self.create_line_input_widgets()

    def create_line_input_widgets(self):
        self.line_widgets = []

        for i in range(self.num_lines):
            line_frame = tk.Frame(self.master)
            line_frame.pack(pady=5)

            # 输入起点和终点的坐标
            start_label = tk.Label(line_frame, text=f"线条{i + 1}的起点坐标(x, y, z):")
            start_label.pack(side="left")
            start_entry = tk.Entry(line_frame)
            start_entry.pack(side="left")

            end_label = tk.Label(line_frame, text=f"线条{i + 1}的终点坐标(x, y, z):")
            end_label.pack(side="left")
            end_entry = tk.Entry(line_frame)
            end_entry.pack(side="left")

            # 输入线条的粗细和颜色
            thickness_label = tk.Label(line_frame, text=f"线条{i + 1}的粗细:")
            thickness_label.pack(side="left")
            thickness_entry = tk.Entry(line_frame)
            thickness_entry.pack(side="left")

            color_label = tk.Label(line_frame, text=f"线条{i + 1}的颜色(大写英文字母):")
            color_label.pack(side="left")
            color_entry = tk.Entry(line_frame)
            color_entry.pack(side="left")

            self.line_widgets.append((start_entry, end_entry, thickness_entry, color_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析线条参数
        lines = []
        for start_entry, end_entry, thickness_entry, color_entry in self.line_widgets:
            start = tuple(map(float, start_entry.get().split(',')))
            end = tuple(map(float, end_entry.get().split(',')))
            thickness = float(thickness_entry.get())
            color = color_entry.get() 
            lines.append((start, end, thickness, color))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes()
        self.add(axes)
"""
        for i, (start, end, thickness, color) in enumerate(lines):
            manim_code += f"""
        # 创建三维线条对象
        line3d_{i + 1} = Line3D(start={start}, end={end}, thickness={thickness}, color="{color}")

        # 添加三维线条对象到场景中
        self.add(line3d_{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class Arrow3DCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")
        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_arrows_label = tk.Label(self.master, text="要生成几个三维箭头?")
        self.num_arrows_label.pack()
        self.num_arrows_entry = tk.Entry(self.master)
        self.num_arrows_entry.pack()

        # 确认箭头的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_arrows = int(self.num_arrows_entry.get())

        # 移除上一个界面的控件
        self.num_arrows_label.pack_forget()
        self.num_arrows_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入箭头特征的控件
        self.create_arrow_input_widgets()

    def create_arrow_input_widgets(self):
        self.arrow_widgets = []

        for i in range(self.num_arrows):
            arrow_frame = tk.Frame(self.master)
            arrow_frame.pack(pady=5)

            # 输入起点位置
            start_label = tk.Label(arrow_frame, text=f"箭头{i + 1}的起点位置(x, y, z):")
            start_label.pack(side="left")
            start_entry = tk.Entry(arrow_frame)
            start_entry.pack(side="left")

            # 输入终点位置
            end_label = tk.Label(arrow_frame, text=f"箭头{i + 1}的终点位置(x, y, z):")
            end_label.pack(side="left")
            end_entry = tk.Entry(arrow_frame)
            end_entry.pack(side="left")

            # 输入颜色
            color_label = tk.Label(arrow_frame, text=f"箭头{i + 1}的颜色:")
            color_label.pack(side="left")
            color_entry = tk.Entry(arrow_frame)
            color_entry.pack(side="left")

            self.arrow_widgets.append((start_entry, end_entry, color_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析箭头参数
        arrows = []
        for start_entry, end_entry, color_entry in self.arrow_widgets:
            start = tuple(map(float, start_entry.get().split(',')))
            end = tuple(map(float, end_entry.get().split(',')))
            color = color_entry.get()
            arrows.append((start, end, color))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes()
        self.add(axes)
"""
        for i, (start, end, color) in enumerate(arrows):
            manim_code += f"""
        # 创建三维箭头对象
        arrow3d_{i + 1} = Arrow3D(start={start}, end={end}, thickness=0.02, color="{color}")

        # 添加三维箭头对象到场景中
        self.add(arrow3d_{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class CrossCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")
        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.num_crosses_label = tk.Label(self.master, text="要生成几个十字架?")
        self.num_crosses_label.pack()
        self.num_crosses_entry = tk.Entry(self.master)
        self.num_crosses_entry.pack()

        # 确认十字架数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        self.num_crosses = int(self.num_crosses_entry.get())

        # 移除上一个界面的控件
        self.num_crosses_label.pack_forget()
        self.num_crosses_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入十字架特征的控件
        self.create_cross_input_widgets()

    def create_cross_input_widgets(self):
        self.cross_widgets = []

        for i in range(self.num_crosses):
            cross_frame = tk.Frame(self.master)
            cross_frame.pack(pady=5)

            # 输入位置
            position_label = tk.Label(cross_frame, text=f"十字架{i + 1}的位置(x, y, z):")
            position_label.pack(side="left")
            position_entry = tk.Entry(cross_frame)
            position_entry.pack(side="left")

            # 输入缩放因子
            scale_factor_label = tk.Label(cross_frame, text=f"十字架{i + 1}的缩放因子:")
            scale_factor_label.pack(side="left")
            scale_factor_entry = tk.Entry(cross_frame)
            scale_factor_entry.pack(side="left")

            # 输入颜色
            color_label = tk.Label(cross_frame, text=f"十字架{i + 1}的颜色:")
            color_label.pack(side="left")
            color_entry = tk.Entry(cross_frame)
            color_entry.pack(side="left")

            self.cross_widgets.append((position_entry, scale_factor_entry, color_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析十字架参数
        crosses = []
        for position_entry, scale_factor_entry, color_entry in self.cross_widgets:
            position = tuple(map(float, position_entry.get().split(',')))
            scale_factor = float(scale_factor_entry.get())
            color = color_entry.get()
            crosses.append((position, scale_factor, color))

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(axes)
"""
        for i, (position, scale_factor, color) in enumerate(crosses):
            manim_code += f"""
        # 创建十字架对象
        cross_{i + 1} = Cross(scale_factor={scale_factor}, color="{color}").move_to({position})

        # 添加十字架对象到场景中
        self.add(cross_{i + 1})
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

if __name__ == "__main__":
    root = tk.Tk()
    app = Arrow3DCodeGenerator(root)
    root.mainloop()
