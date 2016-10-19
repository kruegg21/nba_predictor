import pandas as pd
import itertools
import math

def final_score(file_names):
	# read FanDuel file and get 'Player' name
	fan_duel_file = pd.read_csv(file_names['main'])
	fan_duel_file["Player"] = fan_duel_file["First Name"] + ' ' + fan_duel_file["Last Name"]
	fan_duel_file = fan_duel_file.sort_values(by = ["Player"])
	fan_duel_file.index = range(0,len(fan_duel_file.index))

	# GET STAT PREDICTIONS:
	point = pd.read_csv('DataSets/ScoresLineups/point_prediction.csv')
	assist = pd.read_csv('DataSets/ScoresLineups/assist_prediction.csv')
	rebound = pd.read_csv('DataSets/ScoresLineups/rebound_prediction.csv')
	steal = pd.read_csv('DataSets/ScoresLineups/steal_prediction.csv')
	turnover = pd.read_csv('DataSets/ScoresLineups/turnover_prediction.csv')
	block = pd.read_csv('DataSets/ScoresLineups/block_prediction.csv')

	# get list of player names
	final = pd.DataFrame()
	final["Player"] = point.Player

	# retranslate players
	final = final.replace(to_replace = 'Bradley Beal', value = 'Brad Beal')
	final = final.replace(to_replace = 'Ish Smith', value = 'Ishmael Smith')
	final = final.replace(to_replace = 'Lou Williams', value = 'Louis Williams')
	final = final.replace(to_replace = 'J.J. Barea', value = 'Jose Juan Barea')
	final = final.replace(to_replace = 'Tim Hardaway', value = 'Tim Hardaway Jr.')
	final = final.replace(to_replace = 'Phil Pressey', value = 'Phil (Flip) Pressey')

	# convert individual score to final score
	final["Score"] = point.point + 1.2 * rebound.rebound + 1.5 * assist.assist + 2 * block.block + 2 * steal.steal - turnover.turnover
	final["Point"] = point.point
	final["Assist"] = assist.assist
	final["Rebound"] = rebound.rebound
	final["Steal"] = steal.steal
	final["Turnover"] = turnover.turnover
	final["Block"] = block.block

	final = final.sort_values(by = ["Player"])
	final.index = range(0,len(final.index))

	# add in 'Cost' 'Position' and 'Team'
	final["Cost"] = fan_duel_file.Salary
	final["Position"] = fan_duel_file.Position
	final["Team"] = fan_duel_file.Team
	# main slate 'Id'
	final["Id"] = fan_duel_file.Id

	# add in variance data
	'''
	variance = pd.read_csv('variance_scores.csv')
	final = pd.merge(final, variance, on = 'Player')
	final['1SD'] = final.Score + final.STD
	final['2SD'] = final.Score + 2 * final.STD
	final['3/2SD'] = final.Score + 1.5 * final.STD
	final['-1/3SD'] = final.Score - 0.3 * final.STD
	'''

	# INDIVIDUAL SLATE FILES:
	scores = final.loc[:,['Player','Score','Position','Team','Cost']]
	try:
		slate_list = pd.read_csv('slate_list.csv')
		if slate_list.columns is not None:
			for i in slate_list.columns:
				file = pd.read_csv(file_names[i])
				file["Player"] = file["First Name"] + ' ' + file["Last Name"]
				file = file.loc[:,['Player','Id']]
				scores = pd.merge(scores, file, on = 'Player')

		 		pg = pd.DataFrame()
				sg = pd.DataFrame()
				sf = pd.DataFrame()
				pf = pd.DataFrame()
				c = pd.DataFrame()
				for j in slate_list[i]:
					if pd.notnull(j):
						pg = pg.append(scores.loc[(scores.Team == j) & (scores.Position == 'PG'),:])
						sg = sg.append(scores.loc[(scores.Team == j) & (scores.Position == 'SG'),:])
						sf = sf.append(scores.loc[(scores.Team == j) & (scores.Position == 'SF'),:])
						pf = pf.append(scores.loc[(scores.Team == j) & (scores.Position == 'PF'),:])
						c = c.append(scores.loc[(scores.Team == j) & (scores.Position == 'C'),:])
				pg = pg.sort_values(by = 'Score')
				sg = sg.sort_values(by = 'Score')
				sf = sf.sort_values(by = 'Score')
				pf = pf.sort_values(by = 'Score')
				c = c.sort_values(by = 'Score')

				pg.to_csv('SlateLists/' + i + '_pg_list.csv', index = False)			
				sg.to_csv('SlateLists/' + i + '_sg_list.csv', index = False)			
				sf.to_csv('SlateLists/' + i + '_sf_list.csv', index = False)			
				pf.to_csv('SlateLists/' + i + '_pf_list.csv', index = False)			
				c.to_csv('SlateLists/' + i + '_c_list.csv', index = False)	
	except:
		pass

	# DUMP:
	final.to_csv('DataSets/ScoresLineups/final_score.csv', index = False)

