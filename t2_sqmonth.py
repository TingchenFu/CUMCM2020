#导入数据并进行预处理
buy,buy_minus_ratio=process('E:\\2020CUMCM\\CUMCM2020Probelms\\C\\data2.xlsx','进项发票信息')
sell,sell_minus_ratio=process('E:\\2020CUMCM\\CUMCM2020Probelms\\C\\data2.xlsx','销项发票信息')

#计算302家企业每一个月的净值并存储
import datetime
buy['tag']=-1*buy['价税合计']
sell['tag']=sell['价税合计']
sq_month=[[0]]
for j in range(1,303):
    sq_month.append([0])
    flow=pd.concat([buy[buy['企业代号']==j],sell[sell['企业代号']==j]],axis=0)# 将销方发票和买方发票进行整合
    flow=flow.sort_values(by=['开票日期'],ascending=True)#按照日期进行排序
    flow['开票日期']=pd.to_datetime(flow['开票日期'])
    begin = flow['开票日期'].min()
    end = flow['开票日期'].max()
    lastmonth=0
    agg=0
    change=[0]
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        if (day.__getattribute__('month')!=lastmonth) and i:#进入一个新的月份
            sq_month[j].append(np.median(change)+agg)
            agg+=change[-1]
            lastmonth=day.__getattribute__('month')
            change=[0]
            change.append(flow.loc[flow['开票日期']==day,'tag'].sum())
        else:
            if day in list(flow['开票日期']):#当日有交易记录
                change.append(change[-1]+flow.loc[flow['开票日期']==day,'tag'].sum())
            else:
                change.append(change[-1])
    sq_month[j].append(np.median(change)+agg)


store=pd.DataFrame(sq_month).T
from openpyxl import Workbook
wb=Workbook()
ws=wb.active
ws.append(list(range(0,303)))
for i in range(len(store)):
    ws.append(list(store.loc[i]))
wb.save('sq_month2.xlsx')