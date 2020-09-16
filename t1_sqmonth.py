#问题预处理
buy,buy_minus_ratio=process('E:\\2020CUMCM\\CUMCM2020Probelms\\C\\data1.xlsx','进项发票信息')
sell,sell_minus_ratio=process('E:\\2020CUMCM\\CUMCM2020Probelms\\C\\data1.xlsx','销项发票信息')

#计算所有企业每一天的的净值序列
# 每一个月取其月中位数作为这一个月净值时间序列数据
buy['tag']=-1*buy['价税合计']#调整符号
sell['tag']=sell['价税合计']
sq_month=[[0]]#每一个元素都是一家企业的月净值信息
for j in range(1,124):
    sq_month.append([0])
    flow=pd.concat([buy[buy['企业代号']==j],sell[sell['企业代号']==j]],axis=0)#整合销方发票和买方发票信息
    flow=flow.sort_values(by=['开票日期'],ascending=True)#按照日期前后进行排序
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
            if day in list(flow['开票日期']):#当日有交易
                change.append(change[-1]+flow.loc[flow['开票日期']==day,'tag'].sum())#记录当日交易给净值带来的变化
            else:
                change.append(change[-1])
    sq_month[j].append(np.median(change)+agg)

#存储月净值序列数据
store=pd.DataFrame(sq_month).T
wb=Workbook()
ws=wb.active
ws.append(list(range(124)))
for i in range(len(store)):
    line=list(store.loc[i])
    ws.append(line)
wb.save('sq_month.xlsx')

# 记录每一家企业交易记录所在的月份
month=[[0]]
for j in range(1,124):
    month.append([0])
    flow=pd.concat([buy[buy['企业代号']==j],sell[sell['企业代号']==j]],axis=0)#整合销方发票和买方发票信息
    flow=flow.sort_values(by=['开票日期'],ascending=True)#按照日期前后进行排序
    flow['开票日期']=pd.to_datetime(flow['开票日期'])
    begin = flow['开票日期'].min()
    end = flow['开票日期'].max()
    lastmonth=0
    agg=0
    change=[0]
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        if day.__getattribute__('month')!=lastmonth:#进入一个新月份
            month[j].append(str(day.__getattribute__('year'))+'-'+str(day.__getattribute__('month')))#记录新月份
            lastmonth=day.__getattribute__('month')
    month[j].append(str(day.__getattribute__('year'))+'-'+str(day.__getattribute__('month')))

#存储月份信息
store=pd.DataFrame(month).T
wb=Workbook()
ws=wb.active
ws.append(list(range(124)))
for i in range(len(store)):
    line=list(store.loc[i])
    ws.append(line)
wb.save('month.xlsx')
