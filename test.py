from diagnostics import *
import pandas as pd
import numpy as np
import xgboost as xgb
from player import build_basic_player_data, build_time_series_player_data
from team import build_basic_team_data, build_time_series_team_data
from helper import *
from stat_lists import *
from nba_scraper import scrape
from gradient_boost import *
from read_write import *
from linear_model import linear_model
from random_forest import train_random_forest, predict_random_forest
from optimal_lineups import optimize_lineups
from minute_estimation import create_minutes_estimation, read_minute_estimation
from cross_validation import cv_method, k_folds_cv

def build_merged_data(player_df, team_df, train = True):
    """
    Input:
        player_df -- DataFrame of fully built player data
        team_df -- DataFrame of fully built team data
        train -- Boolean indicating whether to train linear models
    Output:
        merged_df -- DataFrame with fully built features
    """

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
    add_bucketed_minutes(merged_df)

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
        # bucketed minutes and estimated pacea
        basic_feature = key[:9]
        linear_model_df = ['Last' + str(window) + 'Average' + key for window in value] + \
                          ['BucketedMinutes', 'EstimatedPace'] + \
                          [basic_feature]
        feature_name = 'PossessionMinuteAdjusted' + key[:9]
        merged_df[feature_name] = linear_model(merged_df[linear_model_df],
                                               basic_feature,
                                               svr = False,
                                               train = train)

        # Iterate through each window and find the one the best correlation
        for window in value:
            # Determine name of our estimator feature
            feature_name = 'Last' + str(window) + 'PossessionMinuteAdjusted' + key[:9]

            merged_df[feature_name] = \
                merged_df['Last' + str(window) + 'Average' + key] * \
                merged_df.EstimatedPlayerPossessions

            # Determine which rows are not NaN for our estimator feature and feature
            good_indices = pd.notnull(merged_df[feature_name]) & pd.notnull(merged_df[key[:9]])
    return merged_df






def train(should_scrape = True, should_dump = True, should_build = True,
          should_train_linear_models = True, cv = None):
    """
    Takes a DataFrame of player data as 'player_df' and scrapes data not
    included in DataFrame. It then builds the dataset for all the data that
    is not new
    """
    # Scrapes data not included in current player data
    if should_scrape:
        scrape()

    if should_build:
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
        team_df = build_time_series_team_data(team_df,
                                              train = should_train_linear_models)

        # Build merged data features
        merged_df = build_merged_data(player_df,
                                      team_df,
                                      train = should_train_linear_models)
    else:
        merged_df = read_merged_data()

    # Dump
    if should_dump:
        dump_player_data(player_df)
        dump_team_data(team_df)
        dump_merged_data(merged_df)

    # Train
    train_model(merged_df)


def train_model(df):
    # Get list of statistics we want to predict
    prediction_statistics = ['Player' + stat for stat in main_stat_list_minus_minutes]

    # Build Random Forest for each statistic
    for element in prediction_statistics:
        train_random_forest(df, element)
        # train_xgboost(element)





def predict(should_scrape = True, should_dump = True, should_build = True):
    # Read in full player DataFrame and determine what to scrape
    player_df = read_player_data()
    team_df = read_team_data()

    # Scrape new data
    if should_scrape:
        scrape()

    if should_build:
        # Read in new and prediction data
        new_player_df = read_new_player_data()
        player_prediction_df = make_player_prediction_data()
        new_team_df = read_new_team_data()
        team_prediction_df = make_team_prediction_data()

        # Remove used data
        new_player_df = remove_used_new_player_rows(player_df, new_player_df)
        new_team_df = remove_used_new_team_rows(team_df, new_team_df)

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
        raw_input('Press <ENTER> to continue after predicting minutes')

        # Add estimated minutes to player data
        player_df = read_minute_estimation(player_df)

        # Build time series features
        player_df = build_time_series_player_data(player_df)
        team_df = build_time_series_team_data(team_df, train = False)

        # Build merged data features
        merged_df = build_merged_data(player_df, team_df, train = False)

        # Select prediction data
        prediction_df = select_prediction_data(merged_df)
    else:
        prediction_df = read_prediction_data()

    if should_dump:
        # Dumps team and player data
        dump_player_data(player_df)
        dump_team_data(team_df)
        dump_merged_data(merged_df)
        dump_prediction_data(prediction_df)

    # Make predictions
    make_prediction(prediction_df)

