#进行数据归一化处理
factor['median']=(factor['median']-np.min(factor['median']))/(np.max(factor['median'])-np.min(factor['median']))
factor['cv']=(factor['cv']-np.min(factor['cv']))/(np.max(factor['cv'])-np.min(factor['cv']))
factor['skew']=(factor['skew']-np.min(factor['skew']))/(np.max(factor['skew'])-np.min(factor['skew']))
factor['kurt']=(factor['kurt']-np.min(factor['kurt']))/(np.max(factor['kurt'])-np.min(factor['kurt']))#归一化
factor['minus']=(factor['minus']-np.min(factor['minus']))/(np.max(factor['minus'])-np.min(factor['minus']))

#使用第一问得到的最好的分类器进行预测，并将结果保留
final_clf.fit(x,y)
#factor=factor.drop(columns=['minus'])
rating=final_clf.predict(factor.iloc[:,[0,1,2,3,4]])
factor['rank']=''
factor['rank']=pd.DataFrame(rating)

from openpyxl import Workbook
wb=Workbook()
ws=wb.active
ws.append(['median','cv','skew','kurt','minus','rank'])
for i in range(len(factor)):
    ws.append(list(factor.loc[i]))
wb.save('factor2.xlsx')