
from math import ceil,floor
import random


J1step=250
J2step=300
J3step=115

J1stepabs = J1step
J2stepabs = J2step
J3stepabs = J3step

if J2step==0:
    J2step=1
if J1step==0:
    J1step=12
flag=0

osztalek= J1step / J2step
if osztalek>1:
    szamlalo = J1step
    nevezo = J2step
    osztalek=szamlalo/nevezo
    flag=1
elif osztalek<1:
    szamlalo = J2step
    nevezo = J1step
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










