syms  thet0 thet1 thet2 thet3 thet4 thet5 r1 r2  alp0 alp2 alp3 alp4  d0 d3 d5

%alpn rn dn thetn   
alp0=-pi/2
%thet0=0
%thet1=0
%thet2=0

%thet3=0
%thet4=0
%thet5=0


rn=0
thetn=0
alpn=0
dn=d3

K = [0;
     0;
     1]

Base = [cos(thetn) -sin(thetn)*cos(alpn) sin(thetn)*sin(alpn) rn*cos(thetn);
     sin(thetn) cos(thetn)*cos(alpn) -cos(thetn)*sin(alpn) rn*sin(thetn);
     0 sin(alpn) cos(alpn) dn;
     0 0 0 1]
 


alpn=alp0
dn=d0

J1 = [cos(thet0) 0 -sin(thet0) 0;
     sin(thet0) 0 cos(thet0) 0;
     0 -1 0 d0;
     0 0 0 1]

J2 =  [cos(thet1-pi/2) -sin(thet1-pi/2) 0 r1*cos(thet1-pi/2);
     sin(thet1-pi/2) cos(thet1-pi/2) 0 r1*sin(thet1-pi/2);
     0 0 1 0;
     0 0 0 1]
J3 =  [cos(thet2) 0 -sin(thet2) r2*cos(thet2);
     sin(thet2) 0 cos(thet2) r2*sin(thet2);
     0 -1 0 0;
     0 0 0 1]
 
J34 = [1 0 0 0;
       0 1 0 0;
       0 0 1 d3;
       0 0 0 1]
        
J4 = [cos(thet3) 0 -sin(thet3) 0;
     sin(thet3) 0 cos(thet3) 0;
     0 -1 0 0;
     0 0 0 1]
J5 = [cos(thet4) 0 sin(thet4) 0;
     sin(thet4) 0 -cos(thet4) 0;
     0 1 0 0;
     0 0 0 1]
J6 = [cos(thet5) -sin(thet5) 0 0;
     sin(thet5) cos(thet5) 0 0;
     0 0 1 d5;
     0 0 0 1] 
     
     
Ei33= [1 0 0;
       0 1 0;
       0 0 1]


T01 = simplify(J1)
T02 = simplify(J1*J2)
T03 = simplify(J1*J2*J3*J34)
T04 = simplify(J1*J2*J3*J34*J4)
T05 = simplify(J1*J2*J3*J34*J4*J5)
T36 = simplify(J4*J5*J6)
T06 = simplify(T03*T36)
R06 = T06(1:3,1:3)
R01 = simplify(T01(1:3,1:3))
R02 = simplify(T02(1:3,1:3))
R03 = simplify(T03(1:3,1:3))
R04 = simplify(T04(1:3,1:3))
R05 = simplify(T05(1:3,1:3))

R00K = eye(3)*K
R01K = R01*K
R02K = R02*K
R03K = R03*K
R04K = R04*K
R05K = R05*K
D06 = T06(1:3,4)
D05 = T05(1:3,4)
D04 = T04(1:3,4)
D03 = T03(1:3,4)
D02 = T02(1:3,4)
D01 = T01(1:3,4)
D00 = [0;
       0;
       0]
syms xdel ydel zdel rolldel pitchdel yawdel thetdel3 thetdel4 thetdel5

out = T03(:,4:4) % Extract columns 3 and 4 only into a new 2D array.
x=out(1,:)
y=out(2,:)
z=out(3,:)

x=simplify(x)
y=simplify(y)
z=simplify(z)

nuta=acos(R06(3,3))
spin=simplify(atan2(R06(3,2),-R06(3,1)))
preci=simplify(atan2(R06(2,3),R06(1,3)))
            
w=[R00K R01K R02K R03K R04K R05K]

v=[cross(R00K,D06-D00) cross(R01K,D06-D01) cross(R02K,D06-D02) cross(R03K,D06-D03) cross(R04K,D06-D04) cross(R05K,D06-D05)]

J=[v;
   w]

jinv=inv(J)

thetdel=jinv*[xdel; ydel; zdel; rolldel; pitchdel; yawdel]
thetdel0=simplify(thetdel(1,:))
thetdel1=simplify(thetdel(2,:))
thetdel2=simplify(thetdel(3,:))
thetdel3=simplify(thetdel(4,:))
thetdel4=simplify(thetdel(5,:))
thetdel5=simplify(thetdel(6,:))