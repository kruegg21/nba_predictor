import pandas as pd
import get_averages as ga
import numpy as np
import helper_functions as hf
import warnings
warnings.filterwarnings('ignore')


#  Takes data frame with team data and formats data / adds features
#  for all rows marked with a 1 in the 'new' column
#  'first_time' indicates if the data_frame is being built for the
#  first time and doesn't have all the columns already established
#
#  The data frame should have the following format:
#  Columns: 
#  Date, Team, Home, Opp, Result, TeamMP
#
#  TeamFG, TeamFGA, TeamFG%, Team2P, Team2PA, Team2P%,
#  Team3P, Team3PA, Team3P%, TeamFT, TeamFTA, TeamFT%,
#
#  TeamPTS, TeamDRB, TeamORB, TeamTRB, TeamAST
#  TeamBLK, TeamTOV, TeamSTL, TeamPF
#
#  TeamORTg, TeamFTr, Team3PAr, TeamTS%, TeameFG%, TeamFT/FGA
#  TeamORB%, TeamTRB%, TeamSTL%, TeamBLK%, TeamTOV%, TeamAST%
#
#  OppFG, OppFGA, OppFG%, Opp2P, Opp2PA, Opp2P%,
#  Opp3P, Opp3PA, Opp3P%, OppFT, OppFTA, OppFT%,
#
#  OppPTS, OppDRB, OppORB, OppTRB, OppAST
#  OppBLK, OppTOV, OppSTL, OppPF
#
#  OppORTg, OppFTr, Opp3PAr, OppTS%, OppeFG%, OppFT/FGA
#  OppORB%, OppTRB%, OppSTL%, OppBLK%, OppTOV%, OppAST%
#
#  Adds the following columns:
#  TeamGameNumber, OppGameNumber, TeamPossessions, Pace
#  TeamPPP, OppPPP
#
#  AdjTeamPTS, AdjOppPTS, AdjOppAST, AdjOppDRB, AdjOppORB
#  AdjOppTRB, AdjOppSTL, AdjOppTOV, AdjOppBLK
#
#  L10-50OppPPP, L10-50AdjOppPTS, L10-50AdjOppAST, L10-50AdjORB
#  L10-50AdjOppDRB, L10-50AdjOppTRB, L10-50AdjOppSTL, L10-50AdjOppTOV,
#  L10-50AdjOppBLK, L10-50TeamPace, L10-50OppPace, L10-50PaceTot

