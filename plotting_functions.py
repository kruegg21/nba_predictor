import time
from datetime import timedelta
from stat_lists import *
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# Plotting
def eda_plotting(df, stat_container, selection_function):
    for key, value in stat_container.iteritems():
        for window in value:
            # Create our x and y
            x, y = selection_function(window, key, value)

            # Scatter plot and print out correlation
            scatter_plot_eda(df, x, y)


def scatter_plot_eda(df, x, y):
    # Select columns of interest and remove any NaN
    df2 = df[[x, y]]
    df2 = df2[np.isfinite(df2.iloc[:,0])]

    # Find linear correlation
    print "Correlation between " + x + \
          " and " + y, sp.stats.pearsonr(df2.iloc[:,0], df2.iloc[:,1])

    # Find proportion of data points NaN
    print "Proportion of data points that are NaN: ", 1 - (float(len(df2)) / len(df))

    # Scatter a random selection of 200 points
    random_indices = np.random.randint(0,len(df2),200)
    plt.scatter(df2.iloc[random_indices,0], df2.iloc[random_indices,1])
    plt.xlabel(df2.columns.values[0])
    plt.ylabel(df2.columns.values[1])
    plt.show()
