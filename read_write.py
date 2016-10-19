from helper import *
import pandas as  pd

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

def read_prediction_data():
    return read_data('prediction')

def read_final_score_data():
    return read_data('final_score')

def read_fan_duel_file(file_name):
    df = pd.read_csv(file_name)
    translate_team_names(df)
    mark_new(df)
    return df


# Abstracted data loading functions
def read_data(label, backup_label = None):
    # Read in data
    try:
        df = pd.read_csv('data/' + label + '_data.csv')
        convert_to_datetime(df)
        unmark_pred(df)
        unmark_new(df)
    except:
        df = pd.read_csv('data/' + backup_label + '_data.csv')
        convert_to_datetime(df)
        unmark_pred(df)
        mark_new(df)

    # Rename certain columns to make names universal
    if label[-4:] == 'team':
        make_better_team_column_names(df)
    else:
        make_better_player_column_names(df)
    return df



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

@timeit
def dump_prediction_data(df):
    dump(df, 'prediction')

# Abstracted dumping data function
def dump(df, label):
    # Removes 'New' and 'Prediction'
    if label != 'prediction':
        df = remove_prediction_data(df)

    if label != 'score':
        unmark_new(df)

    # Prints info on data before dumping
    print "Number of elements in ", label, len(df)

    # Dumps
    if label != 'score':
        suffix = '_data'
    else:
        suffix = ''
    df.to_csv('data/{}{}.csv'.format(label, suffix), index = False)

    # Remove DataFrame from memory
    del df



# Read and write pickled model
def load_pickled_model(model_name):
    """
    Inputs:
        model_name -- string of model that we want to open
    Output:
        model -- sklearn object of a model
    """

    with open('models/{}.obj'.format(model_name), 'r') as f:
        model = pickle.load(f)
    return model

def dump_pickled_model(model, model_name):
    """
    Inputs:
        model -- sklearn Object that we want to pickle
        model_name -- string of the name of model we want to pickle
    Outputs:
        None
    """

    with open('models/{}.obj'.format(model_name), 'w+') as f:
        pickle.dump(model, f)



# Read prediction data
def make_team_prediction_data():
    return make_prediction_data('team')

def make_player_prediction_data():
    return make_prediction_data('player')

def make_prediction_data(label):
    file_names = find_fd_filenames()

    # Read all FanDuel files
    df = pd.DataFrame()
    for f in file_names:
        df = stack_data_frames([df, read_fan_duel_file(f)])

    # Find home
    df['Home'] = np.where(df.Team == df.apply(lambda x: x.Game.split('@')[0], \
                                                  axis = 1), False, True)

    # Get FanDuel player Id
    get_player_id(df)

    # Drop duplicate player Id
    df.drop_duplicates('PlayerID', inplace = True)

    # Rename columns
    df.rename(columns = {'Opponent': 'Opp',
                         'Salary': 'Cost'}, inplace = True)
    # Get date
    df['Date'] = get_fd_file_date(file_names[0])

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
