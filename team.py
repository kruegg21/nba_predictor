from helper import *

@timeit
def build_basic_team_data(team_df):
    """
    Inputs:
        team_df -- DataFrame with player data without complex features
    Outputs:
        team_df -- DataFrame with player data with complex features built

    Build all the features and cleans all data for a set of team data. Does
    not build any features that require time series.
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
def build_time_series_team_data(team_df, train = True):
    """
    Input:
        team_df -- DataFrame with player data
    Output:
        team_df -- DataFrame with time series features built

    Builds all the time series data that requires grouping by various
    attributes.
    """
    # Group by team
    team_df = group_by_team(team_df, split = True)

    # Group by season
    team_df = group_by_team_season(team_df, split = True)

    # Group by opponent
    team_df = group_by_opponent(team_df, split = True)

    # Add estimated game possesssions
    add_estimated_game_pace(team_df, should_train_linear_model = train)

    return team_df
