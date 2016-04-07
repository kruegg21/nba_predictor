import pandas as pd
import helper_functions as hf
import build_final_dataset as bfd
import build_prediction_set as bps

def build_toy_set():
	# FILE AND DATE FOR PREDICTION SET
	file = 'FanDuelFiles/FanDuel-NBA-2016-02-27-14807-players-list.csv'
	date = '2016-02-27'
	'''
	# SELECTS ONLY RECENT GAMES AND DUMPS TO:
	# 'player_dataset_toy.csv' and 'team_dateset_toy.csv'
	player_data = pd.read_csv('ScrapedData/raw_player_data.csv')
	team_data = pd.read_csv('ScrapedData/raw_team_data.csv')
	new_player_data = pd.DataFrame()
	new_team_data = pd.DataFrame()

	bps.build_prediction_set(file, date)
	prediction_set_team = pd.read_csv('prediction_set_team.csv')
	prediction_set_player = pd.read_csv('prediction_set_player.csv')

	player_data = hf.add_numeric_date(player_data)
	team_data = hf.add_numeric_date(team_data)

	player_data_toy = player_data.loc[player_data.NumericDate > 5786]
	team_data_toy = team_data.loc[team_data.NumericDate > 5786]

	player_data_toy.to_csv('raw_player_dataset_toy.csv')
	team_data_toy.to_csv('raw_team_dataset_toy.csv')

	data = bfd.add_new_data(new_team_data, new_player_data, team_data_toy, player_data_toy,  prediction_set_team, prediction_set_player)
	full_player_data = data[0]
	full_team_data = data[1]
	full_player_data.to_csv('full_player_data.csv', index = False)
	full_team_data.to_csv('full_team_data.csv', index = False)
	'''

	full_player_data = pd.read_csv('full_player_data.csv')
	full_team_data = pd.read_csv('full_team_data.csv')

	final_dataset = bfd.build_final_dataset(full_player_data, full_team_data,  0)
	final_dataset.to_csv('full_final_data.csv', index = False)

	full_data = hf.merge_team_and_player_sets(player_data, team_data)
	full_data_toy = full_data.loc[full_data.NumericDate > 5786]

	full_data_toy.to_csv('full_dataset_toy.csv', index = False)


build_toy_set()

