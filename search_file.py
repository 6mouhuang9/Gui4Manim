import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk


class FileSearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("文件查询应用")

        # 添加查询输入框
        self.query_label = tk.Label(self.master, text="请输入要查询的关键词：")
        self.query_label.pack()

        self.query_entry = tk.Entry(self.master)
        self.query_entry.pack()

        # 添加选择文件夹按钮
        self.select_folder_button = tk.Button(self.master, text="搜索", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

         # 创建滚动条
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建文件列表框
        self.file_listbox = tk.Listbox(self.master, width=100, height=50, yscrollcommand=self.scrollbar.set)
        self.file_listbox.pack()

        self.scrollbar.config(command=self.file_listbox.yview)

        # 绑定文件列表框的双击事件
        self.file_listbox.bind("<Double-Button-1>", self.open_selected_file)

        # 添加右键菜单
        self.context_menu = tk.Menu(self.file_listbox, tearoff=0)
        self.context_menu.add_command(label="前往文件夹", command=self.open_folder)
        self.file_listbox.bind("<Button-1>", self.show_context_menu)

    def select_folder(self):
        # 打开文件对话框以选择文件夹
        folder_path = filedialog.askdirectory()
        if folder_path:
            print("选择的文件夹路径:", folder_path)
            query = self.query_entry.get()
            if query:
                self.search_files(folder_path, query)
            else:
                #print("请输入查询内容！")
                messagebox.showinfo("提示", "请输入查询内容！")

    def search_files(self, folder_path, query):
        # 在选择的文件夹中搜索包含查询内容的文件
        search_results = []
        for file_name in os.listdir(folder_path):
            if query in file_name:
                search_results.append(os.path.join(folder_path, file_name))
        if search_results:
            #print("搜索结果：", search_results)

            # 清空文件列表框
            self.file_listbox.delete(0, tk.END)

            # 将搜索结果添加到文件列表框中
            for file_name in search_results:
                self.file_listbox.insert(tk.END, file_name)

        else:
            #print("未找到匹配的文件！")
            messagebox.showinfo("提示", "未找到匹配的文件！")

    def open_selected_file(self, event):
        # 获取选中的文件名
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            # 直接打开选中的文件
            os.startfile(selected_file)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def open_folder(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        folder_path = os.path.dirname(selected_file)
        os.system(f'explorer "{folder_path}"')  # Windows下打开资源管理器

class VideoPlayerApp:
    def __init__(self, master, video_file):
        self.master = master
        self.master.title("视频播放器")
        
        # 打开视频文件
        self.cap = cv2.VideoCapture(video_file)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 创建用于显示视频的标签
        self.video_label = tk.Label(self.master)
        self.video_label.pack()

        # 开始播放视频
        self.play_video()

    def play_video(self):
        ret, frame = self.cap.read()
        if ret:
            # 将OpenCV帧转换为PIL图像
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image=img)

            # 更新视频播放器标签
            self.video_label.config(image=img)
            self.video_label.img = img

            # 循环调用play_video方法，以持续更新视频帧
            self.master.after(10, self.play_video)
        else:
            # 当视频播放结束时释放资源
            self.cap.release()

def main():
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
