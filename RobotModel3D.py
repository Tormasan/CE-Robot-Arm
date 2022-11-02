
import matplotlib.pyplot as plt
from numpy import cos,sin,pi
import numpy as np
from mpl_toolkits import mplot3d
import serial
import time
from typing import List
import re

from gcodeparser import GcodeParser


import keyboard


arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
minn=-1
maxn=1
thet0=0
thet1=0
thet2=0
def test():
    thet0 = float(0)
    thet1 = float(0)
    thet2 = float(0)
    xdel = 0.0025
    ydel = 0.0025
    zdel = 0

    B = 0.19
    CB = 0.03
    CH = 0.2
    HL = 0.2
    x = []
    y = []
    z = []
    thetdel0 = []
    thetdel1 = []
    thetdel2 = []
    th0array = []
    th1array = []
    th2array = []

    resolution=0.02


    #print(CH * np.sin(thet2))
    for i in range(50):

        thetdel0.append(clamp((ydel * cos(thet0) - xdel * sin(thet0)) / (CB - HL * sin(thet1 + thet2) + CH * cos(thet1)), minn, maxn))

        thetdel1.append(clamp(-(zdel * cos(thet1) * cos(thet2) - zdel * sin(thet1) * sin(thet2) + xdel * cos(thet0) * cos(thet1) * sin(thet2) + xdel * cos(thet0) * cos(thet2) * sin(thet1) + ydel * cos(thet1) * sin(thet0) * sin(thet2) + ydel * cos(thet2) * sin(thet0) * sin(thet1)) / (CH * cos(thet2)), minn, maxn))

        thetdel2.append(clamp((CH * zdel * sin(thet1) - CH * xdel * cos(thet0) * cos(thet1) + HL * zdel * cos(thet1) * cos(thet2) - CH * ydel * cos(thet1) * sin(thet0) - HL * zdel * sin(thet1) * sin(thet2) + HL * xdel * cos(thet0) * cos(thet1) * sin(thet2) + HL * xdel * cos(thet0) * cos(thet2) * sin(thet1) + HL * ydel * cos(thet1) * sin(thet0) * sin(thet2) + HL * ydel * cos(thet2) * sin(thet0) * sin(thet1)) / (CH * HL * cos(thet2)), minn, maxn))

        thet0=thet0+thetdel0[i]
        thet1=thet1+thetdel1[i]
        thet2=thet2+thetdel2[i]

        th0array.append(thet0*57)
        th1array.append(thet1*57)
        th2array.append(thet2*57)

        x.append(cos(thet0)*(CB - HL*sin(thet1 + thet2) + CH*cos(thet1)))
        y.append(sin(thet0)*(CB - HL*sin(thet1 + thet2) + CH*cos(thet1)))
        z.append(B - HL*cos(thet1 + thet2) - CH*sin(thet1))

    plt.figure()
    plt.subplot(221)
    plt.plot(thetdel0)
    plt.plot(thetdel1)
    plt.plot(thetdel2)
    plt.xlabel('time/step')
    plt.ylabel('del/speed')

    #plt.show()

    #for thet1 in np.arange(-np.pi/2, np.pi/2, resolution):
    #    for thet2 in np.arange(-np.pi/4, np.pi+np.pi/4, resolution):
    #        x.append(-HL * np.sin(thet1 + thet2) + CH * np.cos(thet1))
    #        y.append(HL * np.cos(thet1 + thet2) + CH * np.sin(thet1))

    plt.subplot(222)
    plt.plot(z, x)
    plt.plot([0,0.4,0.4],[0.23,0.23,0])
    plt.xlabel('z')
    plt.ylabel('x')
    plt.subplot(2,2,3)
    plt.plot(th1array)
    plt.xlabel('TH0/TH1/TH2')
    plt.plot(th0array)
    plt.plot(th2array)
    plt.subplot(2,2,4) # projection='polar'
    plt.plot(y, x)
    plt.plot([0,0,0],[0.23,0.23,0])
    plt.xlabel('y')
    plt.ylabel('x')
    plt.figure()
    plt.plot(z, y)
    plt.plot(0)
    plt.xlabel('z')
    plt.ylabel('y')
    plt.show()


    thd0 = []
    thd1 = []
    thd2 = []
    th0 = float(0)
    th1 = float(0)
    th2 = float(0)

    print(thet0,thet0*57)
    print(thet1,thet1*57)
    print(thet2,thet2*57)

    print(thetdel0)
    print(thetdel1)
    print(thetdel2)

    my_list0 = thetdel0
    my_list1 = thetdel1
    my_list2 = thetdel2
    result0 = [round(item * 142*57.2958) for item in my_list0]
    result1 = [round(item * 944*57.2958) for item in my_list1]
    result2 = [round(item * 144*57.2958) for item in my_list2]
    print(result0)
    print(result1)
    print(result2)


