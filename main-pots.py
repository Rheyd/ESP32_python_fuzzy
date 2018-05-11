import builtins,os,time
from machine import Pin,PWM,ADC
#definition for th inputs of the system
temperatura=ADC(Pin(34))
humedad=ADC(Pin(35))
#definition for the output of the system
out=PWM(Pin(32))
out.freq(1000)
out.duty(0);
#define the functinos to use in the program
#max function for use with vectors
def maxvec(one,two):
    output=[];
    for a in range(0,len(one)):
        if(one[a]<two[a]):
            output.extend([two[a]]);
        else:
            output.extend([one[a]]);
    return output;
#triangular function
def triang( ini,fin,a,b,c ):
    axis=[]
    for d in range(ini,fin):
        axis.extend([d]);
    vector=[]
    c=c+1;
    for e in range(0,len(axis)):
        if axis[e]<a:
            vector.extend([0]);
        elif a<=axis[e] and axis[e]<b:
            vector.extend([(axis[e]-a)/(b-a)]);
        elif b<=axis[e] and axis[e]<=c:
            vector.extend([(c-axis[e])/(c-b)]);
        elif axis[e]>c:
            vector.extend([0]);
    return vector
#bell fucntion
def bell( ini,fin,a,b,c ):
    axis=[]
    for d in range(ini,fin):
        axis.extend([d]);
    vector=[]
    for e in range(0,len(axis)):
        vector.extend([1/(1+abs((pow(((axis[e]-c)/a),2*b))))]);
    return vector
#centroid
def centroid(vector):
    k=0;
    g=0;
    for a in range(0,len(vector)):
        k=k+(vector[a])
        g=g+((vector[a])*a)
    return (g/k)

while(1):
    #star of the main program
    xh=[];#x axis in humidity
    xt=[];#x axis in temperature
    xo=[];#x axis in the air flow
    for b in range(60,101):
        xh.extend([b]);
    for b in range(10,31):
        xt.extend([b]);
    for b in range(0,101):
        xo.extend([b]);
    #creation of empty vector for the MF
    tb=[];#empty vector of low temperature
    tm=[];#empty vector of mid temperature
    ta=[];#empty vector of high temperature
    hb=[];#empty vector of low humidity
    hm=[];#empty vector of mid humidity
    ha=[];#empty vector of high humidity
    fb=[];#empty vector of low flow
    fm=[];#empty vector of mid flow
    fa=[];#empty vector of high flow
    #creation of the MF
    #temperature functions
    tb=bell(10,31,8,4,10);
    tm=triang(10,31,20,22,24);
    ta=bell(10,31,8,4,30);
    #humidity functions
    hb=triang(60,101,60,60,75);
    hm=triang(60,101,65,80,95);
    ha=triang(60,101,85,100,100);
    #output functions
    fb=triang(0,101,0,0,30);
    fm=bell(0,101,20,3.5,50);
    fa=triang(0,101,70,100,100);
    #ask for user input
    #the read is between 0 and 4095
    a=int(humedad.read()/102);
    b=int(temperatura.read()/204);
    #evaluate the functions
    lowflow= max(min(hb[a],tb[b]),min(hb[a],tm[b]),min(hm[a],tb[b]),min(hm[a],tm[b]));
    midflow= max(min(ha[a],tb[b]),min(ha[a],tm[b]));
    highflow=max(min(hb[a],ta[b]),min(hm[a],ta[b]),min(ha[a],ta[b]));
    #
    lowcut=[];#empty vector of low cutline
    midcut=[];#empty vector of mid cutline
    highcut=[];#empty vector of high cutline
    #
    for a in range(0,len(fb)):
        if(fb[a]<lowflow):
            lowcut.extend([fb[a]]);
        else:
            lowcut.extend([lowflow]);
    for a in range(0,len(fm)):
        if(fm[a]<midflow):
            midcut.extend([fm[a]]);
        else:
            midcut.extend([midflow]);
    for a in range(0,len(fa)):
        if(fa[a]<highflow):
            highcut.extend([fa[a]]);
        else:
            highcut.extend([highflow]);
    f=centroid(maxvec(maxvec(lowcut,midcut),highcut));
    print(f);
    print(int(f));
    time.sleep_ms(500)
    out.duty(int((int(f)*10.23)))
