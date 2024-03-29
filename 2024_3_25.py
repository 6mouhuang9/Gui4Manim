import subprocess
import uuid
import threading
import time


import tkinter as tk
from tkinter import ttk
from threading import Thread

class AnimationThread(Thread):
    def __init__(self, gui, index, object_type, num_animations):
        super().__init__()

        
        self.gui = gui
        self.index = index
        self.object_type = object_type
        self.num_animations = num_animations
        self.animation_types = []

    def run(self):
        # 创建窗口
        self.thread_window = tk.Toplevel()
        self.thread_window.title(f"Object {self.index + 1} Animations")

        # 设置窗口大小
        window_width = 400
        window_height = 300
        screen_width = self.thread_window.winfo_screenwidth()
        screen_height = self.thread_window.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.thread_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # 添加选择动画类型的部件
        self.create_animation_type_comboboxes()

        # 添加确认按钮
        self.confirm_button = tk.Button(self.thread_window, text="确认动画类型", command=self.confirm_animation_types)
        self.confirm_button.pack()

    def create_animation_type_comboboxes(self):
        # 输入动画类型
        self.animation_types_label = tk.Label(self.thread_window, text="选择动画类型:")
        self.animation_types_label.pack()
        self.animation_types_comboboxes = []

        for i in range(self.num_animations):
            combobox = ttk.Combobox(self.thread_window, values=["FadeIn", "FadeOut", "Transform", "MoveTo", "Rotate", "Scale"])
            combobox.pack()
            self.animation_types_comboboxes.append(combobox)

    def confirm_animation_types(self):
        self.animation_types = [combobox.get() for combobox in self.animation_types_comboboxes]
        self.thread_window.destroy()
        self.gui.animation_types_ready(self.index, self.animation_types)

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manim GUI")

        # 设置窗口大小
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


        self.num_objects = 0
        self.object_types = []
        self.animation_types = []

        self.create_widgets()

    def create_widgets(self):
        # 输入动画对象数量
        self.num_objects_label = tk.Label(self.root, text="选择动画对象数量:")
        self.num_objects_label.pack()
        self.num_objects_entry = tk.Entry(self.root)
        self.num_objects_entry.pack()

        # 确认动画对象数量
        self.confirm_objects_button = tk.Button(self.root, text="确认对象数量", command=self.confirm_objects)
        self.confirm_objects_button.pack()

    def confirm_objects(self):
        self.num_objects = int(self.num_objects_entry.get())
        self.create_object_type_comboboxes()

    def create_object_type_comboboxes(self):
        # 输入动画对象类型
        self.object_types_label = tk.Label(self.root, text="选择动画对象类型:")
        self.object_types_label.pack()
        self.object_types_comboboxes = []

        for i in range(self.num_objects):
            combobox = ttk.Combobox(self.root, values=["Circle", "Square", "Triangle"])
            combobox.pack()
            self.object_types_comboboxes.append(combobox)

        # 确认动画对象类型
        self.confirm_types_button = tk.Button(self.root, text="确认对象类型", command=self.confirm_types)
        self.confirm_types_button.pack()

    def confirm_types(self):
        self.object_types = [combobox.get() for combobox in self.object_types_comboboxes]
        self.create_animation_quantity_entries()

    def create_animation_quantity_entries(self):
        # 输入每个对象的动画数量
        self.animation_quantity_entries = []

        for i in range(self.num_objects):
            label = tk.Label(self.root, text=f"动画对象 {i+1} 的动画数量:")
            label.pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.animation_quantity_entries.append(entry)

        # 确认动画数量
        self.confirm_animation_quantity_button = tk.Button(self.root, text="确认动画数量", command=self.confirm_animation_quantity)
        self.confirm_animation_quantity_button.pack()

    def confirm_animation_quantity(self):
        animation_quantities = [int(entry.get()) for entry in self.animation_quantity_entries]
        # 创建线程来处理每个对象的动画类型选择
        for i, (object_type, num_animations) in enumerate(zip(self.object_types, animation_quantities)):
            thread = AnimationThread(self, i, object_type, num_animations)
            thread.start()

    def animation_types_ready(self, index, animation_types):
        self.animation_types.append((index, animation_types))
        if len(self.animation_types) == self.num_objects:
            # 所有动画类型都准备好了
            print("All animation types are ready. Generating Manim code...")
            self.generate_manim_code()

    def generate_manim_code(self):
        # 生成完整的Manim代码
        manim_code = ""
        manim_code += "from manim import *\n\n"
        manim_code += f"class MyScene(Scene):\n"
        manim_code += "    def construct(self):\n"

        for index, (object_type, animation_types) in enumerate(self.animation_types):
            # 生成动画对象的代码
            manim_code += f"        obj_{index+1} = {object_type}()\n"
            for animation_type in animation_types:
               # 生成动画效果的代码
                if animation_type == "FadeIn":
                    manim_code += f"        self.play(FadeIn(obj_{index+1}))\n"
                elif animation_type == "FadeOut":
                    manim_code += f"        self.play(FadeOut(obj_{index+1}))\n"
                elif animation_type == "Transform":
                    manim_code += f"        self.play(Transform(obj_{index+1}, new_obj_{index+1}))\n"
                elif animation_type == "MoveTo":
                    manim_code += f"        self.play(obj_{index+1}.move_to(new_position))\n"
                elif animation_type == "Rotate":
                    manim_code += f"        self.play(obj_{index+1}.rotate(angle))\n"
                elif animation_type == "Scale":
                    manim_code += f"        self.play(obj_{index+1}.scale(scale_factor))\n"

        # 执行所有动画效果后等待一段时间
        manim_code += "        self.wait(1)\n"

        # 将代码写入文件
        with open("manim_code.py", "w") as f:
            f.write(manim_code)

        print("Manim代码已生成并保存到manim_code.py文件中。")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
    