def format_team_data(team_data, first_time):
	# DEFINITIONS:
	day_list = [1,2,3,5,10,20,30,40,50]

	# UPKEEP:
	# remove useless columns
	hf.error_checking(team_data, 'TEAM DATA PRE UPKEEP', 0)
	if first_time:
		team_data = hf.remove_columns(team_data)

	n = len(team_data.index)

	# n is number of rows in team_data
	hf.error_checking(team_data, 'TEAM DATA POST UPKEEP', 0)

	# ADD IN GAME AND DATE FEATURES:
	# add in TeamGameNumber
	team_data = hf.calculate_game_number(team_data, "Team")

	# add in OppGameNumber
	team_data = hf.calculate_game_number(team_data, "Opp")

	# add in Overtime column
	team_data["Overtime"] = [((a - 240) / 25) for a in team_data.TeamMP];

	# add numeric date column
	team_data = hf.add_numeric_date(team_data)

	# HOME TO NUMERIC:
	# turn 'Home' into numeric, takes previous 'Home' column if this is not
	# the first time and turns any entry that is new into  if an '@' is in 
	# the column and 1 otherwise
	home = team_data.loc[:,"Home"]
	home = home.replace(to_replace = '@', value = 0)
	home[home.isnull()] = 1
	team_data["Home"] = home

	# BACK TO BACK:
	team_data = team_data.sort_values(by = ["Team", "TeamGameNumber"])
	team_data.index = xrange(0,n)
	back_to_back = [0] * n
	team = team_data.loc[0,"Team"]
	for i in xrange(0,n):
		if team_data.loc[i,"TeamGameNumber"] == 1:
			back_to_back[i] = -999
		else:
			if team_data.loc[i,"NumericDate"] == team_data.loc[i-1,"NumericDate"] + 1:
				back_to_back[i] = 1
			else:
				back_to_back[i] = 0
	team_data["B2B"] = back_to_back
	team_data["B2BHome"] = back_to_back * home
	team_data.loc[team_data.B2B == -999, "B2BHome"] = -999

	team_data["B2BAway"] = (-1 * (back_to_back + team_data.B2BHome)) + 2
	team_data.loc[team_data.B2B == -999, "B2BAway"] = -999
	team_data.loc[team_data.B2BAway == 2, "B2BAway"] = 0

	# POSSESSIONS AND PACE:
	# calculate possessions and pace data
	team_possessions = 0
	pace = 0
	if first_time == 1:
		team_possessions = [0] * n
		pace = [0] * n
	else:
		team_possessions = team_data.loc[:,"TeamPossessions"]
		pace = team_data.loc[:,"Pace"]
	for i in range(0,n):
		# only calculate if game is newly added
		if team_data.loc[i,"New"] == 1:
			team_possessions[i] = hf.calc_possessions(team_data, i)
			pace[i] = hf.calc_pace(team_data, i, team_possessions[i])
	team_data["TeamPossessions"] = team_possessions
	team_data["Pace"] = pace

	# add in per possession data for each game
	team_data["TeamPTSPerPoss"] = team_data.TeamPTS / team_data.TeamPossessions
	team_data["OppPTSPerPoss"] = team_data.OppPTS / team_data.TeamPossessions
	team_data["TeamASTPerPoss"] = team_data.TeamAST / team_data.TeamPossessions
	team_data["OppASTPerPoss"] = team_data.OppAST / team_data.TeamPossessions
	team_data["TeamORBPerPoss"] = team_data.TeamORB / team_data.TeamPossessions
	team_data["OppORBPerPoss"] = team_data.OppORB / team_data.TeamPossessions
	team_data["TeamDRBPerPoss"] = team_data.TeamDRB / team_data.TeamPossessions
	team_data["OppDRBPerPoss"] = team_data.OppDRB / team_data.TeamPossessions
	team_data["TeamTRBPerPoss"] = team_data.TeamTRB / team_data.TeamPossessions
	team_data["OppTRBPerPoss"] = team_data.OppTRB / team_data.TeamPossessions
	team_data["TeamSTLPerPoss"] = team_data.TeamSTL / team_data.TeamPossessions
	team_data["OppSTLPerPoss"] = team_data.OppSTL / team_data.TeamPossessions
	team_data["TeamBLKPerPoss"] = team_data.TeamBLK / team_data.TeamPossessions
	team_data["OppBLKPerPoss"] = team_data.OppBLK / team_data.TeamPossessions
	team_data["TeamTOVPerPoss"] = team_data.TeamTOV / team_data.TeamPossessions
	team_data["OppTOVPerPoss"] = team_data.OppTOV / team_data.TeamPossessions


	####### ADJUSTED STATS (adjusted for overtime) #######
	# points
	team_data = hf.adj_stat(team_data, "TeamPTS", "", 1)
	team_data = hf.adj_stat(team_data, "TeamAST", "", 1)
	team_data = hf.adj_stat(team_data, "TeamDRB", "", 1)
	team_data = hf.adj_stat(team_data, "TeamORB", "", 1)
	team_data = hf.adj_stat(team_data, "TeamTRB", "", 1)
	team_data = hf.adj_stat(team_data, "TeamSTL", "", 1)
	team_data = hf.adj_stat(team_data, "TeamTOV", "", 1)
	team_data = hf.adj_stat(team_data, "TeamBLK", "", 1)

	####### AVERAGES OVER LAST 10,20,30,40, 50 GAMES ########

	# OPPONENT AVERAGES:
	# sorted by opponent
	team_data = hf.sort_and_reindex(team_data, ["Opp", "Date"])
	ga.get_averages(team_data, "TeamPTSPerPoss", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "TeamASTPerPoss", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "TeamDRBPerPoss", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "TeamORBPerPoss", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "TeamTRBPerPoss", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "TeamSTLPerPoss", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "TeamBLKPerPoss", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "TeamTOVPerPoss", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "AdjTeamPTS", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "AdjTeamAST", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "AdjTeamORB", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "AdjTeamDRB", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "AdjTeamTRB", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "AdjTeamSTL", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "AdjTeamTOV", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "AdjTeamBLK", "OppGivenUp", "OppGameNumber", day_list, first_time)
	ga.get_averages(team_data, "Pace", "Opp", "OppGameNumber", day_list, first_time)

	# TEAM AVERAGES:
	# sorted by team
	team_data = hf.sort_and_reindex(team_data, ["Team","Date"])
	ga.get_averages(team_data, "Pace", "Team", "TeamGameNumber", day_list, first_time)

	# COMPOSITE AVERAGES:
	# expected pace (average of both teams' previous pace totals)
	lag_time_windows = [10, 20, 30, 40, 50]
	for i in lag_time_windows:
		team_data["L" + str(i) + "PaceTot"] = (team_data.loc[:,"L" + str(i) + "OppPace"] + \
										 team_data.loc[:,"L" + str(i) + "TeamPace"]) / 2
		team_data.loc[team_data.loc[:,"L" + str(i) + "PaceTot"] < 0,"L" + str(i) + "PaceTot"] = -999

	return team_data