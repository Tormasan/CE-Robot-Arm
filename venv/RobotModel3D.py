
import matplotlib.pyplot as plt
from numpy import cos,sin,pi
import numpy as np
from mpl_toolkits import mplot3d
import serial
import time

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)
minn=-1
maxn=1

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


def MoveL(thet0,thet1,thet2,xdel,ydel,zdel,rangen):
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
    for i in range(rangen):

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

    return thetresult0, thetresult1, thetresult2, thet0, thet1, thet2


def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n



buffthd0, buffthd1,buffthd2,thnex0,thnex1,thnex2 = MoveL(0,0,0,0.0025,0.0025,0,20)
#buff1thd0, buff1thd1,buff1thd2,th1nex0,th1nex1,th1nex2 = MoveL(thnex0,thnex1,thnex2,-0.0025,0,0,50)
#buff2thd0, buff2thd1,buff2thd2,th2nex0,th2nex1,th2nex2 = MoveL(th1nex0,th1nex1,th1nex2,0,-0.0025,0,50)



def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    num = input("Enter a number: ")
    value = write_read("B"+str(buffthd0)+"N"+str(buffthd1)+"M"+str(buffthd2))
    print(value) # printing the value

print("B"+str(buffthd0)+"N"+str(buffthd1)+"M"+str(buffthd2))
#rajzolassal tervezes ez nagyon tavoli cel
#leveskavargatós program elkészítés
#zonahatár jelzése warning-al tervezéskor vagy a 3 d ábrán
#sd kártyára program mentés
#serial interface es tanitas




