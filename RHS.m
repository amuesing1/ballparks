function f = RHS(t,y,wall_dis,wall_h,alt)

% Density
% rho = 1.275;
m=0.148835; %kg
r=0.037; %m
CD=0.3; %NASA's CD of a baseball
[~,~,~,rho]=atmoscoesa(alt*0.3048);

% Surface Area
A = pi*r^2;

% Gravitational Coefficient
g = -9.81;

% Velocity
vel_x = y(1);
vel_y = y(2);

% Drag
D = 0.5*CD*rho*(vel_x^2+vel_y^2)*A;

% Angle of velocity
theta = atan2(vel_y,vel_x);

% RHS vector
f(1,1) = -D*cos(theta)/m;
f(2,1) = -D*sin(theta)/m+g;
f(3,1) = vel_x;
f(4,1) = vel_y;
f(5,1) = 0;
f(6,1) = 0;
end