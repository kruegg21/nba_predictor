import pandas as pd
import get_averages as ga
import numpy as np
import helper_functions as hf
import time
import warnings
warnings.filterwarnings('ignore')

#  Takes data frame with player data and formats data / adds features
#  for all rows marked with a 1 in the 'new' column
#  'first_time' indicates if the data_frame is being built for the
#  first time and doesn't have all the columns already established
#
#  The data frame should have the following format:
#  Columns: 
#  Player, Age, Pos, Date, Team, Home, Opp, Result, GS, MP
#
#  FG, FGA, FG%, 2P, 2PA, 2P%, 3P, 3PA, 3P%, FT, FTA, FT%,
#  ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, GmSc
#
#  Adds the following columns:
#  NumericDate, PlayerGameNumer, TeamPossessions
#
#  AdjPlayerPTS, AdjPlayerAST, AdjPlayerDRB, AdjPlayerORB,
#  AdjPlayerTRB, AdjPlayerSTL, AdjPlayerTOV, AdjPlayerBLK
#
#  L10-50AdjPlayerPTS, L10-50AdjPlayerAST, L10-50AdjPlayerDRB,
#  L10-50AdjPlayerTRB, L10-50AdjPlayerSTL, L10-50AdjPlayerTOV

def format_player_data(player_data, first_time):
	# DEFINITIONS:
	n = len(player_data.index)
	day_list = [1,2,3,5,10,20,30,40,50]
	t0 = time.time()
	tp = t0
	hf.error_checking(player_data, "START OF FORMATTING PLAYER DATA", 0)

	# UPKEEP:
	if first_time:
		player_data = hf.remove_columns(player_data)
	# percent cells are NA if a player did not make an attempt, so
	# change these to -999
	player_data.loc[player_data.loc[:,'3P%'].isnull(),'3P%'] = -999
	player_data.loc[player_data.loc[:,'2P%'].isnull(),'2P%'] = -999
	player_data.loc[player_data.loc[:,'FG%'].isnull(),'FG%'] = -999
	player_data.loc[player_data.loc[:,'FT%'].isnull(),'FT%'] = -999

	# HOME TO NUMERIC:
	home = player_data.loc[:,"Home"]
	home = home.replace(to_replace = '@', value = 0)
	home[home.isnull()] = 1
	player_data["Home"] = home
	tp = hf.time_checkpoint(t0, tp, "CONVERTED HOME TO NUMERIC")

	# NUMERIC DATE AND PLAYER GAME NUMBER:
	# does not change existing 'Date' column, simply adds 'NumericDate'
	player_data = hf.add_numeric_date(player_data)
	tp = hf.time_checkpoint(t0, tp, "ADDED NUMERIC DATE")

	# PLAYER GAME NUMBER
	player_data = hf.calculate_game_number(player_data, "Player")
	tp = hf.time_checkpoint(t0, tp, "CALCULATED GAME NUMBER")

	# NUMERIC POSITION:
	# does not change existing 'Pos' column, just adds 'NumPos'
	if player_data.Pos.dtype.name != 'int64':
		pos = player_data.loc[:,"Pos"]
		pos[pos == "PG"] = 1
		pos[pos == "G"] = 2
		pos[pos == "G-F"] =3
		pos[pos == "F-G"] = 4
		pos[pos == "F"] = 5
		pos[pos == "PF"] = 6
		pos[pos == "F-C"] = 7
		pos[pos == "C-F"] = 8
		pos[pos == "C"] = 9
		pos[pos.isnull()] = -999
		player_data["NumPos"] = pos.astype(int)
	tp = hf.time_checkpoint(t0, tp, "CALCULATED NUMERIC POSITION")

	# CALCULATE TEAM SWITCH
	player_data = hf.calculate_team_change(player_data, 'Player')
	tp = hf.time_checkpoint(t0, tp, "CALCULATED TEAM SWITCH")

	# CALCULATE FAN DUEL POINTS:
	player_data["FanDuelScore"] = player_data.PTS + 1.2 * player_data.TRB + 1.5 * player_data.AST + 2 * player_data.BLK + 2 * player_data.STL - player_data.TOV

	# GET AVERAGES:
	player_data = player_data.sort_values(by = ["Player","Date"])
	ga.get_averages(player_data, "PTS", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "AST", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "DRB", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "TRB", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "STL", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "TOV", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "ORB", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "BLK", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "MP", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "FG%", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "3P%", "Player", "PlayerGameNumber", day_list, first_time)

	# PER MINUTE STATS:
	player_data["PTSPerMP"] = player_data.PTS / player_data.MP 
	player_data["ASTPerMP"] = player_data.AST / player_data.MP
	player_data["TRBPerMP"] = player_data.TRB / player_data.MP
	player_data["DRBPerMP"] = player_data.DRB / player_data.MP
	player_data["ORBPerMP"] = player_data.ORB / player_data.MP
	player_data["STLPerMP"] = player_data.STL / player_data.MP
	player_data["BLKPerMP"] = player_data.BLK / player_data.MP
	player_data["TOVPerMP"] = player_data.TOV / player_data.MP

	ga.get_averages(player_data, "PTSPerMP", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "ASTPerMP", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "DRBPerMP", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "TRBPerMP", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "STLPerMP", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "TOVPerMP", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "ORBPerMP", "Player", "PlayerGameNumber", day_list, first_time)
	ga.get_averages(player_data, "BLKPerMP", "Player", "PlayerGameNumber", day_list, first_time)

	tp = hf.time_checkpoint(t0, tp, "FINISHED CALCULATING PLAYER AVERAGES")
	hf.error_checking(player_data, "FINISHED FORMATTING PLAYER DATA", 0)

	#############################################################################################
	# PLAYER DATA DATAFRAME INFORMATION
	# NUMROWS:
	# 384600
	# Rank 0 0 0
	# Player 0 0 0
	# Age 0 0 0
	# Pos 0 0 0
	# Date 0 0 0
	# Team 0 0 0
	# Home 0 0 0
	#Opp 0 0 0
	#Result 0 0 0
	#GS 0 0 0
	#MP 0 0 0
	#FG 0 0 0
	#FGA 0 0 0
	#FG% 0 20344 20344
	#2P 0 0 0
	#2PA 0 0 0
	#2P% 0 29946 29946
	#3P 0 0 0
	#3PA 0 0 0
	#3P% 0 177680 177680
	#FT 0 0 0
	#FTA 0 0 0
	#FT% 0 155512 155512
	#ORB 0 0 0
	#DRB 0 0 0
	#TRB 0 0 0
	#AST 0 0 0
	#STL 0 0 0
	#BLK 0 0 0
	#TOV 0 0 0
	#PF 0 0 0
	#PTS 0 0 0
	#GmSc 0 0 48111
	#New 0 0 0
	#NumericDate 0 0 0
	#PlayerGameNumber 0 0 0
	#NumPos 0 0 0
	#FanDuelScore 0 0 3030
	#L1PlayerPTS 0 1523 1523
	#L2PlayerPTS 0 3031 3031
	#L3PlayerPTS 0 4514 4514
	#L5PlayerPTS 0 7432 7432
	#L10PlayerPTS 0 14464 14464
	#L20PlayerPTS 0 27790 27790
	#L30PlayerPTS 0 40285 40285
	#L40PlayerPTS 0 52165 52165
	#L50PlayerPTS 0 63449 63449
	#L1PlayerAST 0 1523 1523
	#L2PlayerAST 0 3031 3031
	#L3PlayerAST 0 4514 4514
	#L5PlayerAST 0 7432 7432
	#L10PlayerAST 0 14464 14464
	#L20PlayerAST 0 27790 27790
	#L30PlayerAST 0 40285 40285
	#40PlayerAST 0 52165 52165
	#L50PlayerAST 0 63449 63449
	#L1PlayerDRB 0 1523 1523
	#L2PlayerDRB 0 3031 3031
	#L3PlayerDRB 0 4514 4514
	#L5PlayerDRB 0 7432 7432
	#L10PlayerDRB 0 14464 14464
	#L20PlayerDRB 0 27790 27790
	#L30PlayerDRB 0 40285 40285
	#L40PlayerDRB 0 52165 52165
	#L50PlayerDRB 0 63449 63449
	#L1PlayerTRB 0 1523 1523
	#L2PlayerTRB 0 3031 3031
	#L3PlayerTRB 0 4514 4514
	#L5PlayerTRB 0 7432 7432
	#L10PlayerTRB 0 14464 14464
	#L20PlayerTRB 0 27790 27790
	#L30PlayerTRB 0 40285 40285
	#L40PlayerTRB 0 52165 52165
	#L50PlayerTRB 0 63449 63449
	#L1PlayerSTL 0 1523 1523
	#L2PlayerSTL 0 3031 3031
	#L3PlayerSTL 0 4514 4514
	#L5PlayerSTL 0 7432 7432
	#L10PlayerSTL 0 14464 14464
	#L20PlayerSTL 0 27790 27790
	#L30PlayerSTL 0 40285 40285
	#L40PlayerSTL 0 52165 52165
	#L50PlayerSTL 0 63449 63449
	#L1PlayerTOV 0 1523 1523
	#L2PlayerTOV 0 3031 3031
	#L3PlayerTOV 0 4514 4514
	#L5PlayerTOV 0 7432 7432
	#L10PlayerTOV 0 14464 14464
	#L20PlayerTOV 0 27790 27790
	#L30PlayerTOV 0 40285 40285
	#L40PlayerTOV 0 52165 52165
	#L50PlayerTOV 0 63449 63449
	#L1PlayerORB 0 1523 1523
	#L2PlayerORB 0 3031 3031
	#L3PlayerORB 0 4514 4514
	#L5PlayerORB 0 7432 7432
	#L10PlayerORB 0 14464 14464
	#L20PlayerORB 0 27790 27790
	#L30PlayerORB 0 40285 40285
	#L40PlayerORB 0 52165 52165
	#L50PlayerORB 0 63449 63449
	#L1PlayerBLK 0 1523 1523
	#L2PlayerBLK 0 3031 3031
	#L3PlayerBLK 0 4514 4514
	#L5PlayerBLK 0 7432 7432
	#L10PlayerBLK 0 14464 14464
	#L20PlayerBLK 0 27790 27790
	#L30PlayerBLK 0 40285 40285
	#L40PlayerBLK 0 52165 52165
	#L50PlayerBLK 0 63449 63449
	#L1PlayerMP 0 1523 1523
	#L2PlayerMP 0 3031 3031
	#L3PlayerMP 0 4514 4514
	#L5PlayerMP 0 7432 7432
	#L10PlayerMP 0 14464 14464
	#L20PlayerMP 0 27790 27790
	#L30PlayerMP 0 40285 40285
	#L40PlayerMP 0 52165 52165
	#L50PlayerMP 0 63449 63449
	#PTSPerMP 1484 0 0
	#ASTPerMP 1508 0 0
	#TRBPerMP 1456 0 0
	#DRBPerMP 1476 0 0
	#ORBPerMP 1504 0 0
	#STLPerMP 1506 0 0
	#BLKPerMP 1520 0 0
	#TOVPerMP 1512 0 0
	#L1PlayerPTSPerMP 0 3029 3029
	#L2PlayerPTSPerMP 0 5868 5868
	#L3PlayerPTSPerMP 0 8577 8577
	#L5PlayerPTSPerMP 0 13629 13629
	#L10PlayerPTSPerMP 0 24812 24812
	#L20PlayerPTSPerMP 0 43593 43593
	#L30PlayerPTSPerMP 0 59729 59729
	#L40PlayerPTSPerMP 0 74159 74159
	#L50PlayerPTSPerMP 0 87331 87331
	#L1PlayerASTPerMP 0 3029 3029
	#L2PlayerASTPerMP 0 5868 5868
	#L3PlayerASTPerMP 0 8577 8577
	#L5PlayerASTPerMP 0 13629 13629
	#L10PlayerASTPerMP 0 24812 24812
	#L20PlayerASTPerMP 0 43593 43593
	#L30PlayerASTPerMP 0 59729 59729
	#L40PlayerASTPerMP 0 74159 74159
	#L50PlayerASTPerMP 0 87331 87331
	#L1PlayerDRBPerMP 0 3029 3029
	#L2PlayerDRBPerMP 0 5868 5868
	#L3PlayerDRBPerMP 0 8577 8577
	#L5PlayerDRBPerMP 0 13629 13629
	#L10PlayerDRBPerMP 0 24812 24812
	#L20PlayerDRBPerMP 0 43593 43593
	#L30PlayerDRBPerMP 0 59729 59729
	#L40PlayerDRBPerMP 0 74159 74159
	#L50PlayerDRBPerMP 0 87331 87331
	#L1PlayerTRBPerMP 0 3029 3029
	#L2PlayerTRBPerMP 0 5868 5868
	#L3PlayerTRBPerMP 0 8577 8577
	#L5PlayerTRBPerMP 0 13629 13629
	#L10PlayerTRBPerMP 0 24812 24812
	#L20PlayerTRBPerMP 0 43593 43593
	#L30PlayerTRBPerMP 0 59729 59729
	#L40PlayerTRBPerMP 0 74159 74159
	#L50PlayerTRBPerMP 0 87331 87331
	#L1PlayerSTLPerMP 0 3029 3029
	#L2PlayerSTLPerMP 0 5868 5868
	#L3PlayerSTLPerMP 0 8577 8577
	#L5PlayerSTLPerMP 0 13629 13629
	#L10PlayerSTLPerMP 0 24812 24812
	#L20PlayerSTLPerMP 0 43593 43593
	#L30PlayerSTLPerMP 0 59729 59729
	#L40PlayerSTLPerMP 0 74159 74159
	#L50PlayerSTLPerMP 0 87331 87331
	#L1PlayerTOVPerMP 0 3029 3029
	#L2PlayerTOVPerMP 0 5868 5868
	#L3PlayerTOVPerMP 0 8577 8577
	#L5PlayerTOVPerMP 0 13629 13629
	#L10PlayerTOVPerMP 0 24812 24812
	#L20PlayerTOVPerMP 0 43593 43593
	#L30PlayerTOVPerMP 0 59729 59729
	#L40PlayerTOVPerMP 0 74159 74159
	#L50PlayerTOVPerMP 0 87331 87331
	#L1PlayerORBPerMP 0 3029 3029
	#L2PlayerORBPerMP 0 5868 5868
	#L3PlayerORBPerMP 0 8577 8577
	#L5PlayerORBPerMP 0 13629 13629
	#L10PlayerORBPerMP 0 24812 24812
	#L20PlayerORBPerMP 0 43593 43593
	#L30PlayerORBPerMP 0 59729 59729
	#L40PlayerORBPerMP 0 74159 74159
	#L50PlayerORBPerMP 0 87331 87331
	#L1PlayerBLKPerMP 0 3029 3029
	#L2PlayerBLKPerMP 0 5868 5868
	#L3PlayerBLKPerMP 0 8577 8577
	#L5PlayerBLKPerMP 0 13629 13629
	#L10PlayerBLKPerMP 0 24812 24812
	#L20PlayerBLKPerMP 0 43593 43593
	#L30PlayerBLKPerMP 0 59729 59729
	#L40PlayerBLKPerMP 0 74159 74159
	#L50PlayerBLKPerMP 0 87331 87331
	#############################################################################################

	return player_data

