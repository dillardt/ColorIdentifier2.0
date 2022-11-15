def rgb_to_xyz(inp_rgb):
    rgb = [float(x) for x in inp_rgb]

    for i, val in enumerate(rgb):
        val /= 255
        val = ((val + 0.055) / 1.055) ** 2.4 if val > 0.04045 else val / 12.92
        val *= 100
        rgb[i] = val

    xyz = [0.0,0.0,0.0]

    xyz[0] = round(rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805, 4)
    xyz[1] = round(rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722, 4)
    xyz[2] = round(rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505, 4)
    
    return xyz

def xyz_to_lab(inp_xyz):
    xyz = [float(x) for x in inp_xyz]

    xyz[0] /= 95.047
    xyz[1] /= 100.0
    xyz[2] /= 108.883

    for i, val in enumerate(xyz):
        val = val ** (1/3) if val > 0.008856 else (7.787 * val) + (16 / 116)
        xyz[i] = val
    
    lab = [0.0,0.0,0.0]

    lab[0] = round((116 * xyz[1]) - 16, 4)
    lab[1] = round(500 * (xyz[0] - xyz[1]), 4)
    lab[2] = round(200 * (xyz[1] - xyz[2]), 4)

    return lab

def rgb_to_lab(inp_rgb):
    return xyz_to_lab(rgb_to_xyz(inp_rgb))

def color_distance(color1, color2):
    pass