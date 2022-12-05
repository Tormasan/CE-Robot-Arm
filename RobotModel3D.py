
import matplotlib.pyplot as plt
from numpy import cos,sin,pi
import numpy as np
from mpl_toolkits import mplot3d
import serial
import time
from typing import List
import re
import ikpy.chain
import math
import ikpy.utils.plot as plot_utils


from gcodeparser import GcodeParser


import keyboard


#arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)
minn=-2
maxn=2
thet0=0.00001
thet1=0.00001
thet2=0.00001
thet3=0.00001
thet4=0.00001
thet5=0.00001

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



def MoveJ(xpos, ypos, zpos ,xrot=0, yrot=0, zrot=0):

    stepc=20
    my_chain = ikpy.chain.Chain.from_urdf_file("robot.urdf",active_links_mask=[False, True, True, True, True, True, True])

    target_position = [xpos, ypos, zpos]
    target_orientation = [xrot, yrot, zrot]

    ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="all")
    iklist =ik.tolist()
    iklist[5]=iklist[5]+iklist[4]/2.95

    print(iklist[0])
    thetresult0 = [round(iklist[1]* 142 * 57.2958 / stepc) for x in range(stepc)]
    thetresult1 = [round(iklist[2] * 944 * 57.2958 / stepc) for th1 in range(stepc)]
    thetresult2 = [round(iklist[3] * 144 * 57.2958 / stepc) for th2 in range(stepc) ]
    thetresult3 = [round(iklist[4] * 32 * 57.2958 / stepc) for th3 in range(stepc)]
    thetresult4 = [round(iklist[5] * 11 * 57.2958 / stepc) for th4 in range(stepc)]
    thetresult5 = [round(iklist[6] * 10 * 57.2958 / stepc) for th5 in range(stepc)]

    return thetresult0, thetresult1, thetresult2, thetresult3, thetresult4, thetresult5

#print("The angles of each joints are : ", list(map(lambda r: math.degrees(r), ik.tolist())))
#kutyaaa=ik.tolist()[1]
#print(kutyaaa)
#computed_position = my_chain.forward_kinematics(ik)
#print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
#print("Computed position (readable) : %s" % ['%.2f' % elem for elem in computed_position[:3, 3]])
print(MoveJ(3,0,4.2,1))

def doIK():
    global ik
    old_position = ik.copy()
    ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Z",
                                     initial_position=old_position)


def updatePlot():
    ax.clear()
    my_chain.plot(ik, ax, target=target_position)
    plt.xlim(-0.5, 0.5)
    plt.ylim(-0.5, 0.5)
    ax.set_zlim(0, 0.6)
    fig.canvas.draw()
    fig.canvas.flush_events()


def move(x, y, z):
    global target_position
    target_position = [x, y, z]
    doIK()
    updatePlot()


#import matplotlib.pyplot as plt
#fig, ax = plot_utils.init_3d_figure()
#fig.set_figheight(9)
#fig.set_figwidth(13)
#my_chain.plot(ik, ax, target=target_position)
#plt.xlim(-0.5, 0.5)
#plt.ylim(-0.5, 0.5)
#ax.set_zlim(0, 0.6)
#plt.ion()

#move(3, 0, 4.2)


