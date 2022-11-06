
from math import ceil,floor
import random


J1stepabs=455
J2stepabs=9
J3stepabs=47

#"[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#[0, 34, 68, 102, 136, 170, 205, 239, 275, 310, 346, 382, 418, 455, 492, 529, 567, 604, 642, 680]
#[206, 201, 196, 191, 187, 182, 177, 172, 168, 163, 159, 154, 150, 145, 140, 136, 131, 126, 122, 117]

#[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#[647, 678, 708, 739, 770, 801, 831, 861, 890, 920, 948, 976, 1004, 1030, 1056, 1081, 1105, 1128, 1150, 1171]
#[101, 97, 93, 88, 84, 80, 76, 71, 67, 63, 58, 54, 49, 45, 40, 35, 30, 26, 21, 16]
# 1 vagy 2 kiesik


if J2stepabs==0:
    J2stepabs=1
if J1stepabs==0:
    J1stepabs=1
if J3stepabs == 0:
    J3stepabs = 1
flag=0
osztalek2=0

if J1stepabs<10:
    if J2stepabs<J3stepabs:
        flag=2
        szamlalo1=J3stepabs
        szamlalo2=0
        nevezo=J2stepabs
        osztalek=szamlalo1/nevezo
    else:
        flag=3
        szamlalo1=J2stepabs
        szamlalo2=0
        nevezo=J3stepabs
        osztalek = szamlalo1 / nevezo
elif J2stepabs<10:
    if J1stepabs<J3stepabs:
        flag=4
        szamlalo1=J3stepabs
        szamlalo2=0
        nevezo=J1stepabs
        osztalek = szamlalo1 / nevezo
    else:
        flag=5
        szamlalo1=J1stepabs
        szamlalo2=0
        nevezo=J3stepabs
        osztalek = szamlalo1 / nevezo
elif J3stepabs<10:
    if J1stepabs<J2stepabs:
        flag=6
        szamlalo1=J2stepabs
        szamlalo2=0
        nevezo=J1stepabs
        osztalek = szamlalo1 / nevezo
    else:
        flag=7
        szamlalo1=J1stepabs
        szamlalo2=0
        nevezo=J2stepabs
        osztalek = szamlalo1 / nevezo
else:
    if J1stepabs<J2stepabs:
        if J1stepabs<J3stepabs:
            flag=8
            szamlalo1=J3stepabs
            szamlalo2=J2stepabs
            nevezo=J1stepabs
            osztalek = szamlalo1 / nevezo
            osztalek2 = szamlalo2 / nevezo
    if J2stepabs<J1stepabs:
        if J2stepabs<J3stepabs:
            flag=9
            szamlalo1=J3stepabs
            szamlalo2=J1stepabs
            nevezo=J2stepabs
            osztalek = szamlalo1 / nevezo
            osztalek2 = szamlalo2 / nevezo
    if J3stepabs<J1stepabs:
        if J3stepabs<J2stepabs:
            flag=10
            szamlalo1=J2stepabs
            szamlalo2=J1stepabs
            nevezo=J3stepabs
            osztalek = szamlalo1 / nevezo
            osztalek2 = szamlalo2 / nevezo


maradek1 = szamlalo1 - floor(osztalek) * nevezo
oszthato1 = nevezo - maradek1

maradek2 = szamlalo2 - floor(osztalek2) * nevezo
oszthato2 = nevezo - maradek2



print(szamlalo1,nevezo,osztalek,maradek1,oszthato1)
print(str(floor(osztalek))+"*"+str(oszthato1)+"+"+str(ceil(osztalek))+"*"+str(maradek1))
print(str(floor(osztalek2))+"*"+str(oszthato2)+"+"+str(ceil(osztalek2))+"*"+str(maradek2))



J1cur = 0
J2cur = 0
J3cur = 0
J1el=1
J2el=1
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
StepCount1 = oszthato1
StepCount2 = maradek1

Stepsize3 = floor(osztalek2)
Stepsize4 = ceil(osztalek2)
StepCount3 = oszthato2
StepCount4 = maradek2




