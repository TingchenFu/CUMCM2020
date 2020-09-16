def process(filename,sheetname):
    data=pd.read_excel(filename,sheet_name=sheetname)
    data.columns=['企业代号','发票号码','开票日期','单位代号','金额','税额','价税合计','发票状态']
    if data.loc[1,'企业代号']!=1:
        data['企业代号']=data['企业代号']-123#企业代号为了方便，转化为数字
    invalidindex=[]
    n=data['企业代号'].max()+1
    print(n)
    invalid=[0]*n
    for i in range(len(data)):
        if data.loc[i,'发票状态']=='作废发票':
            invalidindex.append(i)#记录作废发票在记录之中的下标，将相应的记录去掉
    data=data.drop(index=invalidindex)
    data.index=list(range(len(data)))
    group=data.groupby('企业代号')
    
    minus=[0]*n
    minus_index=[]
    depart_index=[]
    for i in range(len(data)):
        if data.loc[i,'价税合计']<0:
            minus[data.loc[i,'企业代号']]+=data.loc[i,'价税合计']
            minus_index.append(i)# 记录负数发票的下标
    minus_ratio=[0]*n
    for i in range(1,n):
        minus_ratio[i]=abs(minus[i])/group.get_group(i)['价税合计'].sum()# 计算负数发票的比重
    return data,minus_ratio