import numpy as np
import pandas as pd

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
