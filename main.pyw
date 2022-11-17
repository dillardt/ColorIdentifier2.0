import pandas
import base64
import pyperclip
from tkinter import *
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

def on_click():
    try:
        tested_color = get_pic_rgb()
    except:
        return
    tested_color_square.config(bg=f"#{''.join(hex(int(x))[2:].zfill(2) for x in tested_color)}")
    closest_color = colors.iloc[find_closest(rgb_to_lab(tested_color))]
    result_color_sqaure.config(bg=f"#{closest_color['Hex Code'][2:]}")
    output_color.config(text=f"Color Name: {closest_color['Name']}\nParent Name: {closest_color['Parent Color']}")

window = Tk()
frame = Frame(window)
window.title("CT2")
window.geometry("200x150")
window.resizable(False,False)
frame.pack(fill=BOTH, expand=True)

img = """
    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
8PeFEPg/2rK7jCY8aKQAAAAASUVORK5CYII=
    """
img= base64.b64decode(img)
img=PhotoImage(data=img) 
window.wm_iconphoto(True, img)

btn = Button(frame, text="Test Color", command=on_click)
output_color = Label(frame, text="Color Name:\nParent Name:", fg="#000000", state=DISABLED)

color_box_frame = Frame(frame)
tested_color_square = Label(color_box_frame, text="Tested Color", pady=10)
result_color_sqaure = Label(color_box_frame, text="Result Color", pady=10)
seper = Label(color_box_frame, padx=10)
tested_color_square.pack(side=LEFT)
seper.pack(side=LEFT)
result_color_sqaure.pack(side=RIGHT)


output_color.pack(side=TOP, pady=10)
color_box_frame.pack(side=TOP)
btn.pack(side=BOTTOM, pady=10)


window.mainloop()