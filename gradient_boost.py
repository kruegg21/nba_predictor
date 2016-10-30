import xgboost
import numpy as np
import pandas as pd
import time
from helper import add_fantasy_score, timeit
from datetime import datetime
from itertools import product
from read_write import load_pickled_model, dump_pickled_model
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import r2_score
from stat_lists import *
from variance import get_variance
from cross_validation import time_series_cv, cv_method, k_folds_cv

"""
Code to transition from functional architecture to class architecture
"""
# class XGBoostRegressor(object):
#     def __init__(self, num_round = 500, early_stopping_rounds = 50):
#         self.num_round = num_round
#         self.early_stopping_rounds = early_stopping_rounds
#         self.model = None
#
#     def fit(self, X_train, y_train):
#         dtrain = xgboost.DMatrix(X_train, label=y_train, missing = -999)
#         params = {'bst:max_depth':5,
#     			  'bst:eta':0.01,
#     			  'silent':0,
#     			  'gamma':0.5,
#     			  'lambda':0.5,
#     			  'subsample':0.3,
#     			  'colsample_bytree':0.3}
#
#         bst = xgboost.train(params,
#                             dtrain,
#                             num_boost_round = self.num_round)
#         self.model = bst
#
#     def score(self, X_test, y_test):
#         dtest = xgboost.DMatrix(X_test, missing = -999)
#         pred = self.model.predict(dtest,ntree_limit=self.model.best_ntree_limit)
#         return r2_score(y_test, pred)
#
# class XGBoostGridSearchCV(object):
#     def __init__(self, param_grid, verbose = False):
#         self.param_grid = param_grid
#         self.best_score = np.inf
#         self.best_params = {}
#         self.verbose = verbose
#
#     def fit(self, X, y):
#         # Make DMatrix
#         dtrain = xgboost.DMatrix(X, label=y, missing = -999)
#
#         # Grid Search
#         s = sorted(param_grid.items())
#         keys, values = zip(*s)
#         for i in product(*values):
#             params = dict(zip(keys, i))
#             scores = xgboost.cv(params,
#                              dtrain,
#                              num_boost_round = 500,
#                              nfold = data_info.splits,
#                              early_stopping_rounds = 5,
#                              show_progress = True,
#                              show_stdv = True,
#                              seed = 100)
#             score = np.min(scores['test-rmse-mean'])
#             if self.verbose:
#                 print "Scores for parameters {} are {}".format(scores, params)
#             if self.best_score > score:
#                 self.best_score = score
#                 self.best_params = params

def xgboost_preprocessing(df, element, cv):
    # Select only features we need for particualr stat
    df = filter_training_set(df, cv)
    df, remaining_features = select_features(df, element, should_dump = True)

    # Create indepentent and dependent variable arrays
    y_train = df.pop(element).values
    X_train = df.values

    # Create DMatrix
    dtrain = xgboost.DMatrix(X_train,
                             label=y_train,
                             missing = -999,
                             feature_names = df.columns)

    # Add dependent variable back to df
    df[element] = y_train

    return dtrain, df, remaining_features

def grid_search_xgboost(df, element = None, data_info = None, param_grid = None,
                        num_boost_round = 500, early_stopping_rounds = 50,
                        log_results = True):
    """
    Input:
        df -- DataFrame
        element -- string of dependent variable
        data_info -- cv_method object that specifies how to filter dataset
        param_grid -- dictionary of parameters to grid search
        num_boost_round -- int of maximum number of boosting rounds
        early_stopping_rounds -- int specifying number of early stopping rounds
        log_results -- bool indicating whether to log results of grid search
    Output:
        None
    """
    # Processes Data
    dtrain, df, _ = xgboost_preprocessing(df, element, data_info)

    # Grid Search
    best_score = np.inf
    best_params = {}
    best_iteration = num_boost_round

    s = sorted(param_grid.items())
    keys, values = zip(*s)
    for i in product(*values):
        params = dict(zip(keys, i))
        s, i = grid_search_round(params, dtrain,
                                 num_boost_round = num_boost_round,
                                 early_stopping_rounds = early_stopping_rounds)
        if best_score > s:
            best_score = s
            best_params = params
            best_iteration = i

    if log_results:
        log_gradient_boosting_results(df,
                                      best_score,
                                      best_params,
                                      element,
                                      data_info,
                                      param_grid,
                                      best_iteration,
                                      num_boost_round)

@timeit
def grid_search_round(params, dtrain, num_boost_round = 500,
                      early_stopping_rounds = 50):
    """
    Inputs:
        params -- dictionary of parameters
        dtrain -- DMatrix of data to train on
        num_boost_round -- int of number of boosting rounds
        early_stopping_rounds -- int of early stopping rounds
    Output:
        score -- float of best score from round
        iteration -- int of iteration that resulted in best score
    """

    if xgboost.__version__ == '0.6':
        scores = xgboost.cv(params,
                            dtrain,
                            num_boost_round = num_boost_round,
                            nfold = data_info.splits,
                            early_stopping_rounds = early_stopping_rounds,
                            verbose_eval = True,
                            show_stdv = True,
                            seed = 100)
    else:
        scores = xgboost.cv(params,
                            dtrain,
                            num_boost_round = num_boost_round,
                            nfold = data_info.splits,
                            early_stopping_rounds = early_stopping_rounds,
                            show_progress = True,
                            show_stdv = True,
                            seed = 100)

    # Display results
    score = np.min(scores['test-rmse-mean'])
    iteration = scores['test-rmse-mean'].idxmin()
    print "\n\n{}\n{}\n\n".format(scores, params)
    return score, iteration


