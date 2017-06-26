function [value,isterminal,direction] = event_checker(~,y)

value(1)=5;
value(2)=5;
% Detect height = 0
if y(3)>=y(5)
    value(1)=y(4);
elseif y(3)<y(5) && y(2)<0
    value(2)=y(4)-y(6);
end

% Stop the integration
isterminal(1) = 1;
isterminal(2) = 1;

% Negative direction only
direction(1) = -1;
direction(2) = -1;