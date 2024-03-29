import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

OBJECTS_PARAMS = {
    "Circle": {"radius": (1, 10), "color": ("RED", "GREEN", "BLUE")},
    "Square": {"side_length": (1, 10), "color": ("RED", "GREEN", "BLUE")},
    # 根据需要添加更多对象及其参数
}

# 创建 GUI 类
class ManimGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 动画参数设置器")

        self.objects_data = {}  # 存储动画对象数据的字典

        self.current_object_index = 1  # 当前动画对象的索引
        self.create_object_selection()

    def create_object_selection(self):
        # 清空之前的界面
        for widget in self.master.winfo_children():
            widget.destroy()

        # 添加标签和输入框，用于设置动画对象数量
        self.num_objects_label = ttk.Label(self.master, text="请输入动画对象数量:")
        self.num_objects_label.grid(row=0, column=0, padx=10, pady=5)
        self.num_objects_entry = ttk.Entry(self.master)
        self.num_objects_entry.grid(row=0, column=1, padx=10, pady=5)

        # 添加确认按钮，用于确认动画对象数量并跳转到下一步
        self.confirm_objects_button = ttk.Button(self.master, text="确认", command=self.confirm_num_objects)
        self.confirm_objects_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def confirm_num_objects(self):
        num_objects = int(self.num_objects_entry.get())
        self.create_object_widgets(num_objects)

    def create_object_widgets(self, num_objects):
        # 清空之前的界面
        for widget in self.master.winfo_children():
            widget.destroy()

        for i in range(num_objects):
            self.create_object_frame(i + 1)

    def create_object_frame(self, index):
        # 创建一个 Frame 用于放置动画对象参数输入框
        object_frame = ttk.Frame(self.master)
        object_frame.grid(row=index - 1, column=0, padx=10, pady=5)

        # 添加标签和下拉菜单，用于选择动画对象类型
        object_type_label = ttk.Label(object_frame, text=f"选择动画对象类型 {index}:")
        object_type_label.grid(row=0, column=0, padx=5, pady=5)
        object_type_var = tk.StringVar()
        object_type_optionmenu = ttk.OptionMenu(
            object_frame, object_type_var, *OBJECTS_PARAMS.keys())
        object_type_optionmenu.grid(row=0, column=1, padx=5, pady=5)

        # 添加确认按钮，用于确认动画对象类型并跳转到下一步
        confirm_button = ttk.Button(object_frame, text="确认", command=lambda: self.confirm_object_type(object_type_var.get()))
        confirm_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        

    def confirm_object_type(self, object_type):
        # TODO: 根据选择的动画对象类型，创建对应的参数输入框
        print(self.objects_data)
        

# 创建主窗口并运行 GUI
root = tk.Tk()
manim_gui = ManimGUI(root)
root.mainloop()


animations_data = [
    {
        "index": "circle_1",
        "type": "Circle",
        "params": {"radius": 1, "color": "BLUE"},
        "animations": [
            {"effect": "FadeIn", "animation_params": {"run_time": 2}},
            {"effect": "FadeOut", "animation_params": {"run_time": 2}}
        ]
    },
    {
        "index": "square_1",
        "type": "Square",
        "params": {"side_length": 2, "color": "RED"},
        "animations": [
            {"effect": "Rotate", "animation_params": {"angle": 3.14, "run_time": 2}},
        ]
    }
]