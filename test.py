import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import xgboost as xgb
import pickle
from helper import *
from stat_lists import *
from nba_scraper import *
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

@timeit
def scrape():
    most_recent_date = read_team_data().Date.max().strftime('%Y-%m-%d')
    scrape_new_data(most_recent_date, only_team = False)

@timeit
def add_estimated_game_pace(df):
    """
    Calculate the estimated for pace for a given game
    """
    # Make DataFrame out of columns that we want to use in pace linear model
    X = pd.DataFrame([func(df, window) for window in pace_linear_model_window_list
                          for func in [get_home_team_pace, get_away_team_pace]]).transpose()
    X['TeamPace'] = df.TeamPace

    # Fit to linear model
    y = linear_fit(X, 'TeamPace', svr = False)
    df['EstimatedPace'] = y

# Fit to Ridge Regression and SVM and choose better model
def linear_fit(df, dependent_variable, ridge = True, svr = True):
    # Find rows of DataFrame that do not have any NaN values
    full_row_indices = np.where(np.all(np.isfinite(df), axis = 1))[0]

    # Subset DataFrame to only include full row indices
    X = df.loc[full_row_indices,:]

    # Make numpy arrays
    y_train = X.pop(dependent_variable).values
    X_train = X.values

    # Standardize data
    scale = StandardScaler()
    X_train = scale.fit_transform(X_train)

    # Create degree 3 polynomial features
    poly = PolynomialFeatures(degree = 3)
    X_train = poly.fit_transform(X_train)

    best_score = 0
    y_pred = None
    if ridge:
        # Train Lasso Regression Model
        ridge = Lasso()
        gscv_ridge = GridSearchCV(ridge,
                                  param_grid = {'alpha': [0,0.01,0.05,0.1]},
                                  verbose = False,
                                  n_jobs = -1,
                                  cv = 5)
        gscv_ridge.fit(X_train, y_train)
        best_score = gscv_ridge.best_score_
        y_pred = gscv_ridge.predict(X_train)
        print "Best parameters for ridge: ", gscv_ridge.best_params_
        print "Best score for ridge: ", gscv_ridge.best_score_
        print "Coefficients for rideg: ", gscv_ridge.best_estimator_.coef_

    if svr:
        # Train SVM Regression Model
        ridge = SVR()
        gscv_svm = GridSearchCV(ridge,
                                param_grid = {'C': [1,2,5],
                                              'gamma': [.2,.4,.6]},
                                verbose = 30,
                                n_jobs = -1,
                                cv = 5)
        gscv_svm.fit(X_train, y_train)
        if gscv_svm.best_score_ > best_score:
            best_score = gscv_svm.best_score_
            y_pred = gscv_ridge.predict(X_train)
        print "Best parameters for SVM: ", gscv_svm.best_params_
        print "Best score for SVM: ", gscv_svm.best_score_

    return pd.Series(data = y_pred, index = full_row_indices)

# Main blocks
@timeit
def build_basic_player_data(player_df):
    """
    Build all the features and cleans all data for a set of player data.

    Wrapper function subsets the data to only include new data and (the columns
    necessary to build the features for new data) <- not yet.

    Unmarks the data as new at the end of function.

    DOES NOT DUMP
    """

    """
    Functions that do not require full dataset
    """
    # Add season data
    add_season(player_df)

    # Sort by 'Date'
    sort_by_date(player_df)

    # Removes a few data points with NaN for 'PTS' or 'MP'
    player_df = remove_nan_rows(player_df, 'PlayerPTS')
    player_df = remove_nan_rows(player_df, 'PlayerMP')

    # Make dummy variable out of 'Home' column
    make_home_dummys(player_df)

    # Make Position Numeric
    make_position_numeric(player_df)

    # Minute adjusted stats
    add_player_per_minute_stats(player_df)

    # Add FanDuel score
    add_fantasy_score(player_df)

    # Drop certain columns
    remove_columns(player_df, ['Rank', 'Unnamed: 0', '2P%', '3P%',
                               'FG%', 'FT%', 'Result', 'GmSc'])

    return player_df

@timeit
@subset
def build_time_series_player_data(player_df):
    """
    Functions that do require full data
    """
    # Group by player and team
    player_df = group_by_player_team(player_df, split = True)

    # Group by season
    player_df = group_by_player_season(player_df, split = True)

    # Group by player
    player_df = group_by_player(player_df, split = True)

    return player_df