def MoveL(xdel, ydel,zdel):
    r0=0.0
    r1=0.2
    r2=0.2

    x = []
    y = []
    z = []
    thetdel0 = []
    thetdel1 = []
    thetdel2 = []
    rangen=20 # step iteration
    for i in range(rangen):
        global thet0
        global thet1
        global thet2
        thetdel0.append(
            clamp((ydel * cos(thet0) - xdel * sin(thet0)) / (r0 + r2 * cos(thet1 + thet2) + r1 * sin(thet1)), minn,
                  maxn))


        thetdel1.append(
            clamp(
                -(zdel * cos(thet1) * sin(thet2) + zdel * cos(thet2) * sin(thet1) - xdel * cos(thet0) * cos(thet1) * cos(
                thet2) - ydel * cos(thet1) * cos(thet2) * sin(thet0) + xdel * cos(thet0) * sin(thet1) * sin(
                thet2) + ydel * sin(thet0) * sin(thet1) * sin(thet2)) / (r1 * cos(thet2)), minn, maxn))



        thetdel2.append(
            clamp(
                -(r1*zdel*cos(thet1) + r1*xdel*cos(thet0)*sin(thet1) - r2*zdel*cos(thet1)*sin(thet2) -
                r2*zdel*cos(thet2)*sin(thet1) + r1*ydel*sin(thet0)*sin(thet1) - r2*ydel*sin(thet0)*sin(thet1)*sin(thet2) +
                r2*xdel*cos(thet0)*cos(thet1)*cos(thet2) + r2*ydel*cos(thet1)*cos(thet2)*sin(thet0) -
                r2*xdel*cos(thet0)*sin(thet1)*sin(thet2))/(r1*r2*cos(thet2)), minn, maxn))

        thet0 = thet0 + thetdel0[i]
        thet1 = thet1 + thetdel1[i]
        thet2 = thet2 + thetdel2[i]

        x.append(cos(thet0)*(r0 + r2*cos(thet1 + thet2) + r1*sin(thet1)))
        y.append(sin(thet0)*(r0 + r2*cos(thet1 + thet2) + r1*sin(thet1)))
        z.append(r1*cos(thet1) - r2*sin(thet1 + thet2) + 19/100)

    my_list0 = thetdel0
    my_list1 = thetdel1
    my_list2 = thetdel2
    thetresult0 = [round(item * 142 * 57.2958) for item in my_list0]
    thetresult1 = [round(item * 944 * 57.2958) for item in my_list1]
    thetresult2 = [round(item * 144 * 57.2958) for item in my_list2]
    print(thetresult0)
    print(thetresult1)
    print(thetresult2)

    #ploting(x,y,z)


    return thetresult0, thetresult1, thetresult2


