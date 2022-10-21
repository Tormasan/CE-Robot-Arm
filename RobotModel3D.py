
import matplotlib.pyplot as plt
from numpy import cos,sin,pi
import numpy as np
from mpl_toolkits import mplot3d
import serial
import time
from typing import List
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


def MoveL(xdel,ydel,zdel):
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
    rangen=20 # step iteration
    for i in range(rangen):
        global thet0
        global thet1
        global thet2
        thetdel0.append(
            clamp((ydel * cos(thet0) - xdel * sin(thet0)) / (CB - HL * sin(thet1 + thet2) + CH * cos(thet1)), minn,
                  maxn))

        thetdel1.append(clamp(-(
                    zdel * cos(thet1) * cos(thet2) - zdel * sin(thet1) * sin(thet2) + xdel * cos(thet0) * cos(
                thet1) * sin(thet2) + xdel * cos(thet0) * cos(thet2) * sin(thet1) + ydel * cos(thet1) * sin(
                thet0) * sin(thet2) + ydel * cos(thet2) * sin(thet0) * sin(thet1)) / (CH * cos(thet2)), minn, maxn))

        thetdel2.append(clamp((CH * zdel * sin(thet1) - CH * xdel * cos(thet0) * cos(thet1) + HL * zdel * cos(
            thet1) * cos(thet2) - CH * ydel * cos(thet1) * sin(thet0) - HL * zdel * sin(thet1) * sin(
            thet2) + HL * xdel * cos(thet0) * cos(thet1) * sin(thet2) + HL * xdel * cos(thet0) * cos(thet2) * sin(
            thet1) + HL * ydel * cos(thet1) * sin(thet0) * sin(thet2) + HL * ydel * cos(thet2) * sin(thet0) * sin(
            thet1)) / (CH * HL * cos(thet2)), minn, maxn))

        thet0 = thet0 + thetdel0[i]
        thet1 = thet1 + thetdel1[i]
        thet2 = thet2 + thetdel2[i]

        x.append(cos(thet0) * (CB - HL * sin(thet1 + thet2) + CH * cos(thet1)))
        y.append(sin(thet0) * (CB - HL * sin(thet1 + thet2) + CH * cos(thet1)))
        z.append(B - HL * cos(thet1 + thet2) - CH * sin(thet1))

    my_list0 = thetdel0
    my_list1 = thetdel1
    my_list2 = thetdel2
    thetresult0 = [round(item * 142 * 57.2958) for item in my_list0]
    thetresult1 = [round(item * 944 * 57.2958) for item in my_list1]
    thetresult2 = [round(item * 144 * 57.2958) for item in my_list2]
    print(thetresult0)
    print(thetresult1)
    print(thetresult2)

    plt.figure()
    plt.subplot(221)
    plt.plot(z, x)
    plt.plot([0, 0.4, 0.4], [0.23, 0.23, 0])
    plt.xlabel('z')
    plt.ylabel('x')

    plt.subplot(2, 2, 2)  # projection='polar'
    plt.plot(y, x)
    plt.plot([0, 0, 0], [0.23, 0.23, 0])
    plt.xlabel('y')
    plt.ylabel('x')

    plt.subplot(2, 2, 3)
    plt.plot(z, y)
    plt.plot(0)
    plt.xlabel('z')
    plt.ylabel('y')
    plt.show()

    return thetresult0, thetresult1, thetresult2


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
    time.sleep(3)





#rajzolassal tervezes ez nagyon tavoli cel
#leveskavargatós program elkészítés
#zonahatár jelzése warning-al tervezéskor vagy a 3 d ábrán
#sd kártyára program mentés
#serial interface es tanitas


def write_read(buff_0, buff_1, buff_2):
    arduino.write(convert_to_bytes(buff_0))
    time.sleep(.05)
    arduino.write(convert_to_bytes(buff_1))
    time.sleep(.05)
    arduino.write(convert_to_bytes(buff_2))
    time.sleep(.05)


step=0.001

while True:

    #x = float(input("x: "))
    #y = float(input("y: "))
    #z = float(input("z: "))

    conMoveL(0, 0.001, 0)
    conMoveL(0, -0.001, 0)

    #print(arduino.readall())





    #while True:


     #   if keyboard.read_key() == "a":
      #      conMoveL(0,0,step)
       #     break
        #if keyboard.read_key() == "d":
         #   conMoveL(0,0,-step)
          #  break
        #if keyboard.read_key() == "q":
         #   conMoveL(0,step,0)
          #  break
        #if keyboard.read_key() == "e":
         #   conMoveL(0,-step,0)
          #  break
        #if keyboard.read_key() == "z":
         #   conMoveL(step,0,0)
          #  break
        #if keyboard.read_key() == "c":
         #   conMoveL(-step,0,0)
          #  break



    #write_read(buffthd0, buffthd1, buffthd2)
    #time.sleep(5)
    #write_read(buff1thd0, buff1thd1, buff1thd2)
    #time.sleep(5)


    #print(arduino.inWaiting())
    #print(arduino.readline())


    #write_read(buff2thd0, buff2thd1, buff2thd2)
    #time.sleep(6.05)


