import pandas as pd
import numpy as np
from diagnostics import get_date_range
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import KFold
from datetime import datetime

class cv_method(object):
    """
    Holds information about how to cross validate our models
    """
    def __init__(self, method, splits, start_date, end_date, minutes_cutoff):
        assert (method in ['time_series', 'k_means']), \
            "Method must be 'time_series' or 'k_means'"
        self.method = method
        self.splits = splits
        self.start_date = start_date
        self.end_date = end_date
        self.minutes_cutoff = minutes_cutoff

    def __str__(self):
        if self.method == 'time_series':
            name = "Time Series"
        else:
            name = "K-Folds"
        return "{} from {} to {} with a minutes cutoff of " \
            .format(name, self.start_date, self.end_date, self.minutes_cutoff)

def time_series_cv(df, n_splits = 5, verbose = False):
    # Global date range
    if verbose:
        print "Total date range: "
        helper.get_date_range(df)
        print "\n"

    # Get numpy array of unique dates
    unique_dates = df.Date.unique()

    # Make model
    tscv = TimeSeriesSplit(n_splits = n_splits)

    # Create splits and loop through them
    splits = []
    for train_index, test_index in tscv.split(df.Date.unique()):
        # Run model on test and train set
        if verbose:
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

        train_indices = np.argwhere(df.Date.isin(unique_dates[train_index])).flatten()
        test_indices = np.argwhere(df.Date.isin(unique_dates[test_index])).flatten()
        splits.append((train_indices, test_indices))
    return splits

def k_folds_cv(df, n_splits = 5, verbose = False):
    k = KFold(n_splits = n_splits)
    k.fit(df.values)
    splits = []
    for train, test in k.split(df.values):
        splits.append((train, test))
    return splits

def filter_training_set(df, cv_method):
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
    # Turn date limits to Datetime
    begin_date = datetime.strptime(cv_method.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(cv_method.end_date, '%Y-%m-%d')

    # Filter based on date limits
    df = df[(df.Date > cv_method.start_date) & (df.Date < cv_method.end_date)]

    # Filter based on minutes played
    return df[df.BucketedMinutes >= cv_method.minutes_cutoff]

if __name__ == "__main__":
    from read_write import read_merged_data
    df = read_merged_data()
    # pre_subset_length = len(df)
    # # df, description = filter_training_set(df, '1999-01-01', '2016-09-01', 3)
    # post_subset_length = len(df)
    #
    # # print description
    # print float(post_subset_length)/pre_subset_length
    #
    # print time_series_cv(df)
