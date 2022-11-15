import math

def CIEDE2000(Lab_1, Lab_2): #lovro-i on github NOT MY CODE
    '''Calculates CIEDE2000 color distance between two CIE L*a*b* colors'''
    C_25_7 = 6103515625 # 25**7
    
    L1, a1, b1 = Lab_1[0], Lab_1[1], Lab_1[2]
    L2, a2, b2 = Lab_2[0], Lab_2[1], Lab_2[2]
    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)
    C_ave = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(C_ave**7 / (C_ave**7 + C_25_7)))
    
    L1_, L2_ = L1, L2
    a1_, a2_ = (1 + G) * a1, (1 + G) * a2
    b1_, b2_ = b1, b2
    
    C1_ = math.sqrt(a1_**2 + b1_**2)
    C2_ = math.sqrt(a2_**2 + b2_**2)
    
    if b1_ == 0 and a1_ == 0: h1_ = 0
    elif a1_ >= 0: h1_ = math.atan2(b1_, a1_)
    else: h1_ = math.atan2(b1_, a1_) + 2 * math.pi
    
    if b2_ == 0 and a2_ == 0: h2_ = 0
    elif a2_ >= 0: h2_ = math.atan2(b2_, a2_)
    else: h2_ = math.atan2(b2_, a2_) + 2 * math.pi

    dL_ = L2_ - L1_
    dC_ = C2_ - C1_    
    dh_ = h2_ - h1_
    if C1_ * C2_ == 0: dh_ = 0
    elif dh_ > math.pi: dh_ -= 2 * math.pi
    elif dh_ < -math.pi: dh_ += 2 * math.pi        
    dH_ = 2 * math.sqrt(C1_ * C2_) * math.sin(dh_ / 2)
    
    L_ave = (L1_ + L2_) / 2
    C_ave = (C1_ + C2_) / 2
    
    _dh = abs(h1_ - h2_)
    _sh = h1_ + h2_
    C1C2 = C1_ * C2_
    
    if _dh <= math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2
    elif _dh  > math.pi and _sh < 2 * math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2 + math.pi
    elif _dh  > math.pi and _sh >= 2 * math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2 - math.pi 
    else: h_ave = h1_ + h2_
    
    T = 1 - 0.17 * math.cos(h_ave - math.pi / 6) + 0.24 * math.cos(2 * h_ave) + 0.32 * math.cos(3 * h_ave + math.pi / 30) - 0.2 * math.cos(4 * h_ave - 63 * math.pi / 180)
    
    h_ave_deg = h_ave * 180 / math.pi
    if h_ave_deg < 0: h_ave_deg += 360
    elif h_ave_deg > 360: h_ave_deg -= 360
    dTheta = 30 * math.exp(-(((h_ave_deg - 275) / 25)**2))
    
    R_C = 2 * math.sqrt(C_ave**7 / (C_ave**7 + C_25_7))  
    S_C = 1 + 0.045 * C_ave
    S_H = 1 + 0.015 * C_ave * T
    
    Lm50s = (L_ave - 50)**2
    S_L = 1 + 0.015 * Lm50s / math.sqrt(20 + Lm50s)
    R_T = -math.sin(dTheta * math.pi / 90) * R_C

    k_L, k_C, k_H = 1, 1, 1
    
    f_L = dL_ / k_L / S_L
    f_C = dC_ / k_C / S_C
    f_H = dH_ / k_H / S_H
    
    dE_00 = math.sqrt(f_L**2 + f_C**2 + f_H**2 + R_T * f_C * f_H)
    return dE_00

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

def simple_color_distance(color1, color2):
    return ((color2[0]-color1[0])**2 + (color2[1]-color1[1])**2 + (color2[2]-color1[2])**2)**0.5