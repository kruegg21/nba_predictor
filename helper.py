import warnings
warnings.filterwarnings("ignore")
import time
import pickle
from datetime import timedelta
from stat_lists import *
import pandas as pd
import numpy as np
import scipy as sp
from os import walk
from datetime import datetime
from linear_model import linear_model
import matplotlib.pyplot as plt
import seaborn

# Timing function
def timeit(method):
    """
    Timing wrapper
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print 'Running %r took %2.4f sec\n' % \
              (method.__name__, te-ts)
        return result
    return timed

# Subsetting function
def subset(method):
    """
    Subsetting wrapper
    """
    def subsets(*args, **kw):
        # Divided into chunks
        main, chunk = subset_player_data(*args, **kw)
        print "Size of main before subsetting: ", len(main) + len(chunk)
        print "Size of chunk after subsetting: ", len(chunk), "\n"
        if not chunk.empty:
            chunk = method(chunk)

        #Combine chunks
        return unsubset_data(main, chunk)
    return subsets


@timeit
def filter_out_prediction(df):
    return df.groupby('Player').filter(lambda x: np.any(x.Prediction == True)).reset_index()







# Removes duplicate data
def remove_used_new_player_rows(player_df, new_player_data):
    return remove_used_rows(player_df, new_player_data)

def remove_used_new_team_rows(team_df, new_team_df):
    return remove_used_rows(team_df, new_team_df)

def remove_used_rows(df, new_df):
    maximum_date = np.max(df.Date)
    return new_df[new_df.Date > maximum_date]




# Marking and unmarking new and prediction functions
def mark_new(df):
    df['New'] = True

def unmark_new(df):
    df['New'] = False

def mark_pred(df):
    df['Prediction'] = True

def unmark_pred(df):
    df['Prediction'] = False



# Translation functions
"""
Translates names from FanDuel format to basketballreference.com format
"""
def translate_team_names(df):
    translate(df, fd_to_br_team_translator)

def translate_player_names(df):
    translate(df, fd_to_br_player_translator)

def translate_position_names(df):
    translate(df, fd_to_br_position_translator)
    df.rename(columns = {'Position': 'Pos'}, inplace = True)

# Abstracted translation function
def translate(df, dictionary):
    df.replace(dictionary, inplace = True)




# FanDuel file functions
"""
Looks in 'data/FanDuel' directory to find the most recent file name or date
"""
@timeit
def find_fd_filenames():
    """
    Input:
        None
    Output:
        file_list -- list of strings indicating the file path to the FanDuel files
                 for the most recent day

    Seaches the directory specified in 'fd_files_path' for the fd
    file with the latest date associated with it.
    """
    for root, dirs, files in walk(fd_files_path):
        # Filter out hidden folders
        files = [f for f in files if not f[0] == '.']

        # Get list of dates
        date_list = [get_fd_file_date(f) for f in files]

        # Find indices of latest date
        indices = np.argwhere(np.equal(date_list, np.amax(date_list)))

        # Get file names for the maximum indices
        file_list = [fd_files_path + str(files[i[0]]) for i in indices]
        return file_list

def get_fd_file_date(file_name):
    """
    Gets the date from a fd file name string
    """
    return datetime.strptime(file_name.split('NBA')[1][1:11], '%Y-%m-%d')

def get_player_id(df):
    df['PlayerID'] = (df.Id.str.split('-').str[1]).apply(pd.to_numeric)


# Selects or removes prediction data
"""
Removes/selects prediction data from DataFrame
"""
def remove_prediction_data(df):
    if 'Prediction' in df.columns:
        return df[df.Prediction == False]
    else:
        return df

def select_prediction_data(df):
    if 'Prediction' in df.columns:
        return df[df.Prediction == True]
    else:
        return df


# Pausing function
def p():
    raw_input('paused')


def add_bucketed_minutes(df):
    """
    0-6 -> 0
    7-12 -> 1
    13-18 -> 2
    19-24 -> 3
    25-30 -> 4
    31-36 -> 5
    37-42 -> 6
    43-48 -> 7

    Has a ceiling of 7 for bucketed minutes
    """
    df['BucketedMinutes'] = np.floor((df.PlayerMP - 1) / 6)
    df[df.BucketedMinutes > 7] = 7

@timeit
def add_estimated_game_pace(df, should_train_linear_model = True):
    """
    Input:
        df -- team data DataFrame
        should_train_linear_model -- boolean indicating if we should train linear model
    Output:
        df -- team data DataFrame with 'EstimatedPace' added

    Calculates the estimated pace using 'linear_model' function.
    Transforms pace rolling averages into the rolling averages for the home team
    and the away team.
    """
    # Make DataFrame out of columns that we want to use in pace linear model
    get_home_team_pace(df, 10)

    X = pd.DataFrame([func(df, window) for window in pace_linear_model_window_list
                          for func in [get_home_team_pace, get_away_team_pace]]).transpose()
    X['TeamPace'] = df.TeamPace

    # Fit to linear model
    y = linear_model(X,
                    'TeamPace',
                    svr = False,
                    train = should_train_linear_model)
    df['EstimatedPace'] = y





# GroupBy Functions
@timeit
def group_by_player(df, split_cols = player_split_cols, split = False):
    return generic_group_by(df,
                            GB_apply_player_data,
                            ['Player'],
                            split_cols,
                            split)

@timeit
def group_by_player_post_merge(df,
                               split_cols = player_post_merge_split_cols,
                               split = False):
    return generic_group_by(df,
                            GB_apply_player_data_post_merge,
                            ['Player'],
                            split_cols,
                            split)

@timeit
def group_by_player_season(df, split_cols = player_season_split_cols, split = False):
    return generic_group_by(df,
                            GB_apply_player_season_data,
                            ['Player', 'Season'],
                            split_cols,
                            split)

@timeit
def group_by_team(df, split_cols = team_split_cols, split = False):
    return generic_group_by(df,
                            GB_apply_team_data,
                            ['Team'],
                            split_cols,
                            split)

@timeit
def group_by_team_season(df, split_cols = team_season_split_cols, split = False):
    return generic_group_by(df,
                            GB_apply_team_season_data,
                            ['Team', 'Season'],
                            split_cols,
                            split)

@timeit
def group_by_opponent(df, split_cols = opponent_split_cols, split = False):
    return generic_group_by(df,
                            GB_apply_opponent_data,
                            ['Opp'],
                            split_cols,
                            split)

@timeit
def group_by_starters(df, split_cols = starter_split_cols, split = False):
    df['IncompleteStarters'] = False
    return generic_group_by(df[df.GS == True],
                            GB_apply_starters_data,
                            ['Team', 'Date'],
                            split_cols,
                            split)

@timeit
def group_by_player_team(df, split_cols = player_team_split_cols, split = False):
    return generic_group_by(df,
                            GB_apply_player_team_data,
                            split_cols,
                            split)

# Abstracted GroupBy Functions
def generic_group_by(df, function, cols, split_cols = None, split = False):
    if split:
        main, chunk = split_into_chunks(df, split_cols)
        del df
        return combine_chunks(main,
                              chunk.groupby(cols, sort = False).apply(function),
                              split_cols)
    else:
        return df.groupby(cols,
                          sort = False).apply(function)




# GroupBy apply functions
def GB_apply_player_data(df):
    add_game_number(df, 'Player')
    add_rolling_averages(df, player_rolling_mean_stat_dict)
    return df

def GB_apply_player_data_post_merge(df):
    add_rolling_averages(df, player_post_merge_rolling_mean_stat_dict)
    return df

def GB_apply_player_season_data(df):
    add_game_number(df, 'PlayerSeason')
    return df

def GB_apply_team_data(df):
    add_back_to_back(df)
    add_game_number(df, 'Team')
    add_rolling_averages(df, team_rolling_mean_stat_dict)
    return df

def GB_apply_team_season_data(df):
    add_game_number(df, 'TeamSeason')
    return df

def GB_apply_opponent_data(df):
    add_rolling_averages(df, opponent_rolling_mean_stat_dict)
    return df

def GB_apply_starters_data(df):
    if len(df) != 5:
        df['IncompleteStarters'] = True
    return df

def GB_apply_player_team_data(df):
    """
    Adds a column that starts at 10 the first game after a player starts
    playing in the NBA or after they are traded to a new team. The number then
    decays by one each game thereafter until reaching 0.
    """
    decay_number = 10
    if len(df) < decay_number:
        df['ChangedTeams'] = range(len(df),0,-1)
    else:
        df['ChangedTeams'] = range(decay_number,0,-1) + \
                             [0] * (len(df) - decay_number)
    return df





# Data cleaning functions
def sort_by_date(df):
    df.sort_values('Date', inplace = True)
    df.reset_index(inplace = True, drop = True)

def convert_to_datetime(df):
    """
    Converts the 'Date' column to datetime
    """
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df.Date)

def remove_nan_rows(df, column):
    """
    Removes all rows with an NaN in 'column' that are not tagged as prediction
    """
    return df[(pd.notnull(df[column])) | (df.Prediction == True)].reset_index(drop = True)

def remove_columns(df, columns):
    """
    Removes the columns in list 'columns'
    """
    for column in columns:
        if column in df.columns:
            df.drop(column, axis = 1, inplace = True)

def make_position_numeric(df):
    df['Position'] = df['Pos'].map(position_dictionary)

def make_home_dummys(df):
    home_dict = {np.nan: True, '@': False}
    df.replace({'Home': home_dict}, inplace = True)

def make_better_player_column_names(df):
    for col in main_stat_list:
        df.rename(columns = {col: 'Player' + col}, inplace = True)

def make_better_team_column_names(df):
    """
    Change column names from 'TeamPTS' to 'OppAllowedPTS' for all the stats
    where this wording makes sense (PTS, AST, ORB, BLK, TRB, DRB, STL).

    Changes the 'TeamTOV' to 'OppForcedTOV' while 'TeamMP' remains the same.
    """
    for col in list(set(main_stat_list) - set(['MP', 'TOV'])):
        df.rename(columns = {'Team' + col: 'OppAllowed' + col}, inplace = True)
    df.rename(columns = {'TeamTOV' : 'OppForcedTOV'}, inplace = True)



# Subsetting and chunking data functions
"""
Used to filter out rows that are not needed for particular calculations
"""
@timeit
def subset_player_data(df):
    return subset_data(df, 'Player', player_feature_container)

def subset_data(df, label, feat_dicts):
    """
    Groups by 'label' and filters out groups that do have an instance of 1
    in the new column. This could be improved by not only filtering out members
    of the column 'label' that are not new, but by also slicing the rows down
    to only a date range within longest window.

    From a brief look this usually will usually subset .13 of the data and cuts
    the time to build data down by around .40
    """
    longest_window = max([max([max(value) for key, value in fd.items()])
                                          for fd in feat_dicts])
    g = df.groupby(label)
    chunk = g.filter(lambda x: np.any(x.New == True))
    main = g.filter(lambda x: np.all(x.New == False))
    return main, chunk

@timeit
def unsubset_data(main, chunk):
    df = stack_data_frames([main, chunk])
    sort_by_date(df)
    return df

"""
Used to filter out columns that are not needed for a particular calculation
"""
@timeit
def split_into_chunks(df, columns):
    return df[list(set(df.columns.values) - set(columns))], df[columns]

@timeit
def combine_chunks(df1, df2, columns):
    # Remove columns that have just been built by 'df2' from 'df1'
    df1 = df1[list((set(df1.columns.values) - \
                   (set(df2.columns.values) - \
                    set(columns))))]

    # Concat the two pieces and return
    return pd.concat([df1, df2], axis = 1)

"""
Used to stack data frames on top of another
"""
@timeit
def stack_data_frames(frame_list):
    return pd.concat(frame_list).reset_index(drop = True)





# Feature building functions
def add_season(df):
    df['Season'] = pd.DatetimeIndex(df['Date']).year
    df.ix[(pd.DatetimeIndex(df['Date']).month > 9), 'Season'] += 1

def add_player_per_minute_stats(df):
    per_minute_stats(df, 'PlayerMP', ['Player' + stat for stat in main_stat_list_minus_minutes])

def add_fantasy_score(df):
    df['FanDuelScore'] = df.PlayerPTS + 1.2 * df.PlayerDRB + \
                         1.2 * df.PlayerORB + 1.5 * df.PlayerAST + \
                         2 * df.PlayerBLK + 2 * df.PlayerSTL - df.PlayerTOV

def add_possessions(df):
    """
    Inputs:
        df -- DataFrame object to add possessions to
    Output:
        None

    Estimates the number of possesssions in a game using statistics from both
    teams
    """
    df['Possessions'] = 0.5 * ((df.TeamFGA + 0.44 * df.TeamFTA - 1.07 * \
                        (df.OppAllowedORB / (df.OppAllowedORB + df.OppDRB)) * \
                        (df.TeamFGA - df.TeamFG) + df.OppForcedTOV) + (df.OppFGA + \
                        0.44 * df.OppFTA - 1.07 * (df.OppORB / (df.OppORB + \
                        df.OppAllowedDRB)) * (df.OppFGA - df.OppFG) + df.OppTOV))

def add_possessions_played(df):
    """
    Estimates the number of possessions played for a player by multiplying the
    fraction of miniutes played by the total number of possessions
    """
    df['PlayerPossessionsPlayed'] = (df.PlayerMP / (df.TeamMP / 5)) * df.Possessions

def add_fg_percentage(df):
    df['PlayerFG%'] = (df.FG + 1) / (df.FGA + 1)

def add_pace(df):
    """
    Pace normalizes possessions to possessions per 48
    """
    df['TeamPace'] = 48 * ((df.Possessions * 2) / (2 * (df.TeamMP / 5)))
    df['OppPace'] = df.TeamPace

def add_overtime(df):
    df['Overtime'] = (df.TeamMP - 240) / 25

def add_result(df):
    df['Won'] = df.Result.str[0] == 'W'

def add_position_metric(df):
	df['PosMetric'] = - df.Last10AveragePlayerAST - df['3PA'] + 2 * \
                        2 * df.Last10AveragePlayerORB

def add_opponenet_per_possession_stats(df):
    for stat in opponent_possession_adjusted_stats_list:
        df[stat + 'PerPossession'] = df[stat]/df.Possessions

def add_player_per_possession_played_stats(df):
    add_possessions_played(df)
    for stat in main_stat_list_minus_minutes:
        df['Player' + stat + 'PerPossession'] = df['Player' + stat] / \
                                                df.PlayerPossessionsPlayed

def get_away_team_pace(df, window):
    return (1 - df.Home) * df['Last' + str(window) + 'AverageTeamPace'] + \
           df.Home * df['Last' + str(window) + 'AverageOppPace']

def get_home_team_pace(df, window):
    return df.Home * df['Last' + str(window) + 'AverageOppPace'] + \
           (1 - df.Home) * df['Last' + str(window) + 'AverageTeamPace']




# Abstracted feature building functions
def per_minute_stats(df, minute_col, stat_list):
    for stat in stat_list:
        df[stat + 'PerMinute'] = df[stat]/df[minute_col]



# Functions to be called from within GroupBy apply functions
def add_game_number(df, label):
    """
    Gets game number assuming a df is sorted by ascending date and we have a
    sing
    le element for 'label'. In other words, we assume we have already
    grouped by 'label' and we are calling this function inside an apply function
    """
    df[label + 'GameNumber'] = range(1,len(df)+1)

def add_rolling_averages(df, dictionary):
    """
    Gets rolling averages for each of the stats (represented by keys in
    'dictionary') for each time window (represented by the values in
    'dictionary'). Makes the assumption that we are calling this function inside
    an apply function where we have already grouped by 'label'
    """
    for key, value in dictionary.iteritems():
        for window in value:
            # Name of new feature
            name = 'Last' + str(window) + 'Average' + key

            # Drop column to prevent duplicates
            if name in df.columns:
                df.pop(name)

            # Get rolling average
            df[name] = df[key].rolling(window = window).mean().shift(1)

def add_exponential_smoothing(df, dictionary):
    for key, value in dictionary.iteritems():
        for window in value:
            # Name of new feature
            name = 'Last' + str(window) + 'ExponentialSmoothingAverage' + key

            # Drop column to prevent duplicates
            if name in df.columns:
                df.pop(name)

            # Get exponential smoothing rolling average
            df[name] = pd.ewma(df[key], halflife = window).shift(1)


def add_back_to_back(df):
    df['BackToBack'] = (df.Date + timedelta(days = 1)).shift(1) == df.Date
    df['BackToBackHome'] = ((df.BackToBack == True) & (df.Home == True))
    df['BackToBackAway'] = ((df.BackToBack == True) & (df.Home == False))
