import tkinter as tk
import threading
import time

class ManimGUI:
    def __init__(self, master):
        self.master = master
        master.title("Manim GUI")

        # 初始化动画对象和动画效果的列表
        self.objects = []
        self.effects = []

        # 询问需要多少个动画对象
        self.num_objects_label = tk.Label(master, text="需要多少个动画对象？")
        self.num_objects_label.pack()

        self.num_objects_entry = tk.Entry(master)
        self.num_objects_entry.pack()

        self.num_objects_button = tk.Button(master, text="确认", command=self.get_objects)
        self.num_objects_button.pack()

    def get_objects(self):
        num_objects = int(self.num_objects_entry.get())
        self.num_objects_label.destroy()
        self.num_objects_entry.destroy()
        self.num_objects_button.destroy()

        # 依次选择动画对象
        for i in range(num_objects):
            object_label = tk.Label(self.master, text=f"选择第 {i+1} 个动画对象:")
            object_label.pack()

            object_var = tk.StringVar()
            object_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE)
            object_listbox.pack()

            # 这里假设有一些动画对象，你可以根据实际情况添加
            objects = ["Square", "Circle", "Triangle"]
            for obj in objects:
                object_listbox.insert(tk.END, obj)

            self.objects.append(object_listbox)

        # 询问需要多少个动画效果
        self.num_effects_label = tk.Label(self.master, text="需要设置多少个动画效果？")
        self.num_effects_label.pack()

        self.num_effects_entry = tk.Entry(self.master)
        self.num_effects_entry.pack()

        self.num_effects_button = tk.Button(self.master, text="确认", command=self.create_windows)
        self.num_effects_button.pack()

    def create_windows(self):
        num_effects = int(self.num_effects_entry.get())
        self.num_effects_label.destroy()
        self.num_effects_entry.destroy()
        self.num_effects_button.destroy()

        # 为每个动画效果创建一个单独的窗口
        for i in range(num_effects):
            effect_window = tk.Toplevel(self.master)
            effect_window.title(f"Effect {i+1}")

            effect_label = tk.Label(effect_window, text=f"选择第 {i+1} 个动画效果:")
            effect_label.pack()

            effect_var = tk.StringVar()
            effect_listbox = tk.Listbox(effect_window, selectmode=tk.SINGLE)
            effect_listbox.pack()

            # 这里假设有一些动画效果，你可以根据实际情况添加
            effects = ["FadeIn", "FadeOut", "MoveTo"]
            for effect in effects:
                effect_listbox.insert(tk.END, effect)

            self.effects.append(effect_listbox)

        # 添加确认按钮
        self.confirm_button = tk.Button(self.master, text="开始处理动画", command=self.start_animation)
        self.confirm_button.pack()

    def start_animation(self):
        threads = []
        for i in range(len(self.effects)):
            selected_objects = [obj.curselection()[0] for obj in self.objects if obj.curselection()]
            selected_effects = [effect.curselection()[0] for effect in self.effects[i] if effect.curselection()]

            objects = [obj.get(selected_objects[j]) for j, obj in enumerate(self.objects)]
            effect = self.effects[i].get(selected_effects[0])

            if i == 0:
                thread = threading.Thread(target=self.generate_class_and_def, args=(objects, effect))
            else:
                thread = threading.Thread(target=self.generate_def, args=(objects, effect))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # 最后将所有代码集中起来
        complete_code = ""
        for thread in threads:
            complete_code += thread.result + "\n"

        print(complete_code)

    def generate_class_and_def(self, objects, effect):
        # 在第一个线程中生成class和def的代码
        class_code = "class MyAnimation(Scene):\n"
        def_code = "    def construct(self):\n"
        for obj in objects:
            def_code += f"        {obj} = {obj}()\n"
        def_code += f"        self.play({effect})\n"
        
        self.result = class_code + def_code

    def generate_def(self, objects, effect):
        # 在后续线程中生成def中的代码
        def_code = ""
        for obj in objects:
            def_code += f"        {obj} = {obj}()\n"
        def_code += f"        self.play({effect})\n"
        
        self.result = def_code

root = tk.Tk()
manim_gui = ManimGUI(root)
root.mainloop()
