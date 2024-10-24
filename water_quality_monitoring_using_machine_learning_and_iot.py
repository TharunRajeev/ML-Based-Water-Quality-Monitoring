import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

"""# Data Selection"""

#Load Data

path="/content/water_potability.csv"
df=pd.read_csv(path)
df.head(10)

df.shape

df.info()

df.describe()

df.dtypes

cols=list(df.columns.values)
cols

"""# Data Visualization"""

sns.pairplot(df,hue = 'Quality')

corrmat = df.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map
g=sns.heatmap(df[top_corr_features].corr(),annot=True,cmap="RdYlGn")

data = df.corr()    # Pairwise correlation with a null value is ignored
# Generate heat map using seaborn
fig, ax = plt.subplots(figsize=(12,8))                          # Create grid of empty subplots using matplotlib library                      
mask = np.triu(np.ones_like(data, dtype=bool))                   # Mask correlation matrix along its line of symmetry to remove redencency and correlation of a feature with itself
sns.heatmap(data, cmap='seismic', annot=True, mask=mask, ax=ax, vmin=-0.2, vmax=0.2)    # Create heat map useing seaborn library
fig.text(0.5, 1.05, 'Correlation Heat Map', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight='bold', transform=ax.transAxes)   # Add title
sns.set_style('white')

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,8))

ax1.hist(df["ph"])
ax1.set_xlabel("ph",fontsize=32)
ax2.hist(df["Hardness"])
ax2.set_xlabel("Hardness(mg/L)",fontsize=32)
ax3.hist(df["Solids"])
ax3.set_xlabel("TDS(ppm)",fontsize=32)
ax4.hist(df["Chloramines"])
ax4.set_xlabel("Chloramine(ppm)",fontsize=32)
plt.tight_layout()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,8))

ax1.hist(df["Sulfate"])
ax1.set_xlabel("Sulfates(mg/L)",fontsize=32)
ax2.hist(df["Conductivity"])
ax2.set_xlabel("Conductivity(uS/cm)",fontsize=32)
ax3.hist(df["Organic_carbon"])
ax3.set_xlabel("TOC(ppm)",fontsize=32)
ax4.hist(df["Trihalomethanes"])
ax4.set_xlabel("Trihalomethanes(ug/L)",fontsize=32)
plt.tight_layout()

sns.heatmap(df.isnull(),cmap="viridis")
plt.gcf().set_size_inches(12,6)

fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(20,10))  # Create empty grid of subplots
fig.subplots_adjust(hspace=.5)                       # Adjust vertical/height spacing 

# Fill each subplot with the distribution of a feature separated by potability
a=0                               # Increment subplot coordinates
for feature in df.drop('Quality', axis=1):    # Iterate through features ('Potability' is a label) 
  df.boxplot(by='Quality', column=[feature], ax=axes[ a%2, a%5 ], grid=False)    # Create boxplots for each feature grouped by potable or not (df.boxplot() auto handles nan correctly). Subplot coordinates [a%2, a%5] start top left and vertically zig zag moving right.
  a+=1

axes[1,4].remove()        # Remove unnecessary subplot from 2x5 grid
plt.show()

"""# Data Cleaning

"""

df.corr()

missing={"missing":df.isnull().sum()," % of missing":round(((df.isnull().sum()/df.shape[0])*100),2)}
pd.DataFrame(missing)

print("number of rows: ", df.shape[0])
print("number of column: ", df.shape[1])
df.Quality.value_counts()
df_notpotable  = df[df['Quality']==0]
df_potable = df[df['Quality']==1] 
df_notpotable.isnull().sum()
df_potable.isnull().sum()

from sklearn.impute import SimpleImputer

impute = SimpleImputer(missing_values=np.nan, strategy = 'mean')

#for df_notpotable
impute.fit(df_notpotable[['ph']])
impute.fit(df_notpotable[['Sulfate']])
impute.fit(df_notpotable[['Trihalomethanes']])
df_notpotable['ph'] = impute.transform(df_notpotable[['ph']])
df_notpotable['Sulfate'] = impute.transform(df_notpotable[['Sulfate']])
df_notpotable['Trihalomethanes'] = impute.transform(df_notpotable[['Trihalomethanes']])

#for df_potable
impute.fit(df_potable[['ph']])
impute.fit(df_potable[['Sulfate']])
impute.fit(df_potable[['Trihalomethanes']])

