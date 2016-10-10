import warnings
warnings.filterwarnings("ignore")
import time
from datetime import timedelta
from stat_lists import *
import pandas as pd
import numpy as np
import scipy as sp
from os import walk
from datetime import datetime

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




# Data loading functions
def read_raw_player_data():
    df = read_data('Raw/raw_player')
    mark_new(df)
    return df

def read_raw_team_data():
    df = (read_data('Raw/raw_team'))
    mark_new(df)
    return df

def read_new_player_data():
    df = read_data('new_player')
    mark_new(df)
    return df

def read_new_team_data():
    df = read_data('new_team')
    mark_new(df)
    return df

def read_player_prediction_data():
    """
    Data will be marked 'New' and 'Prediction'
    in 'read_prediction_data' function
    """
    return read_prediction_data('player')

def read_team_prediction_data():
    """
    Data will be marked 'New' and 'Prediction'
    in 'read_prediction_data' function
    """
    return read_prediction_data('team')

def read_player_data():
    """
    Reads and return 'player_data.csv' if it exists and 'Raw/raw_player.csv'
    if not.
    """
    return read_data('player', 'Raw/raw_player')

def read_team_data():
    """
    Reads and returns 'team_data.csv' if it exists and 'Raw/raw_team.csv'
    if not.
    """
    return read_data('team', 'Raw/raw_team')

def read_merged_data():
    return read_data('merged')

def read_fan_duel_file(file_name):
    df = pd.read_csv(file_name)
    mark_new(df)
    return df

# Abstracted data loading functions
def read_data(label, backup_label = None):
    # Read in data
    try:
        df = pd.read_csv('Data/' + label + '_data.csv')
        convert_to_datetime(df)
        unmark_pred(df)
        unmark_new(df)
    except:
        df = pd.read_csv('Data/' + backup_label + '_data.csv')
        convert_to_datetime(df)
        unmark_pred(df)
        mark_new(df)

    # Rename certain columns to make names universal
    if label[-4:] == 'team':
        make_better_team_column_names(df)
    else:
        make_better_player_column_names(df)
    return df




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






# Functions to make prediction data
"""
Reads FanDuel file and makes the data compatible
"""
def make_team_prediction_data():
    return make_prediction_data('team')

def make_player_prediction_data():
    return make_prediction_data('player')

def make_prediction_data(label):
    file_name = find_fd_filename()

    # Read in fd file
    df = read_fan_duel_file(file_name)

    # Find home
    df['Home'] = np.where(df.Team == df.apply(lambda x: x.Game.split('@')[0], \
                                                  axis = 1), False, True)

    # Rename columns
    df.rename(columns = {'Opponent': 'Opp',
                         'Salary': 'Cost',
                         'Id': 'FanDuelId'}, inplace = True)
    # Get date
    df['Date'] = get_fd_file_date(file_name)

    # Translate team names
    translate_team_names(df)

    # Get full player name
    if label == 'player':
        df['Player'] = (df['First Name'] + str(' ') + df['Last Name'])
        translate_player_names(df)
        translate_position_names(df)
        mark_new(df)
        mark_pred(df)
        return df[player_prediction_set_columns]

    if label == 'team':
        # Select only one row per game
    	df.drop_duplicates(subset = ['Team', 'Opp', 'Date'], inplace = True)
        mark_new(df)
        mark_pred(df)
        return df[team_prediction_set_columns]





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
Looks in data/FanDuel directory to find the most recent file name or date
"""
@timeit
def find_fd_filename():
    """
    Seaches the directory specified in 'fd_files_path' for the fd
    file with the latest date associated with it.
    """
    for root, dirs, files in walk(fd_files_path):
        return fd_files_path + str(files[np.argmax([get_fd_file_date(f) for f in files])])

def get_fd_file_date(file_name):
    """
    Gets the date from a fd file name string
    """
    return datetime.strptime(file_name.split('NBA')[1][1:11], '%Y-%m-%d')





# Dumping data functions
@timeit
def dump_player_data(df):
    dump(df, 'player')

@timeit
def dump_team_data(df):
    dump(df, 'team')

@timeit
def dump_merged_data(df):
    dump(df, 'merged')

# Abstracted dumping data function
def dump(df, label):
    # Removes 'New' and 'Prediction'
    df = remove_prediction_data(df)
    unmark_new(df)

    # Prints info on data before dumping
    print "Number of elements in ", label, len(df)

    # Dumps
    df.to_csv('Data/' + label + '_data.csv', index = False)

    # Remove DataFrame from memory
    del df




# Selects or removes prediction data
"""
Removes/selects prediction data from DataFrame
"""
def remove_prediction_data(df):
    return df[df.Prediction == False]

def select_prediction_data(df):
    return df[df.Prediction == True]



# Diagnostic Functions
def print_count_nan(df):
    """
    Prints a Series with column names as the index and the number
    of NaN for each column
    """
    s = len(df.index) - df.count()
    for n_nan, col_name in zip(s, s.index):
        if n_nan != 0:
            print col_name, n_nan
    print "\n"

def print_new_pred_counts(df, label):
    """
    Prints the counts of rows that are new and prediction
    """
    print "The number of new in", label, "is", np.sum(df.New == True)
    print "The number of prediction in", label, "is", np.sum(df.Prediction == True)
    print "\n"

def get_date_range(df):
    """
    Prints out the earliest and latest date from DataFrame
    """
    print "The latest date is: ", df.Date.max()
    print "The most recent date is: ", df.Date.min(), "\n"

def print_player_data_duplicates(df):
    # print df[df.duplicated(subset = ['Player', 'Date'], keep = False)][['Player', 'Date', 'Team']]
    print "The number of duplicate entries is: ", np.sum(df.duplicated(subset = ['Player', 'Date']))

def print_duplicate_indices(df):
    print df[df.index.duplicated()]

def diagnostics(df, subject = None, columns = None):
    """
    1. Print out the number of rows and columns
    2. Prints first 10 entries
    3. Prints out date range
    4. Prints number of duplicate player/date sets
    5. Prints out number of new and prediction
    6. Prints a list of all the count of NaN for each column
    7. Prints out stats for player or team
    """
    print "There are", len(df), "rows and", len(df.columns), "columns"

    if columns:
        print df[columns].head(10)
    else:
        print df.head(5)

    get_date_range(df)

    print_player_data_duplicates(df)

    print_new_pred_counts(df, '')

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
    if not ((np.any(df.Home) == False) | (np.any(df.Home) == True)):
        df['Home'] = pd.isnull(df.Home)

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

def add_possessions_played(df):
    """
    Estimates the number of possessions played for a player by multiplying the
    fraction of miniutes played by the total number of possessions
    """
    df['PlayerPossessionsPlayed'] = (df.PlayerMP / (df.TeamMP / 5)) * df.Possessions

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
            # Drop column to prevent duplicates
            if 'Last' + str(window) + 'Average' + key in df.columns:
                df.pop('Last' + str(window) + 'Average' + key)

            # Get rolling average
            df['Last' + str(window) + 'Average' + key] = \
                df[key].rolling(window = window).mean().shift(1)

def add_back_to_back(df):
    df['BackToBack'] = (df.Date + timedelta(days = 1)).shift(1) == df.Date
    df['BackToBackHome'] = ((df.BackToBack == True) & (df.Home == True))
    df['BackToBackAway'] = ((df.BackToBack == True) & (df.Home == False))
