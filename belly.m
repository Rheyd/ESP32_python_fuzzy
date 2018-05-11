function [y x] = trap(start,stop,step,a,b,c)
y=[];
x=[start:step:stop];
    for d=1:length(x)
        y(d)=1/(1+abs((((x(d)-c)/a)^(2*b))));
    end
end