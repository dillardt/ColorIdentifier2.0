import pandas
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

pic = ImageGrab.grabclipboard()
average_lab = rgb_to_lab(ImageStat.Stat(pic).mean[:-1])

print(average_lab)
print(colors.iloc[find_closest(average_lab)])