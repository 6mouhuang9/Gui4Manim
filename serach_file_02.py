import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

class FileSearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("文件搜索器")

        # 添加查询输入框
        self.search_label = tk.Label(self.master, text="请输入要查询的关键词：")
        self.search_label.pack()

        # 创建搜索框
        self.search_entry = tk.Entry(self.master)
        self.search_entry.pack(pady=10)

        # 设置文件夹路径
        self.folder_path = ""

        # 添加选择文件夹按钮
        self.select_folder_button = tk.Button(self.master, text="选择文件夹", command=self.select_folder)
        self.select_folder_button.pack()

        # 添加搜索按钮
        self.search_button = tk.Button(self.master, text="搜索", command=self.search_videos)
        self.search_button.pack()

        # 创建用于显示搜索结果的列表框
        self.search_results_listbox = tk.Listbox(self.master, width=50, height=30,)
        self.search_results_listbox.pack(fill=tk.BOTH, expand=True)

        # 添加滚动条
        scrollbar = tk.Scrollbar(self.master, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.search_results_listbox.yview)

        # 绑定双击事件
        self.search_results_listbox.bind("<Double-1>", self.play_selected_video)

        # 创建右键菜单
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="下载", command=self.download_file)
        self.context_menu.add_command(label="查看文件所在位置", command=self.open_folder)

        # 绑定右键菜单
        self.search_results_listbox.bind("<Button-3>", self.show_context_menu)


    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        #print("已选择文件夹:", self.folder_path)

    def search_videos(self):
        
        # 清空之前的搜索结果
        self.search_results_listbox.delete(0, tk.END)

        # 获取搜索关键字
        keyword = self.search_entry.get()

        if self.folder_path and keyword:
            for file_name in os.listdir(self.folder_path):
                if keyword in file_name:
                    if file_name.endswith(".mp4"):
                        self.search_results_listbox.insert(tk.END, os.path.join(self.folder_path, file_name))
                #else:
                    #print("没有这个关键词！")
            #print("搜索完成！")
        else:
            #print("请先选择文件夹！")
            messagebox.showinfo("提示", "请先选择文件夹！")


    def play_selected_video(self, event):
        selected_index = self.search_results_listbox.curselection()
        if selected_index:
            selected_file = self.search_results_listbox.get(selected_index)
            video_player.play_video(selected_file)

    def show_context_menu(self, event):
        # 在鼠标右键位置显示菜单
        self.context_menu.post(event.x_root, event.y_root)
    
    def download_file(self):
        # 获取当前选中的文件路径
        selected_file = self.search_results_listbox.get(tk.ACTIVE)

        try:
            # 读取文件内容
            with open(selected_file, 'rb') as f:
                content = f.read()
            # 提示用户选择保存位置
            save_path = filedialog.asksaveasfilename(initialfile=os.path.basename(selected_file))

            if save_path:
                # 将文件内容写入到指定位置
                with open(save_path, 'wb') as f:
                    f.write(content)

                messagebox.showinfo("下载成功", f"文件已成功下载到：{save_path}")
            else:
                messagebox.showwarning("下载取消", "下载已取消")
        except Exception as e:
            messagebox.showerror("下载失败", f"下载文件时发生错误：{str(e)}")


    
    def open_folder(self):
        selected_file = self.search_results_listbox.get(tk.ACTIVE)
        folder_path = os.path.dirname(selected_file)
        os.system(f'explorer "{folder_path}"')  # Windows下打开资源管理器


class VideoPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("视频播放器")
        
        # 创建用于显示视频的标签
        self.video_label = tk.Label(self.master)
        self.video_label.pack()

        # 创建视频播放器
        self.video_cap = None

    def play_video(self, video_file):
        if self.video_cap is not None:
            self.video_cap.release()

        # 打开视频文件
        self.video_cap = cv2.VideoCapture(video_file)

        # 播放视频
        self.play_video_frame()

    def play_video_frame(self):
        ret, frame = self.video_cap.read()
        if ret:
            # 将OpenCV帧转换为PIL图像
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image=img)

            # 更新视频播放器标签
            self.video_label.config(image=img)
            self.video_label.img = img

            # 循环调用play_video_frame方法，以持续更新视频帧
            self.master.after(10, self.play_video_frame)
        else:
            print("视频播放结束！")
            self.video_cap.release()

if __name__ == "__main__":
    root = tk.Tk()

    # 创建文件搜索器应用
    file_search_app = FileSearchApp(root)

    # 创建视频播放器应用
    video_player = VideoPlayerApp(root)

    root.mainloop()
