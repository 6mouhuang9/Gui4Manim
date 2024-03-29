import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
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
        self.master.title("Manim 动画数量选择")

        # 初始化动画对象和动画效果的列表
        self.objects = []
        self.effects = []
        self.window_data = []

        # 询问需要多少个动画对象
        self.num_objects_label = tk.Label(master, text="需要多少个动画对象？")
        self.num_objects_label.pack()

        self.num_objects_entry = tk.Entry(master)
        self.num_objects_entry.pack()

        self.num_objects_button = tk.Button(master, text="确认", command=self.create_object_window)
        self.num_objects_button.pack()

        self.params_widgets = {}  # 存储参数名称和对应控件的字典

        self.manim_code = f"""
from manim import *

class MyAnimation(Scene):
    def construct(self):
"""

    def create_object_window(self):
        num_objects = int(self.num_objects_entry.get())
        self.num_objects_label.destroy()
        self.num_objects_entry.destroy()
        self.num_objects_button.destroy()

        # 为每个动画对象创建一个单独的窗口
        for i in range(num_objects):
            object_window = tk.Toplevel(self.master)
            object_window.title(f"动画对象 {i+1}")

            window_data_dict = {}  # 创建一个字典来存储这个窗口的信息

            object_label = tk.Label(object_window, text=f"选择第 {i+1} 个动画对象:")
            object_label.pack()

            object_type_var = tk.StringVar()

            object_type_optionmenu = tk.OptionMenu(object_type_var, *OBJECTS_PARAMS.keys(), command=self.on_object_type_selected)
            object_type_optionmenu.pack()

    def on_object_type_selected():
        pass

root = tk.Tk()
app = ManimGUI(root)
root.mainloop()