def train_xgboost(df, element = None, params = None,
                  data_info = None, num_boost_round = 500):
    """
    Input:
    Output:
    """
    dtrain, df, _ = xgboost_preprocessing(df, element, data_info)

    model = xgboost.train(params,
                          dtrain,
                          num_boost_round = num_boost_round)

    # Dump model to pickle
    dump_pickled_model(model, '{}GradientBoostedRegressor'.format(element))

def select_features(df, element, should_dump = True):
    """
    Input:
        df -- merged DataFrame with all features
        element -- string of the form 'PlayerStat'
    Output:
        DataFrame of features we want

    Selects all columns that are involved in predicting a stat. This includes
    all columns with 'Stat' and 'Last' and the features in list
    'basic_features'. Also changes all NaN and Inf to -999 to make the data
    compatible with tree methods.
    """
    if element[:6] == 'Player':
        features_list = get_relevent_columns(df, element) + [element] + basic_features
    else:
        features_list = []
        for stat in main_stat_list_minus_minutes:
            features_list += get_relevent_columns(df, stat)
        features_list += [element]
        features_list += basic_features

    # Get features that are not selected
    remaining_features = df[list(set(df.columns) - set(features_list))]

    # Mark all NaN and Inf as -999
    features = df[features_list].replace([np.inf, np.nan], -999)

    # Dump features to file
    if should_dump:
        features['Player'] = df.Player
        features.to_csv('{}_prediction_data.csv'.format(element), index = False)
        features.drop('Player', axis = 1, inplace=  True)

    # Turn all data to float data type
    for column in features.columns:
        features[column] = features[column].astype(float)

    return features, remaining_features

def get_relevent_columns(df, element):
    """
    Input:
        element -- string of statistic we are getting columns for
    Output:
        list of strings of the column names we are interested in
    """
    return [column for column in df.columns if (element[-3:] in column) and \
            (('Last' in column) or ('Adjusted' in column))]

def filter_training_set(df, data_info):
    """
    Input:
        df -- DataFrame of data
        begin_date -- string of the lower bound date
        end_date -- string of the upper bound date
        minutes_cutoff -- int of lower bound for bucketed minutes

    Output:
        DataFrame that can then be passed to time_series cv

    Filters our DataFrame to dates between 'begin_date' and 'end_date' and
    players who have played more minutes than 'minutes_cutoff'
    """
    # Turn date limits to Datetime
    begin_date = datetime.strptime(data_info.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(data_info.end_date, '%Y-%m-%d')

    # Filter based on date limits
    df = df[(df.Date > data_info.start_date) & (df.Date < data_info.end_date)]

    # Filter based on minutes played
    return df[df.BucketedMinutes >= data_info.minutes_cutoff]

def log_gradient_boosting_results(df, best_score, best_params, element,
                                  data_info, param_grid, best_iter,
                                  num_boost_round):
    """
    Input:
        df -- DataFrame used to train RandomForestRegressor
        gscv -- GridSearchCV object used to grid search and cross validate
                random forest
        element -- string indicating which stat our random forest is predicting
    Output:
        None

    Prints information about grid search to files in 'logs' folder.
    """
    with open('logs/{}GradientBoostedLog.txt'.format(element), 'a+') as f:
        f.write('-' * 40)
        f.write("\nTrain Set:\n")
        f.write("Start date {}, end date {}, with {} splits and \
                bucketed minutes cutoff of {}\n".format(data_info.start_date,
                                                      data_info.end_date,
                                                      data_info.splits,
                                                      data_info.minutes_cutoff))
        f.write("\nColumns Used:\n")
        for column in sorted(df.columns):
            f.write("\t{}\n".format(column))
        f.write("\nParameter Grid:\n")
        for key, value in param_grid.iteritems():
            f.write("\t{}: {}\n".format(key, value))
        f.write("\nBest Parameters:\n")
        for key, value in best_params.iteritems():
            f.write("\t{}: {}\n".format(key, value))
        f.write("\tnum_boost_round: {}/{}\n".format(best_iter, num_boost_round))
        f.write("\nBest Score: ")
        f.write(str(best_score))
        f.write('\n' * 3)

if __name__ == "__main__":
    from read_write import read_merged_data
    df = read_merged_data()
    data_info = cv_method(method = k_folds_cv,
                          splits = 5,
                          start_date = '1999-01-01',
                          end_date = '2016-09-01',
                          minutes_cutoff = 3)

    param_grid = {
                  'bst:max_depth':[3,4,5],
    			  'bst:eta':[0.01, 0.005],
    			  'silent':[1],
    			  'gamma':[0.1],
    			  'lambda':[0.1],
    			  'subsample':[0.6],
    			  'colsample_bytree':[0.5, 0.6, 0.7]
                 }

    if False:
        xgboost_cv = grid_search_xgboost(df,
                                         element = 'PlayerPTS',
                                         data_info = data_info,
                                         param_grid = param_grid,
                                         num_boost_round = 500,
                                         early_stopping_rounds = 50,
                                         log_results = True)
    if True:
        print "Grid Search GB for FanDuelScore"
        add_fantasy_score(df)
        xgboost_cv = grid_search_xgboost(df,
                                         element = 'FanDuelScore',
                                         data_info = data_info,
                                         param_grid = param_grid,
                                         num_boost_round = 1000,
                                         early_stopping_rounds = 15,
                                         log_results = True)

    if False:
        add_fantasy_score(df)
        params = {
                  'colsample_bytree': 0.4,
                  'silent': 1,
                  'bst:max_depth': 5,
                  'subsample': 0.6,
                  'bst:eta': 0.01,
                  'gamma': 0.1,
                  'lambda': 0.1
                 }

        train_xgboost(df,
                      element = 'FanDuelScore',
                      params = params,
                      data_info = data_info,
                      num_boost_round = 17)
