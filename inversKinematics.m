

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

T03 = simplify(J1*J2*J3*J34)
T36 = simplify(J4*J5*J6)
T06 = simplify(T03*T36)
R06 = T06(1:3,1:3)
R03 = simplify(T03(1:3,1:3))



out = T03(:,4:4) % Extract columns 3 and 4 only into a new 2D array.
x=out(1,:)
y=out(2,:)
z=out(3,:)

x=simplify(x)
y=simplify(y)
z=simplify(z)
%or directly
%%S = simplify(sin(x)^2 + cos(x)^2)

j=jacobian([x,y,z,roll,pitch,yaw],[thet0, thet1, thet2, thet3, thet4, thet5])

jinv=adjoint(j)/det(j)

syms xdel ydel zdel

thetdel=jinv*[xdel; ydel; zdel]
thetdel0=simplify(thetdel(1,:))
thetdel1=simplify(thetdel(2,:))
thetdel2=simplify(thetdel(3,:))
