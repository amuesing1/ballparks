function f = energy_of_hit(x,wall_dis, wall_h, alt)
[~,IE] = simulate_projectile(x(1),x(2),wall_dis, wall_h, alt);
% If IE is 1, the ball cleared the wall
if IE == 1
    scalar = 0;
    
% If IE is 2, the ball did not clear the wall
elseif IE == 2
    scalar = 1E8;

% If IE isn't 1 or 2 something went wrong. Throw out an error.
else
    scalar = 1E8;
%     error('Something wrong with IE')
end

% Find f using scalar and the magnitude of delta V
f = scalar + (x(1)^2 + x(2)^2);
end