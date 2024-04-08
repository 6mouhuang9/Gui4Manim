import tkinter as tk
from tkinter import font as tkFont
from tkinter import PhotoImage, Toplevel, ttk
import subprocess
import uuid
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
import cv2
from PIL import Image, ImageTk
import os
from LMAnim import AnimationGUI
from video_search_play_final import FileSearchApp, VideoPlayerApp
from Main_animations import AnimationOptionsGUI


class MainGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim 动画生成器")

        # 设置窗口大小和背景颜色
        self.master.geometry("600x400")
        #self.master.configure(bg='#FAD7A0')  # 深蓝色背景

        # 使用 Pillow 加载背景图片
        original_image = Image.open(r'gui4manim\background\b06.jpg')
        resized_image = original_image.resize((600, 400), Image.ANTIALIAS) 
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background_label = tk.Label(self.master, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 设置菜单字体大小
        menu_font = tkFont.Font(family="Verdana", size=12)

        # 创建菜单栏
        self.menu_bar = tk.Menu(self.master, font = menu_font)
        self.master.config(menu=self.menu_bar)

        # 创建帮助下拉菜单
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0, font=menu_font)
        self.help_menu.add_command(label="常见 F&Q", command=self.show_faq)
        self.help_menu.add_command(label="联系作者", command=self.contact_author)
        self.help_menu.add_command(label="Manim 官方文档", command=self.open_manim_document)
        self.menu_bar.add_cascade(label="帮助", menu=self.help_menu)

        # 设置按钮样式
        button_style = {"font": ("Verdana", 20), "bg": "#FAD7A0", "fg": "black"}

        # 创建生成动画按钮
        self.generate_button = tk.Button(self.master, text="生成动画", command=self.generate_animation, **button_style)
        self.generate_button.pack(fill='x', padx=50, pady=20)

        # 创建查询范例按钮
        self.query_button = tk.Button(self.master, text="查询范例", command=self.query_examples, **button_style)
        self.query_button.pack(fill='x', padx=50, pady=20)

        # 加载并调整 Logo 图片大小
        self.original_logo = Image.open(r'gui4manim\background\LMLogo.jpg')  
        self.resized_logo = self.original_logo.resize((500, 250), Image.ANTIALIAS)    
        self.logo_image = ImageTk.PhotoImage(self.resized_logo)
        self.logo_label = tk.Label(self.master, image=self.logo_image, bg='#FAD7A0')
        self.logo_label.pack(padx=20, pady=20)


    def show_faq(self):
        # 创建一个新窗口来展示 FAQ
        faq_window = Toplevel(self.master)
        faq_window.title("常见问题解答")
        faq_window.geometry("500x300")

        # 假设您的 FAQ 内容存储在文档中
        with open(r"gui4manim\normal_question.txt", "r", encoding="utf-8") as file:
            faq_content = file.read()

        # 在窗口中添加一个文本框来显示 FAQ
        text_widget = tk.Text(faq_window)
        text_widget.pack(expand=True, fill='both')
        text_widget.insert('1.0', faq_content)

    def contact_author(self):
        # 创建一个新窗口来展示作者信息
        author_window = Toplevel(self.master)
        author_window.title("联系作者")
        author_window.geometry("500x300")

        # 假设您的作者信息存储在文档中
        with open(r"gui4manim\author_introduction.txt", "r", encoding="utf-8") as file:
            author_info = file.read()

        # 在窗口中添加一个标签来显示作者信息
        label = tk.Label(author_window, text=author_info)
        label.pack(expand=True)

    def open_manim_document(self):
        # 打开 ManimCE 官方文档网页
        webbrowser.open("https://docs.manim.community/")

    def generate_animation(self):

         # 销毁当前界面
        self.master.destroy()

        # 创建新的窗口
        new_root = tk.Tk()
        AnimationOptionsGUI(new_root)

        

    def query_examples(self):
        # 在这里添加查询范例的逻辑
        self.master.destroy()

        root1 = tk.Tk()
        
        video_player = VideoPlayerApp(root1)
        file_search_app = FileSearchApp(root1, video_player)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root) 
    root.mainloop()