import pandas as pd
import get_averages as ga
import numpy as np
import helper_functions as hf
import format_team_data as ftd
import format_player_data as fpd
import time
import warnings
warnings.filterwarnings('ignore')

# BUILD FLOW:
# if this is the first time:
# 1. Read new player data and team data in 
#    'player_data_new.csv' and 'team_data_new.csv'
# 2. Read old player data_


def build_final_dataset(player_data, team_data, full_dataset, first_time, 
						only_offensive_load):
	############################################################################
	# PREPROCESSING:

	# start time
	t0 = time.time()
	tp = t0

	# day list
	day_list = [1,2,3,5,10,20,30,40,50]

	# merge datasets
	final_dataset = pd.DataFrame()
	final_dataset = hf.merge_team_and_player_sets(player_data, team_data)
	del player_data, team_data

	# add numberic date
	final_dataset = hf.remove_duplicate_columns(final_dataset)
	final_dataset = hf.add_numeric_date(final_dataset)
	tp = hf.time_checkpoint(t0, tp, "ADDED NUMERIC DATE")

	# error check
	# hf.error_checking(final_dataset, 'MERGED PLAYER AND TEAM IN BFD', 0)
	# hf.check_na(final_dataset, 'merged_player_team_bfd')

	# remove and rename overlapping columns from merge
	final_dataset = hf.remove_duplicate_columns(final_dataset)
	full_dataset = hf.remove_duplicate_columns(full_dataset)
	tp = hf.time_checkpoint(t0, tp, "MERGED TEAM AND PLAYER")

	if not first_time:
		# SHRINK DATASET TO MAKE COMPUTATION FASTER:
		# error check before we shrink dataset
		#hf.error_checking(final_dataset, 'FINAL DATASET PRE-SHRINK', 0)
		#hf.check_na(final_dataset, 'final_set_pre_shrink')

		# set all new data as 'New'
		new_data = final_dataset[final_dataset.New == 1]

		# take a slice of data only recent enough to be necessary to calculate
		# the averages that we want
		recent_data = full_dataset[full_dataset.NumericDate > 5749]
		recent_data["New"] = 0
		recent_data["Pred"] = 0

		# combine our new data and our recent data to create small set
		final_dataset = pd.concat([recent_data, new_data])
		final_dataset = final_dataset.drop("PlayerGameNumber",1)
		final_dataset = hf.calculate_game_number(final_dataset, "Player")
		final_dataset = hf.remove_duplicate_columns(full_dataset)

		# error check our shrunk down dataset
		# hf.error_checking(final_dataset, 'FINAL DATASET POST-SHRINK', 0)
		# hf.check_na(final_dataset, 'final_set_post_shrink')
	tp = hf.time_checkpoint(t0, tp, "SHRUNK DATASETS")
	final_dataset = hf.sort_and_reindex(final_dataset, ['Player','Date'])
	############################################################################

	######################################################################################
	# PLAYER STATS PER POSSESSION PLAYED STATS:
	# calculate estimated number of possessions played by each player for each game
	# this stat is the heart of all our calculations. if we can estimate the number
	# of minutes a player will play and the expected number of possessions a game will
	# produce, we can estimate the number of possessions a player will take part in

	# takes the fraction of time spent on the floor and multiplies it by the total 
	# number of team possessions
	if not only_offensive_load:
		df = final_dataset[['Player','Date','NumericDate','PlayerGameNumber','MP','TeamMP','TeamPossessions',
							'PTS','AST','TRB','DRB','ORB','BLK','STL','TOV']]

		df["EstimatedPlayerPossessions"] = (df.MP / (df.TeamMP / 5)) * df.TeamPossessions

		# calculate expected stats per possession played by player (possessions and minute adjusted)
		df["PlayerPTSPerPossPlayed"] = df.PTS / df.EstimatedPlayerPossessions
		df["PlayerASTPerPossPlayed"] = df.AST / df.EstimatedPlayerPossessions
		df["PlayerTRBPerPossPlayed"] = df.TRB / df.EstimatedPlayerPossessions
		df["PlayerDRBPerPossPlayed"] = df.DRB / df.EstimatedPlayerPossessions
		df["PlayerORBPerPossPlayed"] = df.ORB / df.EstimatedPlayerPossessions
		df["PlayerBLKPerPossPlayed"] = df.BLK / df.EstimatedPlayerPossessions
		df["PlayerSTLPerPossPlayed"] = df.STL / df.EstimatedPlayerPossessions
		df["PlayerTOVPerPossPlayed"] = df.TOV / df.EstimatedPlayerPossessions

		# get averages
		df = ga.get_averages(df, "PlayerPTSPerPossPlayed", "", "PlayerGameNumber", day_list, first_time) 
		df = ga.get_averages(df, "PlayerASTPerPossPlayed", "", "PlayerGameNumber", day_list, first_time) 
		df = ga.get_averages(df, "PlayerTRBPerPossPlayed", "", "PlayerGameNumber", day_list, first_time) 
		df = ga.get_averages(df, "PlayerORBPerPossPlayed", "", "PlayerGameNumber", day_list, first_time) 
		df = ga.get_averages(df, "PlayerDRBPerPossPlayed", "", "PlayerGameNumber", day_list, first_time) 
		df = ga.get_averages(df, "PlayerBLKPerPossPlayed", "", "PlayerGameNumber", day_list, first_time) 
		df = ga.get_averages(df, "PlayerSTLPerPossPlayed", "", "PlayerGameNumber", day_list, first_time) 
		df = ga.get_averages(df, "PlayerTOVPerPossPlayed", "", "PlayerGameNumber", day_list, first_time)

		# get over/under performance metric for points
		# OverUnderPTS = L40PlayerPTSPerPossPlayed - PlayerPTSPerPossPlayed
		df["OverUnderPTS"] = df.PlayerPTSPerPossPlayed - \
							 df.L40PlayerPTSPerPossPlayed
							 
		df.loc[df.OverUnderPTS < -900, "OverUnderPTS"] = -999

		# dump and delete frame
		df.to_csv('DataSets/player_stats_per_possessions_played.csv', index = False)
		tp = hf.time_checkpoint(t0, tp, "CALCULATED ESTIMATED STATS PER POSSESSION PLAYED") 
	######################################################################################

	######################################################################################
	# PLAYER STATS PER TEAM POSSESSION STATS:
	# can likely be replaced by stats per possessions played. these stats are essentially
	# a worse version of the above stats
	if (not only_offensive_load):
		# single game
		final_dataset["PlayerPTSPerPoss"] = final_dataset.PTS / final_dataset.TeamPossessions
		final_dataset["PlayerASTPerPoss"] = final_dataset.AST / final_dataset.TeamPossessions
		final_dataset["PlayerTRBPerPoss"] = final_dataset.TRB / final_dataset.TeamPossessions
		final_dataset["PlayerDRBPerPoss"] = final_dataset.DRB / final_dataset.TeamPossessions
		final_dataset["PlayerORBPerPoss"] = final_dataset.ORB / final_dataset.TeamPossessions
		final_dataset["PlayerBLKPerPoss"] = final_dataset.BLK / final_dataset.TeamPossessions
		final_dataset["PlayerSTLPerPoss"] = final_dataset.STL / final_dataset.TeamPossessions
		final_dataset["PlayerTOVPerPoss"] = final_dataset.TOV / final_dataset.TeamPossessions

		# averages
		final_dataset = hf.sort_and_reindex(final_dataset, ['Player','Date'])
		final_dataset = ga.get_averages(final_dataset, "PlayerPTSPerPoss", "", "PlayerGameNumber", day_list, first_time)
		final_dataset = ga.get_averages(final_dataset, "PlayerASTPerPoss", "", "PlayerGameNumber", day_list, first_time)
		final_dataset = ga.get_averages(final_dataset, "PlayerDRBPerPoss", "", "PlayerGameNumber", day_list, first_time)
		final_dataset = ga.get_averages(final_dataset, "PlayerTRBPerPoss", "", "PlayerGameNumber", day_list, first_time)
		final_dataset = ga.get_averages(final_dataset, "PlayerORBPerPoss", "", "PlayerGameNumber", day_list, first_time)
		final_dataset = ga.get_averages(final_dataset, "PlayerSTLPerPoss", "", "PlayerGameNumber", day_list, first_time)
		final_dataset = ga.get_averages(final_dataset, "PlayerBLKPerPoss", "", "PlayerGameNumber", day_list, first_time)
		final_dataset = ga.get_averages(final_dataset, "PlayerTOVPerPoss", "", "PlayerGameNumber", day_list, first_time)
	######################################################################################

	######################################################################################
	# PACE ADJUSTED EXPECTED STATS:
	# StatPerPossession * ExpectedPossessions
	# assumes L30PaceTot is the best indicator of pace
	if not only_offensive_load:
		pts = df.loc[:,["L" + str(i) + "PlayerPTSPerPossPlayed" for i in day_list]]
		pts["L30PaceTot"] = final_dataset.L30PaceTot
		pts["PTS"] = final_dataset.PTS
		pts = hf.get_expected_stats(pts, "PlayerPTS", "PerPossPlayed")
		pts = pts.drop(["L" + str(i) + "PlayerPTSPerPossPlayed" for i in day_list] + ["L30PaceTot"],1)

		ast = df.loc[:,["L" + str(i) + "PlayerASTPerPossPlayed" for i in day_list]]
		ast["L30PaceTot"] = final_dataset.L30PaceTot
		ast["AST"] = final_dataset.AST
		ast = hf.get_expected_stats(ast, "PlayerAST", "PerPossPlayed")
		ast = ast.drop(["L" + str(i) + "PlayerASTPerPossPlayed" for i in day_list] + ["L30PaceTot"],1)

		trb = df.loc[:,["L" + str(i) + "PlayerTRBPerPossPlayed" for i in day_list]]
		trb["L30PaceTot"] = final_dataset.L30PaceTot
		trb["TRB"] = final_dataset.TRB
		trb = hf.get_expected_stats(trb, "PlayerTRB", "PerPossPlayed")
		trb = trb.drop(["L" + str(i) + "PlayerTRBPerPossPlayed" for i in day_list] + ["L30PaceTot"],1)

		orb = df.loc[:,["L" + str(i) + "PlayerORBPerPossPlayed" for i in day_list]]
		orb["L30PaceTot"] = final_dataset.L30PaceTot
		orb["ORB"] = final_dataset.ORB
		orb = hf.get_expected_stats(orb, "PlayerORB", "PerPossPlayed")
		orb = orb.drop(["L" + str(i) + "PlayerORBPerPossPlayed" for i in day_list] + ["L30PaceTot"],1)

		drb = df.loc[:,["L" + str(i) + "PlayerDRBPerPossPlayed" for i in day_list]]
		drb["L30PaceTot"] = final_dataset.L30PaceTot
		drb["DRB"] = final_dataset.DRB
		drb = hf.get_expected_stats(drb, "PlayerDRB", "PerPossPlayed")
		drb = drb.drop(["L" + str(i) + "PlayerDRBPerPossPlayed" for i in day_list] + ["L30PaceTot"],1)

		stl = df.loc[:,["L" + str(i) + "PlayerSTLPerPossPlayed" for i in day_list]]
		stl["L30PaceTot"] = final_dataset.L30PaceTot
		stl["STL"] = final_dataset.STL
		stl = hf.get_expected_stats(stl, "PlayerSTL", "PerPossPlayed")
		stl = stl.drop(["L" + str(i) + "PlayerSTLPerPossPlayed" for i in day_list] + ["L30PaceTot"],1)

		blk = df.loc[:,["L" + str(i) + "PlayerBLKPerPossPlayed" for i in day_list]]
		blk["L30PaceTot"] = final_dataset.L30PaceTot
		blk["BLK"] = final_dataset.BLK
		blk = hf.get_expected_stats(blk, "PlayerBLK", "PerPossPlayed")
		blk = blk.drop(["L" + str(i) + "PlayerBLKPerPossPlayed" for i in day_list] + ["L30PaceTot"],1)

		tov = df.loc[:,["L" + str(i) + "PlayerTOVPerPossPlayed" for i in day_list]]
		tov["L30PaceTot"] = final_dataset.L30PaceTot
		tov["TOV"] = final_dataset.TOV
		tov = hf.get_expected_stats(tov, "PlayerTOV", "PerPossPlayed")
		tov = tov.drop(["L" + str(i) + "PlayerTOVPerPossPlayed" for i in day_list] + ["L30PaceTot"],1)

		# combine sets and dump to csv
		df2 = pd.concat([pts, ast, trb, orb, drb, stl, blk, tov], 1)
		df2.to_csv('DataSets/expected_player_stats_per_possessions_played.csv', index = False)

		final_dataset = pd.concat([final_dataset, df2], axis = 1)
		del df2, pts, ast, trb, drb, orb, stl, blk, tov

		final_dataset = hf.get_expected_stats(final_dataset, "PlayerPTS", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "PlayerAST", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "PlayerTRB", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "PlayerORB", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "PlayerDRB", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "PlayerSTL", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "PlayerBLK", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "PlayerTOV", "PerPoss")

		# OppGivenUpTeamPTSPerPoss calculated in 'format_team_data' module
		final_dataset = hf.get_expected_stats(final_dataset, "OppGivenUpTeamPTS", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "OppGivenUpTeamAST", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "OppGivenUpTeamTRB", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "OppGivenUpTeamORB", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "OppGivenUpTeamDRB", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "OppGivenUpTeamSTL", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "OppGivenUpTeamBLK", "PerPoss")
		final_dataset = hf.get_expected_stats(final_dataset, "OppGivenUpTeamTOV", "PerPoss")

		tp = hf.time_checkpoint(t0, tp, "CALCULATED PACE ADJUSTED STATS")
	######################################################################################

	######################################################################################
	# GET PLAYER POSITION:
	# first sorts by numeric position and then uses 'PosMetric' to estimate based on
	# stats what position the player is

	if not only_offensive_load:
		# select appropriate columns
		positional = final_dataset[['Player','Team','GS','Opp','NumPos','Date','OppGameNumber','PTS']]
		positional["PlayerPTSPerPossPlayed"] = df.PlayerPTSPerPossPlayed
		positional["OverUnderPTS"] = df.OverUnderPTS

		# SELECT ONLY PLAYERS WITH NON-NA VALUE FOR OVER UNDER PTS
		positional = positional[positional.OverUnderPTS != -999]
		positional = hf.calculate_game_number(positional, 'Opp')

		# calculate 'PosMetric'
		positional["PosMetric"] = - final_dataset.L10PlayerAST - final_dataset['3PA'] + 2 * \
									 final_dataset.L10PlayerBLK + final_dataset.L10PlayerORB

		# select only starters
		positional = positional[positional.GS == 1]

		# label positions
		positional = positional.sort_values(by = ['Date','Team','NumPos', 'PosMetric'])
		positional.index = xrange(len(positional.index))
		num_games = len(positional.index) / 5
		positional["Position"] = range(1,6) * num_games

		# divide into starter spots
		one_spot = positional[positional.Position == 1]
		two_spot = positional[positional.Position == 2]
		three_spot = positional[positional.Position == 3]
		four_spot = positional[positional.Position == 4]
		five_spot = positional[positional.Position == 5]

		one_spot = one_spot.sort_values(by = ["Opp","Date"])
		one_spot.index = range(0,len(one_spot.index))
		one_spot = ga.get_averages(one_spot, "PlayerPTSPerPossPlayed", "OppPositional", "OppGameNumber", day_list, first_time)
		one_spot = ga.get_averages(one_spot, "OverUnderPTS", "OppPositional", "OppGameNumber", day_list, first_time)

		
		two_spot = two_spot.sort_values(by = ["Opp","Date"])
		two_spot.index = range(0,len(two_spot.index))
		two_spot = ga.get_averages(two_spot, "PlayerPTSPerPossPlayed", "OppPositional", "OppGameNumber", day_list, first_time)
		two_spot = ga.get_averages(two_spot, "OverUnderPTS", "OppPositional", "OppGameNumber", day_list, first_time)

		three_spot = three_spot.sort_values(by = ["Opp","Date"])
		three_spot.index = range(0,len(three_spot.index))
		three_spot = ga.get_averages(three_spot, "PlayerPTSPerPossPlayed", "OppPositional", "OppGameNumber", day_list, first_time)
		three_spot = ga.get_averages(three_spot, "OverUnderPTS", "OppPositional", "OppGameNumber", day_list, first_time)

		four_spot = four_spot.sort_values(by = ["Opp","Date"])
		four_spot.index = range(0,len(four_spot.index))
		four_spot = ga.get_averages(four_spot, "PlayerPTSPerPossPlayed", "OppPositional", "OppGameNumber", day_list, first_time)
		four_spot = ga.get_averages(four_spot, "OverUnderPTS", "OppPositional", "OppGameNumber", day_list, first_time)

		five_spot = five_spot.sort_values(by = ["Opp","Date"])
		five_spot.index = range(0,len(five_spot.index))
		five_spot = ga.get_averages(five_spot, "PlayerPTSPerPossPlayed", "OppPositional", "OppGameNumber", day_list, first_time)
		five_spot = ga.get_averages(five_spot, "OverUnderPTS", "OppPositional", "OppGameNumber", day_list, first_time)

		# vertically concat all positions
		df = pd.concat([one_spot, two_spot, three_spot, four_spot, five_spot])

		# drop unnecessary columns
		df = df.drop(['PlayerPTSPerPossPlayed','OppGameNumber'],1)

		# set all the averages that were calculated using a -999 to -999

		# dump to csv
		df.to_csv('PositionalDatasets/combined_positional_full.csv', index = False)

		if first_time:
			one_spot.to_csv('PositionalDatasets/one_spot_full.csv', index = False)
			two_spot.to_csv('PositionalDatasets/two_spot_full.csv', index = False)
			three_spot.to_csv('PositionalDatasets/three_spot_full.csv', index = False)
			four_spot.to_csv('PositionalDatasets/four_spot_full.csv', index = False)
			five_spot.to_csv('PositionalDatasets/five_spot_full.csv', index = False)
		del one_spot, two_spot, three_spot, four_spot, five_spot, df

		tp = hf.time_checkpoint(t0, tp, "CALCULATED POSITION STATS")
	######################################################################################

	######################################################################################
	# GET OFFENSIVE LOAD STATS:
	# the number of shots a player takes relative to the total shots of the team is a good
	# proxy for how much a player is relied on to take an offensive burden
	# this formula is an adjusted version of the usage rate formula, with turnovers removed
	#
	# Usg% Usage Percentage (available since the 1977-78 season in the NBA); 
	# the formula is:
	#
	# 100 * ((FGA + 0.44 * FTA + TOV) * (Tm MP / 5)) / (MP * (Tm FGA + 0.44 * Tm FTA + Tm TOV)). 
	#
	# Usage percentage is an estimate of the percentage of team plays used by a player while he 
	# was on the floor.

	# name is changed to be compatible with current model (real name is 'Usg%')
	final_dataset["Usg%"] = ((final_dataset.FGA + 0.44 * final_dataset.FTA) * (final_dataset.TeamMP / 5)) / \
								 (final_dataset.MP * (final_dataset.TeamFGA + 0.44 * final_dataset.TeamFTA))

	final_dataset = hf.sort_and_reindex(final_dataset, ['Player','Date'])
	final_dataset = ga.get_averages(final_dataset, "Usg%", "", "PlayerGameNumber", day_list, first_time)

	# calculate percent of team shots
	final_dataset["PercTeamShots"] = (final_dataset.FGA + final_dataset.FTA) / (final_dataset.TeamFGA + final_dataset.TeamFTA)
	final_dataset = ga.get_averages(final_dataset, "PercTeamShots", "", "PlayerGameNumber", day_list, first_time)


	# calculate estimated Usg% and PercTeamShots based on lineup changes
	# subsample dataset
	df = final_dataset[['FGA','FTA','TeamMP','MP','TeamFGA','TeamFTA',
						'Date','PTS','Team','Player','GS','PlayerGameNumber']]

	# select out starters and get adjusted usage
	# usage is adjusted based on which players are going to start a game, 
	# with the idea that if a star player rests, there is more usage for 
	# other players to use
	starters = df[df.GS == 1]

	# get starter FTA
	n_play = 5
	column = 'FTA'
	starters = hf.sort_and_reindex(starters, ['Team','Date'])


	col = starters[column]
	starters["Avg" + column] = pd.rolling_mean(starters.loc[:,column], n_play)
	every_nth = starters.loc[:,'Avg' + column].ix[[(n_play * (i + 1)) - 1 for i in range((len(starters.index)/n_play))]]
	every_nth = every_nth * n_play
	starters["Starter" + column] = [i for i in every_nth for j in range(n_play)]

	# get starter FGA
	column = 'FGA'
	starters = starters.sort_values(by = ['Team','Date'])
	starters.index = xrange(len(starters.index))
	col = starters.loc[:,column]
	starters["Avg" + column] = pd.rolling_mean(starters.loc[:,column], n_play)
	every_nth = starters.loc[:,'Avg' + column].ix[[(n_play * (i + 1)) - 1 for i in range((len(starters.index)/n_play))]]
	every_nth = every_nth * n_play
	starters["Starter" + column] = [i for i in every_nth for j in range(n_play)]

	starters['PercStartersShots'] = (starters.FGA + 0.44 * starters.FTA) / (starters.StarterFGA + 0.44 * starters.StarterFTA)

	starters = hf.calculate_game_number(starters, 'Player')
	starters = hf.sort_and_reindex(starters, ['Player','Date'])
	starters = ga.get_averages(starters, "PercStartersShots", "", "PlayerGameNumber", day_list, first_time)

	# paramters
	# time window of perc of starters shots to use
	# value to replace n/a with
	# correlation between ExpectedL10PercStartersShots and PercStartersShots, followed
	# by the number of examples still available
	# (L10, -999) -> 0.768097, 148885/188025

	# (L20, -999) -> 0.771311, 122755/188025
	# (L30, -999) -> 0.724116, 188025/188025
	#
	#
	column = 'L30PercStartersShots'
	starters = hf.get_expected_usage(starters, column, 5, -999)

	# add in expected stats and fill in empty cells (non-starters) with -999
	starters = starters[['Player', 'Date', 'PercStartersShots', column, 'Expected' + column,
						 'Excess' + column, 'Total' + column]]
	starters.to_csv('DataSets/starters_usage.csv', index = False)


	# select out bench players to get usage
	bench = df[df.GS == 0]

	df = df.merge(starters, on = ['Player','Date'], how = 'left')
	df = df.fillna(-999)

	# dump
	df.to_csv('DataSets/usage_set.csv', index = False)

	tp = hf.time_checkpoint(t0, tp, "CALCULATED USAGE STATS")
	######################################################################################

	# COMBINE ALL FEATURES BUILT

	# BUILD DATASET TO COUNTER SHRINKING DONE IN ADD NEW DATA
	if not first_time:
		new_data = final_dataset[final_dataset.loc[:,"New"] == 1]
		full_dataset["Pred"] = 0
 		final_dataset = pd.concat([full_dataset, new_data])
 		final_dataset = hf.calculate_game_number(final_dataset, 'Player')
 		hf.error_checking(final_dataset, 'FINAL DATASET ANTI-SHRINK', 1)
		hf.check_na(final_dataset, 'final_set_anti_shrink')
	else:
		# print out all the columns
		for column in final_dataset.columns:
			print "\"" + column + "\","

	return final_dataset

