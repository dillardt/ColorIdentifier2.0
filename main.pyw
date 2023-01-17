import pandas
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import pyperclip
from PIL import Image, ImageGrab, ImageStat
from color_stuffs import *

colors = pandas.read_csv("colordata.csv")
colors_len = len(colors)
for i in range(colors_len):
    colors.iloc[i]["Rgb"] = tuple(eval(colors.iloc[i]["Rgb"]))
    colors.iloc[i]["Lab"] = tuple(eval(colors.iloc[i]["Lab"]))

def find_closest(start_color):
    min_color = 0
    min_color_distance = CIEDE2000(start_color, colors.iloc[min_color]["Lab"])
    for i in range(1,colors_len):
        current_distance = CIEDE2000(start_color, colors.iloc[i]["Lab"])
        if current_distance < min_color_distance:
            min_color = i
            min_color_distance = current_distance
    return min_color

def get_pic_rgb():
    try:
        return ImageStat.Stat(ImageGrab.grabclipboard()).mean[:-1]
    except:
        return tuple(eval(pyperclip.paste()[4:-1]))

class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        # Set Icon and Title
        self.setWindowIcon(QIcon('Color_circle_(RGB).svg'))
        self.setWindowTitle("C.I.")

        # Create the "Identify Color" button
        self.button = QPushButton("Identify Color", self)
        self.button.clicked.connect(self.on_button_clicked)

        # Create the "Original Color" and "Result Color" labels
        self.original_square_label = QLabel("Original Color", self)
        self.result_square_label = QLabel("Result Color", self)

        # Create the color squares
        self.original_square = QFrame(self)
        self.original_square.setFrameShape(QFrame.Panel)
        self.original_square.setLineWidth(1)
        self.original_square.setMidLineWidth(0)
        self.original_square.setFixedSize(60, 60)

        self.result_square = QFrame(self)
        self.result_square.setFrameShape(QFrame.Panel)
        self.result_square.setLineWidth(1)
        self.result_square.setMidLineWidth(0)
        self.result_square.setFixedSize(60, 60)

        # Create a label for the result color
        self.result_color_label = QLabel("Closest Color:", self)
        self.result_parent_color_label = QLabel("Closest Parent Color:", self)

        # Create a horizontal layout for the labels and squares
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.original_square, 0, 0, alignment=Qt.AlignHCenter | Qt.AlignBottom)
        grid_layout.addWidget(self.result_square, 0, 1, alignment=Qt.AlignHCenter | Qt.AlignBottom)
        grid_layout.addWidget(self.original_square_label, 1, 0, alignment=Qt.AlignHCenter | Qt.AlignTop)
        grid_layout.addWidget(self.result_square_label, 1, 1, alignment=Qt.AlignHCenter | Qt.AlignTop)

        # Create a vertical layout for the button and horizontal layout
        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.result_color_label, alignment=Qt.AlignCenter | Qt.AlignBottom)
        v_layout.addWidget(self.result_parent_color_label, alignment=Qt.AlignCenter | Qt.AlignTop)
        v_layout.addLayout(grid_layout)
        v_layout.addWidget(self.button, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.setLayout(v_layout)

        # Set window size and fix it
        self.setFixedSize(280, 240)

    def on_button_clicked(self):
        #print(self.size())
        try:
            tested_color = get_pic_rgb()
        except:
            return
        closest_color = colors.iloc[find_closest(rgb_to_lab(tested_color))]
        self.result_color_label.setText(closest_color["Name"])
        self.result_parent_color_label.setText(closest_color["Parent Color"])
        self.original_square.setStyleSheet("QFrame { background-color: #%02x%02x%02x; }" % tested_color)
        self.result_square.setStyleSheet("QFrame { background-color: #%s; }" % closest_color['Hex Code'][2:])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())