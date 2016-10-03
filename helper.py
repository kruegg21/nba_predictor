import time
from datetime import timedelta
from stat_lists import *
import pandas as pd
import numpy as np
import scipy as sp

# Timing functions
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

# Data loading functions
def read_raw_player_data():
    return read_data('Raw/raw_player')

def read_raw_team_data():
    return read_data('Raw/raw_team')

@timeit
def read_player_data():
    return read_data('player')

@timeit
def read_team_data():
    return read_data('team')

@timeit
def read_merged_data():
    return read_data('merged')

def read_data(label):
    df = pd.read_csv('Data/' + label + '_data.csv')
    convert_to_datetime(df)
    return df


@timeit
def dump_player_data(df):
    dump(df, 'player')

@timeit
def dump_team_data(df):
    dump(df, 'team')

@timeit
def dump_merged_data(df):
    dump(df, 'merged')

def dump(df, label):
    df.to_csv('Data/' + label + '_data.csv', index = False)

# Diagnostic Functions
def print_count_nan(df):
    """
    Prints a Series with column names as the index and the number
    of NaN for each column
    """
    s = len(df.index) - df.count()
    for n_nan, col_name in zip(s, s.index):
        print col_name, n_nan
    print "\n"

def get_date_range(df):
    """
    Prints out the earliest and latest date from DataFrame
    """
    print "The latest date is: ", df.Date.max()
    print "The most recent date is: ", df.Date.min(), "\n"

def diagnostics(df, subject = None, columns = None):
    """
    1. Print out the number of rows and columns
    2. Prints first 10 entries
    3. Prints a list of all the count of NaN for each column
    4. Prints out stats for player or team
    """
    print "There are", len(df), "rows and", len(df.columns), "columns"

    if columns:
        print df[columns].head(10)
    else:
        print df.head(10)

    print_count_nan(df)

    if subject:
        if 'Player' in df.columns:
            if columns:
                print df[df.Player == subject][columns]
            else:
                print df[df.Player == subject]
        else:
            if columns:
                print df[df.Team == subject][columns]
            else:
                print df[df.Team == subject]

# Generic GroupBy
@timeit
def split_into_chunks(df, columns):
    return df[list(set(df.columns.values) - set(columns))], df[columns]

@timeit
def combine_chunks(df1, df2):
    return pd.concat([df1, df2], axis = 1)

# GroupBy Functions
def generic_group_by(df, function, cols, split_cols = None, split = False):
    if split:
        main, chunk = split_into_chunks(df, split_cols)
        del df
        return combine_chunks(main, chunk.groupby(cols,
                                                  sort = False).apply(function))
    else:
        return df.groupby(cols,
                          sort = False).apply(function)

# Data cleaning functions
def sort_by_date(df):
    df.sort_values('Date', inplace = True)
    df.reset_index(inplace = True, drop = True)

def convert_to_datetime(df):
    """
    Converts the 'Date' column to datetime
    """
    df['Date'] = pd.to_datetime(df.Date)

def remove_nan_rows(df, column):
    """
    Removes all rows with an NaN in 'column'
    """
    return df[pd.notnull(df[column])]

def remove_columns(df, columns):
    """
    Removes the columns in list 'columns'
    """
    df.drop(columns, axis = 1, inplace = True)

def make_position_numeric(df):
    df['Pos'] = df['Pos'].map(position_dictionary)

def make_dummys(df, column):
    return pd.get_dummies(df, columns = column, drop_first = False)

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
    df.rename(columns = {'Home_@': 'Away'}, inplace = True)


# Feature building functions
def add_season(df):
    df['Season'] = pd.DatetimeIndex(df['Date']).year
    df.ix[(pd.DatetimeIndex(df['Date']).month > 9), 'Season'] += 1

def add_player_per_minute_stats(df):
    per_minute_stats(df, 'PlayerMP', player_minute_adjusted_stats_list)

def add_fantasy_score(df):
    df['FanDuelScore'] = df.PlayerPTS + 1.2 * df.PlayerTRB + 1.5 * \
                         df.PlayerAST + 2 * df.PlayerBLK + 2 * \
                         df.PlayerSTL - df.PlayerTOV

def add_possessions(df):
    """
    Estimates the number of possesssions in a game using statistics from both
    teams
    """
    df['Possessions'] = 0.5 * ((df.TeamFGA + 0.44 * df.TeamFTA - 1.07 * \
                        (df.OppAllowedORB / (df.OppAllowedORB + df.OppDRB)) * \
                        (df.TeamFGA - df.TeamFG) + df.OppForcedTOV) + (df.OppFGA + \
                        0.44 * df.OppFTA - 1.07 * (df.OppORB / (df.OppORB + \
                        df.OppAllowedDRB)) * (df.OppFGA - df.OppFG) + df.OppTOV))
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
                        df.Last10AveragePlayerBLK + df.Last10AveragePlayerORB

def add_possession_adjusted_stats(df):
    for stat in opponent_possession_adjusted_stats_list:
        df[stat + 'PerPossession'] = df[stat]/df.Possessions


# Abstracted feature building functions
def per_minute_stats(df, minute_col, stat_list):
    for stat in stat_list:
        df[stat + 'PerMinute'] = df[stat]/df[minute_col]


# Functions to be called from within GroupBy apply functions
def add_game_number(df, label):
    """
    Gets game number assuming a df is sorted by ascending date and we have a
    single element for 'label'. In other words, we assume we have already
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
            df['Last' + str(window) + 'Average' + key] = \
                df[key].rolling(window = window).mean().shift(1)

def add_back_to_back(df):
    df['BackToBack'] = (df.Date + timedelta(days = 1)).shift(1) == df.Date
    df['BackToBackHome'] = ((df.BackToBack == True) & (df.Away == False))
    df['BackToBackAway'] = ((df.BackToBack == True) & (df.Away == True))
