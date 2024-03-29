from tkinter import ttk
import tkinter as tk
import subprocess
import uuid

# 示例动画对象类型及其参数定义
OBJECTS_PARAMS = {
    "Circle": {"radius": (1, 10)},
    "Square": {"side_length": (1, 10)},
    # 可以根据需要添加更多类型及其参数
}

class ManimGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 动画代码生成器")

        #self.current_params_widgets = []  # 当前展示的参数控件列表
        self.params_widgets = {}  # 存储参数名称和对应控件的字典
        self.create_initial_widgets()

    def create_initial_widgets(self):
        # 动画对象类型选择
        self.object_type_label = tk.Label(self.master, text="选择动画对象类型:")
        self.object_type_label.pack()
        self.object_type_var = tk.StringVar()
        self.object_type_optionmenu = tk.OptionMenu(
            self.master, self.object_type_var, *OBJECTS_PARAMS.keys(), command=self.on_object_type_selected)
        self.object_type_optionmenu.pack()

    def on_object_type_selected(self, choice):
        # 清除旧的参数控件
        for widget in self.params_widgets:
            widget.destroy()
        self.params_widgets.clear()

        # 为所选对象类型创建新的参数控件
        for param, range in OBJECTS_PARAMS[choice].items():
            label = tk.Label(self.master, text=f"{param}:")
            label.pack()
            scale = tk.Scale(self.master, from_=range[0], to=range[1], orient="horizontal")
            scale.pack()
            self.params_widgets[param] = {'label' : label , 'scale' : scale}

        # 添加生成代码的按钮
        self.generate_button = tk.Button(self.master, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

        # 添加用于显示生成的代码的文本框
        self.code_text = tk.Text(self.master, wrap="word", height=15, width=50)
        self.code_text.pack(pady = 10)

    def generate_manim_code(self):
        # 获取参数值并生成Manim代码
        # 注意：这里的实现需要根据实际参数和对象类型进行调整
        object_type = self.object_type_var.get()
        #params = {widget.cget("text"): widget.get() for widget in self.current_params_widgets if isinstance(widget, tk.Scale)}
        params = {param: widget['scale'].get() for param, widget in self.params_widgets.items()}
        class_name = "MyScene_" + str(uuid.uuid4()).replace("-", "")
        manim_code = f"""
from manim import *

class {class_name}(Scene):
    def construct(self):
        obj = {object_type}({', '.join([f'{k}={v}' for k, v in params.items()])})
        self.play(Create(obj))
        self.wait(2)
"""

        # 展示生成的代码
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, manim_code)

        # 生成manim代码文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        # 运行manim代码
        subprocess.run([f"manim", "-pql", "manim_code.py", "{class_name}"])

def main():
    root = tk.Tk()
    app = ManimGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
