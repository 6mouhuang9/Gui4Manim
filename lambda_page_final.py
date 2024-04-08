import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSpinBox, QColorDialog, QHBoxLayout, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from object_params_final import OBJECTS_PARAMS,animation_params_options
import json
import subprocess

class ManimParametricGraphGeneratorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.manim_script_path = 'manim_code_4_7.py'

    def initUI(self):
        self.setWindowTitle("Manim 动画生成器")
        self.setGeometry(300, 300, 800, 600)

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # 动画数量询问
        self.animation_count_label = QLabel("动画数量：")
        self.animation_count_label.setFont(QFont('Arial', 20))
        self.animation_count_spinner = QSpinBox()
        self.animation_count_spinner.setMinimum(1)
        self.animation_count_spinner.setMaximum(10)
        self.animation_count_spinner.valueChanged.connect(self.createParamInputs)
        self.layout.addWidget(self.animation_count_label)
        self.layout.addWidget(self.animation_count_spinner)

        # 参数输入区域
        self.param_inputs = []
        self.layout.addLayout(self.form_layout)

        # 创建生成代码按钮
        self.generate_code_button = QPushButton("生成动画", self)
        self.generate_code_button.setFont(QFont('Arial', 20))
        self.generate_code_button.clicked.connect(self.generate_code)
        self.layout.addWidget(self.generate_code_button)

        self.setLayout(self.layout)

    def createParamInputs(self):
        # 清除旧的输入控件
        for i in reversed(range(self.form_layout.count())): 
            self.form_layout.itemAt(i).widget().setParent(None)

        # 创建新的输入控件
        self.param_inputs = []
        for i in range(self.animation_count_spinner.value()):
            formula_input = QLineEdit(self)
            range_input = QLineEdit(self)
            color_input = QLineEdit(self)
            color_button = QPushButton("选择颜色", self)
            color_button.clicked.connect(lambda _, x=i: self.openColorDialog(x))

            self.form_layout.addRow(QLabel(f"图形 {i+1} 公式："), formula_input)
            self.form_layout.addRow(QLabel(f"图形 {i+1} 范围："), range_input)
            self.form_layout.addRow(QLabel(f"图形 {i+1} 颜色："), color_input)
            self.form_layout.addRow(color_button)

            self.param_inputs.append((formula_input, range_input, color_input))

    def openColorDialog(self, index):
        color = QColorDialog.getColor()
        if color.isValid():
            self.param_inputs[index][2].setText(color.name())

    def generate_code(self):
        manim_code = "from manim import *\n\nclass MultiGraphScene(Scene):\n    def construct(self):\n"
        manim_code += "        plane = NumberPlane()\n        self.add(plane)\n"
        for formula_input, range_input, color_input in self.param_inputs:
            formula = formula_input.text()
            x_range = range_input.text()
            color = color_input.text()
            manim_code += f"        self.play(Create(ParametricFunction(lambda x: np.array([x, {formula}, 0]), t_range=[{x_range}], color='{color}')), run_time = 5)\n"
        manim_code += "        self.wait(2)\n"
        print(manim_code)
        self.create_manim_script(manim_code)
    
    def create_manim_script(self,manim_code):
        # 方法实现 - 创建Manim脚本并执行
        with open(self.manim_script_path, "w") as f:
            f.write(manim_code)
        subprocess.run(["manim", "-pql", self.manim_script_path, "MyScene"])

""" app = QApplication(sys.argv)
ex = ManimParametricGraphGeneratorGUI()
ex.show()
sys.exit(app.exec_())
 """

#不是，等会，我怎么感觉这个生成新框的方法比tk简单多了？