def make_prediction(df):
    # Get list of statistics we want to predict
    prediction_statistics = ['Player' + stat for stat in main_stat_list_minus_minutes]

    # Dictionary to weight scores based on FanDuel values
    weighting_dictionary = {'PlayerAST': 1.5, 'PlayerPTS': 1, 'PlayerDRB': 1.2,
                            'PlayerORB': 1.2, 'PlayerTOV': -1, 'PlayerSTL': 2,
                            'PlayerBLK': 2}

    # Make predictions
    score = np.zeros(len(df))
    variance = np.zeros(len(df))
    for stat in prediction_statistics:
        # Get predictions and variance
        prediction, variance = predict_random_forest(df, stat)

        # Get weight of particular stat
        weight = weighting_dictionary[stat]

        # Accumulate scores and variance
        score = np.add(score, np.multiply(prediction, weight))
        variance = np.add(variance, np.multiply(variance, int(weight**2)))

        # predict_xgboost(df, element)

    # Create DataFrame with 'Player', 'PlayerID', 'Score', and 'Variance'
    predictions = pd.DataFrame(df[['Player', 'PlayerID']])
    predictions['Score'] = score
    predictions['Variance'] = variance

    # Dump to file
    dump(predictions, 'final_score')





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

2. Create a logs for linear models.

3.
"""

@timeit
def add_player_position(df, data_info):
    """
    Input:
        df -- DataFrame of merged player and team data
        data_info -- cv_method object to specify what data to predict on
    Output:

    Loads our current 'FanDuelScoreGradientBoostedRegressor' model and makes
    residuals column 'R'. Then groups
    """

    # Read model
    m = load_pickled_model('FanDuelScoreGradientBoostedRegressor')

    # Add numeric position
    add_fantasy_score(df)
    add_position_metric(df)
    element = 'FanDuelScore'
    m = load_pickled_model(element + 'GradientBoostedRegressor')

    # Filter to only games with all five starters
    starters = df[df.GS == 1]
    all_five = starters.groupby(['Team', 'Date']).filter(lambda x: len(x) == 5)
    all_five = add_lineup_position(all_five)

    # Calculate residuals for filtered dataset
    dtrain, all_five, remaining = xgboost_preprocessing(all_five, element, data_info)
    pred = m.predict(dtrain)

    print len(pred)
    print len(all_five)
    raw_input()

    df['R'] = pred - all_five.FanDuelScore

    # Add back 'Team' and 'Date' columns
    df['Date'] = df_remaining.Date
    df['Team'] = df_remaining.Team


def add_lineup_position(df):
    num_games = len(df)/5
    df.sort_values(['Position', 'PosMetric'])
    df['LineupOrder'] = range(1,6) * num
    return df

if __name__ == "__main__":
    # Specifies cross validation technique to use for training
    cv = cv_method(k_folds_cv, 5, '1999-01-01', '2016-09-01', 3)

    # # Train
    # train(should_scrape = False,
    #       should_dump = True,
    #       should_build = True,
    #       should_train_linear_models = False,
    #       cv = cv)
    from read_write import read_merged_data

    data_info = cv_method(method = k_folds_cv,
                          splits = 5,
                          start_date = '1999-01-01',
                          end_date = '2016-09-01',
                          minutes_cutoff = 3)
    df = read_merged_data()
    add_player_position(df, data_info)

    # # Predict
    # predict(should_scrape = False,
    #         should_dump = False,
    #         should_build = True)
    #
    # # Pick optimal lineups
    # optimize_lineups(n_lineups = 100)
