import sklearn
from sklearn import svm
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import recall_score,precision_score,accuracy_score
# 进行数据预处理
x,y=np.split(svmdata,indices_or_sections=(6,),axis=1) #x为数据，y为标签
x['skew']=x['skew'].fillna(0)
x['kurt']=x['kurt'].fillna(0)#峰度和偏度的缺失值全部填充为0
x['cv']=np.abs(x['cv'])
x['cv']=(x['cv']-np.min(x['cv']))/(np.max(x['cv'])-np.min(x['cv']))
#x['flow']=(x['flow']-np.min(x['flow']))/(np.max(x['flow'])-np.min(x['flow']))
#x=x.drop(columns=['cv'])
x['median']=(x['median']-np.min(x['median']))/(np.max(x['median'])-np.min(x['median']))#数据归一化操作
#x=x.drop(columns=['median'])
x['loss']=(x['loss']-np.min(x['loss']))/(np.max(x['loss'])-np.min(x['loss']))
x=x.drop(columns=['loss'])
x['minus']=(x['minus']-np.min(x['minus']))/(np.max(x['minus'])-np.min(x['minus']))
#x=x.drop(columns=['minus'])
x['skew']=(x['skew']-np.min(x['skew']))/(np.max(x['skew'])-np.min(x['skew']))
#x=x.drop(columns=['skew'])
x['kurt']=(x['kurt']-np.min(x['kurt']))/(np.max(x['kurt'])-np.min(x['kurt']))
#分割训练集和测试集
train_data,test_data,train_label,test_label =sklearn.model_selection.train_test_split(x,y, random_state=1, train_size=0.7,test_size=0.3)


#尝试使用SVM进行拟合
classifier=svm.SVC(C=2,kernel='rbf') 
classifier.fit(train_data,train_label) #SVM拟合
pred_label=classifier.predict(test_data)#SVM预测
print(recall_score(test_label,pred_label,average='micro'))
print(precision_score(test_label,pred_label,average='micro'))

#Adaboost尝试进行拟合
from sklearn.ensemble import AdaBoostClassifier
from sklearn import metrics
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=10, min_samples_split=5, min_samples_leaf=5),
                         algorithm="SAMME",
                         n_estimators=250, learning_rate=0.20)#设置Adaboost分类器
bdt.fit(train_data, train_label)
pred_label=bdt.predict(test_data)
print(accuracy_score(test_label,pred_label))
print(recall_score(test_label,pred_label,average='micro'))
print(precision_score(test_label,pred_label,average='micro'))
print(metrics.confusion_matrix(test_label, pred_label, sample_weight=None))#打印混淆矩阵

# 使用PCA对几个因子进行主成因子分析
from sklearn.decomposition import PCA
pca = PCA(n_components=4)
trim= pca.fit(x).transform(x)
print(x.shape)#原始变量维度
print(trim.shape)#主成分变量的维度
trim=pd.DataFrame(trim)
print('各主成分贡献度:{}'.format(pca.explained_variance_ratio_))
train_data,test_data,train_label,test_label =sklearn.model_selection.train_test_split(trim,y,random_state=1, train_size=0.7,test_size=0.3)

#进行了PCA之后重新进行Adaboost拟合
from sklearn.ensemble import AdaBoostClassifier
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=11, min_samples_split=5, min_samples_leaf=10),
                         algorithm="SAMME",
                         n_estimators=150, learning_rate=0.25)
bdt.fit(train_data, train_label)
pred_label=bdt.predict(test_data)
print(accuracy_score(test_label,pred_label))
print(recall_score(test_label,pred_label,average='micro'))
print(precision_score(test_label,pred_label,average='micro'))
final_clf=bdt

