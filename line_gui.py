import tkinter as tk
from tkinter import ttk
import subprocess
import uuid
import numpy as np


class LineCodeGenerator:
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

        self.start_label = tk.Label(self.master, text="起点(x,y,z)(逗号请使用英文形式):")
        self.start_label.pack()
        self.start_entry = tk.Entry(self.master)
        self.start_entry.pack()

        self.end_label = tk.Label(self.master, text="终点(x,y,z)(逗号请使用英文形式):")
        self.end_label.pack()
        self.end_entry = tk.Entry(self.master)
        self.end_entry.pack()

        self.buff_label = tk.Label(self.master, text="缓冲:")
        self.buff_label.pack()
        self.buff_entry = tk.Entry(self.master)
        self.buff_entry.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        duration = self.duration_entry.get()
        start_str = self.start_entry.get()
        end_str = self.end_entry.get()
        buff = self.buff_entry.get()
        class_name = "Line_" + str(uuid.uuid4()).replace("-", "")

        # 解析起点和终点字符串为数组
        start = np.array([float(x) for x in start_str.split(',')])
        end = np.array([float(x) for x in end_str.split(',')])

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建直线对象
        line = Line({tuple(start)}, {tuple(end)}, buff={buff})

        # 添加直线对象到场景中
        self.add(line)
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
app = LineCodeGenerator(root)
root.mainloop()


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

        self.start_x_label = tk.Label(self.master, text="起点x:")
        self.start_x_label.pack()
        self.start_x_entry = tk.Entry(self.master)
        self.start_x_entry.pack()

        self.start_y_label = tk.Label(self.master, text="起点y:")
        self.start_y_label.pack()
        self.start_y_entry = tk.Entry(self.master)
        self.start_y_entry.pack()

        self.start_z_label = tk.Label(self.master, text="起点z:")
        self.start_z_label.pack()
        self.start_z_entry = tk.Entry(self.master)
        self.start_z_entry.pack()

        self.end_x_label = tk.Label(self.master, text="终点x:")
        self.end_x_label.pack()
        self.end_x_entry = tk.Entry(self.master)
        self.end_x_entry.pack()

        self.end_y_label = tk.Label(self.master, text="终点y:")
        self.end_y_label.pack()
        self.end_y_entry = tk.Entry(self.master)
        self.end_y_entry.pack()

        self.end_z_label = tk.Label(self.master, text="终点z:")
        self.end_z_label.pack()
        self.end_z_entry = tk.Entry(self.master)
        self.end_z_entry.pack()

        self.buff_label = tk.Label(self.master, text="缓冲:")
        self.buff_label.pack()
        self.buff_entry = tk.Entry(self.master)
        self.buff_entry.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        duration = self.duration_entry.get()
        start_x = self.start_x_entry.get()
        start_y = self.start_y_entry.get()
        start_z = self.start_z_entry.get()
        end_x = self.end_x_entry.get()
        end_y = self.end_y_entry.get()
        end_z = self.end_z_entry.get()
        buff = self.buff_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建直线对象
        line = Line(np.array([{start_x}, {start_y}, {start_z}]), np.array([{end_x}, {end_y}, {end_z}]), buff={buff})

        # 添加直线对象到场景中
        self.add(line)
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