import pandas as pd

def create_minutes_estimation(player_df):
    # Filter out rows to only select those needed to build minutes estimation
    pred_player_df = filter_out_prediction(player_df)

    # Build features for minutes estimation
    pred_player_df = group_by_player(pred_player_df, split = True)

    # Select only prediction players
    pred_player_df = pred_player_df[pred_player_df.Prediction == True]

    # Select columns we want in our minute estimation file
    pred_player_df = pred_player_df[minutes_estimation_file_list]

    # Sort by team
    pred_player_df.sort_values('Team', inplace = True)

    # Add empty column to fill in minutes
    pred_player_df['PlayerMP'] = np.nan
    pred_player_df['GS'] = np.nan

    pred_player_df['PlayerMP'] = 30
    pred_player_df['GS'] = 1

    # Dump to 'minute_estimation_file.csv'
    pred_player_df.to_csv('minute_estimation_file.csv', index = False)

def read_minute_estimation(player_df):
    # Read file
    minute_estimation_df = pd.read_csv('minute_estimation_file.csv')

    # Put dummies in
    minute_estimation_df['PlayerMP'] = 30
    minute_estimation_df['GS'] = 1

    # Select essential rows from minutes estimation file
    minute_estimation_df = minute_estimation_df[['Player', 'PlayerMP', 'GS']]

    # Player
    prediction_player_df = player_df[player_df.Prediction == True]
    prediction_player_df.drop(['PlayerMP', 'GS'], axis = 1, inplace = True)
    prediction_player_df = prediction_player_df.merge(minute_estimation_df,
                                                      on = ['Player'])

    player_df = player_df[player_df.Prediction == False]

    player_df = stack_data_frames([player_df, prediction_player_df])

    return player_df
