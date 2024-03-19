import tkinter as tk
from tkinter import simpledialog
import subprocess
import uuid
import numpy as np

class ManimCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加输入框用于输入参数
        self.duration_label = tk.Label(self.master, text="动画持续时间:")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(self.master)
        self.duration_entry.pack()

        self.point_label = tk.Label(self.master, text="点的坐标(x, y, z):")
        self.point_label.pack()
        self.point_entry = tk.Entry(self.master)
        self.point_entry.pack()

        self.radius_label = tk.Label(self.master, text="半径:")
        self.radius_label.pack()
        self.radius_entry = tk.Entry(self.master)
        self.radius_entry.pack()

        self.stroke_width_label = tk.Label(self.master, text="线宽:")
        self.stroke_width_label.pack()
        self.stroke_width_entry = tk.Entry(self.master)
        self.stroke_width_entry.pack()

        self.fill_opacity_label = tk.Label(self.master, text="填充透明度:")
        self.fill_opacity_label.pack()
        self.fill_opacity_entry = tk.Entry(self.master)
        self.fill_opacity_entry.pack()

        self.color_label = tk.Label(self.master, text="颜色:")
        self.color_label.pack()
        self.color_entry = tk.Entry(self.master)
        self.color_entry.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 创建参数输入框
        self.modify_params_button = tk.Button(self.master, text="修改参数", command=self.modify_params)
        self.modify_params_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        duration = self.duration_entry.get()
        point_str = self.point_entry.get()
        radius = self.radius_entry.get()
        stroke_width = self.stroke_width_entry.get()
        fill_opacity = self.fill_opacity_entry.get()
        color = self.color_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 解析点的坐标字符串为数组
        point = np.array([float(x) for x in point_str.split(',')])

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建点对象
        dot = Dot({tuple(point)}, 
                  radius={radius}, 
                  stroke_width={stroke_width}, 
                  fill_opacity={fill_opacity}, 
                  color="{color}")

        # 添加点对象到场景中
        self.add(dot)
        self.wait({duration})
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

    def modify_params(self):
        # 在这里更新参数值为用户输入的新值
        new_duration = simpledialog.askfloat("修改参数", "请输入新的动画持续时间:")
        if new_duration is not None:
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, new_duration)
# 创建主窗口
root = tk.Tk()
app = ManimCodeGenerator(root)
root.mainloop()
