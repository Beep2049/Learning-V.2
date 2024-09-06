import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn import metrics

import warnings
warnings.filterwarnings('ignore')

# Importing the dataset
df = pd.read_csv(r"C:\Users\ebello\OneDrive - United Against Poverty\Desktop\D.A.P\AAPL.csv")
print(df.head())
#
print(df.shape)
#
print(df.describe())
#
print(df.info())

# Exploratory Data Analysis
plt.figure(figure=(15,5))
plt.plot(df['Close'])
plt.title('Apple Close Price.', fontsize=15)
plt.ylabel('Price in dollars.')
plt.show()
#
df.head()
#
df.isnull().sum()

# Distribution Plot
features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

#
plt.subplots(figsize=(20,10))

for i, col in enumerate(features):
  plt.subplot(2,3,i+1)
  sb.histplot(df[col], kde=True, stat='density')
plt.show()

# Boxplot
plt.subplots(figsize=(20,10))
for i, col in enumerate(features):
  plt.subplot(2,3, i+1)
  sb.boxplot(df[col], orient='h')
plt.show()

# Feature Engineering
splitted = df['Date'].str.split('/' , expand=True)
#
df['day'] = splitted[1].astype('int')
df['month'] = splitted[0].astype('int')
df['year'] = splitted[2].astype('int')
#
df.head()

# Quarter end
df['is_quarter_end'] = np.where(df['month']%3==0, 1, 0)
df.head()
#
data_grouped = df.groupby('year').mean(numeric_only=True)
plt.subplots(figsize=(20,10))
#
for i, col in enumerate(['Open', 'High', 'Low', 'Close']):
  plt.subplot(2,2, i+1)
  data_grouped[col].plot.bar()
plt.show()
#
df.groupby('is_quarter_end').mean(numeric_only=True)
#
df['open-close'] = df['Open'] - df['Close']
df['low-high'] = df['Low'] - df['High']
df['target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)

# Pie Chart
plt.pie(df['target'].value_counts().values, labels=[0, 1], autopct='%1.1f%%')
plt.show()

# Heatmap 
plt.figure(figsize=(10,10))
sb.heatmap(df.corr(numeric_only=True) > 0.9, annot=True, cbar=False)
plt.show()
#
features = df[['open-close', 'low-high', 'is_quarter_end']]
target = df['target']
#
scaler = StandardScaler()
features = scaler.fit_transform(features)
#
X_train, X_valid, Y_train, Y_valid = train_test_split(
    features, target, test_size=0.1, random_state=2022)
print(X_train.shape, X_valid.shape)

models =[LogisticRegression(), SVC(
    kernel='poly', probability=True), XGBClassifier()]
#
for i in range(3): 
  models[i].fit(X_train, Y_train) 
  
  print(f'{models[i]} : ') 
  print('Training Accuracy : ', metrics.roc_auc_score( 
    Y_train, models[i].predict_proba(X_train)[:,1])) 
  print('Validation Accuracy : ', metrics.roc_auc_score( 
    Y_valid, models[i].predict_proba(X_valid)[:,1])) 
  print()
#
  metrics.ConfusionMatrixDisplay.from_estimator(models[0], X_valid, Y_valid) 
plt.show()