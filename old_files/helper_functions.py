import pandas as pd
import numpy as np
import time

# gets the expected stats for a column
# StatPerPoss * ExpPoss (L30PaceTot)

# df -> dataframe we are working on
# column -> column with stat we are intersted in
# player -> 1 if we are working with player stats, 0 if team

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print 'Running %r took %2.2f sec' % \
              (method.__name__, te-ts)
        return result
    return timed

@timeit
def get_expected_stats(df, column, end_string):
	print "GETTING EXPECTED STATS FOR"
	print column

	previous_games = [1,2,3,5,10,20,30,40,50]

	pace_column = df.loc[:,"L30PaceTot"]
	df2 = df.loc[:,["L" + str(i) + column + end_string for i in previous_games]]

	for i in previous_games:
		if "L" + str(i) + "Exp" + column in df.columns:
			df.drop("L" + str(i) + "Exp" + column, axis = 1, inplace = True)
		df2["L" + str(i) + "Exp" + column] = pace_column.multiply(df2.loc[:,"L" + str(i) + column + end_string])
		df2.loc[df2.loc[:, "L" + str(i) + "Exp" + column] > 200, "L" + str(i) + "Exp" + column] = -999
		df2.loc[df2.loc[:, "L" + str(i) + "Exp" + column] < 0, "L" + str(i) + "Exp" + column] = -999

	df2 = df2.drop(["L" + str(i) + column + end_string for i in previous_games],1)

	df = pd.concat([df, df2], axis = 1)

	return df

# def pace_adjust()
@timeit
def min_adjusted_stats(df, column):
	previous_games = [1,2,3,5,10,20,30,40,50]
	expected_stats = pd.DataFrame()

	for i in previous_games:
		if "L" + str(i) + "ExpMinAdj" + column in df.columns:
			locat = df.columns.get_loc("L" + str(i) + "ExpMinAdj" + column)
			df.drop("L" + str(i) + "ExpMinAdj" + column, axis = 1, inplace = True)
			col = df.BucketedMin * df.loc[:,"L" + str(i) + "Player" + column + "PerMP"]
			# set unknowns to -999
			col[col > 200] = -999
			col[col < 0] = -999
			df.insert(locat, "L" + str(i) + "ExpMinAdj" + column, col)
		else:
			col = df.BucketedMin * df.loc[:,"L" + str(i) + "Player" + column + "PerMP"]
			# set unknowns to -999
			col[col > 200] = -999
			col[col < 0] = -999
			df["L" + str(i) + "ExpMinAdj" + column] = col
	return df

@timeit
def adj_stat(df, stat_name, mid_column_name, first_time):
	df["Adj" + str(mid_column_name) + str(stat_name)] = df.loc[:,stat_name] * (df.TeamMP / 240)
	return df

#  Combines horizontally the data frames td1, td2, td3, td4 ,td5 ,td6
#  Used to combine the .csv files of team data that are scraped from
#  basketballreference.com

#  The result of concat_team_data on the primary team data is in the
#  file 'fresh_team_data.csv'
def concat_team_data(td1,td2,td3,td4,td5,td6):
	td2 = td2.drop("Rank",1)
	td3 = td3.drop("Rank",1)
	td4 = td4.drop("Rank",1)
	td5 = td5.drop("Rank",1)
	td6 = td6.drop("Rank",1)

	team_data = pd.merge(td1, td2, on = ["Date", "Team", "Opp",
										 "Result", "TeamMP", "Home"])
	team_data = pd.merge(team_data, td3, on = ["Date", "Team", "Opp",
										 "Result", "TeamMP", "Home"])
	team_data = pd.merge(team_data, td4, on = ["Date", "Team", "Opp",
										 "Result", "TeamMP", "Home"])
	team_data = pd.merge(team_data, td5, on = ["Date", "Team", "Opp",
										 "Result", "TeamMP", "Home"])
	team_data = pd.merge(team_data, td6, on = ["Date", "Team", "Opp",
										 "Result", "TeamMP", "Home"])

	if ("Unnamed: 0" in team_data.columns):
		team_data = team_data.drop("Unnamed: 0",1)

	return team_data

def sort_and_reindex(df, sort_cols):
	df.sort_values(by = sort_cols, inplace = True)
	df.index = xrange(len(df.index))
	return df

