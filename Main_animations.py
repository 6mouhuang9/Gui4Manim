import tkinter as tk
from class_basic_page import ObjectAnimationConfigurator
from object_params_final import OBJECTS_PARAMS,animation_params_options
from class_transform_page import TransformAnimationConfigurator
from transform_objects_params_final import TRANSFORM_OBJECTS_PARAMS
from lambda_page_final import ManimParametricGraphGeneratorGUI
from PyQt5.QtWidgets import QApplication
import sys
from PIL import Image, ImageTk


class AnimationOptionsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("动画选项")
        self.master.geometry("600x400")
        #self.master.configure(bg='#F3F3F3')

        # 使用 Pillow 加载背景图片
        original_image = Image.open(r'gui4manim\background\b02.jpg')
        resized_image = original_image.resize((600, 400), Image.ANTIALIAS) 
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 设置统一的按钮样式
        button_style = {"font": ("Arial", 18), "bg": "#FAD7A0", "fg": "black"}

        # 创建菜单栏
        self.menu_bar = tk.Menu(self.master)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="说明", command=self.show_help)
        self.menu_bar.add_cascade(label="帮助", menu=self.help_menu)
        self.master.config(menu=self.menu_bar)

        # 创建按钮
        self.basic_animation_button = tk.Button(
            self.master, text="创建基本动画", command=self.create_basic_animation, **button_style
        )
        self.basic_animation_button.pack(fill='x', padx=50, pady=10)

        self.transition_animation_button = tk.Button(
            self.master, text="创造转换动画", command=self.create_transition_animation, **button_style
        )
        self.transition_animation_button.pack(fill='x', padx=50, pady=10)

        self.function_graph_animation_button = tk.Button(
            self.master, text="创建函数图形动画", command=self.create_function_graph_animation, **button_style
        )
        self.function_graph_animation_button.pack(fill='x', padx=50, pady=10)

        self.gif_image_path = r'gui4manim\background\g01.gif'  
        self.original_image = Image.open(self.gif_image_path)
        self.gif_frame_index = 0

        # 创建一个标签来显示 GIF
        self.gif_label = tk.Label(self.master)
        self.gif_label.pack()

        # 更新 GIF 动画
        self.update_gif()

    def update_gif(self):
        try:
            # 更新 GIF 图像的帧
            self.original_image.seek(self.gif_frame_index)
            self.gif_frame_index += 1
        except EOFError:
            # 当达到最后一帧时，重置帧索引
            self.gif_frame_index = 0
            self.original_image.seek(self.gif_frame_index)

        resized_frame = self.original_image.resize((500, 300), Image.ANTIALIAS) 
        self.tk_image = ImageTk.PhotoImage(resized_frame)
        self.gif_label.config(image=self.tk_image)

        # 设置定时器来更新帧
        self.master.after(1, self.update_gif)  

    def show_help(self):
        # 创建一个新窗口来展示 FAQ
        faq_window = tk.Toplevel(self.master)
        faq_window.title("动画说明")
        faq_window.geometry("500x300")

        # 假设您的 FAQ 内容存储在文档中
        with open(r"gui4manim\animations_explaination.txt", "r", encoding="utf-8") as file:
            faq_content = file.read()

        # 在窗口中添加一个文本框来显示 FAQ
        text_widget = tk.Text(faq_window)
        text_widget.pack(expand=True, fill='both')
        text_widget.insert('1.0', faq_content)

    def create_basic_animation(self):
        self.master.destroy()
        configurator = ObjectAnimationConfigurator(OBJECTS_PARAMS,animation_params_options)
        configurator.run()


    def create_transition_animation(self):
        self.master.destroy()
        configurator = TransformAnimationConfigurator(TRANSFORM_OBJECTS_PARAMS)
        configurator.run()

    def create_function_graph_animation(self):
        # 这里确保只在点击按钮时才启动 PyQt 应用
        self.master.destroy()
        app = QApplication(sys.argv)
        ex = ManimParametricGraphGeneratorGUI()
        ex.show()
        sys.exit(app.exec_())


root = tk.Tk()
ao = AnimationOptionsGUI(root)
root.mainloop() 