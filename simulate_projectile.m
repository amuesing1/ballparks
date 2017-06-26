function [y,ie]=simulate_projectile(vx0,vy0,wall_dis,wall_h,alt)
% Set simulation options
options = odeset('Events',@event_checker,'RelTol', 1e-8);
tspan = [0 1e2];
y_init = [vx0; vy0; 0; 0.9144; wall_dis; wall_h];

[~,y,~,~,ie] = ode45(@(t,y)RHS(t,y,wall_dis,wall_h,alt),tspan,y_init,options);
end