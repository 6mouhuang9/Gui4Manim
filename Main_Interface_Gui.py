import tkinter as tk
from tkinter import ttk
import subprocess
import uuid

class MainGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 动画生成器")

        # 设置窗口大小
        self.master.geometry("600x400")

        # 创建一个 Frame 来容纳按钮
        self.button_frame_top = tk.Frame(self.master)
        self.button_frame_top.pack(side="top", fill="x")

        # 创建生成动画按钮
        self.generate_button = tk.Button(self.master, text="生成动画", command=self.generate_animation, font=("Times New Roman", 20))
        self.generate_button.pack(fill='x', padx=50, pady=50)

        # 创建一个 Frame 来容纳按钮
        self.button_frame_bottom = tk.Frame(self.master)
        self.button_frame_bottom.pack(side="bottom", fill="x")

         # 创建查询范例按钮
        self.query_button = tk.Button(self.master, text="查询范例", command=self.query_examples, font=("Times New Roman", 20))
        self.query_button.pack(fill='x', padx=50, pady=50)

    def generate_animation(self):

        # 创建生成动画界面
        animation_gui = AnimationGUI(tk.Tk())

        # 销毁当前界面
        self.master.destroy()

    def query_examples(self):
        # 在这里添加查询范例的逻辑
        self.master.destroy()

        example_gui = ExampleGUI()

class AnimationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        # 添加下拉菜单
        self.graph_type_label = tk.Label(self.master, text="选择图像类型:", font=("Times New Roman", 12))
        self.graph_type_label.pack()
        self.graph_type_variable = tk.StringVar(master)
        self.graph_type_variable.set("角")  # 默认为角
        self.graph_type_menu = tk.OptionMenu(self.master, self.graph_type_variable, "角", "圆形", "矩形", "三角形","星形")
        self.graph_type_menu.pack()

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.duration_label = tk.Label(self.master, text="动画持续时间:")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(self.master)
        self.duration_entry.pack()

        self.num_objects_label = tk.Label(self.master, text="要生成几个图形?")
        self.num_objects_label.pack()
        self.num_objects_entry = tk.Entry(self.master)
        self.num_objects_entry.pack()

        # 添加按钮用于确认对象的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_num_objects)
        self.confirm_button.pack(pady=5)

    def confirm_num_objects(self):
        # 获取输入框的值，确认要生成的对象的数量
        self.num_objects = int(self.num_objects_entry.get())

        # 移除上一个界面的控件
        self.duration_label.pack_forget()
        self.duration_entry.pack_forget()
        self.num_objects_label.pack_forget()
        self.num_objects_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 根据用户选择的图像类型创建相应的控件
        if self.graph_type_variable.get() == "角":
            self.create_arc_input_widgets()
        elif self.graph_type_variable.get() == "圆形":
            self.create_circle_input_widgets()
        elif self.graph_type_variable.get() == "矩形":
            self.create_rectangle_input_widgets()
        elif self.graph_type_variable.get() == "三角形":
            self.create_triangle_input_widgets
        elif self.graph_type_variable.get() == "星形":
            self.create_star_input_widgets()
            
    def create_arc_input_widgets(self):
        self.arc_widgets = []

        for i in range(self.num_objects):
            arc_frame = ttk.Frame(self.master)
            arc_frame.pack(pady=5)

            start_angle_label = tk.Label(arc_frame, text=f"弧{i + 1}的起始角度:")
            start_angle_label.pack(side="left")

            start_angle_entry = tk.Entry(arc_frame)
            start_angle_entry.pack(side="left")

            angle_label = tk.Label(arc_frame, text=f"弧{i + 1}的角度:")
            angle_label.pack(side="left")

            angle_entry = tk.Entry(arc_frame)
            angle_entry.pack(side="left")

            radius_label = tk.Label(arc_frame, text=f"弧{i + 1}的半径:")
            radius_label.pack(side="left")

            radius_entry = tk.Entry(arc_frame)
            radius_entry.pack(side="left")

            self.arc_widgets.append((start_angle_entry, angle_entry, radius_entry))

        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def create_circle_input_widgets(self):
        self.circle_widgets = []

        for i in range(self.num_objects):
            circle_frame = ttk.Frame(self.master)
            circle_frame.pack(pady=5)

            #半径输入框
            radius_label = tk.Label(circle_frame, text=f"圆{i + 1}的半径:")
            radius_label.pack(side="left")

            radius_entry = tk.Entry(circle_frame)
            radius_entry.pack(side="left")

            #x坐标输入框
            x_label = tk.Label(circle_frame, text=f"圆{i + 1}的 x 坐标:")
            x_label.pack(side="left")

            x_entry = tk.Entry(circle_frame)
            x_entry.pack(side="left")

            #y坐标输入框
            y_label = tk.Label(circle_frame, text=f"圆{i + 1}的 y 坐标:")
            y_label.pack(side="left")

            y_entry = tk.Entry(circle_frame)
            y_entry.pack(side="left")

            self.circle_widgets.append((radius_entry, x_entry, y_entry))

        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()
    
    def create_rectangle_input_widgets(self):
        # 添加矩形图像的输入框设置
        self.rectangle_widgets = []

        for i in range(self.num_objects):
            triangle_frame = ttk.Frame(self.master)
            triangle_frame.pack(pady=5)

            # 添加边长输入框
            side_length_label = tk.Label(triangle_frame, text=f"三角形{i + 1}的边长:")
            side_length_label.pack(side="left")

            side_length_entry = tk.Entry(triangle_frame)
            side_length_entry.pack(side="left")

            # 添加 x 坐标输入框
            x_label = tk.Label(triangle_frame, text=f"三角形{i + 1}的 x 坐标:")
            x_label.pack(side="left")

            x_entry = tk.Entry(triangle_frame)
            x_entry.pack(side="left")

            # 添加 y 坐标输入框
            y_label = tk.Label(triangle_frame, text=f"三角形{i + 1}的 y 坐标:")
            y_label.pack(side="left")

            y_entry = tk.Entry(triangle_frame)
            y_entry.pack(side="left")

            # 将当前三角形的输入框添加到三角形的小部件列表中
            self.triangle_widgets.append((side_length_entry, x_entry, y_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def create_triangle_input_widgets(self):
        # 添加三角形的输入框设置
        self.triangle_widgets = []

        for i in range(self.num_objects):
            triangle_frame = ttk.Frame(self.master)
            triangle_frame.pack(pady=5)

            # 添加边长输入框
            side_length_label = tk.Label(triangle_frame, text=f"三角形{i + 1}的边长:")
            side_length_label.pack(side="left")

            side_length_entry = tk.Entry(triangle_frame)
            side_length_entry.pack(side="left")

            # 添加 x 坐标输入框
            x_label = tk.Label(triangle_frame, text=f"三角形{i + 1}的 x 坐标:")
            x_label.pack(side="left")

            x_entry = tk.Entry(triangle_frame)
            x_entry.pack(side="left")

            # 添加 y 坐标输入框
            y_label = tk.Label(triangle_frame, text=f"三角形{i + 1}的 y 坐标:")
            y_label.pack(side="left")

            y_entry = tk.Entry(triangle_frame)
            y_entry.pack(side="left")

            # 将当前三角形的输入框添加到三角形的小部件列表中
            self.triangle_widgets.append((side_length_entry, x_entry, y_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    
    def create_star_input_widgets(self):
        self.stars_widgets = []

        for i in range(self.num_objects):
            stars_frame = ttk.Frame(self.master)
            stars_frame.pack(pady=5)

            n_label = tk.Label(stars_frame, text=f"星形{i + 1}的角数:")
            n_label.pack(side="left")

            n_entry = tk.Entry(stars_frame)
            n_entry.pack(side="left")

            outer_radius_label = tk.Label(stars_frame, text=f"星形{i + 1}的外半径:")
            outer_radius_label.pack(side="left")

            outer_radius_entry = tk.Entry(stars_frame)
            outer_radius_entry.pack(side="left")

            inner_radius_label = tk.Label(stars_frame, text=f"星形{i + 1}的内半径:")
            inner_radius_label.pack(side="left")

            inner_radius_entry = tk.Entry(stars_frame)
            inner_radius_entry.pack(side="left")

            density_label = tk.Label(stars_frame, text=f"星形{i + 1}的密度:")
            density_label.pack(side="left")

            density_entry = tk.Entry(stars_frame)
            density_entry.pack(side="left")

            color_label = tk.Label(stars_frame, text=f"星形{i + 1}的颜色:")
            color_label.pack(side="left")

            color_entry = tk.Entry(stars_frame)
            color_entry.pack(side="left")

            position_x_label = tk.Label(stars_frame, text=f"星形{i + 1}的 X 坐标:")
            position_x_label.pack(side="left")

            position_x_entry = tk.Entry(stars_frame)
            position_x_entry.pack(side="left")

            position_y_label = tk.Label(stars_frame, text=f"星形{i + 1}的 Y 坐标:")
            position_y_label.pack(side="left")

            position_y_entry = tk.Entry(stars_frame)
            position_y_entry.pack(side="left")

            self.stars_widgets.append((n_entry, outer_radius_entry, inner_radius_entry, density_entry, color_entry, position_x_entry, position_y_entry))

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        duration = int(self.duration_entry.get())
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据用户选择的图像类型生成相应的 Manim 代码
        if self.graph_type_variable.get() == "角":
            manim_code = self.generate_arc_manim_code(duration, class_name)
        elif self.graph_type_variable.get() == "圆形":
            manim_code = self.generate_circle_manim_code(duration, class_name)
        elif self.graph_type_variable.get() == "矩形":
            manim_code = self.generate_rectangle_manim_code(duration, class_name)
        elif self.graph_type_variable.get() == "三角形":
            manim_code = self.generate_triangle_manim_code(duration, class_name)
        elif self.graph_type_variable.get() == "星形":
            manim_code = self.generate_star_manim_code(duration, class_name)
        

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

    def generate_arc_manim_code(self, duration, class_name):
        # 生成弧形图像类型的 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, arc_widget in enumerate(self.arc_widgets):
            start_angle = arc_widget[0].get()
            angle = arc_widget[1].get()
            radius = arc_widget[2].get()

            manim_code += f"""
        # 创建弧对象
        arc{i+1} = Arc(start_angle={start_angle}, angle={angle}, radius={radius})

        # 添加弧对象到场景中
        self.add(arc{i+1})
        self.wait({duration/self.num_objects})
    """

        return manim_code

    def generate_circle_manim_code(self, duration, class_name):
        # 生成圆形的 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""
        
        for i, circle_widget in enumerate(self.circle_widgets):
            radius = circle_widget[0].get()
            x = circle_widget[1].get()
            y = circle_widget[2].get()

            manim_code += f"""
        # 创建圆对象
        circle{i+1} = Circle(radius={radius}).shift({x}, {y})

        # 添加圆对象到场景中
        self.add(circle{i+1})
        self.wait({duration/self.num_objects})
"""

        return manim_code

    def generate_rectangle_manim_code(self, duration, class_name):
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, rectangle_widget in enumerate(self.rectangle_widgets):
            width = rectangle_widget[0].get()
            height = rectangle_widget[1].get()

            manim_code += f"""
            # 创建矩形对象
            rectangle{i+1} = Rectangle(width={width}, height={height})

            # 添加矩形对象到场景中
            self.add(rectangle{i+1})
            self.wait({duration/self.num_objects})
    """

        return manim_code

    def generate_triangle_manim_code(self, duration, class_name):
        # 生成其他类型图像的 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, triangle_widget in enumerate(self.triangle_widgets):
            side_length = triangle_widget[0].get()
            x = triangle_widget[1].get()
            y = triangle_widget[2].get()

            manim_code += f"""
            # 创建三角形对象
            triangle{i+1} = Triangle(**{{
                "side_length": {side_length},
                "stroke_width": 2,
                "fill_opacity": 0.5,
                "color": WHITE
            }}).shift({x}, {y})

            # 添加三角形对象到场景中
            self.add(triangle{i+1})
            self.wait({duration/self.num_objects})
    """

        return manim_code

    def generate_star_manim_code(self, duration, class_name):
        # 生成星形图像类型的 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, stars_widget in enumerate(self.stars_widgets):
            n = stars_widget[0].get()
            outer_radius = stars_widget[1].get()
            inner_radius = stars_widget[2].get()
            density = stars_widget[3].get()
            color = stars_widget[4].get()
            position_x = stars_widget[5].get()
            position_y = stars_widget[6].get()

            manim_code += f"""
        # 创建星形对象
        star_{i+1} = Star(n={n}, 
                          outer_radius={outer_radius}, 
                          inner_radius={inner_radius}, 
                          density={density},
                          color={color}).shift({position_x}, {position_y})

        # 添加星形对象到场景中
        self.play(Create(star_{i+1}))
        self.wait({duration/self.num_objects})
"""

class ExampleGUI:
    pass

def main():
    root = tk.Tk()
    app = MainGUI(root) 
    root.mainloop()

if __name__ == "__main__":
    main()
