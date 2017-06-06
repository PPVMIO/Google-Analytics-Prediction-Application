import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from time import time
from scipy.stats import randint as sp_randint
from collections import defaultdict
from random import randint


print('HI HI HI HI HI HI HI HI HI HI HI')


def check_wd():
    import os
    cwd = os.getcwd()
    text_file = open('cwd.txt', 'w')
    text_file.write(cwd)
    text_file.close()
    
def export_text(txt_name, txt_data):
    text_file = open(txt_name, 'w')
    text_file.write(txt_data)
    text_file.close()
    
def export_dict(txt_name, dictionary):
    txt_data = ''
    for k, v in dictionary.items():
        txt_data = txt_data + str(k) + '\t' + str(v) + '\n'       
    export_text(txt_name, txt_data)
    
#   Build random forest and optimize the classifier
#   Return the best fit classifier
def build_model(dimensions, categorical, metrics, date_range):
    start = time()
    dimensions_edit = [x for x in dimensions if x != 'ga:nthMinute']
    ### READ IN DATA
    df = pd.read_csv('analytics_data/exported_data.csv', sep='|', error_bad_lines=False)
    
    multi_bounce_flag = df['ga:bounces'] > 1
    df.loc[multi_bounce_flag, 'ga:bounces'] = 1  
    dimension_names = dimensions_edit + categorical
    categorical_names = categorical
    X = df[dimension_names]
    y = df['ga:bounces']
    for var in categorical_names:
        dummies = pd.get_dummies(X[var], prefix=var)
        X = pd.concat([X, dummies], axis=1)
        X.drop([var], axis=1, inplace=True)
    ### BUILD MODEL
    random_num = randint(0, 4294967295)
    org_clf = RandomForestClassifier(oob_score=True, random_state=42)
    org_clf.fit(X, y)
    ### HYPER PARAMETER RANDOM SEARCH
    param_dist = {"n_estimators": sp_randint (50, 100),
              "max_features": sp_randint(1, len(dimensions)),
              "min_samples_split": sp_randint(2, 20),
              "min_samples_leaf": sp_randint(1, 20)}
    
    n_iter_search = 20
    random_search = RandomizedSearchCV(org_clf, param_distributions=param_dist,
                                   n_iter=n_iter_search)
    
    random_search.fit(X, y)
    #X.to_csv('X_var.csv', sep='|')
    

    best_params = random_search.best_params_
    opt_clf = random_search.best_estimator_
    dummy_dimensions = list(X.columns.values)
    time_taken = (time() - start)
    start_date = date_range[0]
    end_date = date_range[1]
    all_dim_names = dimensions + categorical
    total_bounces = len(df[df['ga:bounces'] == 1])
    data_points = len(df)
    org_oob = org_clf.oob_score_
    opt_oob = opt_clf.oob_score_

    
    
    importance_df = pd.concat((pd.DataFrame(X.iloc[:, 1:].columns, columns = ['variable']), 
           pd.DataFrame(opt_clf.feature_importances_, columns = ['importance'])), 
          axis = 1).sort_values(by='importance', ascending = False)
    
    org_combined_features_series, org_feature_name_dict= combined_feature_importances(org_clf, X.iloc[:, 1:].columns, categorical)
    opt_combined_features_series, opt_feature_name_dict = combined_feature_importances(opt_clf, X.iloc[:, 1:].columns, categorical)

    
    output_data_json = {
        "timeTaken": time_taken,
        "originalData":{
            "dateRange":{
                "startDate": start_date,
                "endDate": end_date,
            },
            "dimensionData":{
                "dimensionNames": all_dim_names,
                "dummyDimensions": dummy_dimensions
            },
            "metricData":{
                "metricNames": metrics
            },
            "totalBounces": total_bounces,
            "dataPoints": data_points,
        },
        "modelData":{
            "OOB": org_oob,
            "optimizedOOB": opt_oob,
            "params": {
                "random_state": random_num,
                "n_estimators": best_params['n_estimators'],
                "max_features": best_params['max_features'],
                "min_samples_split": best_params['min_samples_split'],
                "min_samples_leaf": best_params['min_samples_leaf']
            }
            
        },
        
        "featureInfo":{
            "optFeatureNameDict": opt_feature_name_dict,
            "orgFeatureNameDict": org_feature_name_dict,
            "featureImportanceNames": importance_df["variable"].fillna("NA"),
            "featureImportance": importance_df["importance"],
            "optCombinedFeatureImportanceNames": opt_combined_features_series.index.tolist(),
            "orgCombinedFeatureImportanceNames": org_combined_features_series.index.tolist(),
            "optCombinedFeatureImportance": opt_combined_features_series.values.tolist(),
            "orgCombinedFeatureImportance": org_combined_features_series.values.tolist()
            
            
        }
    }
    
    return output_data_json, opt_clf
def combined_feature_importances(model, feature_names, summarized_columns=None):    
    
    combined_feature_dict=dict(zip(feature_names, model.feature_importances_))
    feature_name_dict = defaultdict(list)
    if summarized_columns: 
        for col_name in summarized_columns: 
            feature_name_dict[col_name] = [i.replace(col_name + '_', '') for i in combined_feature_dict.keys() if col_name in i]

            sum_value = sum(x for i, x in combined_feature_dict.items() if col_name in i )  
            keys_to_remove = [i for i in combined_feature_dict.keys() if col_name in i ]
            for i in keys_to_remove:
                combined_feature_dict.pop(i)
            combined_feature_dict[col_name] = sum_value
    combined_feature_series = pd.Series(combined_feature_dict)
    #feature_name_series = pd.Series(feature_name_dict)
    
    return [combined_feature_series, feature_name_dict]
 
                