import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import subprocess
import uuid
from threading import Thread

# 示例动画对象类型及其参数定义
OBJECTS_PARAMS = {
    "Circle": {"radius": (1, 10)},
    "Square": {"side_length": (1, 10)},
    # 可以根据需要添加更多类型及其参数
}

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Manim GUI")

        self.num_objects = 0
        self.object_types = []
        self.object_threads = []


        self.create_widgets()

        self.code_text = tk.Text(wrap="word", height=15, width=50)
        self.code_text.pack(pady = 10)

    def create_widgets(self):
        # 添加输入框用于输入动画对象数量
        self.num_objects_label = tk.Label(self.root, text="要生成几个动画对象?")
        self.num_objects_label.pack()
        self.num_objects_entry = tk.Entry(self.root)
        self.num_objects_entry.pack()

        # 确认动画对象数量
        self.confirm_button = tk.Button(self.root, text="确认", command=self.confirm_num_objects)
        self.confirm_button.pack(pady=5)

    def confirm_num_objects(self):
        self.num_objects = int(self.num_objects_entry.get())
        
        # 创建相应数量的 ObjectThread 实例
        for index in range(self.num_objects):
            thread = ObjectThread(self, index)
            thread.start()
            self.object_threads.append(thread)

class ObjectThread(Thread):
    def __init__(self, gui, index):
        super().__init__()
        
        self.gui = gui
        self.index = index
        self.object_type = ""

    def run(self):
        # 创建窗口
        self.thread_window = tk.Toplevel()
        self.thread_window.title(f"Object {self.index + 1}")

        # 动画对象类型选择
        self.object_type_label = tk.Label(self.thread_window, text="选择动画对象类型:")
        self.object_type_label.pack()
        self.object_type_var = tk.StringVar()
        self.object_type_optionmenu = tk.OptionMenu(
            self.thread_window, self.object_type_var, *OBJECTS_PARAMS.keys(), command=self.on_object_type_selected)
        self.object_type_optionmenu.pack()

        # 存储参数名称和对应控件的字典
        self.params_widgets = {}

        # 添加生成代码的按钮
        self.generate_button = tk.Button(self.thread_window, text="生成 Manim 代码", command=self.generate_manim_code)
        self.generate_button.pack(pady=10)

    def on_object_type_selected(self, choice):
        # 清除旧的参数控件
        for widget in self.params_widgets.values():
            widget['label'].destroy()
            widget['scale'].destroy()
        self.params_widgets.clear()

        # 为所选对象类型创建新的参数控件
        for param, range in OBJECTS_PARAMS[choice].items():
            label = tk.Label(self.thread_window, text=f"{param}:")
            label.pack()
            scale = tk.Scale(self.thread_window, from_=range[0], to=range[1], orient="horizontal")
            scale.pack()
            self.params_widgets[param] = {'label': label, 'scale': scale}
        

        # 添加用于显示生成的代码的文本框
        #self.code_text = tk.Text(self.thread_window, wrap="word", height=15, width=50)
        #self.code_text.pack(pady = 10)

    def generate_manim_code(self):
        # 获取参数值并生成Manim代码
        object_type = self.object_type_var.get()
        params = {param: widget['scale'].get() for param, widget in self.params_widgets.items()}
        print("Object Type:", object_type)
        print("Params:", params)


app = GUI()
app.root.mainloop()