
syms  thet0 thet1 thet2  B CB CH HL

%alpn rn dn thetn
%B=0.19
%CD=0.03
%CH=0.2
%HL=0.2
 
DH = [cos(thet0) 0 -sin(thet0) CB*cos(thet0);
     sin(thet0) 0 cos(thet0) CB*sin(thet0);
     0 -1 0 B;
     0 0 0 1]

A =  [cos(thet1) -sin(thet1) 0 CH*cos(thet1);
     sin(thet1) cos(thet1) 0 CH*sin(thet1);
     0 0 1 0;
     0 0 0 1]
B =  [cos(thet2+pi/2) -sin(thet2+pi/2) 0 HL*cos(thet2+pi/2);
     sin(thet2+pi/2) cos(thet2+pi/2) 0 HL*sin(thet2+pi/2);
     0 0 1 0;
     0 0 0 1]
     
C = DH*A*B

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
