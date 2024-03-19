import tkinter as tk
from tkinter import filedialog
import os
import cv2
from PIL import Image, ImageTk

class VideoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("视频应用")

        # 创建选择文件夹按钮
        self.folder_button = tk.Button(self.master, text="选择文件夹", command=self.choose_folder)
        self.folder_button.pack()

        # 创建搜索按钮
        self.search_button = tk.Button(self.master, text="搜索视频", command=self.search_videos)
        self.search_button.pack()

        # 创建搜索框、搜索按钮和播放按钮
        self.search_entry = tk.Entry(self.master)
        self.search_entry.pack(padx=10, pady=5, side=tk.LEFT)
        self.search_button = tk.Button(self.master, text="搜索", command=self.search_videos)
        self.search_button.pack(padx=5, pady=5, side=tk.LEFT)
        self.play_button = tk.Button(self.master, text="播放选定视频", command=self.play_selected_video)
        self.play_button.pack()

        # 初始化搜索结果列表
        self.search_results = []

        # 创建打开视频文件按钮
        self.open_button = tk.Button(self.master, text="打开视频文件", command=self.open_video_file_dialog)
        self.open_button.pack(padx=5, pady=5, side=tk.LEFT)

        # 创建视频预览框
        self.video_preview_label = tk.Label(self.master)
        self.video_preview_label.pack()

        # 初始化视频捕获器
        self.cap = None

    # 选择文件夹
    def choose_folder(self):
        folder_path = filedialog.askdirectory()  # 打开文件夹选择对话框
        if folder_path:
            self.folder_path = folder_path
            print(f"已选择文件夹：{self.folder_path}")

    def search_videos(self):
        if hasattr(self, 'folder_path'):
            self.search_results = []
            for file_name in os.listdir(self.folder_path):
                if file_name.endswith(".mp4"):  # 可以根据需要修改文件扩展名
                    self.search_results.append(os.path.join(self.folder_path, file_name))
            print("搜索完成！")
        else:
            print("请先选择文件夹！")
            

    def play_selected_video(self):
        selected_index = 0  # 假设选择第一个视频
        if self.search_results:
            selected_video = self.search_results[selected_index]
            print(f"播放视频：{selected_video}")
        else:
            print("没有找到视频！")

    def play_video(self, file_path):
        # 打开选择的视频文件
        self.cap = cv2.VideoCapture(file_path)

        # 更新视频预览
        self.update_preview()

    def open_video_file_dialog(self):
        # 打开文件对话框选择视频文件
        file_path = filedialog.askopenfilename(filetypes=[("视频文件", "*.mp4")])

        # 如果选择了视频文件，则打开该视频文件
        if file_path:
            self.open_video_file(file_path)

    def open_video_file(self, file_path):
        # 打开选择的视频文件
        self.cap = cv2.VideoCapture(file_path)

        # 更新视频预览
        self.update_preview()

    def update_preview(self):
        # 从视频捕获帧
        ret, frame = self.cap.read()

        if ret:
            # 将OpenCV帧转换为PIL图像
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)

            # 将PIL图像转换为Tkinter图像
            img_tk = ImageTk.PhotoImage(img)

            # 更新视频预览标签
            self.video_preview_label.img_tk = img_tk
            self.video_preview_label.config(image=img_tk)

            # 循环调用update_preview方法，以持续更新视频预览
            self.video_preview_label.after(10, self.update_preview)
        else:
            # 关闭视频文件
            self.cap.release()


def main():
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
