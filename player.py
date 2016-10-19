from helper import *

@timeit
def build_basic_player_data(player_df):
    """
    Inputs:
        player_df -- DataFrame with player data without complex features
    Outputs:
        player_df -- DataFrame with player data with complex features built

    Build all the features and cleans all data for a set of player data. Does
    not build any features that require time series.
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
    # add_fantasy_score(player_df)

    # Drop certain columns
    remove_columns(player_df, ['Rank', 'Unnamed: 0', '2P%', '3P%',
                               'FG%', 'FT%', 'Result', 'GmSc'])

    return player_df

@timeit
@subset
def build_time_series_player_data(player_df):
    """
    Input:
        player_df -- DataFrame with player data
    Output:
        player_df -- DataFrame with time series features built

    Builds all the time series data that requires grouping by various
    attributes. Wrapper function subsets the data to only include players with an
    instance of a new date.
    """
    # Group by player and team
    player_df = group_by_player_team(player_df, split = True)

    # Group by season
    player_df = group_by_player_season(player_df, split = True)

    # Group by player
    player_df = group_by_player(player_df, split = True)

    return player_df
