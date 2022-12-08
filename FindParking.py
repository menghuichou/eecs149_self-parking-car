import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def find_parking(distance, angle, maxRange = 4, cornerThres = 0.01):
    isParking = False
    width = 0
    depth = 0
    center_parking = 0

    # convert to cartesian
    x,y = data_conversion(angle, distance, maxRange)
    # corner detection
    i_c, line = corner_detection(x,y,cornerThres)
    wall_angle = np.arctan(line[0][0])
    # characterize parking slot
    if len(i_c) >= 3:  # tell if there is a parking slot
        isParking = True
        depth, width, center_parking, angle_parking= characterize_parking(i_c, x, y)

    return depth, width, center_parking, angle_parking, wall_angle, isParking


def data_conversion(angle,distance,maxRange):
    angle = angle[distance <= maxRange]
    distance = distance[distance <= maxRange]

    x = distance * np.sin(angle)
    y = distance * np.cos(angle)
    x = x[y > 0]
    y = y[y > 0]
    y = y[x > 0]
    x = x[x > 0]
    return x,y


def break_detection(x,y,e):
    drho = np.sqrt(np.diff(x)**2+np.diff(y)**2)
    drho_ave = np.mean(drho)
    drho_dev = abs(drho - drho_ave)
    i_bp = np.asarray(np.where(drho_dev>e))
    i_bp = np.append(i_bp,i_bp+1)
    return i_bp


def corner_detection(x, y, e):
    n = len(x)
    i_c = []
    ini = 0
    line = []
    for i in range(1,n-1):
        if i+1-ini >= 2:
            p = np.polyfit(x[ini:i+1], y[ini:i+1], 1)
            pd = np.abs(p[0]*x[i+1]-y[i+1]+p[1])/np.sqrt(p[0]**2+p[1]**2)
            if pd > e:
                i_c.append(i)
                ini = i+1
                line.append(p)
    return i_c,line


def characterize_parking(i_c,x,y):
    c1 = np.asarray([x[i_c[0]], y[i_c[0]]])
    c2 = np.asarray([x[i_c[1]], y[i_c[1]]])
    c3 = np.asarray([x[i_c[-1]], y[i_c[-1]]])
    c2c1 = c1 - c2
    c2c3 = c3 - c2
    cs = np.dot(c2c3, c2c1) / np.linalg.norm(c2c1, 2) / np.linalg.norm(c2c3, 2)
    depth = min([cs * np.linalg.norm(c2c3, 2), np.linalg.norm(c2c1, 2)])  # depth of parking slot
    width = np.linalg.norm(c2c3, 2) * np.sqrt(1 - cs ** 2)  # width of parking slot
    depth_vec = c2c1/ np.linalg.norm(c2c1, 2) * depth / 2
    width_dir = (-c2c1[1], c2c1[0])
    width_vec = width_dir / np.linalg.norm(width_dir) * width / 2
    center_parking = c2 + width_vec + depth_vec  # position of center of parking slot
    angle_parking = np.arctan(c2c1[1]/c2c1[0])
    return depth,width,center_parking,angle_parking
