# Global lists and dictionaries to choose features to build
main_stat_list = ['ORB', 'DRB', 'TRB', 'AST', 'MP',
                  'STL', 'BLK', 'TOV', 'PTS']

player_minute_adjusted_stats_list = ['PlayerORB', 'PlayerDRB', 'PlayerTRB',
                                     'PlayerAST', 'PlayerSTL', 'PlayerBLK',
                                     'PlayerTOV', 'PlayerPTS']

opponent_possession_adjusted_stats_list = ['OppAllowedORB', 'OppAllowedDRB',
                                           'OppAllowedTRB', 'OppAllowedAST',
                                           'OppAllowedSTL', 'OppAllowedBLK',
                                           'OppForcedTOV', 'OppAllowedPTS']

player_rolling_mean_stat_dict = {'PlayerPTS' : [5,10,20],
                                 'PlayerAST' : [5,10,20],
                                 'PlayerBLK' : [5,10,20],
                                 'PlayerORB' : [5,10,20],
                                 'PlayerMP' : [1,2,3,4,5,10]}

opponent_rolling_mean_stat_dict = {'OppAllowedPTS': [5,10,20],
                                   'OppAllowedTRB': [5,10,20],
                                   'OppAllowedAST': [5,10,20],
                                   'OppAllowedBLK': [5,10,20],
                                   'OppForcedTOV': [5,10,20],
                                   'OppAllowedSTL': [5,10,20],
                                   'OppAllowedPTSPerPossession': [5,10,20],
                                   'OppPace': [5,10,30,31,32,33,34,35]}

team_rolling_mean_stat_dict = {'TeamPace': [5,10,30,31,32,33,34,35]}

pace_linear_model_window_list = [5, 10, 33]

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
team_split_cols = ['Team', 'Away', 'Date'] + team_rolling_mean_stat_dict.keys()

# Miscellaneous Feature dictionaries and lists
position_dictionary = {'G': 1, 'C-F': 7, 'F': 4, 'F-G': 3, 'C': 8,
                       'F-C': 6, 'G-F': 2, 'PF': 5}