# GET EXPECTED USAGE STAT:
# sums the Usg% (% of statistic consumed while player on court)
# of all 'n_play' to get an estimate of any 'usage gaps'
# must specify the 'column' that has the % stat we are concerned with
# and 'n_play' which indicates the number of players per team we are concerned with
def get_expected_usage(df, column, n_play, replace_na):
	df = df.sort_values(by = ['Team','Date'])
	df.index = xrange(len(df.index))

	# replaces any -999 with 0.1
	# this means that we are assuming any player who
	# has not played more than 10 games can be expected
	# to accumulate around 10% of stats while on floor
	col = df[column]

	# REPLACE ANY -999 IN COLUMN WITH .10
	col[col < 0] = replace_na
	df[column] = col

	df["Avg" + column] = pd.rolling_mean(df.loc[:,column], n_play)
	every_nth = df.loc[:,'Avg' + column].ix[[(n_play * (i + 1)) - 1 for i in range((len(df.index)/n_play))]]
	every_nth = every_nth * n_play
	df["Total" + column] = [i for i in every_nth for j in range(n_play)]
	df["Excess" + column] = 1 - df["Total" + column]
	df["Expected" + column] = (df.loc[:,column] / (df.loc[:,"Total" + column]))

	# eliminate all with tons of non-starters
	df.loc[df.loc[:,"Total" + column] < 0,"Expected" + column] = -999
	df.loc[df.loc[:,"Total" + column] < 0,"Total" + column] = -999
	df[column] = col

	return df


# MERGES TEAM AND PLAYER DATA SETS:
# merges on columns that can be merged on and remove rows that
# are unnecessary
def merge_team_and_player_sets(player_data, team_data):
	if 'Pred' in player_data.columns:
		full_data = pd.merge(player_data, team_data, on = ['Team','Opp','Home','Pred','NumericDate'])
	else:
		full_data = pd.merge(player_data, team_data, on = ['Team','Date'])
	full_data = full_data.drop('Result_x',1)
	full_data["Result"] = full_data.Result_y
	full_data = full_data.drop('Result_y',1)
	if "Home_x" in  full_data.columns:
		full_data["Home"] = full_data.Home_x
		full_data.drop('Home_x', 1, inplace = 1)
		full_data.drop('Home_y', 1, inplace = 1)

	return full_data


def convert_excel_date_format(file_name, date_column):
	df = pd.read_csv(file_name, parse_dates = [date_column])
	df.to_csv(file_name, date_format= '%m-%d-%Y', index = False)

# Removes unnecessary columns from data frames
#
# Removes the following:
# 'Rank'
# 'Result'
def remove_columns(df):
	return df

# Reformats dates stored in 'Date' column from Excel autoformat format
# to format usable by R and Pandas

def reformat_excel_dates(df):
	n = len(df.index)
	date_list = [0] * n
	for i in range(0,n):
		date = str(df.loc[i,"Date"])
		year = "20" + str(date[-2]) + str(date[-1])
		month = "01"
		day = "01"
		if date[1] == '/':
			month = "0" + str(date[0])
			if date[3] == '/':
				day = "0" + str(date[2])
			else:
				day = str(date[2]) + str(date[3])
		else:
			if date[1] == "2":
				month = "12"
			elif date[1] == "1":
				month = "11"
			else:
				month = "10"

			if date[4] == '/':
				day = "0" + str(date[3])
			else:
				day = str(date[3]) + str(date[4])
		date_list[i] = year + "-" + month + "-" + day
	df["Date"] = date_list
	return df

# calculates the 'game_number' for each row in dataframe. The
# game number is the number of games a particular game is past
# the first row chronologically in the dataframe. The 'sort_column'
# specifies the column we are finding the game number for. For example,
# if we are looking for each player's game number, we use 'Player' as
# the 'sort_column' argument
def calculate_game_number(df, sort_column):
	n = len(df.index)

	df = df.sort_values(by = [sort_column,"Date"])
	df.index = xrange(n)

	counts = df.loc[:, sort_column].value_counts()
	counts = counts.sort_index()

	game_number = []
	for i in xrange(len(counts.index)):
		game_number = game_number + range(1,counts[i]+1)
	df[sort_column + "GameNumber"] = game_number

	return df

# finds when a player transitions to anther team
# the first game a player is on a new team, the 'TeamChange'
# column will be marked with a 10, this number then decays
# to 0 to give an indicator of how long a player has been with a new team
def calculate_team_change(df, sort_column):
	n = len(df.index)

	df = df.sort_values(by = [sort_column,"Date"])
	df.index = xrange(n)

	team_change = [0] * n

	for i in xrange(1,11):
		prev_game_team = df['Team'].shift(i)
		prev_player = df[sort_column].shift(i)

		col = ((df[sort_column] == prev_player) & (df['Team'] != prev_game_team)).astype(int)
		team_change = col * (11 - i) + team_change

	df['TeamChange'] = team_change

	return df

