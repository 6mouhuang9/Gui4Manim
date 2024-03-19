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

        self.num_annuli_label = tk.Label(self.master, text="要生成几个环?")
        self.num_annuli_label.pack()
        self.num_annuli_entry = tk.Entry(self.master)
        self.num_annuli_entry.pack()

        # 添加按钮用于确认环的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_num_annuli)
        self.confirm_button.pack(pady=5)

    def confirm_num_annuli(self):
        # 获取输入框的值，确认要生成的环的数量
        self.num_annuli = int(self.num_annuli_entry.get())

        # 移除上一个界面的控件
        self.duration_label.pack_forget()
        self.duration_entry.pack_forget()
        self.num_annuli_label.pack_forget()
        self.num_annuli_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入环特征的控件
        self.create_annuli_input_widgets()

    def create_annuli_input_widgets(self):
        self.annuli_widgets = []

        for i in range(self.num_annuli):
            annuli_frame = ttk.Frame(self.master)
            annuli_frame.pack(pady=5)

            inner_radius_label = tk.Label(annuli_frame, text=f"环{i + 1}的内半径:")
            inner_radius_label.pack(side="left")

            inner_radius_entry = tk.Entry(annuli_frame)
            inner_radius_entry.pack(side="left")

            outer_radius_label = tk.Label(annuli_frame, text=f"环{i + 1}的外半径:")
            outer_radius_label.pack(side="left")

            outer_radius_entry = tk.Entry(annuli_frame)
            outer_radius_entry.pack(side="left")

            fill_opacity_label = tk.Label(annuli_frame, text=f"环{i + 1}的填充透明度:")
            fill_opacity_label.pack(side="left")

            fill_opacity_entry = tk.Entry(annuli_frame)
            fill_opacity_entry.pack(side="left")

            stroke_width_label = tk.Label(annuli_frame, text=f"环{i + 1}的线宽:")
            stroke_width_label.pack(side="left")

            stroke_width_entry = tk.Entry(annuli_frame)
            stroke_width_entry.pack(side="left")

            color_label = tk.Label(annuli_frame, text=f"环{i + 1}的颜色:")
            color_label.pack(side="left")

            color_entry = tk.Entry(annuli_frame)
            color_entry.pack(side="left")

            self.annuli_widgets.append((inner_radius_entry, outer_radius_entry, fill_opacity_entry, stroke_width_entry, color_entry))

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

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        for i, annuli_widget in enumerate(self.annuli_widgets):
            inner_radius = annuli_widget[0].get()
            outer_radius = annuli_widget[1].get()
            fill_opacity = annuli_widget[2].get()
            stroke_width = annuli_widget[3].get()
            color = annuli_widget[4].get()

            manim_code += f"""
        # 创建环对象
        annulus{i+1} = Annulus(inner_radius={inner_radius}, 
                                outer_radius={outer_radius}, 
                                fill_opacity={fill_opacity}, 
                                stroke_width={stroke_width}, 
                                color="{color}")

        # 添加环对象到场景中
        self.add(annulus{i+1})
        self.wait({duration/self.num_annuli})
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

