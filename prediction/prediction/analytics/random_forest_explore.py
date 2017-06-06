# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:18:52 2017

@author: PaulPelayo
"""
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import roc_auc_score



def graph_feature_importances(model, feature_names, autoscale=True, headroom=0.05, width=10, summarized_columns=None):    
    if autoscale:
        x_scale = model.feature_importances_.max()+ headroom
    else:
        x_scale = 1
    
    feature_dict=dict(zip(feature_names, model.feature_importances_))
    
    if summarized_columns: 
        for col_name in summarized_columns: 
            sum_value = sum(x for i, x in feature_dict.items() if col_name in i )  
            keys_to_remove = [i for i in feature_dict.keys() if col_name in i ]
            for i in keys_to_remove:
                feature_dict.pop(i)
            feature_dict[col_name] = sum_value
    results = pd.Series(feature_dict)
    results.sort_values(inplace=True)
    results.plot(kind="barh", figsize=(width,len(results)/4), xlim=(0,x_scale))



### Read in Data and clean (convert categorical to dummy binary variables)
df = pd.read_csv('analytics_data2.csv', sep='|',  index_col=False)
multi_bounce_flag = df['bounce'] > 1
df.loc[multi_bounce_flag, 'bounce'] = 1  
feature_names = ['region', 'source', 'keyword', 'landing', 'hour', 'userType']
categorical_var = ['region', 'source', 'keyword', 'landing', 'userType']
X = df[feature_names]
y = df['bounce']
for var in categorical_var:
    dummies = pd.get_dummies(X[var], prefix=var)
    X = pd.concat([X, dummies], axis=1)
    X.drop([var], axis=1, inplace=True)
    
### Train basic model to get a baseline score
model = RandomForestClassifier(100, oob_score=True, random_state=42)
model.fit(X, y)
print('Baseline Score:', model.oob_score_)

### Look at Importance Featues
importance_df = pd.concat((pd.DataFrame(X.iloc[:, 1:].columns, columns = ['variable']), 
           pd.DataFrame(model.feature_importances_, columns = ['importance'])), 
          axis = 1).sort_values(by='importance', ascending = False)
graph_feature_importances(model, X.columns, summarized_columns=categorical_var)

### Improve by changing n_estimators
"""
results = []
n_estimator_options = [100, 200, 400, 800, 1600, 3200]
for trees in n_estimator_options:
    model = RandomForestClassifier(trees, oob_score=True, n_jobs=-1, random_state=42)
    model.fit(X, y)
    print (trees, "trees")
    print ("OOB: ", model.oob_score_)
    #results.append(roc)
    print ("")
pd.Series(results, n_estimator_options).plot();
"""# results, run with 400 estimators

"""
max_features_options = ["auto", None, "sqrt", "log2", 0.9, 0.2]
for max_features in max_features_options:
    model = RandomForestClassifier(n_estimators=400, oob_score=True, n_jobs=-1, random_state=42, max_features=max_features)
    model.fit(X, y)
    print (max_features, "option")
    print ("OOB: ", model.oob_score_)
    #results.append(roc)
    print ("")
"""# results, run with 0.9 features
    
"""
results = []
min_samples_leaf_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for min_samples in min_samples_leaf_options:
    model = RandomForestClassifier(n_estimators=400, 
                                   oob_score=True, 
                                   n_jobs=-1, 
                                   random_state=42, 
                                   max_features=0.9, 
                                   min_samples_leaf=1)
    model.fit(X, y)
    print (min_samples, "min samples")
    print ("OOB: ", model.oob_score_)
    results.append(roc)
    print ("")
"""# results, run with 8 leaves 

df_test = pd.read_csv('analytics_data3.csv', sep='|',  index_col=False)
X_test = df_test[feature_names]
for var in categorical_var:
    dummies = pd.get_dummies(X_test[var], prefix=var)
    X_test = pd.concat([X_test, dummies], axis=1)
    X_test.drop([var], axis=1, inplace=True)