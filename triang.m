function [y x] = triangular(start,stop,step,a,b,c)
x=[start:step:stop];
c=c+1;
y=[];
    for d=1:length(x)
        if (x(d)<a)
            y(d)=0;
        elseif ((a<=x(d)) && (x(d)<b))
            y(d)=(x(d)-a)/(b-a);
        elseif ((b<=x(d)) && (x(d)<c))
            y(d)=(c-x(d))/(c-b);
        elseif (x(d)>=c)
            y(d)=0;
        end
    end
end
