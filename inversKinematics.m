

syms  thet0 thet1 thet2  r1 r2 r0 alp0 d0

%alpn rn dn thetn
alp0=-pi/2

d0=0.19
rn=r0
thetn=thet0
alpn=alp0
dn=d0

Base = [cos(thetn) -sin(thetn)*cos(alpn) sin(thetn)*sin(alpn) rn*cos(thetn);
     sin(thetn) cos(thetn)*cos(alpn) -cos(thetn)*sin(alpn) rn*sin(thetn);
     0 sin(alpn) cos(alpn) dn;
     0 0 0 1]



rn=r0
thetn=thet0
alpn=alp0
dn=d0

A0 = [cos(thet0) 0 -sin(thet0) r0*cos(thet0);
     sin(thet0) 0 cos(thet0) r0*sin(thet0);
     0 -1 0 dn;
     0 0 0 1]

A =  [cos(thet1-pi/2) -sin(thet1-pi/2) 0 r1*cos(thet1-pi/2);
     sin(thet1-pi/2) cos(thet1-pi/2) 0 r1*sin(thet1-pi/2);
     0 0 1 0;
     0 0 0 1]
B =  [cos(thet2+pi/2) -sin(thet2+pi/2) 0 r2*cos(thet2+pi/2);
     sin(thet2+pi/2) cos(thet2+pi/2) 0 r2*sin(thet2+pi/2);
     0 0 1 0;
     0 0 0 1]

C = A0*A*B

out = C(:,4:4) % Extract columns 3 and 4 only into a new 2D array.
x=out(1,:)
y=out(2,:)
z=out(3,:)

x=simplify(x)
y=simplify(y)
z=simplify(z)
%or directly 
%%S = simplify(sin(x)^2 + cos(x)^2)

j=jacobian([x,y,z],[thet0, thet1, thet2])

jinv=adjoint(j)/det(j)

syms xdel ydel zdel

thetdel=jinv*[xdel; ydel; zdel]
thetdel0=simplify(thetdel(1,:))
thetdel1=simplify(thetdel(2,:))
thetdel2=simplify(thetdel(3,:))
