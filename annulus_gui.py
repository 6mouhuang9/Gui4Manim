import tkinter as tk
from tkinter import ttk
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

        self.inner_radius_label = tk.Label(self.master, text="内半径:")
        self.inner_radius_label.pack()
        self.inner_radius_entry = tk.Entry(self.master)
        self.inner_radius_entry.pack()

        self.outer_radius_label = tk.Label(self.master, text="外半径:")
        self.outer_radius_label.pack()
        self.outer_radius_entry = tk.Entry(self.master)
        self.outer_radius_entry.pack()

        self.fill_opacity_label = tk.Label(self.master, text="填充透明度:")
        self.fill_opacity_label.pack()
        self.fill_opacity_entry = tk.Entry(self.master)
        self.fill_opacity_entry.pack()

        self.stroke_width_label = tk.Label(self.master, text="线宽:")
        self.stroke_width_label.pack()
        self.stroke_width_entry = tk.Entry(self.master)
        self.stroke_width_entry.pack()

        self.color_label = tk.Label(self.master, text="颜色:")
        self.color_label.pack()
        self.color_entry = tk.Entry(self.master)
        self.color_entry.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        duration = self.duration_entry.get()
        inner_radius = self.inner_radius_entry.get()
        outer_radius = self.outer_radius_entry.get()
        fill_opacity = self.fill_opacity_entry.get()
        stroke_width = self.stroke_width_entry.get()
        color = self.color_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建环对象
        annulus = Annulus(inner_radius={inner_radius}, 
                          outer_radius={outer_radius}, 
                          fill_opacity={fill_opacity}, 
                          stroke_width={stroke_width}, 
                          color="{color}")

        # 添加环对象到场景中
        self.add(annulus)
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

# 创建主窗口
root = tk.Tk()
app = ManimCodeGenerator(root)
root.mainloop()
