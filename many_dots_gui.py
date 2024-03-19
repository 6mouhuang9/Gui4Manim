import tkinter as tk
from tkinter import ttk
import subprocess
import uuid
import numpy as np

class ManimCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.num_points = 0

        self.create_widgets()

    def create_widgets(self):
        #持续时间
        self.duration_label = tk.Label(self.master, text="动画持续时间:")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(self.master)
        self.duration_entry.pack()

        #输入点的数量
        self.num_points_label = tk.Label(self.master, text="要生成几个点?")
        self.num_points_label.pack()
        self.num_points_entry = tk.Entry(self.master)
        self.num_points_entry.pack()

        #确认点的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_input)
        self.confirm_button.pack(pady=5)

    def confirm_input(self):
        # 获取时间与生成的点的数量
        self.duration = int(self.duration_entry.get())
        self.num_points = int(self.num_points_entry.get())

        # 移除上一个界面的控件
        self.duration_label.pack_forget()
        self.duration_entry.pack_forget()
        self.num_points_label.pack_forget()
        self.num_points_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入点特征的控件
        self.create_point_input_widgets()

    def create_point_input_widgets(self):
        self.point_widgets = []

        for i in range(self.num_points):
            point_frame = ttk.Frame(self.master)
            point_frame.pack(pady=5)

            point_label = tk.Label(point_frame, text=f"点{i + 1}的坐标(x, y, z):")
            point_label.pack(side="left")

            point_entry = tk.Entry(point_frame)
            point_entry.pack(side="left")

            self.point_widgets.append(point_entry)

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        duration = int(self.duration_entry.get())
        #radius = self.radius_entry.get()
        #stroke_width = self.stroke_width_entry.get()
        #fill_opacity = self.fill_opacity_entry.get()
        #color = self.color_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析点的坐标字符串为数组
        points = []
        for widget in self.point_widgets:
            point_str = widget.get()
            point = np.array([float(x) for x in point_str.split(',')])
            points.append(point)

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, point in enumerate(points):
            manim_code += f"""
        # 创建点对象
        dot{i+1} = Dot({tuple(point)}, 
                       radius={0.08}, 
                       stroke_width={0}, 
                       fill_opacity={1.0}, 
                       color="WHITE")

        # 添加点对象到场景中
        self.add(dot{i+1})
        self.wait({duration/self.num_points})
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

# 创建主窗口
root = tk.Tk()
app = ManimCodeGenerator(root)
root.mainloop()