@timeit
def build_basic_team_data(team_df):
    """
    Functions that do not require full data.
    """
    # Read team data
    convert_to_datetime(team_df)
    add_season(team_df)

    # Make dummy variable out of 'Home' column
    make_home_dummys(team_df)

	# Add in Overtime column
    add_overtime(team_df)

    # Add in possessions and pace
    add_possessions(team_df)
    add_pace(team_df)

    # Calculate opponent per possessions stats
    add_opponenet_per_possession_stats(team_df)

    # Add in result
    add_result(team_df)

    # Sort by 'Date'
    sort_by_date(team_df)

    return team_df

@timeit
def build_time_series_team_data(team_df):
    """
    Functions that do require full data
    """
    # Group by team
    team_df = group_by_team(team_df, split = True)

    # Group by season
    team_df = group_by_team_season(team_df, split = True)

    # Group by opponent
    team_df = group_by_opponent(team_df, split = True)

    # Add estimated game possesssions
    add_estimated_game_pace(team_df)

    return team_df

def build_merged_data(player_df, team_df):
    # Merge 'player_df' and 'team_df'
    merged_df = player_df.merge(team_df, on = ['Team', 'Date', 'Opp', 'Home',
                                               'New', 'Prediction'])

    # Bucket minutes
    """
    0-5 -> 0
    6-11 -> 1
    12-17 -> 2
    18-23 -> 3
    24-29 -> 4
    30-35 -> 5
    36-41 -> 6
    """
    merged_df['BucketedMinutes'] = np.floor(merged_df.PlayerMP / 6)

    # Get stats per possession played
    add_player_per_possession_played_stats(merged_df)

    # Group by player
    merged_df = group_by_player_post_merge(merged_df)

    # Estimate number of possessions a player will take part in
    merged_df['EstimatedPlayerPossessions'] = ((merged_df.BucketedMinutes * 6 + 3) / 48) * \
                                                merged_df.EstimatedPace

    for key, value in player_post_merge_rolling_mean_stat_dict.iteritems():
        # Predict player stats with simple rate muliplication
        """
        'PossessionMinuteAdjustedPlayer' + stat =
        (Stat / Possession) * (Estimated PlayerPossessions)
        """

        # Run linear model analysis with per possession played averages,
        # bucketed minutes and estimated pace
        linear_model_df = ['Last' + str(window) + 'Average' + key for window in value] + \
                          ['BucketedMinutes', 'EstimatedPace', key[:9]]

        linear_fit(merged_df[linear_model_df], key[:9], svr = False)

        # Iterate through each window and find the one the best correlation
        for window in value:
            merged_df['Last' + str(window) + 'PossessionMinuteAdjusted' + key] = \
            merged_df['Last' + str(window) + 'Average' + key] * \
            merged_df.EstimatedPlayerPossessions
            print "Rate multiplication R2 score: ", r2_score(merged_df[pd.notnull(merged_df['Last' + str(window) + 'PossessionMinuteAdjusted' + key])][key[:9]],
                                                             merged_df[pd.notnull(merged_df['Last' + str(window) + 'PossessionMinuteAdjusted' + key])]['Last' + str(window) + 'PossessionMinuteAdjusted' + key])
    return merged_df

from sklearn.ensemble import RandomForestRegressor
from sklearn.grid_search import GridSearchCV
def train_model(X_train):
    # Get list of statistics we want to predict
    prediction_statistics = main_stat_list.remove(['MP', 'ORB'])
    print df.info()
    print prediction_statistics
    raw_input()

    # Random Forest
    rfr = RandomForestRegressor()


    df = df.select_dtypes(include=['float64','int64'])

    label = df.PlayerPTS.values
    data = df[list(set(df.columns) - set(['PlayerPTS']))].values

    x_pred = xgb.DMatrix(data[:10,:])

    dtrain = xgb.DMatrix(data, label = label)
    param = {'bst:max_depth':2, 'bst:eta':1, 'silent':1}
    bst = xgb.train(param, dtrain)



