
from math import ceil,floor
import random


J1stepabs=250
J2stepabs=300
J3stepabs=115

#"[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#[0, 34, 68, 102, 136, 170, 205, 239, 275, 310, 346, 382, 418, 455, 492, 529, 567, 604, 642, 680]
#[206, 201, 196, 191, 187, 182, 177, 172, 168, 163, 159, 154, 150, 145, 140, 136, 131, 126, 122, 117]

#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#[647, 678, 708, 739, 770, 801, 831, 861, 890, 920, 948, 976, 1004, 1030, 1056, 1081, 1105, 1128, 1150, 1171]
#[101, 97, 93, 88, 84, 80, 76, 71, 67, 63, 58, 54, 49, 45, 40, 35, 30, 26, 21, 16]
# 1 vagy 2 kiesik

J1stepabs = J1
J2stepabs = J2
J3stepabs = J3

if J2stepabs==0:
    J2stepabs=1
if J1stepabs==0:
    J1stepabs=1
if J3stepabs == 0:
    J3stepabs = 1
flag=0

osztalek= J1stepabs / J2stepabs
if osztalek>1:
    if J1stepabs
    szamlalo = J1stepabs
    nevezo = J2stepabs
    osztalek=szamlalo/nevezo
    flag=1
elif osztalek<1:
    szamlalo = J2stepabs
    nevezo = J1stepabs
    osztalek=szamlalo/nevezo
    flag=2


maradek = szamlalo - floor(osztalek) * nevezo
oszthato = nevezo - maradek
eredmeny = oszthato * floor(osztalek) + ceil(osztalek) * maradek


print(szamlalo,nevezo,osztalek,maradek,oszthato,eredmeny)
print(str(floor(osztalek))+"*"+str(oszthato)+"+"+str(ceil(osztalek))+"*"+str(maradek))




J1cur = 0
J2cur = 0
J3cur = 0
J1el=1
J2el=-1
J3el=1

class robotPrint:
  #def __init__(self):

  def step(x,z):
    print(str(z))


rot1Stepper = robotPrint()
rot2Stepper = robotPrint()
baseStepper = robotPrint()



Stepsize1 = floor(osztalek)
Stepsize2 = ceil(osztalek)
StepCount1 = oszthato
StepCount2 = maradek


while (J1cur < J1stepabs or J2cur < J2stepabs or J3cur < J3stepabs):



    while (StepCount1 > 0):

        if flag==1:
            rot1Stepper.step(Stepsize1 * J2el)
            rot2Stepper.step(J3el)
            J3cur = J3cur+1
            J2cur = J2cur+Stepsize1

        elif flag == 2:
            rot1Stepper.step(J2el)
            rot2Stepper.step(Stepsize1 * J3el)
            J2cur = J2cur+1
            J3cur = J3cur + Stepsize1

        if (J1cur < J1stepabs):
            J1cur = J1cur+1
            baseStepper.step(J1el)

        StepCount1=StepCount1-1

    while (StepCount2 > 0):

        if flag == 1:
            rot1Stepper.step(Stepsize2 * J2el)
            rot2Stepper.step(J3el)
            J3cur = J3cur+1
            J2cur = J2cur + Stepsize2

        elif flag == 2:
            rot1Stepper.step(J2el)
            rot2Stepper.step(Stepsize2 * J3el)
            J2cur = J2cur+1
            J3cur = J3cur + Stepsize2

        if (J1cur < J1stepabs):
            J1cur = J1cur+1
            baseStepper.step(J1el)

        StepCount2 = StepCount2 - 1

    if (J1cur < J1stepabs):
        J1cur = J1cur+1
        baseStepper.step(J1el)










