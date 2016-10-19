import xgboost as xgb
import matplotlib
import numpy as np
import csv
import pandas as pd

#
# Runs xgboost on datasets built to prediction on stat
# specified in 'stat'. Parameters are passed in the 'parameters'
# argument as a dictionary list like the following:
#
#			{'bst:max_depth':5, 
#			 'bst:eta':0.01, 
#			 'silent':1, 
#			 'gamma':0.5,
#			 'lambda':0.5,
#			 'subsample':0.3,
#			 'colsample_bytree':0.3
#			 }
#

def nba_xgboost(parameters, stat):
	# open all needed files
	training_set_name = 'DataSets/XgboostSets/final_' + str(stat) + '_train.csv'
	training_set_labels_name = 'DataSets/XgboostSets/final_' + str(stat) + '_train_label.csv'
	cv_set_name = 'DataSets/XgboostSets/final_' + str(stat) + '_cv.csv'
	cv_set_label_name = 'DataSets/XgboostSets/final_' + str(stat) + '_cv_label.csv'
	prediction_set_name = 'DataSets/XgboostSets/' + str(stat) + '_prediction_set.csv'

	prediction_set = pd.read_csv(prediction_set_name)
	player = prediction_set["Player"]

	# HACK TO SEE IF WE HAVE ANY PLAYERS THAT HAVE DIFFERENT NAME SPELLINGS
	# in the future, could check prediction set with our current data to
	# see if our player is having a 'fist game.' Also, keep track of 
	# player name changes so as to match basketballrefernce names

	prediction_set = prediction_set.drop("Player",1)

	dm_train = np.loadtxt(open(training_set_name,'rb'), delimiter = ",", skiprows = 1)
	labels_train = np.loadtxt(open(training_set_labels_name,'rb'), delimiter = ",")
	dm_cv = np.loadtxt(open(cv_set_name,'rb'), delimiter = ",", skiprows = 1)
	labels_cv = np.loadtxt(open(cv_set_label_name,'rb'), delimiter = ",")
	prediction_set = prediction_set.as_matrix()

	# replace all instances of N/A with common value
	dm_train[dm_train < 0] = -999
	dm_train[dm_train > 998000] = -999

	prediction_set[prediction_set < 0] = -999
	prediction_set[prediction_set > 99800] = -999

	dm_cv[dm_cv < 0] = -999
	dm_cv[dm_cv > 998000] = -999

	# create training set and cross validation set
	dtrain = xgb.DMatrix(dm_train, label = labels_train, missing = -999)
	dtest = xgb.DMatrix(dm_cv, label = labels_cv, missing = -999)
	dpredict = xgb.DMatrix(prediction_set, missing = -999)

	# create cross validation set
	evallist  = [(dtrain,'train'), (dtest,'eval')]

	# set parameters
	# Result of first grid search
	# Score: 5.904164 (5, 0.01, 0.5, 0.5, 0.25, 0.5)
	# Score (with assists): 5.915168

	param = parameters

	# runs xgboost for 10000 rounds at most with early stopping if
	# cv error does not decrease after 100 rounds
	num_round = 10000
	bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds = 50)
	num_round = bst.best_iteration

	# combines training and cross validation sets and reruns 
	# xgboost with the optimal number of iterations
	dm_train_plus_cv = np.concatenate((dm_train, dm_cv), axis = 0)
	dm_train_plus_cv_label = np.concatenate((labels_train, labels_cv), axis = 0)
	dtrain_cv = xgb.DMatrix(dm_train_plus_cv, label = dm_train_plus_cv_label, missing = -999)
	bst = xgb.train(param, dtrain_cv, num_round)

	# dump model
	bst.save_model(str(stat) + '.model')

	# makes predictions for our prediciton set
	ypred = bst.predict(dpredict)

	# dumps prediction set to 'stat_prediction.csv'
	# set contains 'Player' and 'stat' column
	prediction_output = pd.DataFrame()	
	prediction_output["Player"] = player
	prediction_output[stat] = ypred
	prediction_output_name = 'DataSets/ScoresLineups/' + str(stat) + '_prediction.csv'
	prediction_output.to_csv(str(prediction_output_name), index = False)

def xgboost_previous_model(stat):
	# LOAD PREDICTION SET:
	prediction_set_name = 'DataSets/XgboostSets/' + str(stat) + '_prediction_set.csv'
	prediction_set = pd.read_csv(prediction_set_name)
	player = prediction_set["Player"]

	prediction_set = prediction_set.drop("Player",1)

	# FORMATTING AND UPKEEP:
	prediction_set = prediction_set.as_matrix()
	prediction_set[prediction_set < 0] = -999
	prediction_set[prediction_set > 99800] = -999
	dpredict = xgb.DMatrix(prediction_set, missing = -999)

	# LOAD PREVIOUS MODEL:
	bst = xgb.Booster({'nthread':4}) #init model
	bst.load_model('XgboostModels/' + str(stat) + '.model')

	# PREDICTS:
	ypred = bst.predict(dpredict)

	# dumps prediction set to 'stat_prediction.csv'
	# set contains 'Player' and 'stat' column
	prediction_output = pd.DataFrame()	
	prediction_output["Player"] = player
	prediction_output[stat] = ypred
	prediction_output_name = 'DataSets/ScoresLineups/' + str(stat) + '_prediction.csv'
	prediction_output.to_csv(str(prediction_output_name), index = False)

# Runs xgboost boost on a particular 'stat' and for set of 'parameters'.
# Displays the cross validation and training error, but does not predict
# or dump the model
def xgboost_test(parameters, stat):
	# open all needed files
	training_set_name = 'DataSets/XgboostSets/final_' + str(stat) + '_train.csv'
	training_set_labels_name = 'DataSets/XgboostSets/final_' + str(stat) + '_train_label.csv'
	cv_set_name = 'DataSets/XgboostSets/final_' + str(stat) + '_cv.csv'
	cv_set_label_name = 'DataSets/XgboostSets/final_' + str(stat) + '_cv_label.csv'

	dm_train = np.loadtxt(open(training_set_name,'rb'), delimiter = ",", skiprows = 1)
	labels_train = np.loadtxt(open(training_set_labels_name,'rb'), delimiter = ",")
	dm_cv = np.loadtxt(open(cv_set_name,'rb'), delimiter = ",", skiprows = 1)
	labels_cv = np.loadtxt(open(cv_set_label_name,'rb'), delimiter = ",")

	# replace all instances of N/A with common value
	dm_train[dm_train < 0] = -999
	dm_train[dm_train > 998000] = -999

	dm_cv[dm_cv < 0] = -999
	dm_cv[dm_cv > 998000] = -999

	# create training set and cross validation set
	dtrain = xgb.DMatrix(dm_train, label = labels_train, missing = -999)
	dtest = xgb.DMatrix(dm_cv, label = labels_cv, missing = -999)

	# create cross validation set
	evallist  = [(dtrain,'train'), (dtest,'eval')]

	# set parameters
	# Result of first grid search
	# Score: 5.904164 (5, 0.01, 0.5, 0.5, 0.25, 0.5)
	# Score (with assists): 5.915168

	param = parameters

	# runs xgboost for 10000 rounds at most with early stopping if
	# cv error does not decrease after 100 rounds
	num_round = 10000
	bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds = 50)
	num_round = bst.best_iteration
