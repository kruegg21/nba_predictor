# Global lists and dictionaries to choose features to build
main_stat_list = ['AST', 'MP', 'PTS']

main_stat_list_minus_minutes = list(set(main_stat_list) - set(['MP']))

opponent_possession_adjusted_stats_list = \
    ['OppForcedTOV' if stat == 'TOV' else 'OppAllowed' + stat \
      for stat in main_stat_list_minus_minutes]

player_rolling_mean_stat_dict = \
    dict([('Player' + stat, [5,10,20]) for stat in main_stat_list] + \
    [('Player' + stat + 'PerMinute', [5,10,20]) for stat in main_stat_list_minus_minutes])

player_post_merge_rolling_mean_stat_dict = \
    dict([('Player' + stat + 'PerPossession', [5,10,20]) \
    for stat in main_stat_list_minus_minutes])

opponent_rolling_mean_stat_dict = \
    dict([('OppAllowed' + stat, [5,10,20]) for stat in main_stat_list_minus_minutes] + \
    [('OppAllowedPTSPerPossession', [5,10,20]), ('OppPace', [5,10,30,31,32,33,34,35])])

team_rolling_mean_stat_dict = {'TeamPace': [5,10,30,31,32,33,34,35]}

pace_linear_model_window_list = [5, 10, 33]

# Feature container lists
"""
Groups feature containers based on the data they are associated with (team or
player)
"""
player_feature_container = [player_rolling_mean_stat_dict]
team_feature_container = [opponent_rolling_mean_stat_dict,
                          team_rolling_mean_stat_dict]

# Split lists
"""
Selecting only the necessary columns before a GroupBy can result in massive
speed ups. The following lists are the essential columns for certain GroupBy
operations
"""
starter_split_cols = ['IncompleteStarters', 'Date', 'Team', 'GS']
player_split_cols = ['Player'] + player_rolling_mean_stat_dict.keys()
player_post_merge_split_cols = ['Player'] + player_post_merge_rolling_mean_stat_dict.keys()
player_season_split_cols = ['Player', 'Season']
opponent_split_cols = ['Opp'] + opponent_rolling_mean_stat_dict.keys()
team_season_split_cols = ['Team', 'Season']
team_split_cols = ['Team', 'Home', 'Date'] + team_rolling_mean_stat_dict.keys()
player_team_split_cols = ['Player', 'Team']

# Miscellaneous Feature dictionaries and lists
position_dictionary = {'PG': 1, 'G': 1, 'C-F': 7, 'F': 4, 'F-G': 3, 'C': 8,
                       'F-C': 6, 'G-F': 2, 'PF': 5}

"""
Translates the team IDs from the format used in basketball reference to
the one used in FanDuel
"""
fd_to_br_team_translator = {'SA': 'SAS', 'GS': 'GSW', 'BKN': 'BRK',
                            'CHA': 'CHO', 'NY': 'NYK', 'NO': 'NOP'}

fd_to_br_player_translator = {'Brad Beal': 'Bradley Beal',
                              'Ishmael Smith': 'Ish Smith',
                              'Louis Williams': 'Lou Williams',
                              'Jose Juan Barea': 'J.J. Barea',
                              'Tim Hardaway Jr.': 'Tim Hardaway',
                              'Phil (Flip) Pressey': 'Phil Pressey'}

fd_to_br_position_translator = {'PG': 'G', 'SF' : 'G-F', 'SG' : 'G'}

"""
Prediction set columns. These are the columns to select from our prediction file
to add to full dataset.
"""
player_prediction_set_columns = ['Player', 'FanDuelId', 'Pos', 'Cost',
                                 'Team', 'Opp', 'Date', 'Home', 'New', 'Prediction']

team_prediction_set_columns = ['Team', 'Opp', 'Date', 'Home', 'New', 'Prediction']

"""
Path to FanDuel prediction files
"""
fd_files_path = 'Data/FanDuelFiles/'

"""
Minutes estimatino file list.
"""
minutes_estimation_file_list = ['Player', 'Date', 'Last1AveragePlayerMP',
                                'Last2AveragePlayerMP', 'Last3AveragePlayerMP',
                                'Last4AveragePlayerMP', 'Last5AveragePlayerMP',
                                'Last10AveragePlayerMP']
