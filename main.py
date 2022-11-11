import colormath
import pandas

class color():
    def __init__(self, name, parent_name, rgb, hex_code):
        self.name = name
        self.parent_name = parent_name
        self.rgb = rgb
        self.hex_code = hex_code
    
df = pandas.read_csv("colordata.csv")
print(df)
