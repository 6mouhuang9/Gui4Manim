import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import json

class ManimCE_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Manim CE 图形化界面")

        # 创建样式
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 20))  # 标签字体大小为16
        self.style.configure('TButton', font=('Helvetica', 12))  # 按钮字体大小为16
        self.style.configure('TCombobox', font=('Helvetica', 16))  # 下拉菜单字体大小为16

        # 创建菜单栏
        self.create_menu_bar()

        # 创建项目管理区域
        self.create_project_manager()

        # 创建参数设置区域
        self.create_parameter_settings()

        # 创建预览区域
        self.create_preview_area()

        # 创建控制按钮
        self.create_control_buttons()

        # 创建状态栏
        self.create_status_bar()

    def create_menu_bar(self):
        self.menu_bar = tk.Menu(self.master)

        # 文件菜单
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="创建新项目", command=self.create_new_project)
        self.file_menu.add_command(label="打开现有项目", command=self.open_existing_project)
        self.file_menu.add_command(label="保存项目", command=self.save_project)
        self.file_menu.add_command(label="导出视频", command=self.export_video)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)

        # 帮助菜单
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="帮助文档", command=self.open_help_documentation)
        self.help_menu.add_command(label="论坛", command=self.open_forum)
        self.menu_bar.add_cascade(label="帮助", menu=self.help_menu)

        self.master.config(menu=self.menu_bar)

    def create_project_manager(self):
        self.project_manager_frame = ttk.LabelFrame(self.master, text="项目管理", style='TLabel')
        self.project_manager_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建项目列表框架
        self.project_list_frame = ttk.Frame(self.project_manager_frame)
        self.project_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建项目列表
        self.project_listbox = tk.Listbox(self.project_list_frame, font=('Helvetica', 14), selectmode=tk.SINGLE)
        self.project_listbox.pack(fill=tk.BOTH, expand=True)

        # 添加滚动条
        self.scrollbar = ttk.Scrollbar(self.project_list_frame, orient=tk.VERTICAL, command=self.project_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_listbox.config(yscrollcommand=self.scrollbar.set)

        # 添加打开和删除按钮
        self.open_button = ttk.Button(self.project_manager_frame, text="打开项目", command=self.open_project, style='TButton')
        self.open_button.pack(side=tk.LEFT, padx=(0, 5))

        self.delete_button = ttk.Button(self.project_manager_frame, text="删除项目", command=self.delete_project, style='TButton')
        self.delete_button.pack(side=tk.LEFT)

    def open_project(self):
        # 获取所选项目的名称
        selected_project = self.project_listbox.curselection()
        if selected_project:
            project_name = self.project_listbox.get(selected_project)
            # TODO: 打开所选项目的操作

    def delete_project(self):
        # 获取所选项目的名称
        selected_project = self.project_listbox.curselection()
        if selected_project:
            project_name = self.project_listbox.get(selected_project)
            # TODO: 删除所选项目的操作

    def create_parameter_settings(self):
        self.parameter_settings_frame = ttk.LabelFrame(self.master, text="参数设置")
        self.parameter_settings_frame.grid(row=0, column=1, padx=10, pady=10)

        # 在此处添加参数设置的输入框、下拉菜单、滑块等控件

    def create_preview_area(self):
        self.preview_frame = ttk.LabelFrame(self.master, text="预览区域")
        self.preview_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # 在此处添加 Manim 动画的预览区域，可以使用画布或视频播放器等控件来显示预览效果
        self.preview_canvas = tk.Canvas(self.preview_frame, width=400, height=300, bg="white")
        self.preview_canvas.pack(expand=True, fill="both")

    def show_preview_animation(self):
        # 在预览区域绘制简单的示例动画
        self.preview_canvas.create_rectangle(50, 50, 200, 200, fill="blue")
        self.preview_canvas.create_oval(250, 50, 400, 200, fill="red")

    def create_control_buttons(self):
        self.control_frame = ttk.Frame(self.master)
        self.control_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # 在此处添加开始渲染动画、暂停渲染、停止渲染等控制按钮

        self.start_button = ttk.Button(self.control_frame, text="开始渲染", command=self.start_render)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = ttk.Button(self.control_frame, text="暂停渲染", command=self.pause_render)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        self.stop_button = ttk.Button(self.control_frame, text="停止渲染", command=self.stop_render)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)
    
    def start_render(self):
        # 开始渲染动画
        pass

    def pause_render(self):
        # 暂停渲染动画
        pass

    def stop_render(self):
        # 停止渲染动画
        pass

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.master, text="就绪", anchor=tk.W)
        self.status_bar.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=(tk.W, tk.E))
#我连项目文件应该是什么类型都不知道，Python文件，还是别的什么？换句话说都是一次性的，要么当时确定，要么直接用现成的，又何必这么折腾？
    def create_new_project(self):
          # 打开文件对话框以选择项目保存的位置和名称
        file_path = filedialog.asksaveasfilename(defaultextension=".manim", filetypes=[("Manim项目文件", "*.manim")])

        if file_path:
            # 在这里执行创建项目的逻辑
            self.update_status(f"项目已创建：{file_path}")
        else:
            self.update_status("创建项目取消")


    def open_existing_project(self):
         # 打开文件对话框以选择要打开的项目文件
        file_path = filedialog.askopenfilename(filetypes=[("Manim项目文件", "*.manim")])

        if file_path:
            # 在这里执行打开项目的逻辑
            self.update_status(f"项目已打开：{file_path}")
        else:
            self.update_status("打开项目取消")

    def save_project(self):
        # 获取项目数据
        project_data = {
            'scene': self.scene_var.get(),
            'object_type': self.object_type_var.get(),
            'animation_effect': self.animation_effect_var.get()
            # 其他项目数据...
        }

        # 打开文件对话框以选择保存项目的位置和名称
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON 文件", "*.json")])

        if file_path:
            # 将项目数据保存到文件
            with open(file_path, 'w') as f:
                json.dump(project_data, f)
            self.update_status(f"项目已保存：{file_path}")
        else:
            self.update_status("保存项目取消")

    def export_video(self):
        # TODO: 导出视频的操作
        """ scene = self.scene_var.get()
        object_type = self.object_type_var.get()
        animation_effect = self.animation_effect_var.get()

        # 构建 Manim 命令
        command = f"manim {scene} {object_type} -a {animation_effect} -o output_video.mp4"

        # 执行命令导出视频
        try:
            subprocess.run(command, shell=True, check=True)
            self.update_status("视频导出成功！")
        except subprocess.CalledProcessError as e:
            self.update_status(f"视频导出失败：{e}") """
        
        pass
    
    def update_status(self, message):
        # 更新状态栏信息
        self.status_bar.config(text=message)

    def open_help_documentation(self):
        # TODO: 打开帮助文档的操作
        pass

    def open_forum(self):
        # TODO: 打开论坛的操作
        pass

def main():
    root = tk.Tk()
    app = ManimCE_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
