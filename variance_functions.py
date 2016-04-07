import pandas as pd
import scipy.stats as st
import numpy as np
import xgboost as xgb
import helper_functions as hf
import math

# creates set of last 200 games to calculate variance and 
# dumps to 'variance_set.csv'

# passes variance set data to xgboost functions that runs
# xgboost for each of the main stats (pts, trb, stl, blk, tov, ast) 
# using the features specified in 'pts_col', 'reb_col', 'stl_col',
# 'blk_col', and 'tov_col'

# LOOK TO SPEED THIS UP IF POSSIBLE
def get_variance_set(df, pts_col, ast_col, reb_col, stl_col, blk_col, tov_col):
	# SORT BY PLAYER AND DATE:
	df = df.sort_values(by = ['Player', 'Date'])
	df.index = xrange(len(df.index))

	# get only games where a player has played for more than 20 minutes
	#df = df[df.MP > 20 | df.MP == -999]
	df = hf.calculate_game_number(df, 'Player')

	# GET LAST 40 GAMES:
	n = 40
	prediction_set = pd.DataFrame()
	for i in xrange(len(df.index)):
		print float(i) / len(df.index)
		if df.loc[i,"Pred"] == 1:
			r = n
			if df.loc[i,"PlayerGameNumber"] < n + 1:
				r = df.loc[i,"PlayerGameNumber"] - 1
			prediction_set = pd.concat([prediction_set, df.loc[i-r:i-1,:]])

	# DUMP:
	prediction_set.to_csv('variance_set.csv', index = False)

	# get actual FanDuel scores:
	actual_scores = prediction_set.FanDuelScore
	actual_scores.index = xrange(len(actual_scores.index))
	player_names = prediction_set.Player
	player_names.index = xrange(len(player_names.index))
	date = prediction_set.Date
	date.index = xrange(len(date.index))
	pgn = prediction_set.PlayerGameNumber
	pgn.index = xrange(len(pgn.index))

	# build properly formatted xgboost sets
	build_variance_xgboost_sets(prediction_set,  'PTS', 'point', pts_col)
	build_variance_xgboost_sets(prediction_set,  'AST', 'assist', ast_col)
	build_variance_xgboost_sets(prediction_set,  'TRB', 'rebound', reb_col)
	build_variance_xgboost_sets(prediction_set,  'STL', 'steal', stl_col)
	build_variance_xgboost_sets(prediction_set,  'BLK', 'block', blk_col)
	build_variance_xgboost_sets(prediction_set,  'TOV', 'turnover', tov_col)

	# run xgboost prediction
	xgboost_variance(actual_scores, player_names, date, pgn)

	return prediction_set

# builds the data sets in the correct format to pass into xgboost
# and dumps files to 'variance_statname_examples.csv' and 
# 'variance_statname_labels.csv'

# sort player_data by player and date and rename indexes
def build_variance_xgboost_sets(player_data, stat, stat_name, columns):
	nrows = len(player_data.index)
	player_data = hf.calculate_game_number(player_data, "Player")
	player_data = player_data.sort_values(by = ["Player","Date"])
	player_data.index = xrange(nrows)

	##############################################
	# UPKEEP (ELIMINATE):
	if "Home_x" in player_data.columns:
		player_data["Home"] = player_data.Home_x
		player_data = player_data.drop("Home_x",1)
	##############################################

	# pick dataset with only relevent columns
	player_data = player_data.loc[:,columns]
	player_data.index = xrange(len(player_data.index))
	
	# upkeep
	player_data = player_data.drop("Pred",1)
	player_data = player_data.drop("Player",1)

	label = player_data.loc[:,stat]
	player_data = player_data.drop(stat,1)

	# dump
	label_file_name = 'variance_' + str(stat_name) + '_labels.csv'
	examples_file_name = 'variance_' + str(stat_name) + '_examples.csv'

	label.to_csv(label_file_name, index = False)
	player_data.to_csv(examples_file_name, index = False)

# runs xgboost on the datasets created by 'build_xgboost_variance_sets'

# 1. creates a dataframe 'scores' where n is the set of all games in 
# the variance set and m is each of the predicted statistical categories
# 2. calculates the total predicted score for each row and adds in the 
# actual scores, player, date, and pgn as columns
# 3. divides into groups based on player and calculates standard
# deviation of each set and dumps to 'variance_scores.csv'

def xgboost_variance(actual_scores, player_names, date, pgn):
	stat_list = ['point','rebound','turnover','steal','assist','block']
	scores = pd.DataFrame()
	for i in stat_list:
		examples = pd.read_csv('variance_' + i + '_examples.csv')
		examples = examples.as_matrix()
		examples[examples < 0] = -999
		examples[examples > 99800] = -999
		dpredict = xgb.DMatrix(examples, missing = -999)
		bst = xgb.Booster({'nthread':4}) #init model
		bst.load_model(i + '.model')
		ypred = bst.predict(dpredict)
		scores[i] = ypred

	scores['total'] = scores.point + 1.2 * scores.rebound + 1.5 * scores.assist + \
					  2 * scores.block + 2 * scores.steal - scores.turnover

	scores['actual'] = actual_scores
	scores['Player'] = player_names
	scores['date'] = date
	scores['pgn'] = pgn

	scores['abs_error'] = scores.actual - scores.total

	# group by player and calculate standard deviation
	grouped = scores.groupby('Player')
	var = pd.DataFrame(columns = ['Player','STD'])
	for i in grouped:
		player = i[1].sort_values(by = 'actual')
		player.index = xrange(len(player.index))
		std = i[1].loc[:,'abs_error'].std()
		player = player.loc[0].Player
		var = var.append(pd.DataFrame(data = [[player, std]], columns = ['Player','STD']))

	var.to_csv('variance_scores.csv', index = False)

'''
# calculate variance on normalized FanDuelScore for each player
# in prediction set using variance set
def calculate_variance():
	# CREATE VARIANCE SET:
	final_score = read.csv('final_score.csv')
	variance_set = get_variance_set(final_score)

	# PREDICT ON EACH

	variance_set = variance_set.sort_values('Player','Date')
	stat_list = ['point','rebound','turnover','steal','assist','block']
	for j in stat_list:
		# FORMATTING AND UPKEEP:
		variance_set = variance_set.as_matrix()
		variance_set[variance_set < 0] = -999
		variance_set[variance_set > 99800] = -999
		dpredict = xgb.DMatrix(variance_set, missing = -999)

		# LOAD PREVIOUS MODEL:
		bst = xgb.Booster({'nthread':4}) #init model
		bst.load_model(str(j) + '.model')

		# PREDICTS:
		ypred = bst.predict(dpredict)

		# dumps prediction set to 'stat_prediction.csv'
		# set contains 'Player' and 'stat' column
		prediction_output = pd.DataFrame()	
		prediction_output["Player"] = player
		prediction_output[j] = ypred
		prediction_output_name = str(j) + '_variance_prediction.csv'
		prediction_output.to_csv(str(prediction_output_name), index = False)


	for i in grouped:
		print i
'''
