import pandas as pd
import get_averages as ga
import numpy as np
import helper_functions as hf
import format_player_data as fpd
import format_team_data as ftd
import build_final_dataset as bfd
import add_minutes_estimation as ame
import time

def build_from_scratch(player_data_file_name, team_data_file_name, only_final_dataset):
	# LOAD FILES:
	print "STARTED BUILD FROM SCRATCH"
	t0 = time.time()

	player_data = None
	team_data = None

	if not only_final_dataset:
		player_data = pd.read_csv(player_data_file_name)
		team_data = pd.read_csv(team_data_file_name)
		t1 = hf.time_checkpoint(t0, t0, "READ IN PLAYER AND TEAM DATA")


		# UPKEEP:
		# some rows in raw data have missing values for PTS and MP
		player_data = player_data[player_data.PTS.notnull()]
		player_data = player_data[player_data.MP.notnull()]
		player_data.index = xrange(len(player_data.index))
		# print information about our raw data files
		hf.error_checking(player_data, 'RAW PLAYER DATA', 0)
		hf.error_checking(team_data, 'RAW TEAM DATA', 0)
		
		# MARK ALL AS NEW:
		player_data["New"] = 1	
		team_data["New"] = 1

		# BUILD DATASETS:
		player_data = fpd.format_player_data(player_data, 1)
		t2 = hf.time_checkpoint(t0, t1, "BUILT PLAYER DATA")
		player_data.to_csv('DataSets/FormattedData/formatted_player_data.csv', index = False)
		t3 = hf.time_checkpoint(t0, t2, "WROTE PLAYER DATA TO MEMORY")
		
		team_data = ftd.format_team_data(team_data, 1)
		t4 = hf.time_checkpoint(t0, t3, "BUILT TEAM DATA")
		team_data.to_csv('DataSets/FormattedData/formatted_team_data.csv', index = False)
		t5 = hf.time_checkpoint(t0, t4, "WROTE TEAM DATA TO MEMORY")
		# NA CHECK:
		# sanity check
		hf.check_na(player_data, 'format_player_data')
		hf.check_na(team_data, 'format_team_data')
	else:
		player_data = pd.read_csv('DataSets/FormattedData/formatted_player_data.csv')
		team_data = pd.read_csv('DataSets/FormattedData/formatted_team_data.csv')

	# BUILD FINAL DATASET:
	full_dataset = pd.DataFrame()
	final_dataset = bfd.build_final_dataset(player_data, team_data, full_dataset, 1)

	# dump to csv in case something fucks up in 'add_minute_estimation'
	final_dataset.to_csv('DataSets/FormattedData/formatted_final_data.csv')

	final_dataset = pd.read_csv('DataSets/FormattedData/formatted_final_data.csv')

	# sanity check to make sure all rows in final_dataset are marked as 'New'
	final_dataset["New"] = 1
	final_dataset = ame.add_minutes_estimation(final_dataset, 1)

	# UPKEEP:
	final_dataset.drop("New", 1, inplace = True)
	
	# DUMP:
	final_dataset.to_csv('DataSets/FormattedData/formatted_final_data.csv', index = False)

	# PRINT COLUMN NAMES:
	# used to know what columns are available for 
	hf.error_checking(final_dataset, 'FINAL DATASET BUILT FROM SCRATCH', 0)
	hf.check_na(final_dataset, 'final_dataset')
	for i in final_dataset.columns:
		print "\"" + i + "\","

player_data = 'DataSets/ScrapedData/raw_player_data_removed_incomplete_starters.csv'
team_data = 'DataSets/ScrapedData/raw_team_data.csv'

# (player_data_file_name, team_data_file_name, only_final_dataset)
build_from_scratch(player_data, team_data, 0)
