import pandas as pd
import numpy as np
from diagnostics import get_date_range
from sklearn.model_selection import TimeSeriesSplit
from datetime import datetime

def time_series_cv(df, n_splits = 5):
    # Global date range
    # print "Total date range: "
    # helper.get_date_range(df)
    # print "\n"

    # Get numpy array of unique dates
    unique_dates = df.Date.unique()

    # Make model
    tscv = TimeSeriesSplit(n_splits = n_splits)

    # Create splits and loop through them
    splits = []
    for train_index, test_index in tscv.split(df.Date.unique()):
        # Run model on test and train set
        print "Train set date range: "
        get_date_range(df[df.Date.isin(unique_dates[train_index])])
        print "Train set length: "
        print len(df[df.Date.isin(unique_dates[train_index])])
        print "\n"

        print "Test set date range: "
        get_date_range(df[df.Date.isin(unique_dates[test_index])])
        print "Test set length: "
        print len(df[df.Date.isin(unique_dates[test_index])])
        print "\n"

        print "Test to train set ratio: "
        print len(df[df.Date.isin(unique_dates[test_index])]) / \
              float(len(df[df.Date.isin(unique_dates[train_index])]))
        print "\n\n"

        train_indices = np.argwhere(df.Date.isin(unique_dates[train_index]))
        test_indices = np.argwhere(df.Date.isin(unique_dates[test_index]))
        splits.append([train_indices, test_indices])

    return splits

def filter_training_set(df, begin_date, end_date, minutes_cutoff):
    """
    Input:
        df -- DataFrame of data
        begin_date -- string of the lower bound date
        end_date -- string of the upper bound date
        minutes_cutoff -- int of lower bound for bucketed minutes

    Output:
        DataFrame that can then be passed to time_series cv

    Filters our DataFrame to dates between 'begin_date' and 'end_date' and
    players who have played more minutes than 'minutes_cutoff'
    """
    # Turn date bookends to Datetime
    begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Filter based on date limits
    df = df[(df.Date > begin_date) & (df.Date < end_date)]

    # Filter based on minutes played
    df =  df[df.BucketedMinutes >= minutes_cutoff]

    # Log
    set_description = "CV ranges from {} to {} with a cutoff at {} bucketed minutes" \
                      .format(begin_date, end_date, minutes_cutoff)

    return df, set_description


if __name__ == "__main__":
    from read_write import read_merged_data
    df = read_merged_data()
    pre_subset_length = len(df)
    # df, description = filter_training_set(df, '1999-01-01', '2016-09-01', 3)
    post_subset_length = len(df)

    # print description
    print float(post_subset_length)/pre_subset_length

    print time_series_cv(df)