def ploting(x,y,z):
    plt.figure()
    plt.subplot(221)
    plt.plot(x, z)
    plt.plot([0, 0, 0.2], [0, 0.39, 0.39])
    plt.xlabel('z')
    plt.ylabel('x')

    plt.subplot(2, 2, 2)  # projection='polar'
    plt.plot(y, z)
    plt.plot([0, 0], [0, 0.4])
    plt.xlabel('y')
    plt.ylabel('x')

    plt.subplot(2, 2, 3)
    plt.plot(x, y)
    plt.plot([0, 0.2], [0, 0])
    plt.xlabel('z')
    plt.ylabel('y')
    plt.show()

def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

def convert_to_bytes(input_array:List[np.int16]):
    output_bytes = bytearray()
    for input_num in input_array:
        output_bytes += (input_num.to_bytes(length=2, byteorder="little", signed=True))
    return output_bytes

def conMoveL(x,y,z):

    buffthd0, buffthd1,buffthd2 = MoveL(x,y,z)
    write_read(buffthd0, buffthd1, buffthd2)
    while arduino.read()!=b'k':  #acknowladge
        time.sleep(dela)

#def posMoveL(xpos, ypos, zpos):

def write_read(buff_0, buff_1, buff_2):
    arduino.write(convert_to_bytes(buff_0))
    time.sleep(.05)
    arduino.write(convert_to_bytes(buff_0))
    time.sleep(.05)
    arduino.write(convert_to_bytes(buff_1))
    time.sleep(.05)
    arduino.write(convert_to_bytes(buff_2))
    time.sleep(.05)


nex=200.0 #start pos x
ney=30.0
nez=390.0
dx=0 #pos dif
dy=0
dz=0

def gcode_read():
    # open gcode file and store contents as variable
    with open('C:/Users/TormaPC/Documents/RoboDK/Programs/Prog2.txt', 'r') as f:
        for line in f:
            sor=str(line)
            pat=re.compile('-?\d{1,4}\.')
            sor_float=[]
            for pos in re.findall(pat,sor): #make a list of all numbers 6 (3pos) (3orient)
                sor_float.append(float(pos))

            if (len(sor_float)>3):  # read the first 3 pos to a variable
                x = sor_float[0]
                y = sor_float[1]
                z = sor_float[2]

                global dx, dy, dz, nex, ney, nez

                dx=x-nex
                dy=y-ney
                dz=z-nez

                div=20000

                conMoveL((dx / div), (dy / div), (dz / div))

                nex=x
                ney=y
                nez=z
                print(dx,dy,dz)
                #print(nex,ney,nez)


def manualL():
    while True:


        if keyboard.read_key() == "z":
           conMoveL(0,0,step)
           break
        if keyboard.read_key() == "c":
           conMoveL(0,0,-step)
           break
        if keyboard.read_key() == "q":
           conMoveL(0,step,0)
           break
        if keyboard.read_key() == "e":
           conMoveL(0,-step,0)
           break
        if keyboard.read_key() == "d":
           conMoveL(step,0,0)
           break
        if keyboard.read_key() == "a":
           conMoveL(-step,0,0)
           break








step=0.004
dela=.01 #azért kell várni hogy ki tudja számolni az ik-t
while True:

    #x = float(input("x: "))
    #y = float(input("y: "))
    #z = float(input("z: "))

    time.sleep(1)
    #manualL()
    #conMoveL(0,-step, 0)
    #conMoveL(0, step, 0)
    gcode_read()

    #conMoveL( 0,0,0)
    #print(arduino.readall())

    #write_read(buffthd0, buffthd1, buffthd2)
    #time.sleep(5)
    #write_read(buff1thd0, buff1thd1, buff1thd2)
    #time.sleep(5)


    #print(arduino.inWaiting())
    #print(arduino.readline())


    #write_read(buff2thd0, buff2thd1, buff2thd2)
    #time.sleep(6.05)



#megcsavarozni ezt a gecit
#roboDK paja teszteles új ik-val
#arduino steppeles optimalizalas
#leveskavargatós program elkészítés
