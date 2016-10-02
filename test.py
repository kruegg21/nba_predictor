import pandas as pd
import helpers
import time
from datetime import timedelta

# Global lists and dictionaries to choose features to build
main_stat_list = ['ORB', 'DRB', 'TRB', 'AST', 'MP',
                  'STL', 'BLK', 'TOV', 'PTS']

player_minute_adjusted_stats_list = ['PlayerORB', 'PlayerDRB', 'PlayerTRB', 'PlayerAST',
                              'PlayerSTL', 'PlayerBLK', 'PlayerTOV', 'PlayerPTS']

opponent_possession_adjusted_stats_list = ['OppAllowedORB', 'OppAllowedDRB',
                                           'OppAllowedTRB', 'OppAllowedAST',
                                           'OppAllowedSTL', 'OppAllowedBLK',
                                           'OppForcedTOV', 'OppAllowedPTS']

player_rolling_mean_stat_dict = {'PlayerPTS' : [5,10,20],
                                 'PlayerAST' : [5,10,20],
                                 'PlayerBLK' : [5,10,20],
                                 'PlayerORB' : [5,10,20]}

opponent_rolling_mean_stat_dict = {'OppAllowedPTS': [5,10,20],
                                   'OppAllowedTRB': [5,10,20],
                                   'OppAllowedAST': [5,10,20],
                                   'OppAllowedBLK': [5,10,20],
                                   'OppForcedTOV': [5,10,20],
                                   'OppAllowedSTL': [5,10,20],
                                   'OppAllowedPTSPerPossession': [5,10,20]}

# Split lists
"""
Selecting only the necessary columns before a GroupBy can result in massive
speed ups. The following lists are the essential columns for certain GroupBy
operations
"""
starter_split_cols = ['IncompleteStarters', 'Date', 'Team', 'GS']
player_split_cols = ['Player'] + player_rolling_mean_stat_dict.keys()
opponent_split_cols = ['Opp'] + opponent_rolling_mean_stat_dict.keys()
team_season_split_cols = ['Team', 'Season']

# Miscellaneous Feature dictionaries and lists
position_dictionary = {'G': 1, 'C-F': 7, 'F': 4, 'F-G': 3, 'C': 8,
                       'F-C': 6, 'G-F': 2, 'PF': 5}





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
    return pd.read_csv('Data/Raw/raw_player_data.csv')

def read_raw_team_data():
    return pd.read_csv('Data/Raw/raw_team_data.csv')



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
    print "The latest date is: ", df['Date'].max()
    print "The most recent date is: ", df['Date'].min(), "\n"

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

@timeit
def add_team_change(df):
    return df.groupby(['Player', 'Team']).apply(GB_apply_add_changed_teams)

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
    df['Pace'] = 48 * ((df.Possessions * 2) / (2 * (df.TeamMP / 5)))

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

@timeit
def add_estimated_player_possessions(df):
    """
    Calculate estimated number of possessions played by each player for each
    game this stat is the heart of all later calculations. If we can estimate
    the number of minutes a player will play and the expected number of
    possessions a game will produce, we can estimate the number of possessions
    a player will take part in.
    """
    df["EstimatedPlayerPossessions"] = (df.PlayerMP / (df.TeamMP / 5)) * df.TeamPossessions


# Abstracted feature building functions
def per_minute_stats(df, minute_col, stat_list):
    for stat in stat_list:
        df[stat + 'PerMinute'] = df[stat]/df[minute_col]



# Functions for dividing and recombining DataFrames
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

@timeit
def group_by_player(df, split_cols = player_split_cols, split = False):
    return generic_group_by(df,
                            GB_apply_player_data,
                            ['Player'],
                            split_cols,
                            split)

@timeit
def group_by_player_season(df, split_cols = None, split = False):
    return generic_group_by(df,
                            GB_apply_player_season_data,
                            ['Player', 'Season'],
                            split_cols,
                            split)

@timeit
def group_by_team(df, split_cols = None, split = False):
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



# GroupBy apply functions
def GB_apply_player_data(df):
    add_game_number(df, 'Player')
    add_rolling_averages(df, player_rolling_mean_stat_dict)
    return df

def GB_apply_player_season_data(df):
    add_game_number(df, 'PlayerSeason')
    return df

def GB_apply_team_data(df):
    add_back_to_back(df)
    add_game_number(df, 'Team')
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

def GB_apply_add_changed_teams(df):
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

# Main blocks
@timeit
def build_player_data():
    # Read player data
    player_df = read_raw_player_data()
    convert_to_datetime(player_df)
    add_season(player_df)

    # Sort by 'Date'
    sort_by_date(player_df)

    # Edit column names
    make_better_player_column_names(player_df)

    # Removes a few data points with NaN for 'PTS' or 'MP'
    player_df = remove_nan_rows(player_df, 'PlayerPTS')
    player_df = remove_nan_rows(player_df, 'PlayerMP')

    # Make Position Numeric
    make_position_numeric(player_df)

    # Minute adjusted stats
    add_player_per_minute_stats(player_df)

    # Add FanDuel score
    add_fantasy_score(player_df)

    # Add team change
    player_df = add_team_change(player_df)

    # Group by player
    player_df = group_by_player(player_df, split = True)

    # Group by season
    player_df = group_by_player_season(player_df)

    # Drop certain columns
    remove_columns(player_df, ['Rank', 'Unnamed: 0', 'Home',
                               'Result', 'Season'])

    return player_df

@timeit
def build_team_data():
    # Read team data
    team_df = read_raw_team_data()
    convert_to_datetime(team_df)
    add_season(team_df)

    # Sort by 'Date'
    sort_by_date(team_df)

    # Make dummy variable out of 'Home' column
    team_df = make_dummys(team_df, ['Home'])

    # Edit column names
    make_better_team_column_names(team_df)

	# Add in Overtime column
    add_overtime(team_df)

    # Add in possessions and pace
    add_possessions(team_df)
    add_pace(team_df)

    # Calculate team per possessions stats
    add_possession_adjusted_stats(team_df)

    # Group by team
    team_df = group_by_team(team_df)

    # Group by season
    team_df = group_by_team_season(team_df, split = True)

    # Group by opponent
    team_df = group_by_opponent(team_df, split = True)

    # Add in result
    add_result(team_df)

    return team_df


if __name__ == "__main__":
    # # Build player data
    # player_df = build_player_data()
    # team_df = build_team_data()
    #
    # # Combine datasets
    # merged_df = player_df.merge(team_df,
    #                             how = 'inner',
    #                             on = ['Team', 'Opp', 'Date'])
    #
    # # Benchmark1
    # merged_df.to_csv('Data/benchmark1.csv', index = False)
    merged_df = pd.read_csv('Data/benchmark1.csv')

    # Add position metric
    add_position_metric(merged_df)

    # Group by starters
    group_by_starters(merged_df, split = True)

    # Dump incomplete starters
    incomplete_starteres = merged_df[merged_df['IncompleteStarters'] == True]

    # Add estimated player possesssions
    add_estimated_player_possessions(merged_df)