def MoveL(xdel, ydel, zdel):
    r1=0.2
    r2=0.03
    d0=0.19
    d3=0.225
    d5=0.075

    degrad=57.2958

    thet0_max = 120 / degrad
    thet0_min = -120 / degrad
    thet1_max= 75/degrad
    thet1_min= -75/degrad
    thet2_max= 85/degrad
    thet2_min= -45/degrad
    thet3_max= 360/degrad
    thet3_min= -360/degrad
    thet4_max = 120 / degrad
    thet4_min = -120 / degrad
    thet5_max = 360 / degrad
    thet5_min = -360 / degrad

    rolldel=-0.0
    pitchdel=0.0
    yawdel=0.0

    global thet0
    global thet1
    global thet2
    global thet3
    global thet4
    global thet5

    #xdel = xdel - d5 * cos(thet3)*sin(thet4)
    #ydel = ydel - d5 * sin(thet3)*sin(thet4)
    #zdel = zdel - d5 * cos(thet4)


    x = []
    y = []
    z = []

    thetdel0 = []
    thetdel1 = []
    thetdel2 = []
    thetdel3 = []
    thetdel4 = []
    thetdel5 = []
    rangen=20 # step iteration
    for i in range(rangen):
        #global thet0
        #global thet1
        #global thet2
        #global thet3
        #global thet4
        #global thet5

        thetdel0.append(
            clamp((ydel*cos(thet0) - xdel*sin(thet0))/(d3*cos(thet1 + thet2) + r2*sin(thet1 + thet2) + r1*sin(thet1)), minn,maxn))

        thetdel1.append(
            clamp((d3*xdel*cos(thet0 - thet1 - thet2) + r2*ydel*cos(thet0 - thet1 - thet2) + d3*ydel*sin(thet0 - thet1 - thet2) - r2*xdel*sin(thet0 - thet1 - thet2) + d3*xdel*cos(thet0 + thet1 + thet2) - r2*ydel*cos(thet0 + thet1 + thet2) + d3*ydel*sin(thet0 + thet1 + thet2) + r2*xdel*sin(thet0 + thet1 + thet2) + 2*r2*zdel*cos(thet1 + thet2) - 2*d3*zdel*sin(thet1 + thet2))/(2*r1*(d3*cos(thet2) + r2*sin(thet2))), minn, maxn))

        thetdel2.append(
            clamp(-(r1*zdel*cos(thet1) + r1*xdel*cos(thet0)*sin(thet1) + r1*ydel*sin(thet0)*sin(thet1) - r2*zdel*sin(thet1)*sin(thet2) + r2*zdel*cos(thet1)*cos(thet2) - d3*zdel*cos(thet1)*sin(thet2) - d3*zdel*cos(thet2)*sin(thet1) + d3*xdel*cos(thet0)*cos(thet1)*cos(thet2) + d3*ydel*cos(thet1)*cos(thet2)*sin(thet0) + r2*xdel*cos(thet0)*cos(thet1)*sin(thet2) + r2*xdel*cos(thet0)*cos(thet2)*sin(thet1) - d3*xdel*cos(thet0)*sin(thet1)*sin(thet2) + r2*ydel*cos(thet1)*sin(thet0)*sin(thet2) + r2*ydel*cos(thet2)*sin(thet0)*sin(thet1) - d3*ydel*sin(thet0)*sin(thet1)*sin(thet2))/(r1*(d3*cos(thet2) + r2*sin(thet2))), minn, maxn))


        #if thet0_min >= thet0 and thet0 <= thet0_max:
        thet0 = thet0 + thetdel0[i]
        #if thet1_min >= thet1 and thet1 <= thet1_max:
        thet1 = thet1 + thetdel1[i]
        #if thet2_min >= thet2 and thet2 <= thet2_max:
        thet2 = thet2 + thetdel2[i]
        #if thet3_min >= thet3 and thet3 <= thet3_max:


        print(thet0*57,thet1*57,thet2*57)
        x.append(cos(thet0)*(d3*cos(thet1 + thet2) + r2*sin(thet1 + thet2) + r1*sin(thet1)))
        y.append(sin(thet0)*(d3*cos(thet1 + thet2) + r2*sin(thet1 + thet2) + r1*sin(thet1)))
        z.append(d0 + r2*cos(thet1 + thet2) - d3*sin(thet1 + thet2) + r1*cos(thet1))

    R0_6 = [[0.0, 0.0, 1.0],
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0]]

    R0_3 = [[sin(thet1 + thet2) * cos(thet0), sin(thet0), cos(thet1 + thet2) * cos(thet0)],
            [sin(thet1 + thet2) * sin(thet0), -cos(thet0), cos(thet1 + thet2) * sin(thet0)],
            [cos(thet1 + thet2), 0, -sin(thet1 + thet2)]]

    invR0_3 = np.linalg.inv(R0_3)

    R3_6 = np.dot(invR0_3, R0_6)

    print(R3_6)
    thet3 = thet3-(np.arctan2(R3_6[1][2], R3_6[0][2]))
    print((np.arctan2(R3_6[1][2], R3_6[0][2])))
    thet4 = thet4-(np.arccos(R3_6[2][2]))
    print(thet4-(np.arccos(R3_6[2][2])))
    if thet4 == 0 or thet4 == pi:
        print("Theta")
    thet5 = thet5-(np.arctan2(R3_6[2][1], R3_6[2][0]))
    print((np.arctan2(R3_6[2][1], R3_6[2][0])))
    print(R3_6[2][1], R3_6[2][0])
    print(thet3,thet4,thet5)
    th3=((thet3-(np.arctan2(R3_6[2][1], R3_6[2][0]))))
    th4=((thet4-(np.arctan2(np.sqrt((R3_6[1][2])**2+(R3_6[0][2])**2),R3_6[2][2]))))
    th5=((thet5-(np.arctan2(R3_6[1][2], -R3_6[0][2]))))

    print(th3*degrad,th4*degrad,th4*degrad)
    for i in range(rangen):
        thetdel3.append(th3)
        thetdel4.append(th4+(th3/2.95))
        thetdel5.append(th5)

    thetresult0 = [round(th0 * 142 * 57.2958) for th0 in thetdel0]
    thetresult1 = [round(th1 * 944 * 57.2958) for th1 in thetdel1]
    thetresult2 = [round(th2 * 144 * 57.2958) for th2 in thetdel2]
    thetresult3 = [round(th3 * 32 ) for th3 in thetdel3]
    thetresult4 = [round(th4 * 11 ) for th4 in thetdel4]
    thetresult5 = [round(th5 * 10 ) for th5 in thetdel5]

    #ki kell egészíteni a diferencia kivonásával
    print(thetresult0)
    print(thetresult1)
    print(thetresult2)
    print(thetresult3)
    print(thetresult4)
    print(thetresult5)

    ploting(x,y,z)


    return thetresult0, thetresult1, thetresult2, thetresult3, thetresult4, thetresult5


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

    buffthd0, buffthd1, buffthd2, buffthd3, buffthd4, buffthd5 = MoveL(x,y,z)
    arrayzero = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    arraypos =[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    array3 = [35, 35, 35, 35, 35, 35, 35, 35, 35, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33]
    arrayneg = [-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100]
    write_read(buffthd0, buffthd1, buffthd2, buffthd3, buffthd4, buffthd5)
    #write_read(arrayzero,arrayzero,arrayzero,arraypos,array3,arrayzero)
    while arduino.read()!=b'k':  #acknowladge
        time.sleep(dela)

def posMoveJ(xpos, ypos, zpos ,xrot, yrot, zrot):

    buffthd0, buffthd1, buffthd2, buffthd3, buffthd4, buffthd5 = MoveJ(xpos, ypos, zpos ,xrot, yrot, zrot)
    write_read(buffthd0, buffthd1, buffthd2, buffthd3, buffthd4, buffthd5)
    while arduino.read()!=b'k':  #acknowladge
        time.sleep(dela)
def write_read(buff_0, buff_1, buff_2, buff_3, buff_4, buff_5):
    arduino.write(convert_to_bytes(buff_0))
    time.sleep(.2)
    arduino.write(convert_to_bytes(buff_0))
    time.sleep(.2)
    arduino.write(convert_to_bytes(buff_1))
    time.sleep(.2)
    arduino.write(convert_to_bytes(buff_2))
    time.sleep(.2)
    arduino.write(convert_to_bytes(buff_3))
    time.sleep(.2)
    arduino.write(convert_to_bytes(buff_4))
    time.sleep(.2)
    arduino.write(convert_to_bytes(buff_5))
    time.sleep(.2)
    print(arduino.readall())

nex=300.0 #start pos x
ney=0.0
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

def gcode_read_ori():
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
                xr = sor_float[3]
                yr = sor_float[4]
                zr = sor_float[5]

                div=100
                raddeg=57.2958
                posMoveJ((x / div), (y / div), (z / div),(xr / raddeg), (yr / raddeg), (zr / raddeg))




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
        if keyboard.read_key() == "n":
           conMoveL(0,0,0)
           break



step=0.004
dela=.01 #azért kell várni hogy ki tudja számolni az ik-t
#while True:

    #x = float(input("x: "))
    #y = float(input("y: "))
    #z = float(input("z: "))


    #manualL()
    #MoveTopG()
    #time.sleep(10)
    #conMoveL(0,-step, 0)
    #conMoveL(0, step, 0)
    #gcode_read()

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


#arduino steppeles optimalizalas


