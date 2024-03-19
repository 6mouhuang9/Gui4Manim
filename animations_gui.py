import tkinter as tk
from tkinter import ttk
import subprocess
import uuid


class ManimTransformGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim Transform Effect Generator")

        # 创建选择Mobject1的下拉菜单
        self.mobject1_label = tk.Label(self.master, text="选择Mobject:")
        self.mobject1_label.pack()

        self.mobject1_variable = tk.StringVar(master)
        self.mobject1_variable.set("Square")  # 默认为Square
        self.mobject1_menu = tk.OptionMenu(self.master, self.mobject1_variable, "Square", "Circle", "Triangle")
        self.mobject1_menu.pack()

        # 创建选择Mobject2的下拉菜单
        self.mobject2_label = tk.Label(self.master, text="选择Mobject:")
        self.mobject2_label.pack()

        self.mobject2_variable = tk.StringVar(master)
        self.mobject2_variable.set("Square")  # 默认为Square
        self.mobject2_menu = tk.OptionMenu(self.master, self.mobject2_variable, "Square", "Circle", "Triangle")
        self.mobject2_menu.pack()

        # 创建设置动画参数的输入框
        self.duration_label = tk.Label(self.master, text="动画持续时间:")
        self.duration_label.pack()

        self.duration_entry = tk.Entry(self.master)
        self.duration_entry.pack()

        # 创建生成Manim代码的按钮
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack()

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取用户输入的参数
        mobject1 = self.mobject1_variable.get()
        mobject2 = self.mobject2_variable.get()
        duration = self.duration_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 生成Manim代码
        manim_code = f"""
from manim import *

class TransformScene(Scene):
    def construct(self):
        # 创建Mobject对象
        if "{mobject1}" == "Square":
            mobject1 = Square()
        elif "{mobject1}" == "Circle":
            mobject1 = Circle()
        elif "{mobject1}" == "Triangle":
            mobject1 = Triangle()
        
        if "{mobject2}" == "Square":
            mobject2 = Square()
        elif "{mobject2}" == "Circle":
            mobject2 = Circle()
        elif "{mobject2}" == "Triangle":
            mobject2 = Triangle()

        # 执行Transform动画
        self.play(Transform(mobject1, mobject2, run_time={duration}))
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
app = ManimTransformGUI(root)
root.mainloop()