# calculates season game number
def calculate_season_game_number(df, sort_column):
	# make sure we are ordered by team and data
	df = sort_and_reindex(df, [sort_column,'Date'])

	# find gap between games so we can recognize the large gap between seasons
	# as well as the 'negative gap' when we move from one team to another
	time_gap = df.NumericDate - df['NumericDate'].shift(1)

	# find the indexes of DataFrame that are at the borders of seasons and
	# switches to other teams
	season_list = (df[pd.isnull(time_gap) | (time_gap < 0) | (time_gap > 30)].index).tolist()
	season_list.append(len(df.index))

	# find the distances between the critical indexes to find the lengths of each season
	season_length_list = [t - s for s, t in zip(season_list, season_list[1:])]

	# add Season Game Number to DataFrame
	df['SeasonGameNumber'] = list(itertools.chain.from_iterable([xrange(1,x+1) for x in season_length_list]))

	return df

# Calculate possessions estimate for a single game
def calc_possessions(team_data, index):
	possessions = 0.5 * ((float(team_data.loc[index,"TeamFGA"]) + 0.44 * \
		float(team_data.loc[index,"TeamFTA"]) - 1.07 * \
		(float(team_data.loc[index,"TeamORB"]) / (float(team_data.loc[index,"TeamORB"]) + \
		float(team_data.loc[index,"OppDRB"]))) * (team_data.loc[index,"TeamFGA"] - \
		team_data.loc[index,"TeamFG"]) + float(team_data.loc[index,"TeamTOV"])) + \
		(team_data.loc[index,"OppFGA"] + 0.44 * team_data.loc[index,"OppFTA"] - \
		1.07 * (float(team_data.loc[index,"OppORB"]) / (float(team_data.loc[index,"OppORB"]) + \
		team_data.loc[index,"TeamDRB"])) * (team_data.loc[index,"OppFGA"] - \
		team_data.loc[index,"OppFG"]) + team_data.loc[index,"OppTOV"]))

	# formula used by TeamRanking, test to see if it gets better results
	# possessions = ( (TeamFGA - TeamORB + TeamTOV + 0.475 * TeamFTA) + (OppFGA - OppORB + OppTOV + 0.475 * OppFTA) ) * 0.5

	return possessions

#
def calc_pace(team_data, index, possessions):
	pace = 48 * ((possessions * 2) / (2 * (team_data.loc[index,"TeamMP"] / \
		5)))

	return pace

#
def add_numeric_date(df):
	n = len(df.index)
	df.index = xrange(n)

	# DROP NUMERIC DATE IF IT IS ALREADY IN COLUMNS
	if 'NumericDate' in df.columns:
		df.drop('NumericDate', 1, inplace = True)

	date_start = np.repeat("2000-01-01", n)
	date_start = pd.Series(data = date_start)
	numeric_date = pd.to_numeric(pd.to_datetime(df.loc[:,"Date"]) - \
		pd.to_datetime(pd.Series(date_start))) / 86400000000000
	df["NumericDate"] = numeric_date

	return df

def error_checking(df, string_indicator, verbose):
	print string_indicator + ':'

	print "ROWS:"
	print df.index

	print "NUM ROW:"
	print len(df.index)

	if verbose:
		for column in df.columns:
			ser = df.loc[:,column]
			print column + ' ' + str(sum(ser.isnull())) + ' ' + str(sum(ser == -999)) + ' ' + str(sum(ser < 0))
	else:
		df.info()

	# sum of prediction
	if "Pred" in df.columns:
		print "Sum of Pred"
		print df.loc[:,"Pred"].sum()
	else:
		print "Pred not in columns"

	# sum of new
	if "New" in df.columns:
		print "Sum of New"
		print df.loc[:,"New"].sum()
	else:
		print "New not in columns"

	print "\n\n"

# STARTS CLOCK:
# returns current time
def start_timer():
	current_time = time.time()
	return current_time

# TIME CHECKPOINT:
# gets current time
# prints difference between current time and 't_init'
# prints difference between current time nad 't_prev'
# returns current time
def time_checkpoint(t_init, t_prev, checkpoint):
	print checkpoint + ':'
	current_time = time.time()

	print 'Time From Start:'
	print current_time - t_init

	print 'Time From Previous:'
	print current_time - t_prev

	print '\n'

	return current_time

