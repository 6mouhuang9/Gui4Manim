import tkinter as tk
from tkinter import ttk
import subprocess
import uuid

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

        self.num_stars_label = tk.Label(self.master, text="要生成几个星形?")
        self.num_stars_label.pack()
        self.num_stars_entry = tk.Entry(self.master)
        self.num_stars_entry.pack()

        # 添加按钮用于确认星形的数量
        self.confirm_button = tk.Button(self.master, text="确认", command=self.confirm_num_stars)
        self.confirm_button.pack(pady=5)

    def confirm_num_stars(self):
        # 获取输入框的值，确认要生成的星形的数量
        self.num_stars = int(self.num_stars_entry.get())

        # 移除上一个界面的控件
        self.duration_label.pack_forget()
        self.duration_entry.pack_forget()
        self.num_stars_label.pack_forget()
        self.num_stars_entry.pack_forget()
        self.confirm_button.pack_forget()

        # 创建输入星形特征的控件
        self.create_stars_input_widgets()

    def create_stars_input_widgets(self):
        self.stars_widgets = []

        # 自动生成递增的 X 坐标
        x_positions = [i * 2 for i in range(self.num_stars)]

        for i in range(self.num_stars):
            stars_frame = ttk.Frame(self.master)
            stars_frame.pack(pady=5)

            n_label = tk.Label(stars_frame, text=f"星形{i + 1}的n:")
            n_label.pack(side="left")

            n_entry = tk.Entry(stars_frame)
            n_entry.pack(side="left")

            outer_radius_label = tk.Label(stars_frame, text=f"星形{i + 1}的外半径:")
            outer_radius_label.pack(side="left")

            outer_radius_entry = tk.Entry(stars_frame)
            outer_radius_entry.pack(side="left")

            inner_radius_label = tk.Label(stars_frame, text=f"星形{i + 1}的内半径:")
            inner_radius_label.pack(side="left")

            inner_radius_entry = tk.Entry(stars_frame)
            inner_radius_entry.pack(side="left")

            density_label = tk.Label(stars_frame, text=f"星形{i + 1}的密度:")
            density_label.pack(side="left")

            density_entry = tk.Entry(stars_frame)
            density_entry.pack(side="left")

            position_x_label = tk.Label(stars_frame, text=f"星形{i + 1}的 X 坐标:")
            position_x_label.pack(side="left")

            position_x_entry = tk.Entry(stars_frame)
            position_x_entry.insert(tk.END, x_positions[i])  # 自动填入递增的 X 坐标
            position_x_entry.pack(side="left")

            position_y_label = tk.Label(stars_frame, text=f"星形{i + 1}的 Y 坐标:")
            position_y_label.pack(side="left")

            position_y_entry = tk.Entry(stars_frame)
            position_y_entry.pack(side="left")

            self.stars_widgets.append((n_entry, outer_radius_entry, inner_radius_entry, density_entry, position_x_entry, position_y_entry))

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

        for i, stars_widget in enumerate(self.stars_widgets):
            n = stars_widget[0].get()
            outer_radius = stars_widget[1].get()
            inner_radius = stars_widget[2].get()
            density = stars_widget[3].get()
            position_x = stars_widget[4].get()
            position_y = stars_widget[5].get()

            manim_code += f"""
        # 创建星形对象
        star_{i+1} = Star(n={n}, 
                          outer_radius={outer_radius}, 
                          inner_radius={inner_radius}, 
                          density={density}).shift({position_x}, {position_y})

        # 添加星形对象到场景中
        self.play(Create(star_{i+1}))
        self.wait({duration/self.num_stars})
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

#还没测试，写不动了(艹皿艹 )