while (J1cur < J1stepabs or J2cur < J2stepabs or J3cur < J3stepabs):

    if flag==8:
        if StepCount1>0:
            StepCount1=StepCount1-1;

            rot1Stepper.step(Stepsize1 * J2el)
            J2cur = J2cur + Stepsize1

        if StepCount2>0 and StepCount1==0:
            StepCount2=StepCount2-1;

            rot1Stepper.step(Stepsize2 * J2el)
            J2cur = J2cur + Stepsize2

        if StepCount3>0 :
            StepCount3=StepCount3-1;

            rot2Stepper.step(Stepsize3 * J3el)
            J3cur = J3cur + Stepsize3

        if StepCount4>0 and StepCount3==0:
            StepCount4=StepCount4-1;

            rot2Stepper.step(Stepsize4 * J3el)
            J3cur = J3cur + Stepsize4

        if J1cur < J1stepabs:
            baseStepper.step(J1el)
            J1cur = J1cur + 1

    elif flag == 9:
        if StepCount1>0:
            StepCount1=StepCount1-1;

            baseStepper.step(Stepsize1 * J1el)
            J1cur = J1cur + Stepsize1

        if StepCount2>0 and StepCount1==0:
            StepCount2=StepCount2-1;

            baseStepper.step(Stepsize2 * J1el)
            J1cur = J1cur + Stepsize2

        if StepCount3>0 :
            StepCount3=StepCount3-1;

            rot2Stepper.step(Stepsize3 * J3el)
            J3cur = J3cur + Stepsize3

        if StepCount4>0 and StepCount3==0:
            StepCount4=StepCount4-1;

            rot2Stepper.step(Stepsize4 * J3el)
            J3cur = J3cur + Stepsize4

        if J2cur < J2stepabs:
            baseStepper.step(J1el)
            J2cur = J2cur + 1

    elif flag == 10:
        if StepCount1 > 0:
            StepCount1 = StepCount1 - 1;

            baseStepper.step(Stepsize1 * J1el)
            J1cur = J1cur + Stepsize1

        if StepCount2 > 0 and StepCount1 == 0:
            StepCount2 = StepCount2 - 1;

            baseStepper.step(Stepsize2 * J1el)
            J1cur = J1cur + Stepsize2

        if StepCount3 > 0:
            StepCount3 = StepCount3 - 1;

            rot1Stepper.step(Stepsize3 * J2el)
            J2cur = J2cur + Stepsize3

        if StepCount4 > 0 and StepCount3 == 0:
            StepCount4 = StepCount4 - 1;

            rot1Stepper.step(Stepsize4 * J2el)
            J2cur = J2cur + Stepsize4

        if J3cur < J3stepabs:
            rot2Stepper.step(J3el)
            J3cur = J3cur + 1

    if flag==3:
        if StepCount1>0:
            StepCount1=StepCount1-1;

            rot1Stepper.step(Stepsize1 * J2el)
            J2cur = J2cur + Stepsize1

        if StepCount2>0 and StepCount1==0:
            StepCount2=StepCount2-1;

            rot1Stepper.step(Stepsize2 * J2el)
            J2cur = J2cur + Stepsize2

        if J3cur < J3stepabs:
            rot2Stepper.step(J3el)
            J3cur = J3cur + 1

        if J1cur < J1stepabs:
            baseStepper.step(J1el)
            J1cur = J1cur + 1

    if flag == 6:
        if StepCount1>0:
            StepCount1=StepCount1-1;

            rot1Stepper.step(Stepsize1 * J2el)
            J2cur = J2cur + Stepsize1

        if StepCount2>0 and StepCount1==0:
            StepCount2=StepCount2-1;

            rot1Stepper.step(Stepsize2 * J2el)
            J2cur = J2cur + Stepsize2

        if J1cur < J1stepabs:
            baseStepper.step(J1el)
            J1cur = J1cur + 1

        if J3cur < J3stepabs:
            rot2Stepper.step(J3el)
            J3cur = J3cur + 1

    if flag == 2:
        if StepCount1>0:
            StepCount1=StepCount1-1;

            rot2Stepper.step(Stepsize1 * J3el)
            J3cur = J3cur + Stepsize1

        if StepCount2>0 and StepCount1==0:
            StepCount2=StepCount2-1;

            rot2Stepper.step(Stepsize2 * J3el)
            J3cur = J3cur + Stepsize2

        if J2cur < J2stepabs:
            baseStepper.step(J1el)
            J2cur = J2cur + 1

        if J1cur < J1stepabs:
            baseStepper.step(J1el)
            J1cur = J1cur + 1

    if flag == 4:
        if StepCount1>0:
            StepCount1=StepCount1-1;

            rot2Stepper.step(Stepsize1 * J3el)
            J3cur = J3cur + Stepsize1

        if StepCount2>0 and StepCount1==0:
            StepCount2=StepCount2-1;

            rot2Stepper.step(Stepsize2 * J3el)
            J3cur = J3cur + Stepsize2

        if J1cur < J1stepabs:
            baseStepper.step(J1el)
            J1cur = J1cur + 1

        if J2cur < J2stepabs:
            baseStepper.step(J1el)
            J2cur = J2cur + 1

    if flag == 5:
        if StepCount1 > 0:
            StepCount1 = StepCount1 - 1;

            baseStepper.step(Stepsize1 * J1el)
            J1cur = J1cur + Stepsize1

        if StepCount2 > 0 and StepCount1 == 0:
            StepCount2 = StepCount2 - 1;

            baseStepper.step(Stepsize2 * J1el)
            J1cur = J1cur + Stepsize2

        if J3cur < J3stepabs:
            rot2Stepper.step(J3el)
            J3cur = J3cur + 1

        if J2cur < J2stepabs:
            rot1Stepper.step(J2el)
            J2cur = J2cur + 1

    if flag == 7:
        if StepCount1 > 0:
            StepCount1 = StepCount1 - 1;

            baseStepper.step(Stepsize1 * J1el)
            J1cur = J1cur + Stepsize1

        if StepCount2 > 0 and StepCount1 == 0:
            StepCount2 = StepCount2 - 1;

            baseStepper.step(Stepsize2 * J1el)
            J1cur = J1cur + Stepsize2

        if J2cur < J2stepabs:
            rot1Stepper.step(J2el)
            J2cur = J2cur + 1

