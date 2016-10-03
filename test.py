import pandas as pd
import numpy as np
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore")
from helper import *
from stat_lists import *
from nba_scraper import *
from sklearn.linear_model import LinearRegression

@timeit
def get_new_data(df):
    most_recent_date = df.Date.max().strftime('%Y-%m-%d')
    scrape_new_data(most_recent_date)

@timeit
def add_estimated_game_pace(df):
    """
    Calculate the estimated for pace for a given game
    """
    # Make DataFrame out of columns that we want to use in pace linear model
    X = pd.DataFrame([func(df, window) for window in pace_linear_model_window_list
                          for func in [get_home_team_pace, get_away_team_pace]]).transpose()

    # Select only rows with no NaN values to train model
    y_train = (df.TeamPace)[np.all(np.isfinite(X), axis = 1)]
    X_train = X[np.all(np.isfinite(X), axis = 1)]

    # Train model
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    # Predict and make sure all NaN values stay NaN
    X.fillna(-99999, inplace = True)
    y = linear_model.predict(X)
    y[y < 0] = np.nan

    # Add to DataFrame
    df['EstimatedPace'] = y

# Get away team pace
def get_away_team_pace(df, window):
    return df.Away * df['Last' + str(window) + 'AverageTeamPace'] + \
           (1 - df.Away) * df['Last' + str(window) + 'AverageOppPace']

# Get home team pace
def get_home_team_pace(df, window):
    return df.Away * df['Last' + str(window) + 'AverageOppPace'] + \
            (1 - df.Away) * df['Last' + str(window) + 'AverageTeamPace']

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


# GroupBy Functions
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
def add_team_change(df):
    return df.groupby(['Player', 'Team']).apply(GB_apply_add_changed_teams)


# Main blocks
@timeit
def build_player_data():
    # Read player data
    player_df = read_raw_player_data()
    add_season(player_df)

    # Scrape all data since most recent date
    get_new_data(player_df)

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
    team_df = group_by_team(team_df, split = True)

    # Group by season
    team_df = group_by_team_season(team_df, split = True)

    # Group by opponent
    team_df = group_by_opponent(team_df, split = True)

    # Add estimated game possesssions
    add_estimated_game_pace(team_df)

    # Add in result
    add_result(team_df)

    return team_df

def full_flow(should_build_player_data = False,
              should_build_team_data = False,
              should_merge_sets = False,
              should_make_all = False):
    if should_build_player_data:
      # Build player data
      player_df = build_player_data()
      dump_player_data(player_df)

    if should_build_team_data:
      # Build team data
      team_df = build_team_data()
      dump_team_data(team_df)

    if should_merge_sets:
      # Read dumped data
      player_data = read_player_data()
      team_data = read_team_data()

      # Combine datasets
      merged_df = player_data.merge(team_data,
                                  how = 'inner',
                                  on = ['Team', 'Opp', 'Date'])
      dump_merged_data(merged_df)

    # Read merged data
    merged_df = read_merged_data()

    if should_make_all:
        # Add position metric
        add_position_metric(merged_df)

        # Group by starters
        group_by_starters(merged_df, split = True)

        # Dump incomplete starters
        incomplete_starteres = merged_df[merged_df['IncompleteStarters'] == True]

    # Use estimated pace to adjust player stats
    add_pace_adjusted_player_stats(merged_df)

    return merged_df



if __name__ == "__main__":
    df = full_flow(should_build_player_data = True,
                   should_build_team_data = False,
                   should_merge_sets = False,
                   should_make_all = False)

    df = df.select_dtypes(include=['float64','int64'])

    label = df.PlayerPTS.values
    data = df[list(set(df.columns) - set(['PlayerPTS']))].values

    x_pred = xgb.DMatrix(data[:10,:])

    dtrain = xgb.DMatrix(data, label = label)
    param = {'bst:max_depth':2, 'bst:eta':1, 'silent':1}
    bst = xgb.train(param, dtrain)
