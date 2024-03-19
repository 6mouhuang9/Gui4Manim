import tkinter as tk
import subprocess
import uuid

class ManimCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加滑块控件用于调整参数
        self.duration_label = tk.Label(self.master, text="动画持续时间:")
        self.duration_label.pack()
        self.duration_scale = tk.Scale(self.master, from_=0, to=10, orient="horizontal", resolution=0.1)
        self.duration_scale.pack()

        self.num_circles_label = tk.Label(self.master, text="圆的数量:")
        self.num_circles_label.pack()
        self.num_circles_scale = tk.Scale(self.master, from_=1, to=10, orient="horizontal")
        self.num_circles_scale.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取滑块的值
        duration = self.duration_scale.get()
        num_circles = self.num_circles_scale.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据参数生成 Manim 代码
        #这里搞一个小区分，把点、线、圆、三角形、矩形、正方形等多边形分别列出来，用输入框选择也好，用下拉框选择也好，用button选择也好
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        animations = []
        for i in range({num_circles}):
            circle = Circle()
            animations.append(Create(circle))
            self.wait({duration / num_circles})
            self.play(*animations)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run([f"manim", "-pql", "manim_code.py", "{class_name}"])

def main():
    root = tk.Tk()
    app = ManimCodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

