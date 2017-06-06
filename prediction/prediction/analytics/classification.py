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