# creates file of all players marked with prediction with GS and MP
# with -999 so they can be manually estimated

# dumps to 'minute_estimation.csv'
def create_minutes_estimation_file(final_dataset):
	final_dataset = final_dataset.sort_values(by = ["Player","Date"])
	final_dataset = calculate_game_number(final_dataset, "Player")
	pred = final_dataset[final_dataset.Pred == 1]

	relevant_columns = pd.DataFrame()
	relevant_columns["Player"] = final_dataset.Player
	relevant_columns["PlayerGameNumber"] = final_dataset.PlayerGameNumber
	relevant_columns["NumPos"] = final_dataset.NumPos
	relevant_columns["PrevGS"] = final_dataset.GS

	previous_day = pd.DataFrame()
	previous_day["PlayerGameNumber"] = pred.PlayerGameNumber - 1
	previous_day["Player"] = pred.Player
	previous_day = pd.merge(previous_day, relevant_columns, on = ['Player','PlayerGameNumber'], how = 'left')

	previous_day.drop('PlayerGameNumber', 1, inplace = True)

	mep = pred.loc[:,["PlayerGameNumber","NumericDate","L30PlayerMP","L20PlayerMP","L10PlayerMP","L5PlayerMP",
					  "L3PlayerMP","L2PlayerMP","L1PlayerMP","MP","GS","Player","Team"]]

	mep = pd.merge(mep, previous_day, on = ["Player"])
	mep = mep.sort_values(by = ["Team"])

	# REORDER COLUMNS TO MORE LOGICAL ORDER:
	mep = mep.fillna(-999)
	mep.to_csv('DataSets/minute_estimation.csv', index = False)

def check_na(df, name):
	print 'Checking NA for ' + name
	print "Number of Rows With NA:"
	print np.count_nonzero(df.isnull())
	if np.count_nonzero(df.isnull()) != 0:
		na_set = df[df.isnull().any(axis=1)]
		na_set.to_csv('DataSets/ErrorChecking/na_set_' + name + '.csv')

# REMOVE INCOMPLETE STARTERS:
# takes 'raw_player_data.csv' and removes all players from games
# that do not have 5 starters listed

# removes approximately 50 games from the dataset
def remove_incomplete_starters():
	df = pd.read_csv('ScrapedData/raw_player_data.csv')

	print 'NUMBER OF PLAYERS BEFORE REMOVING INCOMPLETE STARTERS'
	print len(df.index)

	df = df.sort_values(by = 'Date')
	grouped = df.groupby(['Date','Team'])

	print 'NUMBER OF GAMES BEFORE REMOVING INCOMPLETE STARTERS'
	print len(grouped)
	for i in grouped:
		if sum(i[1].GS) != 5:
			print "PROBLEM"
			print i[1].loc[:,['GS','Team','Date']]
			df = df[(df.Team != i[1].iloc[0].Team) | (df.Date != i[1].iloc[0].Date)]

	grouped = df.groupby(['Date','Team'])

	print 'NUMBER OF PLAYERS AFTER REMOVING INCOMPLETE STARTERS'
	print len(df.index)
	print 'NUMBER OF GAMES AFTER REMOVING INCOMPLETE STARTERS'
	print len(grouped)

	df.to_csv('ScrapedData/raw_player_data_removed_incomplete_starters.csv')

def remove_duplicate_columns(df):
	if "New_x" in df.columns:
		df["New"] = df.New_x
		df = df.drop("New_x",1)

	if "New_y" in df.columns:
		df["New"] = df.New_y
		df = df.drop("New_y",1)

	if "Date_y" in df.columns:
		df["Date"] = df.Date_y
		df = df.drop("Date_y",1)

	if "Date_x" in df.columns:
		df["Date"] = df.Date_x
		df = df.drop("Date_x",1)

	if "Home_x" in df.columns:
		df["Home"] = df.Home_x
		df = df.drop("Home_x",1)

	if "Home_y" in df.columns:
		df["Home"] = df.Home_y
		df = df.drop("Home_y",1)

	if "Opp_x" in df.columns:
		df["Opp"] = df.Opp_x
		df = df.drop(["Opp_x","Opp_y"],1)

	if "Cost" in df.columns:
		df = df.drop("Cost",1)

	if "Unnamed: 0" in df.columns:
		df = df.drop("Unnamed: 0", 1)

	return df
