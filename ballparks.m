close all
clear all
clc

data=csvread('ballparks.csv',1,2);
energy_array=zeros(length(data),5);
for i=1:length(data)
    for j=1:5
%         display(i)
%         display(j)
        wall_dis=data(i,j);
        wall_h=data(i,j+5);
        wall_dis=wall_dis*0.3048;
        wall_h=wall_h*0.3048;
        alt=data(i,11);
        % Insert your best guess here.
        x0 = [110 110];
        options=optimset('MaxFunEvals',10000,'MaxIter',5000);
        func=@(y)energy_of_hit(y,wall_dis,wall_h,alt);
        % Call the minimizer function with your initial conditions
        x = fminsearch(func,x0,options);
        m=0.148835; %kg
        energy=0.5*m*(x(1)^2 + x(2)^2);
        theta = atan2(x(2),x(1));
        theta = rad2deg(theta);
        energy_array(i,j)=energy;
        energy_array(i,j+5)=theta;
    end
end
csvwrite('ballparks_stats.csv',energy_array);