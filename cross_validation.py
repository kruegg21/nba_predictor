import pandas as pd
import numpy as np
from diagnostics import get_date_range
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import KFold
from datetime import datetime

# Dependent variable transformations
def log_transform(df, element):
    df[element] = np.log(df[element])

def log_reverse_transform(df, element):
    if isinstance(df, pd.DataFrame):
        df[element] = np.exp(df[element])
        return None
    else:
        return np.exp(df)

def power_transform(df, element):
    df[element] = df[element]**(1.5)
    df[element].fillna(0, inplace = True)

def power_reverse_transform(df, element):
    if isinstance(df, pd.DataFrame):
        df[element] = df[element].pow(float(1)/1.5)
    else:
        return df**(float(1)/1.5)

def no_transform(df, element):
    if isinstance(df, pd.DataFrame):
        return None
    else:
        return df


class cv_method(object):
    """
    Holds information about how to cross validate our models
    """
    def __init__(self,
                 method = None,
                 splits = 5,
                 start_date = '1999-01-01',
                 end_date = '2016-09-01',
                 minutes_cutoff = 3,
                 target_variable = 'FanDuelScore',
                 target_transformation = no_transform):
        assert (method in [time_series_cv, k_folds_cv]), \
            "Method must be 'time_series' or 'k_means'"
        self.method = method
        self.splits = splits
        self.start_date = start_date
        self.end_date = end_date
        self.minutes_cutoff = minutes_cutoff
        self.target_variable = target_variable
        self.target_transformation = target_transformation

        self.transform = None
        self.target_reverse_transformation = None
        if self.target_transformation == log_transform:
            self.transform = "log"
            self.target_reverse_transformation = log_reverse_transform
        elif self.target_transformation == power_transform:
            self.transform = "power"
            self.target_reverse_transformation = power_reverse_transform
        else:
            self.transform = ""
            self.target_reverse_transformation = no_transform

    def __str__(self):
        if self.method == time_series_cv:
            name = "Time Series"
        else:
            name = "K-Folds"

        if not self.transform:
            transform = "no"
        else:
            transform = self.transform
        return "{} from {} to {} with a minutes cutoff of {} and {} dependent \
                variable transform".format(name,
                                           self.start_date,
                                           self.end_date,
                                           self.minutes_cutoff,
                                           transform)


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
    splits = []
    for train, test in k.split(df.values):
        splits.append((train, test))
    return splits

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
