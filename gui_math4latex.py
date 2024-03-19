import tkinter as tk
from sympy import latex, sympify

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("数学公式转LaTeX形式转换器")

        # 创建标签和文本框
        self.label = tk.Label(self, text="输入数学公式:")
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        # 创建按钮
        self.convert_button = tk.Button(self, text="转换", command=self.convert_formula)
        self.convert_button.pack()

        # 创建文本框用于显示 LaTeX 结果
        self.latex_text = tk.Text(self, wrap="word", height=10)
        self.latex_text.pack(fill="both", expand=True)

    # 转换数学公式为 LaTeX 格式
    def convert_formula(self):
        formula = self.entry.get()
        try:
            latex_formula = latex(sympify(formula))
            self.latex_text.delete("1.0", "end")
            self.latex_text.insert("end", latex_formula)
        except Exception as e:
            self.latex_text.delete("1.0", "end")
            self.latex_text.insert("end", "Error: " + str(e))

# 创建应用程序实例并运行
app = Application()
app.mainloop()
