import tkinter as tk
from tkinter import filedialog

class VideoStorageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("视频存储系统")

        self.create_widgets()

    def create_widgets(self):
        # 上传按钮
        self.upload_button = tk.Button(self.master, text="上传视频", command=self.upload_video)
        self.upload_button.pack(pady=10)

        # 视频列表
        self.video_listbox = tk.Listbox(self.master, height=10, width=50)
        self.video_listbox.pack()

        # 下载按钮
        self.download_button = tk.Button(self.master, text="下载选定视频", command=self.download_video)
        self.download_button.pack(pady=10)

    def upload_video(self):
        # 打开文件对话框选择视频文件
        file_path = filedialog.askopenfilename(filetypes=[("视频文件", "*.mp4")])
        if file_path:
            # 在视频列表中显示文件名
            video_name = file_path.split("/")[-1]
            self.video_listbox.insert(tk.END, video_name)

            # TODO: 将文件上传到服务器并保存视频信息到数据库

    def download_video(self):
        # 获取用户选定的视频文件名
        selected_video = self.video_listbox.get(tk.ACTIVE)
        if selected_video:
            # TODO: 从服务器下载选定的视频文件

            # 提示下载完成
            tk.messagebox.showinfo("提示", f"已下载视频：{selected_video}")

def main():
    root = tk.Tk()
    app = VideoStorageApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