def add_new_data(team_data, player_data, old_team_data, old_player_data, current_dataset,
				 pred_team_data, pred_player_data):
	# LABEL NEW AND PRED:
	# new
	team_data["New"] = 1
	player_data["New"] = 1
	pred_player_data["New"] = 1
	pred_team_data["New"] = 1
	old_player_data["New"] = 0
	old_team_data["New"] = 0
	current_dataset["New"] = 0

	# pred
	team_data["Pred"] = 0
	player_data["Pred"] = 0
	pred_player_data["Pred"] = 1
	pred_team_data["Pred"] = 1
	old_player_data["Pred"] = 0
	old_team_data["Pred"] = 0
	current_dataset["Pred"] = 0

	# COMBINE SETS:
	full_dataset_team = pd.concat([old_team_data, pred_team_data, team_data])
	hf.error_checking(full_dataset_team, "COMBINED TEAM OLD, NEW, PREDICTION", 0)
	full_dataset_team.index = xrange(len(full_dataset_team.index))
	full_dataset_player = pd.concat([old_player_data, pred_player_data, player_data])
	hf.error_checking(full_dataset_player, "COMBINED PLAYER OLD, NEW, PREDICTION", 0)

	# TRANSFER POS AND AGE FROM OLD DATASET DATA TO NEW
	#
	#  TO DO
	#
	#
	#

	# upkeep
	full_dataset_team = hf.remove_duplicate_columns(full_dataset_team)
	full_dataset_player = hf.remove_duplicate_columns(full_dataset_player)

	# add numeric data
	full_dataset_team = hf.add_numeric_date(full_dataset_team)
	full_dataset_player = hf.add_numeric_date(full_dataset_player)

	# SHRINK DATASET TO MAKE COMPUTATION MORE MANAGABLE:
	# sample only data from 2015 on
	full_dataset_team_recent = full_dataset_team[full_dataset_team.NumericDate > 5650]
	full_dataset_player_recent = full_dataset_player[full_dataset_player.NumericDate > 5650]

	# build features
	full_dataset_player_recent.index = xrange(len(full_dataset_player_recent.index))
	full_dataset_team_recent.index = xrange(len(full_dataset_team_recent.index))
	hf.error_checking(full_dataset_team_recent, "COMBINED TEAM OLD, NEW, PREDICTION RECENT", 0)
	hf.error_checking(full_dataset_player_recent, "COMBINED TEAM OLD, NEW, PREDICTION RECENT", 0)

	full_dataset_player_recent = fpd.format_player_data(full_dataset_player_recent, 0)
	hf.error_checking(full_dataset_player_recent, "COMBINED PLAYER OLD, NEW, PREDICTION RECENT WITH FEATURES BUILT", 0)

	hf.create_minutes_estimation_file(full_dataset_player_recent)
	print("Added new data, time for minutes prediction\n")

	full_dataset_team_recent = ftd.format_team_data(full_dataset_team_recent, 0)
	hf.error_checking(full_dataset_team_recent, "COMBINED TEAM OLD, NEW, PREDICTION RECENT WITH FEATURES BUILT", 0)


	# sample out new data
	full_dataset_player_new = full_dataset_player_recent[full_dataset_player_recent.New == 1]
	full_dataset_team_new = full_dataset_team_recent[full_dataset_team_recent.New == 1]

	# combine new data with old data
	full_dataset_player = pd.concat([old_player_data, full_dataset_player_new])
	full_dataset_team = pd.concat([old_team_data, full_dataset_team_new])

	return [full_dataset_player, full_dataset_team]