# passes in 2 lists, 'list_1' and 'list_2', which have the following charactersistics:
#	1. Each index of the lists represents a PRICE
#	2. At each price, we have an ordered list of sets of players that optimally fit this
#	   cost
#	3. Each player list is composed of a price as the first index and a list of players
#	   that compose this set
# 'n_players' : list of size 2 that represents the number of players per set in each of
#				the two lists passed
# 'maximum_player_cost' : maximum cost per player
# 'minimum_player_cost' : minimum cost per player
# 'depth' : number of player sets at each cost
# 'slots' : number of price slots we are interested in

# takes the two lists passed and finds the optimal way to pick set combinations for 
# each price

def combine_layers(list_1, list_2, n_players, maximum_player_cost, minimum_player_cost, depth, slots):
	ls = [[[0,0] for i in range(depth)] for j in range(slots+1)]

	max_1 = maximum_player_cost * n_players[0]
	if max_1 > slots:
		max_1 = slots

	max_2 = maximum_player_cost * n_players[1]
	if max_2 > slots:
		max_2 = slots

	for i in range(minimum_player_cost * n_players[0], max_1 + 1):
		for j in range(minimum_player_cost * n_players[1], max_2 + 1):
			if i+j < slots+1:
				# permute each combination and append to all possible lists
				# 2 options:
				# 1. Append each permutation to each score list from minimum price to maximum price
				# 2. Check to make sure we are not appending repeats
				if (list_1[i][0][0] != 0) & (list_2[j][0][0] != 0):
					l1 = [x for x in list_1[i] if x[0] != 0]
					l2 = [x for x in list_2[j] if x[0] != 0] 

					combinations = [x for x in itertools.product(l1,l2)]

					for l in combinations:
						if (l[0][0] != 0) & (l[1][0] != 0):
							score = l[0][0] + l[1][0]
							players = l[0][1] + l[1][1]
							ls[i+j].append([score, players])	

	for i in range(slots+1):
		ls[i] = sorted(ls[i], key = lambda x: x[0], reverse = True)
		ls[i] = ls[i][:depth]

	return ls

