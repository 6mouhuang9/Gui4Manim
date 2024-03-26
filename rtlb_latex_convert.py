import tkinter as tk
from manim import *
import subprocess
from sympy import latex,sympify
import uuid

class AnimatedBoundaryGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("动画边界生成器")

        # 添加输入框用于输入参数
        self.text_label = tk.Label(self, text="输入文本：")
        self.text_label.pack()
        self.text_entry = tk.Entry(self)
        self.text_entry.pack()

        self.colors_label = tk.Label(self, text="输入颜色（以逗号分隔的十六进制值）：")
        self.colors_label.pack()
        self.colors_entry = tk.Entry(self)
        self.colors_entry.pack()

        self.max_stroke_width_label = tk.Label(self, text="最大线宽：")
        self.max_stroke_width_label.pack()
        self.max_stroke_width_entry = tk.Entry(self)
        self.max_stroke_width_entry.pack()

        self.cycle_rate_label = tk.Label(self, text="循环率：")
        self.cycle_rate_label.pack()
        self.cycle_rate_entry = tk.Entry(self)
        self.cycle_rate_entry.pack()

        self.back_and_forth_label = tk.Label(self, text="来回移动：")
        self.back_and_forth_label.pack()
        self.back_and_forth_var = tk.BooleanVar()
        self.back_and_forth_checkbutton = tk.Checkbutton(self, variable=self.back_and_forth_var)
        self.back_and_forth_checkbutton.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        text = self.text_entry.get()
        #colors = self.colors_entry.get().split(',')
        colors = self.colors_entry.get()
        max_stroke_width = self.max_stroke_width_entry.get()
        cycle_rate = self.cycle_rate_entry.get()
        back_and_forth = self.back_and_forth_var.get()

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class AnimatedBoundaryScene(Scene):
    def construct(self):
        # 创建 AnimatedBoundary 对象
        text = Text("{text}"),
        boundary = AnimatedBoundary(
            text,
            colors=[{colors}],
            max_stroke_width={max_stroke_width},
            cycle_rate={cycle_rate},
            back_and_forth={back_and_forth}
        )

        # 播放动画
        self.add(text, boundary)
        self.wait(3)
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("animated_boundary_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "animated_boundary_code.py", "AnimatedBoundaryScene"])


class RTLBCodeGenerator:
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

        self.text_label = tk.Label(self.master, text="文本:")
        self.text_label.pack()
        self.text_entry = tk.Entry(self.master)
        self.text_entry.pack()

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
        text = self.text_entry.get()
        buff = self.buff_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建文本对象
        text = Text("{text}")

        # 添加文本对象到场景中
        self.add(text)

        # 对文本对象应用 RemoveTextLetterByLetter 动画效果
        self.play(
            RemoveTextLetterByLetter(text, buff={buff}),  # 逐字删除文本
            run_time={duration}  # 动画时长
        )
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class ADLBCodeGenerator:
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

        self.text_label = tk.Label(self.master, text="文本:")
        self.text_label.pack()
        self.text_entry = tk.Entry(self.master)
        self.text_entry.pack()

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
        text = self.text_entry.get()
        buff = self.buff_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建文本对象
        text = Text("{text}")

        # 添加文本对象到场景中
        self.add(text)

        # 对文本对象应用 AddTextLetterByLetter 动画效果
        self.play(
            AddTextLetterByLetter(text, buff={buff}),  # 逐字添加文本
            run_time={duration}  # 动画时长
        )
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])


class CircumscribeCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加选择动画对象的下拉菜单
        self.animation_label = tk.Label(self.master, text="选择动画对象:")
        self.animation_label.pack()
        self.animation_var = tk.StringVar(self.master)
        self.animation_var.set("Dot")  # 默认选择 Dot
        self.animation_options = ["Dot", "Circle", "Square", "Text"]
        self.animation_dropdown = tk.OptionMenu(self.master, self.animation_var, *self.animation_options)
        self.animation_dropdown.pack()

        # 添加输入框用于输入 Mobject 对象字符串
        self.mobject_label = tk.Label(self.master, text="输入 Mobject 对象字符串:")
        self.mobject_label.pack()
        self.mobject_entry = tk.Entry(self.master)
        self.mobject_entry.pack()

        # 添加按钮用于转换 MathType 到 LaTeX
        self.convert_button = tk.Button(self.master, text="转换到 LaTeX", command=self.convert_to_latex)
        self.convert_button.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def convert_to_latex(self):
        # 从输入框中获取 MathType 字符串
        math_type_str = self.mobject_entry.get()
        # 使用 sympy 的 latex 函数将 MathType 字符串转换为 LaTeX 字符串
        latex_str = latex(sympify(math_type_str))
        # 在文本框中显示 LaTeX 字符串
        self.mobject_entry.delete(0, tk.END)
        self.mobject_entry.insert(0, latex_str)

    def generate_manim_code(self):
        # 获取输入框的值
        animation_type = self.animation_var.get()
        mobject_str = self.mobject_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据选择生成 Mobject 对象字符串
        if animation_type == "Text":
            animation_str = f'Text(r"{mobject_str}")'
        else:
            animation_str = f"{animation_type}()"

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建动画对象
        animation_obj = {animation_str}

        # 添加 Mobject 对象到场景中
        self.add(animation_obj)

        # 应用动画效果
        self.play(
            Circumscribe(animation_obj)
        )
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class ShowCreationThenFadeOutCodeGenerator:
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

        self.mobject_label = tk.Label(self.master, text="Mobject 对象字符串:")
        self.mobject_label.pack()
        self.mobject_entry = tk.Entry(self.master)
        self.mobject_entry.pack()

        # 添加按钮用于转换 MathType 到 LaTeX
        self.convert_button = tk.Button(self.master, text="转换到 LaTeX", command=self.convert_to_latex)
        self.convert_button.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def convert_to_latex(self):
        # 从输入框中获取 MathType 字符串
        math_type_str = self.mobject_entry.get()
        # 使用 sympy 的 latex 函数将 MathType 字符串转换为 LaTeX 字符串
        latex_str = latex(sympify(math_type_str))
        # 在文本框中显示 LaTeX 字符串
        self.mobject_entry.delete(0, tk.END)
        self.mobject_entry.insert(0, latex_str)

    def generate_manim_code(self):
        # 获取输入框的值
        duration = self.duration_entry.get()
        mobject_str = self.mobject_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 创建 Mobject 对象
        mobject = f"Text(r'{mobject_str}')"  # 使用 Text 作为示例

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建 Mobject 对象
        mobject = {mobject}

        # 添加 Mobject 对象到场景中并显示
        self.play(ShowCreationThenFadeOut(mobject))
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

class BroadcastCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 代码生成器")

        self.create_widgets()

    def create_widgets(self):
        # 添加选择动画对象的下拉菜单
        self.animation_label = tk.Label(self.master, text="选择动画对象:")
        self.animation_label.pack()
        self.animation_var = tk.StringVar(self.master)
        self.animation_var.set("Dot")  # 默认选择 Dot
        self.animation_options = ["Dot", "Circle", "Square", "Text"]
        self.animation_dropdown = tk.OptionMenu(self.master, self.animation_var, *self.animation_options)
        self.animation_dropdown.pack()

        # 添加输入框用于输入 Mobject 对象字符串
        self.mobject_label = tk.Label(self.master, text="输入 Mobject 对象字符串:")
        self.mobject_label.pack()
        self.mobject_entry = tk.Entry(self.master)
        self.mobject_entry.pack()

        # 添加按钮用于转换 MathType 到 LaTeX
        self.convert_button = tk.Button(self.master, text="转换到 LaTeX", command=self.convert_to_latex)
        self.convert_button.pack()

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def convert_to_latex(self):
        # 从输入框中获取 MathType 字符串
        math_type_str = self.mobject_entry.get()
        # 使用 sympy 的 latex 函数将 MathType 字符串转换为 LaTeX 字符串
        latex_str = latex(sympify(math_type_str))
        # 在文本框中显示 LaTeX 字符串
        self.mobject_entry.delete(0, tk.END)
        self.mobject_entry.insert(0, latex_str)

    def generate_manim_code(self):
        # 获取输入框的值
        animation_type = self.animation_var.get()
        mobject_str = self.mobject_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据选择生成 Mobject 对象字符串
        if animation_type == "Text":
            animation_str = f'Text(r"{mobject_str}")'
        else:
            animation_str = f"{animation_type}()"

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
        # 创建动画对象
        animation_obj = {animation_str}

        # 添加 Mobject 对象到场景中
        self.add(animation_obj)

        # 应用动画效果
        self.play(
            Broadcast(animation_obj)
        )
"""

        # 将生成的代码显示在文本框中
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run(["manim", "-pql", "manim_code.py", f"{class_name}"])

class SuccessionGenerator:
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

        # 添加按钮用于生成代码
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加文本框用于显示生成的代码
        self.code_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.code_text.pack()

    def generate_manim_code(self):
        # 获取输入框的值
        duration = self.duration_entry.get()
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")

        # 根据参数生成 Manim 代码
        manim_code = f"""\
from manim import *

class {class_name}(Scene):
    def construct(self):
"""

        # 添加 Succession 动画效果代码
        manim_code += f"""
        dot1 = Dot(point=LEFT * 2 + UP * 2, radius=0.16, color=BLUE)
        dot2 = Dot(point=LEFT * 2 + DOWN * 2, radius=0.16, color=MAROON)
        dot3 = Dot(point=RIGHT * 2 + DOWN * 2, radius=0.16, color=GREEN)
        dot4 = Dot(point=RIGHT * 2 + UP * 2, radius=0.16, color=YELLOW)
        self.add(dot1, dot2, dot3, dot4)

        self.play(Succession(
            dot1.animate.move_to(dot2),
            dot2.animate.move_to(dot3),
            dot3.animate.move_to(dot4),
            dot4.animate.move_to(dot1),
            run_time = {duration}
        ))
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
def run():
    root = tk.Tk()
    app = AnimatedBoundaryGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    run()