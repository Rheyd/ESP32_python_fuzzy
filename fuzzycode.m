clc;clear all;close all;
val11 = input('ingrese el valor de humedad(60-100)\n');
val22 = input('ingrese el valor de temperatura(10-30)\n');
% paso = input('ingrese el valor del grid para el surface\n');
%humidity MF
[hb,xh]=triang(60,100,1,60,60,75);
hm =triang(60,100,1,65,80,95);
ha =triang(60,100,1,85,100,100);
%ploting the humidity signals
figure;
subplot(2,1,1);
axis([60 100 0 1])
hold on;
plot(xh,hb);
plot(xh,hm);
plot(xh,ha);
title('humidity');
xlabel('x');
ylabel('fuzzy membership');
%temperature MF
[tb,xt]=belly(10,30,1,8,4,10);
tm =triang(10,30,1,20,22,24);
ta =belly(10,30,1,8,4,30);
%ploting the humidity signals
subplot(2,1,2);
axis([10 30 0 1]);
hold on;
plot(xt,tb);
plot(xt,tm);
plot(xt,ta);
title('temperature');
xlabel('x');
ylabel('fuzzy membership');
%air flow MF
[fb,xo]=triang(0,100,1,0,0,30);
fm=belly(0,100,1,20,3.5,50);
fa=triang(0,100,1,70,100,100);
pp=0;
for p=0:1:41
    qq=0;
    for q=0:1:21
        if(q==0 && p==0)
            val1f= val11-59;
            val2f= val22-9;
        end
        if(q~=0 && p~=0)
            val1f=p;
            val2f=q;
        end;  
        %max-min for the flow based on the Inference Table.
        lowflow=max([min(hb(val1f),tb(val2f)),min(hb(val1f),tm(val2f)),min(hm(val1f),tb(val2f)),min(hm(val1f),tm(val2f))]);
        midflow=max([min(ha(val1f),tb(val2f)),min(ha(val1f),tm(val2f))]);
        highflow=max([min(hb(val1f),ta(val2f)),min(hm(val1f),ta(val2f)),min(ha(val1f),ta(val2f))]);
        cutlow=[0:1:100];
        cutmid=[0:1:100];
        cuthig=[0:1:100];
        for f=1:length(xo)
            if(fb(f)<lowflow)
                  cutlow(f)=fb(f);
            else
                  cutlow(f)=lowflow;
            end
        end
        for f=1:length(xo)
            if(fm(f)>midflow)
                  cutmid(f)=midflow;
            elseif(fm(f)<=midflow)
                  cutmid(f)=fm(f);
            end
        end
        for f=1:length(xo)
            if(fa(f)>highflow)
                  cuthig(f)=highflow;
            elseif(fa(f)<=highflow)
                  cuthig(f)=fa(f);
            end
        end 
        
        if(q==0 && p==0)
             finn=max(max(cutlow,cutmid),cuthig);
        end
        if(q~=0 && p~=0)
            Z(qq,pp)=(defuzz(xo,max(max(cutlow,cutmid),cuthig),'centroid'));
        end;        
        qq=qq+1;
    end
    pp=pp+1;
end
figure;
hold on;
plot(xo,fb);
plot(xo,fm);
plot(xo,fa);
plot(xo,finn,'*');
text(50,0.5,strcat('output value=',num2str(defuzz(xo,finn,'centroid'))));
figure;
surf(Z)