def optimal_lineup_test(cap, column, cut_off, categories, players_per_category, file_name):
	# TO MAKE GENERAL FORMULA, HERE ARE THE NEEDED THINGS:
	# input is data of 'Score' and 'Cost' divided into
	# different categories

	# num_categories : self explanatory
	# players_per_category : self explanatory
	# minimum_player_cost : self explanatory
	# maximum_player_cost : self explanatory
	# depth : number of players to keep track of at each price point
	# the depth should be small for the first few layers and increase
	# as we combine layers. the depth at the last layer is the number
	# of lineups we want to build

	# the general strategy is to find the best lineups for 
	# each price for each category, then combine the categories 
	# finding the best players for multiple lineups combined
	# at a particular price

	# we can think of layer one as each category standing alone.
	# we find the optimum for each price of each stand alone category
	# at each layer.
	# when we move up to another layer, we combine pairs of categories

	minimum_player_cost = 35
	maximum_player_cost = 115
	depth = 5

	# number of slots is 600
	slots = cap/100
	num_categories = len(categories)
	num_players = sum(players_per_category)

	df = pd.read_csv('DataSets/ScoresLineups/final_score.csv')
	score = df.loc[:,column]

	df["Cost"] = df.Cost / 100
	df["ScoreCostRatio"] = score / df.Cost
	df = df.sort_values(by = 'ScoreCostRatio')

	print len(df.index)
	df = df[(df.ScoreCostRatio > cut_off) | (df.Cost > 800)]
	print len(df.index)

	# place dataframes divided by position into the indices of 'cat'
	cat = [0] * num_categories
	for i in xrange(num_categories):
		cat[i] = df[df.Position == categories[i]]
		cat[i].index = xrange(len(cat[i].index))

	# make list of lists	
	ls = [[[[0,0] for i in range(depth)] for j in range(slots+1)] for k in range(num_categories)]
	cat = [0] * num_categories
	for i in xrange(num_categories):
		cat[i] = df[df.Position == categories[i]]
		for subset in itertools.combinations(cat[i].index, players_per_category[i]):
			players = [0] * players_per_category[i]
			cost = 0
			score = 0
			ctr = 0
			for k in subset:
			 	score += cat[i].loc[k, column]
			 	cost += cat[i].loc[k, 'Cost']
			 	players[ctr] = cat[i].loc[k, 'Player']
			 	ctr += 1		
				ls[i][int(cost)].append([score, players])
		for j in range(slots):
			ls[i][j] = sorted(ls[i][j], key = lambda x: x[0], reverse = True)
			ls[i][j] = ls[i][j][:depth]

	ls2 = []
	n_players = [players_per_category[0], players_per_category[1]]
	ls2.append(combine_layers(ls[0], ls[1], n_players, maximum_player_cost, minimum_player_cost, depth, slots))
	n_players = [players_per_category[2], players_per_category[3]]
	ls2.append(combine_layers(ls[2], ls[3], n_players, maximum_player_cost, minimum_player_cost, depth, slots))
	ls2.append(ls[4])


	n_players = [4,1]

	ls3 = []
	ls3.append(combine_layers(ls2[1], ls2[2], n_players, maximum_player_cost, minimum_player_cost, 40, slots))
	ls3.append(ls2[0])

	n_players = [5,4]
	final_linups = combine_layers(ls3[0], ls3[1], n_players, maximum_player_cost, minimum_player_cost, 200, slots)

	# looks through linupes that spend 45000 or more to pick the global optimal lineups
	lineups = []
	for i in xrange(450,601):
		lineups += final_linups[i]
	lineups = sorted(lineups, key = lambda x: x[0], reverse = True)

	best_lineups = lineups[:100]

	scores = [0] * len(best_lineups)
	players = [0] * len(best_lineups)
	for i in xrange(len(best_lineups)):
		players[i] = best_lineups[i][1] 
		scores[i] = best_lineups[i][0]
	bl = pd.DataFrame(players, columns = ['SmallForward1','SmallForward2','PowerForward1','PowerForward2',
										  'Center','PointGuard1','PointGuard2','ShootingGuard1','ShootingGuard2'])
	# reorder to PG, SG, SF, PF, C
	cols = bl.columns.tolist()
	cols = cols[5:7] + cols[7:] + cols[:5]
	bl = bl[cols]

	# add in Score columns
	bl['Scores'] = scores

	# add in player code for mass lineup submissions
	d = df.set_index('Player').to_dict()
	bl['PG1'] = [d['Id'][x] for x in bl.PointGuard1.tolist()]
	bl['PG2'] = [d['Id'][x] for x in bl.PointGuard2.tolist()]
	bl['SG1'] = [d['Id'][x] for x in bl.ShootingGuard1.tolist()]
	bl['SG2'] = [d['Id'][x] for x in bl.ShootingGuard2.tolist()]
	bl['SF1'] = [d['Id'][x] for x in bl.SmallForward1.tolist()]
	bl['SF2'] = [d['Id'][x] for x in bl.SmallForward2.tolist()]
	bl['PF1'] = [d['Id'][x] for x in bl.PowerForward1.tolist()]
	bl['PF2'] = [d['Id'][x] for x in bl.PowerForward2.tolist()]
	bl['C'] = [d['Id'][x] for x in bl.Center.tolist()]

	# dump
	bl.to_csv('DataSets/ScoresLineups/' + file_name + '_best_linups.csv', index = False)
