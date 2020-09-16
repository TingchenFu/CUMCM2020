function  f  = fun(x)
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
sum=0;
global data
for i=1:123
    money=x(i);
    rate=x(i+123);
    if data(i)==1
        sum=sum+money*rate*(76.41*rate*rate-21.98*rate+1.85);
    end
    if data(i)==2
        sum=sum+money*(67.93*rate*rate-20.21*rate+1.83)*(-0.0263+0.9737*rate);
    end
    if data(i)==3
        sum=sum+money*(63.94*rate*rate-19.57*rate+1.82)*(-0.0588+0.9412*rate);
    end
    

end
f=-sum;


