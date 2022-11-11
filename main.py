import colormath
import pandas

def color_distance(color1, color2):
    return ((color2[0]-color1[0])**2 + (color2[1]-color1[1])**2 + (color2[2]-color1[2])**2)**0.5

colors = pandas.read_csv("colordata.csv")
colors_len = len(colors)
for i in range(colors_len):
    colors.iloc[i]["Rgb"] = tuple(eval(colors.iloc[i]["Rgb"]))

def find_closest(start_color):
    min_color = 0
    min_color_distance = color_distance(start_color, colors.iloc[min_color]["Rgb"])
    for i in range(1,colors_len):
        current_distance = color_distance(start_color, colors.iloc[i]["Rgb"])
        if current_distance < min_color_distance:
            min_color = i
            min_color_distance = current_distance
    return min_color

print(colors.iloc[find_closest((100,100,100))])