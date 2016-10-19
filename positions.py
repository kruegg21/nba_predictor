from helper import add_position_metric
from read_write import read_merged_data
from sklearn.cluster import KMeans
from random_forest import select_features
import numpy as np

if __name__ == "__main__":
    df = read_merged_data()
    players = df.Player
    add_position_metric(df)

df.sort_values(['Position', 'PosMetric'], inplace = True)

g = df.groupby(by = ['Team', 'Date'])

for group in g:
    g_df = group[1]
    print g_df[(g_df.GS == True)][['Player', 'Team', 'Date']]
