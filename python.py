import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
#%matplotlib inline

df = pd.read_csv("C:/Users/Roy/Documents/IDC/practicum/train.csv")
#print(df.head())
func = lambda x: 100*x.count()/df.shape[0]
pivot_df = pd.pivot_table(df,index=["Neighborhood"],values=["SalePrice"],aggfunc=[np.mean,np.median,len,func])
pivot_df['mean'] = pivot_df['mean'].apply(lambda x: round(x,2))
pivot_df["Neighborhood"] = pivot_df.index
pivot_df2 = pd.pivot_table(df,index=["Neighborhood"],values=["SalePrice","YearBuilt"],aggfunc=[np.mean,np.median,len,func])

pivot_df1 = pd.pivot_table(df,index=["Neighborhood"],values=["YearBuilt"],aggfunc=[np.mean,np.median])
pivot_df1['mean'] = pivot_df1['mean'].apply(lambda x: round(x,2))
#result = pivot_df.join(pivot_df1, on='Neighborhood',how='outer')
result = pivot_df.merge(pivot_df1, how='inner', left_index=True,  right_index=True, suffixes=('', '_y'))
flattened = pd.DataFrame(pivot_df2.to_records())

#flattened.drop("('len', 'YearBuilt')", axis=1, inplace=True)
#flattened.drop("('<lambda>', 'SalePrice')", axis=1, inplace=True)
flattened.drop(flattened.columns[[6,7]], axis=1, inplace=True)

#flattened.to_csv("df1.csv", encoding='utf-8', index=False)

flattened.columns = ['Neighborhood', 'SalePrice_Mean', 'YearBuilt_Mean', 'SalePrice_Median', 'YearBuilt_Median', 'Quantity', 'Percentage']

filtered_df = flattened.loc[flattened['Quantity'] > 50]
#result = pivot_df.merge(pivot_df1,how='left',on="Neighborhood")
#df_b = pd.DataFrame(pivot_df., columns = ['Neighborhood', 'Mean', 'Median','Sum','Percent'])
#df = pd.DataFrame(pivot_df, index = ['Neighborhood'])
#df.merge(pivot_df1,how='left',on=None)
#pivot_df1["Neighborhood"] = pivot_df1.index
#print(pivot_df1.head())
#flattened.to_csv("df2.csv", encoding='utf-8', index=False) # save csv to drive
filtered_df.to_csv("df_filtered.csv", encoding='utf-8', index=False) # save csv to drive
#print(flattened.head())
print(filtered_df.head())
print(filtered_df)

#scatter plot grlivarea/saleprice
var = 'GrLivArea'
data = pd.concat([df['SalePrice'], df[var]], axis=1)
data.plot.scatter(x=var, y='SalePrice', ylim=(0,800000));
plt.show()
#box plot overallqual/saleprice
var = 'OverallQual'
data = pd.concat([df['SalePrice'], df[var]], axis=1)
f, ax = plt.subplots(figsize=(8, 6))
fig = sns.boxplot(x=var, y="SalePrice", data=data)
fig.axis(ymin=0, ymax=800000);
plt.show()


#correlation matrix
corrmat = df.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True);
#saleprice correlation matrix
k = 10 #number of variables for heatmap
cols = corrmat.nlargest(k, 'SalePrice')['SalePrice'].index
cm = np.corrcoef(df[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()

#scatterplot
sns.set()
cols = ['SalePrice', 'OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt']
sns.pairplot(df[cols], size = 2.5)
plt.show();
