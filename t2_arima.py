#该函数接受时间序列数据及其一阶差分作为数据，训练得到ARIMA模型
def arima(sample,dx):
    pmax = int(len(dx) / 10)    #一般阶数不超过 length /10
    qmax = int(len(dx) / 10)
    bic_matrix = []
    for p in range(pmax +1):
        temp= []
        for q in range(qmax+1):
            try:
                temp.append(ARIMA(sample, (p, 1, q)).fit().bic)
            except:
                temp.append(None)
            bic_matrix.append(temp)

    bic_matrix = pd.DataFrame(bic_matrix)   
    p,q = bic_matrix.stack().idxmin()  #找出最小值所在位置
    model = ARIMA(sample, (p,1,q)).fit()#模型拟合
    return list(model.forecast(6)[0])



#使用ARIMA预测未来六个月的公司净值
from statsmodels.tsa.arima_model import ARIMA 
pred=[[0,0,0,0,0,0]]
for i in range(1,303):
    sample=pd.DataFrame(sq_month[i]).dropna()
    dx=sample.diff().dropna()
    sample.columns=['value']
    try:
        one=arima(sample,dx)
    except:
        one=[0,0,0,0,0,0]
    pred.append(one)

from openpyxl import Workbook
wb=Workbook()
ws=wb.active
ws.append(['pred1','pred2','pred3','pred4','pred5','pred6'])
for i in range(len(pred)):
    ws.append(list(pred[i]))
wb.save('pred2.xlsx')

