function  f  = fun2(x)
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
sum=0;
global data
for i=1:302
    money=x(i);
    rate=x(i+302);
    if data(i)==1
        sum=sum+money*rate*(71.41*rate*rate-21.98*rate+1.6971);
    end
    if data(i)==2
        sum=sum+money*(62.93*rate*rate-20.21*rate+1.6504)*(-0.0263+0.9737*rate);
    end
    if data(i)==3
        sum=sum+money*(64.94*rate*rate-19.57*rate+1.3393)*(-0.0588+0.9412*rate);
    end
end
f=-sum;

