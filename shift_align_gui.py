import tkinter as tk
from tkinter import ttk
from manim import *
import subprocess
import uuid


class AnnulusGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("圆环 GUI")

        self.create_widgets()

    def create_widgets(self):
        self.radius_label = tk.Label(self.master, text="半径:")
        self.radius_label.pack()
        self.radius_entry = tk.Entry(self.master)
        self.radius_entry.pack()

        self.inner_radius_label = tk.Label(self.master, text="内部半径:")
        self.inner_radius_label.pack()
        self.inner_radius_entry = tk.Entry(self.master)
        self.inner_radius_entry.pack()

        self.fill_opacity_label = tk.Label(self.master, text="F填充度:")
        self.fill_opacity_label.pack()
        self.fill_opacity_entry = tk.Entry(self.master)
        self.fill_opacity_entry.pack()

        self.shift_button = tk.Button(self.master, text="向左移动", command=self.shift_annulus_left)
        self.shift_button.pack()

        self.align_button = tk.Button(self.master, text="移动到起点", command=self.align_annulus_to_origin)
        self.align_button.pack()

        self.create_button = tk.Button(self.master, text="创建圆环", command=self.create_annulus)
        self.create_button.pack()

    def create_annulus(self):
        radius = float(self.radius_entry.get())
        inner_radius = float(self.inner_radius_entry.get())
        fill_opacity = float(self.fill_opacity_entry.get())

        # 创建Annulus对象
        annulus = Annulus(inner_radius=inner_radius, outer_radius=radius, fill_opacity=fill_opacity)

        # 显示Annulus
        scene = Scene()
        scene.add(annulus)
        scene.render()

    def shift_annulus_left(self):
        # 将Annulus对象向左移动
        radius = float(self.radius_entry.get())
        inner_radius = float(self.inner_radius_entry.get())
        fill_opacity = float(self.fill_opacity_entry.get())

        annulus = Annulus(inner_radius=inner_radius, outer_radius=radius, fill_opacity=fill_opacity)
        annulus.shift(LEFT * 2)  # 移动到左侧

        # 显示Annulus
        scene = Scene()
        scene.add(annulus)
        scene.render(True)

    def align_annulus_to_origin(self):
        # 将Annulus对象对齐到原点
        radius = float(self.radius_entry.get())
        inner_radius = float(self.inner_radius_entry.get())
        fill_opacity = float(self.fill_opacity_entry.get())

        annulus = Annulus(inner_radius=inner_radius, outer_radius=radius, fill_opacity=fill_opacity)
        annulus.align_to(ORIGIN)  # 对齐到原点

        # 显示Annulus
        scene = Scene()
        scene.add(annulus)
        scene.render()

# 创建主窗口
root = tk.Tk()
app = AnnulusGUI(root)
root.mainloop()
