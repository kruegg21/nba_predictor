import pandas as pd
import nba_scraper as ns
import build_xgboost_datasets as bxd
import nba_xgboost as nx
import build_final_dataset as bfd
import build_prediction_set as bps
import final_score as fs
import helper_functions as hf
import get_averages as ga
import numpy as np

def add_minutes_estimation(df, first_time):
	if not first_time:
		# add minute estimation data from 'minute_estimation.csv'
		min_est = pd.read_csv('minute_estimation.csv')
		min_est = min_est.sort_values(by = "Player")
		min_est.index = xrange(len(min_est.index))

		pred_set = df[df.loc[:,"Pred"] == 1]
		pred_set = pred_set.sort_values(by = "Player")
		pred_set.index = xrange(len(pred_set.index))
		df = df[df.loc[:,"Pred"] != 1]

		print min_est.MP
		print min_est.GS
		pred_set["MP"] = min_est.MP
		pred_set["GS"] = min_est.GS
		pred_set["NumPos"] = min_est.NumPos

		df = pd.concat([df, pred_set])
	else:
		df["New"] = 1

	# BUCKET MINUTES:
	# edit to put a cap on potential minutes!!!!!
	df["BucketedMin"] = (np.floor((df.MP - 1) / 6) * 6) + 3

	# CALCULATE MINUTE ADJUSTED EXPECTED STATS:
	# must first determine the time windows that work best for this
	df = hf.min_adjusted_stats(df, 'PTS')
	df = hf.min_adjusted_stats(df, 'AST')
	df = hf.min_adjusted_stats(df, 'DRB')
	df = hf.min_adjusted_stats(df, 'ORB')
	df = hf.min_adjusted_stats(df, 'TRB')
	df = hf.min_adjusted_stats(df, 'STL')
	df = hf.min_adjusted_stats(df, 'BLK')
	df = hf.min_adjusted_stats(df, 'TOV')

	# PRINT COLUMNS NAMES:
	for i in df.columns:
		print "\"" + i + "\","

	df = hf.calculate_game_number(df, "Player")

	return df