def train(should_scrape = True):
    """
    Takes a DataFrame of player data as 'player_df' and scrapes data not
    included in DataFrame. It then builds the dataset for all the data that
    is not new
    """
    # Scrapes data not included in current player data
    if should_scrape:
        scrape()

    # Read in new and old player data
    player_df = read_player_data()
    new_player_df = read_new_player_data()
    team_df = read_team_data()
    new_team_df = read_new_team_data()

    # Remove used data
    new_player_df = remove_used_new_player_rows(player_df, new_player_df)
    new_team_df = remove_used_new_team_rows(team_df, new_team_df)

    # Combine new and old data
    player_df = stack_data_frames([player_df,
                                   new_player_df])
    team_df = stack_data_frames([team_df,
                                 new_team_df])


    # Build features
    player_df = build_basic_player_data(player_df)
    team_df = build_basic_team_data(team_df)

    # Build time series features
    player_df = build_time_series_player_data(player_df)
    team_df = build_time_series_team_data(team_df)

    # Build merged data features
    merged_df = build_merged_data(player_df, team_df)

    # Dump
    # dump_player_data(player_df)
    # dump_team_data(team_df)
    dump_merged_data(merged_df)

    # Train
    # train_model(merged_df)

def predict(should_scrape = True):
    # Read in full player DataFrame and determine what to scrape
    player_df = read_player_data()
    team_df = read_team_data()

    # Scrape new data
    if should_scrape:
        scrape()

    # Read in new and prediction data
    new_player_df = read_new_player_data()
    player_prediction_df = make_player_prediction_data()
    new_team_df = read_new_team_data()
    team_prediction_df = make_team_prediction_data()

    # Remove used data
    new_player_df = remove_used_new_player_rows(player_df, new_player_df)
    new_team_df = remove_used_new_team_rows(team_df, new_team_df)

    # Build basic features
    # new_player_df = build_basic_player_data(new_player_df)
    # new_team_df = build_basic_team_data(new_team_df)

    # Append DataFrames on top on one another
    player_df = stack_data_frames([player_df,
                                   new_player_df,
                                   player_prediction_df])
    team_df = stack_data_frames([team_df,
                                 new_team_df,
                                 team_prediction_df])

    player_df = build_basic_player_data(player_df)
    team_df = build_basic_team_data(team_df)

    # Create minutes estimation file and pause program
    create_minutes_estimation(player_df)
    merged_dfut('Press <ENTER> to continue after predicting minutes')

    # Add estimated minutes to player data
    player_df = read_minute_estimation_file(player_df)

    # Build time series features
    player_df = build_time_series_player_data(player_df)
    team_df = build_time_series_team_data(team_df)

    # Build merged data features
    # merged_df = build_merged_data(player_df, team_df)

    # Dumps team and player data
    dump_player_data(player_df)
    dump_team_data(team_df)

    # Select prediction data
    # prediction_df = select_prediction_data(merged_df)

    # Predict
    # xgboost_predict(prediction_df)

def create_minutes_estimation(player_df):
    # Filter out rows to only select those needed to build minutes estimation
    pred_player_df = filter_out_prediction(player_df)

    # Build features for minutes estimation
    pred_player_df = group_by_player(pred_player_df, split = True)

    # Select only prediction players
    pred_player_df = pred_player_df[pred_player_df.Prediction == True]

    # Select columns we want in our minute estimation file
    pred_player_df = pred_player_df[minutes_estimation_file_list]

    # Add empty column to fill in minutes
    pred_player_df['PlayerMP'] = np.nan
    pred_player_df['GS'] = np.nan

    # Dump to 'minute_estimation_file.csv'
    pred_player_df.to_csv('minute_estimation_file.csv', index = False)

@timeit
def read_minute_estimation_file(player_df):
    # Read file
    minute_estimation_df = pd.read_csv('minute_estimation_file.csv')

    minute_estimation_df['PlayerMP'] = 1
    minute_estimation_df['GS'] = 1

    # Select essential rows from minutes estimation file
    minute_estimation_df = minute_estimation_df[['Player', 'PlayerMP', 'GS']]

    # Player
    prediction_player_df = player_df[player_df.Prediction == True]
    prediction_player_df.drop(['PlayerMP', 'GS'], axis = 1, inplace = True)
    prediction_player_df = prediction_player_df.merge(minute_estimation_df,
                                                      on = ['Player'])

    player_df = player_df[player_df.Prediction == False]


    player_df = stack_data_frames([player_df, prediction_player_df])

    return player_df

"""
There are 3 scenarios that we need to prepare for:

1. We need to compute a completely new set of features from our raw data and
train our model.

2. We need to add new rows to our data sets with the same features and use
these to train a new model.

3. We want to make a prediction.
"""

"""
Things to do:
1. Find way to differentiate between players with the same name. There are only
about 20 instances of players with the same name having an overlap. There may
be others without overlap, which will be much more difficult to deal with.
"""

if __name__ == "__main__":
    # Read in raw data
    train(should_scrape = False)
