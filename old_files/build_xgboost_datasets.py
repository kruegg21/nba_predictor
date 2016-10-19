import pandas as pd
import numpy as np
import helper_functions as hf

def build_xgboost_datasets(player_data, stat, stat_name, columns, rebuild_xgboost):
	# sort player_data by player and date and rename indexes
	nrows = len(player_data.index)
	player_data = player_data.sort_values(by = ["Player","Date"])
	player_data.index = xrange(nrows)

	##############################################
	# UPKEEP (ELIMINATE):
	if "Home_x" in player_data.columns:
		player_data["Home"] = player_data.Home_x
		player_data = player_data.drop("Home_x",1)
	##############################################

	# pick dataset with only relevent columns
	f_point_dataset = player_data.loc[:,columns]
	f_point_dataset.index = xrange(len(f_point_dataset.index))
	
	# remove prediction data 
	prediction_set = f_point_dataset[f_point_dataset.Pred == 1]
	prediction_set = prediction_set.drop("Pred",1)
	prediction_set = prediction_set.drop(stat,1)

	f_point_dataset.drop(f_point_dataset[f_point_dataset.Pred == 1].index, inplace = True)
	f_point_dataset = f_point_dataset.drop("Pred",1)
	f_point_dataset = f_point_dataset.drop("Player",1)

	# DIVIDE INTO TRAIN AND CV:
	# 80-20 splits (can also hard code date)
	f_point_dataset = f_point_dataset.sort_values(by = 'NumericDate')
	nrows = len(f_point_dataset.index)
	f_point_dataset.index = xrange(nrows)

	# 80-20
	f_point_cv = f_point_dataset.iloc[int(np.floor(nrows * .8)):]
	f_point_train = f_point_dataset.iloc[:int(np.floor(nrows * .8))]
	# hard code a date
	#f_point_cv = f_point_dataset[f_point_dataset.NumericDate > 5464]
	#f_point_train = f_point_dataset[f_point_dataset.NumericDate <= 5464]

	# get labels for both cross validation and training sets
	f_point_cv_label = f_point_cv.loc[:,stat]
	f_point_train_label = f_point_train.loc[:,stat]

	# remove label from train and cross validation sets
	f_point_train = f_point_train.drop(stat,1)
	f_point_cv = f_point_cv.drop(stat,1)

	prediction_set_file_name = 'DataSets/XgboostSets/' + str(stat_name) + '_prediction_set.csv'
	cv_set_file_name = 'DataSets/XgboostSets/final_' + str(stat_name) + '_cv.csv'
	train_set_file_name = 'DataSets/XgboostSets/final_' + str(stat_name) + '_train.csv'
	cv_set_label_file_name = 'DataSets/XgboostSets/final_' + str(stat_name) + '_cv_label.csv'
	train_set_label_file_name = 'DataSets/XgboostSets/final_' + str(stat_name) + '_train_label.csv'

	prediction_set.to_csv(prediction_set_file_name, index = False)
	if rebuild_xgboost:
		f_point_cv.to_csv(cv_set_file_name, index = False)
		f_point_train.to_csv(train_set_file_name, index = False)
		f_point_cv_label.to_csv(cv_set_label_file_name, index = False)
		f_point_train_label.to_csv(train_set_label_file_name, index = False)

	return

# reads the changes made in 'minute_estimation.csv' and updates the
# predictions sets for each stat without having to rebuild all the
# columns of the prediction set

# make sure to update any feature that is dependent on either MP of GS here

def xgboost_dataset_quick_minute_update(min_est):
	stat_list = ['point','assist','turnover','block','rebound','steal']

	for i in stat_list:
		prediction_set_file_name = 'DataSets/XgboostSets/' + i + '_prediction_set.csv'
		prediction_set = pd.read_csv(prediction_set_file_name)
		prediction_set = prediction_set.sort_values(by = 'Player')
		prediction_set.index = xrange(len(prediction_set.index))
		prediction_set["BucketedMin"] = (np.floor((min_est.MP - 1) / 6) * 6) + 3
		prediction_set["GS"] = min_est.GS
		prediction_set = hf.min_adjusted_stats(prediction_set, 'PTS')
		prediction_set = hf.min_adjusted_stats(prediction_set, 'AST')
		prediction_set = hf.min_adjusted_stats(prediction_set, 'DRB')
		prediction_set = hf.min_adjusted_stats(prediction_set, 'ORB')
		prediction_set = hf.min_adjusted_stats(prediction_set, 'TRB')
		prediction_set = hf.min_adjusted_stats(prediction_set, 'STL')
		prediction_set = hf.min_adjusted_stats(prediction_set, 'BLK')
		prediction_set = hf.min_adjusted_stats(prediction_set, 'TOV')
		prediction_set.to_csv(prediction_set_file_name, index = False)



