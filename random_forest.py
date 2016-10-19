import numpy as np
import pandas as pd
from read_write import load_pickled_model, dump_pickled_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.grid_search import GridSearchCV
from stat_lists import *
from variance import get_variance
from cross_validation import time_series_cv, filter_training_set, cv_method

def train_random_forest(df, element, cv, log_results = True):
    # Subset training set
    df = filter_training_set(df, cv)

    # Select relevent features for element
    df = select_features(df, element)

    # Create indepentent and dependent variable arrays
    y_train = df.pop(element).values
    X_train = df.values

    # Instantiate
    rfr = RandomForestRegressor()

    # Grid search cross validate
    param_grid = {'n_estimators': [10, 100, 200, 500]}
    gscv = GridSearchCV(rfr,
                        param_grid = param_grid,
                        verbose = 20,
                        n_jobs = -1,
                        cv = cv.method)
    gscv.fit(X_train, y_train)

    # Print out results
    print "Best parameters for", element, "Random Forest:", gscv.best_params_
    print "Best score for", element, "Random Forest:", gscv.best_score_

    # Log results
    if log_results:
        log_random_forest_results(df, gscv, element, cv)

    print gscv.best_estimator_.predict(X_train)
    raw_input('paused')

    # Dump model to pickle
    dump_pickled_model(gscv.best_estimator_,
                       '{}RandomForestRegressor'.format(element))

def predict_random_forest(df, element):
    """
    Input:
        df -- DataFrame with all features
        element -- string indicating which stat we are predicting
    Output:
        y_pred -- numpy array with predictions
        variance_pred -- numpy array with estimated variance for stat
    """

    # Select player names
    players = df.Player

    # Select relevent features
    df = select_features(df, element)
    df.pop(element)
    X_test = df.values

    # Open pickled model
    rfr = load_pickled_model(element + 'RandomForestRegressor')

    # Predict
    y_pred = rfr.predict(X_test)
    variance_pred = get_variance(rfr, X_test, players, element, plot = False)

    return y_pred, variance_pred

def select_features(df, element):
    """
    Input:
    df: merged DataFrame with all features
    element: string of the form 'PlayerStat'
    Output:
    features: DataFrame of features we want

    Selects all columns that are involved in predicting a stat. This includes
    all columns with 'Stat' and 'Last' and the features in list
    'basic_features'. Also changes all NaN and Inf to -999 to make interactions
    with ensemble trees smooth.
    """
    features_list = [column for column in df.columns if (element[-3:] in column) and ('Last' in column)] + \
                    [element] + \
                    basic_features

    # Mark all NaN and Inf as -999
    features = df[features_list].replace([np.inf, np.nan], -999)

    # Turn all columns in float data type
    for column in features.columns:
        features[column] = features[column].astype(float)

    return features

def log_random_forest_results(df, gscv, element, cv_method):
    """
    Input:
        df -- DataFrame used to train RandomForestRegressor
        gscv -- GridSearchCV object used to grid search and cross validate
                random forest
        element -- string indicating which stat our random forest is predicting
    Output:
        None
    """
    with open('logs/{}RandomForestLog.txt'.format(element), 'w+') as f:
        f.write('#' * 20)
        f.write("\nTrain Set: ")
        f.write("{}".format(cv_method))
        f.write("\nColumns Used: ")
        f.write(str(df.columns))
        f.write("\nBest Parameters: ")
        f.write(str(gscv.best_params_))
        f.write("\nBest Score: ")
        f.write(str(gscv.best_score_))
        f.write('\n' * 3)


if __name__ == "__main__":
    from read_write import read_merged_data
    df = read_merged_data()
    cv = cv_method('time_series', 5, '1999-01-01', '2016-09-01', 3)

    train_random_forest(df, 'PlayerPTS', cv, log_results = False)
