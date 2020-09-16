#计算峰度和偏度并存储
kurtlist=[0]
for i in range(1,124):
    part_sell=sell.loc[sell['企业代号']==i]
    group=part_sell.groupby('单位代号')##按照买方单位代号进行分组
    kurtlist.append(group['价税合计'].sum().kurt())

skewlist=[0]
for i in range(1,124):
    part_buy=buy.loc[buy['企业代号']==i]
    skewlist.append(part_buy['价税合计'].skew())

wb=Workbook()
ws=wb.active
ws.append(['skew','kurt'])
for i in range(1,124):
    line=[skewlist[i],kurtlist[i]]
    ws.append(line)
wb.save('峰度偏度.xlsx')

#计算负数发票占比，月亏空，供求关系的峰度和偏度
pred=pd.read_excel('pred.xlsx')
month_loss=(pd.read_excel('month_loss.xlsx')).T
svmdata=pred.drop(columns=['pred1','pred2','pred3','pred4','pred5','pred6'])
svmdata['minus']=''
svmdata['loss']=''
svmdata['skew']=''
svmdata['kurt']=''
#svmdata['flow']=''
svmdata['rank']=''
for i in range(123):
    svmdata.loc[i,'minus']=sell_minus_ratio[i+1]
    svmdata.loc[i,'loss']=np.max(month_loss.loc[i+1])
    #svmdata.loc[i,'flow']=sell.loc[sell['企业代号']==i+1,'价税合计'].sum()+buy.loc[buy['企业代号']==i+1,'价税合计'].sum()
sk=pd.read_excel('峰度偏度.xlsx')
svmdata['skew']=sk['skew']
svmdata['kurt']=sk['kurt']
svmdata['rank']=sk['评级']

#将计算结果进行存储
from openpyxl import Workbook
wb=Workbook()
ws=wb.active
ws.append(['median','cv','minus','loss','skew','kurt','rank'])
for i in range(len(svmdata)):
    ws.append(list(svmdata.loc[i]))
wb.save('factor1.xlsx')

