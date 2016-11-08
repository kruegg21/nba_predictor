import xgboost
import numpy as np
import pandas as pd
import time
import copy
from multiprocessing import Pool, cpu_count
from helper import add_fantasy_score, timeit
from datetime import datetime
from itertools import product
from read_write import load_pickled_model, dump_pickled_model, read_merged_data
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

def xgboost_preprocessing(df, element, data_info, should_dump = True):
    # Select only features we need for particualr stat
    df = filter_training_set(df, data_info)
    filtered_df, remaining_df = select_features(df,
                                                element,
                                                should_dump = should_dump)

    untransformed = df[element].values
    print "Y train untransformed is {}".format(untransformed)

    # Transform dependent variable
    data_info.target_transformation(filtered_df, element)

    # Create indepentent and dependent variable arrays
    y_train = filtered_df.pop(element).values
    X_train = filtered_df.values
    print "X train is {}".format(X_train)

    print "Y train transformed is {}".format(y_train)
    print y_train[np.isnan(y_train)]

    # Create DMatrix
    dtrain = xgboost.DMatrix(X_train,
                             label=y_train,
                             missing = -999,
                             feature_names = filtered_df.columns)

    # Add dependent variable back to df
    filtered_df[element] = y_train

    # Combine all features (DataFrame is still filtered)
    column_names = filtered_df.columns
    filtered_df = pd.concat([filtered_df, remaining_df], axis = 1)
    filtered_df.reset_index(inplace = True, drop = True)

    return dtrain, filtered_df, column_names

def grid_search_xgboost(element = None, data_info = None, param_grid = None,
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
    # Read in data
    df = read_merged_data()

    # # Processes Data
    dtrain, filtered_df, column_names = xgboost_preprocessing(df,
                                                              element,
                                                              data_info,
                                                              should_dump = True)
    dtrain.save_binary("data/train.buffer")

    # Grid Search
    best_score = np.inf
    best_params = {}
    best_iteration = num_boost_round

    s = sorted(param_grid.items())
    keys, values = zip(*s)

    # Multiprocessing Grid Search
    p = Pool(4)
    arg_list = [(dict(zip(keys, i)), num_boost_round, data_info, early_stopping_rounds)
                for i in product(*values)]
    results = p.map(parameter_wrapper, arg_list)
    print results

    for trial in zip(results, arg_list):
        s = trial[0][0]
        i = trial[0][1]
        params = trial[1][0]
        if best_score > s:
            best_score = s
            best_params = params
            best_iteration = i

    # for i in product(*values):
    #     params = dict(zip(keys, i))
    #     s, i = grid_search_round(params, dtrain,
    #                              num_boost_round = num_boost_round,
    #                              early_stopping_rounds = early_stopping_rounds)
    #     if best_score > s:
    #         best_score = s
    #         best_params = params
    #         best_iteration = i

    if log_results:
        log_gradient_boosting_results(column_names,
                                      best_score,
                                      best_params,
                                      element,
                                      data_info,
                                      param_grid,
                                      best_iteration,
                                      num_boost_round)

def parameter_wrapper(args):
    """
    Inputs:
        args -- tuple of arguments
    Output:
        None

    Unpacks the tuple of argument 'args' and passes them to
    the function 'grid_search_round'
    """
    return grid_search_round(*args)

@timeit
def grid_search_round(params, num_boost_round = 500, data_info = None,
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

    dtrain = xgboost.DMatrix("data/train.buffer")
    print "Running search on {}".format(params)
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
    dtrain, filtered_df, column_names = xgboost_preprocessing(df,
                                                              element,
                                                              data_info,
                                                              should_dump = False)

    print "Training xgboost with {} rounds".format(num_boost_round)
    print "On features :"
    for column in column_names:
        print "{}".format(column)

    model = xgboost.train(params,
                          dtrain,
                          num_boost_round = num_boost_round)

    # Dump model to pickle
    dump_pickled_model(model, '{}{}GradientBoostedRegressor'.format(data_info.transform,
                                                                    element))

def predict_xgboost(df, element = None, data_info = None, should_dump = True):
    """
    """
    # Filter data
    dtrain, filtered_df, column_names = xgboost_preprocessing(df,
                                                              element,
                                                              data_info,
                                                              should_dump = should_dump)

    # Load model
    m = load_pickled_model('{}{}GradientBoostedRegressor'.format(data_info.transform,
                                                                 element))

    # Predict
    pred = m.predict(dtrain)

    print "Untransformed predictions: {}".format(pred)
    raw_input()

    # Untransform predictions
    pred = data_info.target_reverse_transformation(pred, element)
    print "Transformed predictions: {}".format(pred)
    raw_input()

    return pred, filtered_df

def select_features(df, element, should_dump = True):
    """
    Input:
        df -- merged DataFrame with all features
        element -- string of the form 'PlayerStat'
    Output:
        features -- DataFrame of features we want
        remaining_features -- DataFrame of the remaining features

    Selects all columns that are involved in predicting a stat. This includes
    all columns with 'Stat' and 'Last' and the features in list
    'basic_features'. Also changes all NaN and Inf to -999 to make the data
    compatible with tree methods.
    """
    if element[:6] == 'Player':
        features_list = get_relevent_columns(df, element) + [element] + basic_features
        features_list += get_extra_columns(df)
    else:
        features_list = []
        for stat in main_stat_list_minus_minutes:
            features_list += get_relevent_columns(df, stat)
        features_list += get_extra_columns(df)
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

def get_extra_columns(df):
    p = set([column for column in df.columns if 'Last' in column])
    for element in main_stat_list_minus_minutes:
        p -= set([column for column in df.columns if (element[-3:] in column)
                    and (('Last' in column) or ('Adjusted' in column))])
    return list(p)


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

def log_gradient_boosting_results(column_names, best_score, best_params, element,
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
        f.write("{}".format(data_info))

        f.write("\nColumns Used:\n")
        for column in sorted(column_names):
            f.write("\t{}\n".format(column))

        f.write("\nParameter Grid:\n")
        for key, value in param_grid.iteritems():
            f.write("\t{}: {}\n".format(key, value))

        f.write("\nBest Parameters:\n")
        for key, value in best_params.iteritems():
            f.write("\t{}: {}\n".format(key, value))

        f.write("\tNum_boost_rounds: {}/{}\n".format(best_iter, num_boost_round))
        f.write("\nBest Score: {}".format(str(best_score)))
        f.write('\n' * 3)

if __name__ == "__main__":
    df = read_merged_data()
    data_info = cv_method(method = k_folds_cv,
                          splits = 5,
                          start_date = '1999-01-01',
                          end_date = '2016-09-01',
                          minutes_cutoff = 3)

    param_grid = {
                  'max_depth':[4],
    			  'learning_rate':[0.5],
    			  'silent':[1],
    			  'gamma':[0.1, 0.15],
    			  'lambda':[0.1, 0.15],
    			  'subsample':[0.5, 0.6, 0.7],
    			  'colsample_bytree':[0.6]
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
        xgboost_cv = grid_search_xgboost(
                                         element = 'FanDuelScore',
                                         data_info = data_info,
                                         param_grid = param_grid,
                                         num_boost_round = 3000,
                                         early_stopping_rounds = 50,
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

        gboost(df,
                      element = 'FanDuelScore',
                      params = params,
                      data_info = data_info,
                      num_boost_round = 17)
