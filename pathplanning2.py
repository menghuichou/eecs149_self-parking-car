import numpy as np
import matplotlib.pyplot as plt

R = 7/2/100             #m
L = 14.9/100            #m
c = 0.01                # clearance
R_min = 20/100         # supposed minimum turning radius

# dis_wall = R_min + c * 1.1 #m measured..
cw = L/2+c

T = 0.02
V = 0.1

def parallel(dis_wall):
    O = np.array([L/2-R_min,np.sqrt((cw+R_min)**2-(R_min-L/2)**2)])
    A = np.array([L/2,np.sqrt((cw+R_min)**2-(R_min-L/2)**2)])
    theta = np.arctan((R_min-L/2)/(R_min+L/2+c))
    B = np.array([-cw*np.sin(theta),cw*np.cos(theta)])
    xc = -(dis_wall-R_min)-R_min*np.sin(theta)
    yc = np.tan(theta)*(xc-B[0])+B[1]
    D = np.array([-dis_wall,yc-R_min*np.cos(theta)])
    xR = -dis_wall+R_min
    yR = D[1]

    # D-C estimated waypoint calc
    th1 = np.arange(np.pi,np.pi/2+theta,-V/R_min*T)
    xDC = xR + R_min*np.cos(th1)
    yDC = yR + R_min*np.sin(th1)

    # C-B
    xCB = np.arange(xc,B[0],V*T*np.cos(theta))
    yCB = np.arange(yc,B[1],V*T*np.sin(theta))

    #BA
    th2 = np.arange(3*np.pi/2+theta, 2*np.pi,V/R_min*T)
    xBA = O[0] + R_min*np.cos(th2)
    yBA = O[1] + R_min*np.sin(th2)

    # parallel waypoint
    x_p = np.concatenate([xDC,xCB,xBA])
    y_p = np.concatenate([yDC,yCB,yBA])
    return x_p,y_p

def straight(dis_wall):
    # straight waypoint
    th = np.arange(np.pi,np.pi/2,-V/R_min*T)
    x12 = -dis_wall + R_min + R_min*np.cos(th)
    y12 = L/2+c - R_min + R_min*np.sin(th)
    x20 = np.arange(-dis_wall+R_min,L/2,V*T)
    y20 = (L/2+c)*np.ones(len(x20))
    x_s = np.concatenate([x12,x20])
    y_s = np.concatenate([y12,y20])

    return x_s, y_s


