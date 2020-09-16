# 计算信用评级影响因子
pred=pd.read_excel('pred2.xlsx')
factor=pred
factor['median']=''
factor['cv']=''
factor['minus']=''
factor['skew']=''
factor['kurt']=''
for i in range(1,303):
    line=pred.loc[i,['pred1','pred2','pred3','pred4','pred5','pred6']]
    #line.columns=['value']
    factor.loc[i,'median']=line.median()
    factor.loc[i,'cv']=np.std(line)/line.mean()
    factor.loc[i,'skew']=buy.loc[buy['企业代号']==i,'价税合计'].skew()
    part_sell=sell.loc[sell['企业代号']==i]
    group=part_sell.groupby('单位代号')
    factor.loc[i,'kurt']=group['价税合计'].sum().kurt()
    factor.loc[i,'minus']=sell_minus_ratio[i]
factor['skew']=factor['skew'].fillna(0)
factor['kurt']=factor['kurt'].fillna(0)#缺失值填充
factor=factor.drop(index=[0])#第一列是为了补齐下标而填充的，应当去掉
factor.index=list(range(len(factor)))
factor=factor.drop(columns=['pred1','pred2','pred3','pred4','pred5','pred6'])