def arima(sample,dx):
    pmax = int(len(dx) / 10)    #阶数超过 length /10,预测效果降低
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

#预测123家企业在未来6个月之中的净值
pred=[[0,0,0,0,0,0]]
for i in range(1,124):
    sample=pd.DataFrame(sq_month.loc[i].dropna())
    dx=sample.diff().dropna()
    sample.columns=['value']
    try:
        one=arima(sample,dx)
    except:
        one=[0,0,0,0,0,0]
    pred.append(one)

#计算六个月净值预测值的中位数和变异系数并进行存储
pred['median']=''
pred['cv']=''
for i in range(123):
    line=pred.loc[i,['pred1','pred2','pred3','pred4','pred5','pred6']]
    pred.loc[i,'median']=line.median()
    pred.loc[i,'cv']=np.std(line)/line.mean()
    #pred.loc[i,'minus']=sell_minus_ratio[i+1]

from openpyxl import Workbook
wb=Workbook()
ws=wb.active
ws.append(['pred1','pred2','pred3','pred4','pred5','pred6','median','cv'])
for i in range(123):
    line=list(pred.loc[i])
    ws.append(line)
wb.save('pred.xlsx')