df_potable['ph'] = impute.transform(df_potable[['ph']])
df_potable['Sulfate'] = impute.transform(df_potable[['Sulfate']])
df_potable['Trihalomethanes'] = impute.transform(df_potable[['Trihalomethanes']])

df_notpotable.isnull().sum()
df.Quality.value_counts()
df = pd.concat([df_notpotable, df_potable])

df.isnull().sum()

Potability=df["Quality"].value_counts()
Potability

plt.pie(Potability,labels=["Non-potable","potable"],startangle=90,explode=[0.3,0])
plt.show()

"""# Data Spliting

"""

df = df.sample(frac = 1)

y=df['Quality']

X=df.drop(['Quality'], axis=1)

# Feature Importance
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
model = ExtraTreesClassifier()
model.fit(X,y)

select=model.feature_importances_
print(select)

feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.plot(kind='barh')
plt.show()

# Train test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import MinMaxScaler
#Now, lets scale all the value in x within 0 to 1...
scaler = MinMaxScaler() # creating object of MinMaxScaler
scaler.fit(X)
X = scaler.transform(X)
X= pd.DataFrame(X)
X

"""# Model Selection

"""

df.hist(bins=10, figsize=(20,15), color = 'teal')

#Create a function within many Machine Learning Models
def models(X_train,Y_train):
  
  #Using Logistic Regression Algorithm to the Training Set
  from sklearn.linear_model import LogisticRegression
  log = LogisticRegression(random_state = 0)
  log.fit(X_train, Y_train)
  
  #Using KNeighborsClassifier Method of neighbors class to use Nearest Neighbor algorithm
  from sklearn.neighbors import KNeighborsClassifier
  knn = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
  knn.fit(X_train, Y_train)

  #Using SVC method of svm class to use Support Vector Machine Algorithm
  from sklearn.svm import SVC
  svc_lin = SVC(kernel = 'linear', random_state = 0)
  svc_lin.fit(X_train, Y_train)

  #Using SVC method of svm class to use Kernel SVM Algorithm
  from sklearn.svm import SVC
  svc_rbf = SVC(kernel = 'rbf', random_state = 0)
  svc_rbf.fit(X_train, Y_train)

  #Using GaussianNB method of naïve_bayes class to use Naïve Bayes Algorithm
  from sklearn.naive_bayes import GaussianNB
  gauss = GaussianNB()
  gauss.fit(X_train, Y_train)

  #Using DecisionTreeClassifier of tree class to use Decision Tree Algorithm
  from sklearn.tree import DecisionTreeClassifier
  tree = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
  tree.fit(X_train, Y_train)

  #Using RandomForestClassifier method of ensemble class to use Random Forest Classification algorithm
  from sklearn.ensemble import RandomForestClassifier
  forest = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
  forest.fit(X_train, Y_train)
  
  #print model accuracy on the training data.
  print('[0]Logistic Regression Training Accuracy:', log.score(X_train, Y_train))
  print('[1]K Nearest Neighbor Training Accuracy:', knn.score(X_train, Y_train))
  print('[2]Support Vector Machine (Linear Classifier) Training Accuracy:', svc_lin.score(X_train, Y_train))
  print('[3]Support Vector Machine (RBF Classifier) Training Accuracy:', svc_rbf.score(X_train, Y_train))
  print('[4]Gaussian Naive Bayes Training Accuracy:', gauss.score(X_train, Y_train))
  print('[5]Decision Tree Classifier Training Accuracy:', tree.score(X_train, Y_train))
  print('[6]Random Forest Classifier Training Accuracy:', forest.score(X_train, Y_train))
  
  return log, knn, svc_lin, svc_rbf, gauss, tree, forest

model = models(X_train,y_train)

"""# Model Evalution"""

from sklearn.metrics import confusion_matrix 
for i in range(len(model)):
   cm = confusion_matrix(y_test, model[i].predict(X_test)) 
   #extracting TN, FP, FN, TP
   TN, FP, FN, TP = confusion_matrix(y_test, model[i].predict(X_test)).ravel()
   print(cm)
   print('Model[{}] Testing Accuracy = "{} !"'.format(i,  (TP + TN) / (TP + TN + FN + FP)))
   print()# Print a new line