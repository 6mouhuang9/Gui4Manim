import tkinter as tk
import subprocess
import threading
from tkinter import messagebox


class CommandGUI:
    def __init__(self):
        self.command_parts = ["", "", "", ""]
        self.root = tk.Tk()
        self.root.title("命令输入")

        self.create_widgets()

    def create_widgets(self):
        labels = [
            "第1部分命令内容：",
            "第2部分命令内容：",
            "第3部分命令内容：",
            "第4部分命令内容：",
        ]
        for i, label_text in enumerate(labels):
            label = tk.Label(self.root, text=label_text, font=("Arial", 14))
            label.grid(row=i, column=0, padx=10, pady=10)
            # 如果是第一部分命令，固定为 "manim"
            if i == 0:  
                entry = tk.Entry(self.root, font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry.insert(0, "manim")
                entry.config(state="readonly")
                entry.grid(row=i, column=1, padx=10, pady=10)
                setattr(self, 'entry1', tk.StringVar(self.root, value='manim'))
            # 如果是第二条命令，创建一个下拉框
            elif i == 1:
                options = ["-pql", "-pqm", "-pqh"]  # 下拉框选项
                entry = tk.StringVar(self.root)
                entry.set(options[0])  # 设置默认选项为"-pql"
                option_menu = tk.OptionMenu(self.root, entry, *options)
                option_menu.config(font=("Arial", 14), width=26, relief="sunken")
                option_menu.grid(row=i, column=1, padx=10, pady=10, sticky="w")
                setattr(self, f'entry{i+1}', entry)  # 保存选项框的值
            else:
                entry = tk.Entry(self.root, font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=10)
                setattr(self, f'entry{i+1}', entry)  # 保存文本框的值
                #给三、四部分加一个未输入的提示 messagebox

        button = tk.Button(
            self.root,
            text="生成命令",
            font=("Arial", 14),
            command=self.on_generate_command,
        )
        button.grid(row=4, columnspan=2, padx=10, pady=10)

    def construct_command(self):

        for i in range(2, 4):  # 检查第三和第四部分命令是否为空
            entry = getattr(self, f'entry{i+1}')
            if not entry.get():
                messagebox.showerror("错误", f"{self.labels[i+1]}不能为空！")           
        
        for i in range(4):
            entry = getattr(self, f"entry{i+1}")
            # 如果是第二部分命令，获取选项框的值
            self.command_parts[i] = entry.get()

        full_command = " ".join(self.command_parts)
        print("完整的命令是：", full_command)
        global global_full_command
        global_full_command = full_command

    def on_generate_command(self):
        # 完成生成命令
        self.construct_command()  
        # 关闭当前界面
        self.root.destroy()  


    def run(self):
        self.root.mainloop()


class Termianl_Process(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ManimCE 视频生成器")

        # 创建文本框用于显示工作日志
        self.log_text = tk.Text(self, wrap="word", font=("Arial", 12))
        self.log_text.pack(fill="both", expand=True)

        # 创建生成视频的按钮
        self.generate_button = tk.Button(
            self, text="生成视频", command=self.generate_video
        )
        self.generate_button.pack()

    # 生成视频的函数，调用 ManimCE 命令行命令
    def generate_video(self):
        command = global_full_command
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        # 创建子线程用于实时更新日志
        threading.Thread(
            target=self.update_log, args=(process.stdout,), daemon=True
        ).start()

    # 实时更新日志到文本框
    def update_log(self, stdout):
        while True:
            line = stdout.readline()
            if not line:
                break
            self.log_text.insert("end", line)
            self.log_text.see("end")
            self.update_idletasks()

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    gui = CommandGUI()
    gui.run()
    app = Termianl_Process()
    app.mainloop()
