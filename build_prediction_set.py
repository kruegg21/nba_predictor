import pandas as pd

def build_prediction_set(file, date):
	df = pd.read_csv(file)

	######################	
	# FAN DUEL PLAYER LIST	
	# HOME:
	home = [1] * len(df.index)
	for i in xrange(len(df.index)):
		game = df.loc[i,'Game'] 
		if (game[0:3] == df.loc[i,'Team']) | (game[0:2] == df.loc[i,'Team']) :
			home[i] = 0
	df["Home"] = home

	# MATCH BASKETBALL REFERENCE:
	# Teams
	# SA -> SAS
	df.loc[df.Team == 'SA','Team'] = 'SAS'
	df.loc[df.Team == 'GS','Team'] = 'GSW'
	df.loc[df.Team == 'BKN','Team'] = 'BRK'
	df.loc[df.Team == 'CHA','Team'] = 'CHO'
	df.loc[df.Team == 'NY','Team'] = 'NYK'
	df.loc[df.Team == 'NO','Team'] = 'NOP'

	df.loc[df.Opponent == 'SA','Opponent'] = 'SAS'
	df.loc[df.Opponent == 'GS','Opponent'] = 'GSW'
	df.loc[df.Opponent == 'BKN','Opponent'] = 'BRK'
	df.loc[df.Opponent == 'NY','Opponent'] = 'NYK'
	df.loc[df.Opponent == 'CHA','Opponent'] = 'CHO'
	df.loc[df.Opponent == 'NO','Opponent'] = 'NOP'

	#############################
	# MAKE PLAYER PREDICTION SET:
	prediction_set_player = pd.DataFrame()

	# GET NAMES:
	prediction_set_player["Player"] = df.loc[:,'First Name'] + str(' ') + df.loc[:,'Last Name']

	# COST:
	prediction_set_player["Cost"] = df.Salary

	# TEAM AND OPPONENT:
	prediction_set_player["Team"] = df.Team
	prediction_set_player["Opp"] = df.Opponent

	# HOME:
	prediction_set_player["Home"] = df.Home

	# DATE:
	prediction_set_player["Date"] = date

	# FIND WAY TO ADD IN MINUTES PLAYED MANUALLY USING L20 MP AS REFERENCE
	# load 
	
	# ADD POSITION BASED ON OUT FULL DATASET

	# MATCH BASKETBALL REFERENCE:
	prediction_set_player = prediction_set_player.replace(to_replace = 'Brad Beal', value = 'Bradley Beal')
	prediction_set_player = prediction_set_player.replace(to_replace = 'Ishmael Smith' , value = 'Ish Smith')
	prediction_set_player = prediction_set_player.replace(to_replace = 'Louis Williams', value = 'Lou Williams')
	prediction_set_player = prediction_set_player.replace(to_replace = 'Jose Juan Barea', value = 'J.J. Barea')
	prediction_set_player = prediction_set_player.replace(to_replace = 'Tim Hardaway Jr.', value = 'Tim Hardaway')
	prediction_set_player = prediction_set_player.replace(to_replace = 'Phil (Flip) Pressey', value = 'Phil Pressey')

	# DUMP:
	prediction_set_player.to_csv('DataSets/PredictionSets/prediction_set_player.csv')
	##############################

	###########################
	# MAKE TEAM PREDICTION SET:
	prediction_set_team = pd.DataFrame()

	# GET TEAMS:
	prediction_set_team["Team"] = df.Team.unique()
	prediction_set_team["Opp"] = df.Opponent.unique()

	# HOME:
	temp = pd.DataFrame({'Team':prediction_set_player.Team, 'Home':prediction_set_player.Home})
	temp.drop_duplicates(inplace = True)
	prediction_set_team = prediction_set_team.merge(temp, on = 'Team')

	# DATE:
	prediction_set_team["Date"] = date

	# DUMP: 
	prediction_set_team.to_csv('DataSets/PredictionSets/prediction_set_team.csv')
