import pandas
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
    return ImageStat.Stat(ImageGrab.grabclipboard()).mean[:-1]

def on_click():
    try:
        closest_color = colors.iloc[find_closest(rgb_to_lab(get_pic_rgb()))]
        output_color.config(text=f"Color Name: {closest_color['Name']}\nParent Name: {closest_color['Parent Color']}")
    except:
        print("Non-image copied to clipboard")

window = Tk()
frame = Frame(window)
window.title("CT2")
window.geometry("200x100")
window.resizable(False,False)
frame.pack(fill=BOTH, expand=True)

btn = Button(frame, text="TEST", command=on_click)
output_color = Label(frame, text="Test", fg="#000000", state=DISABLED)

output_color.pack(side=TOP, pady=10)
btn.pack(side=BOTTOM, pady=10)


window.mainloop()