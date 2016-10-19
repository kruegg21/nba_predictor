import numpy as np
import pandas as pd
import itertools
from collections import Counter
from helper import find_fd_filenames, get_player_id, p
from read_write import read_fan_duel_file, read_final_score_data

# looks at slate information and finds lineup permutations for 'slate'

# 1. Reads position specific player lists from 'SlateList' folder
# 2. Creates combinations for all lineups
# 3. Filters the possible lineups based on the following rules
#	a) No more than 4 players from one team
#	b) Minimum of 3 teams represented
#	c) df.Salary does not exceed 'maximum_df.Salary'
#	d) df.Salary is not less than 'minimum_df.Salary'
# 4. Dumps the lineups that pass the filter into 'perm_lineups.csv'

def get_slate_df(slate):
	"""
	Input:
		slate -- string indicating the file path for the slate we are picking
				 optimal lineups for
	Output:
		DataFrame with the data necessary to get optimal lineups for a given
		slate
	"""
	# Read slate file
	slate_df = read_fan_duel_file(slate)

	# Get slate ID
	slate_id = get_slate_id(slate)

	# Get player ID
	get_player_id(slate_df)

	# Read final score
	final_score_df = read_final_score_data()

	# Merge
	return slate_id, slate_df.merge(final_score_df, on = 'PlayerID')

def get_slate_id(slate):
	return slate.split('-')[5]

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

def optimal_lineup_test(df, column, cut_off, players_per_category, file_name):
	"""
	Inputs:
		df -- DataFrame with 'Player', 'PlayerID', 'Id', 'Score', 'Variance',
			  'df.Salary', 'Team', 'Position'
		column -- string with column name that we are attempting to maximize
		cut_off -- float of the minimum score to df.Salary ratio that we will
				   consider; the higher this value, the more players we weed out
				   and the faster the calculation, but the higher chance we are
				   missing optimal lineups

	1. Divides all pricing by 100 to eliminate useless digites (3500 -> 35)
	2. Cuts down data set by only taking players with a score to df.Salary ratio
	   above a certain threshold. This could be improved by automatically
	   creating a way to create a threshold.
	"""
	# TO MAKE GENERAL FORMULA, HERE ARE THE NEEDED THINGS:
	# input is data of 'Score' and 'df.Salary' divided into
	# different categories

	# num_categories : self explanatory
	# players_per_category : self explanatory
	# minimum_player_df.Salary : self explanatory
	# maximum_player_df.Salary : self explanatory
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

	# Parameters
	cap = 60000
	minimum_player_salary = 3500
	maximum_player_salary = 11500
	uncuttable_salary = 8000
	minimum_total_salary = 45000
	depth = 5
	categories = ['PG','SG','SF','PF','C']

	# Divide all df.Salary related values by 100
	slots = cap/100
	minimum_player_salary /= 100
	maximum_player_salary /= 100
	uncuttable_salary /= 100
	minimum_total_salary /= 100
	df['Salary'] = df.Salary / 100

	# Definitions
	num_categories = len(categories)
	num_players = np.sum(players_per_category)
	score = df[column]

	# Cut down based on score, df.Salary ratio
	score_salary_ratio = score / df.Salary
	print "Number of rows before ratio cut: {}".format(len(df.index))
	df = df[((score_salary_ratio > cut_off) | (df.Salary > uncuttable_salary))]
	print "Number of rows after ratio cut: {}".format(len(df.index))

	# Find optimal player choices for a given position and amount of salary
	ls = [[[[0,0] for i in range(depth)] for j in range(slots+1)] for k in range(num_categories)]
	cat = [0] * num_categories
	for i in xrange(num_categories):
		cat[i] = df[df.Position == categories[i]]
		for subset in itertools.combinations(cat[i].index, players_per_category[i]):
			players = [0] * players_per_category[i]
			salary = 0
			score = 0
			ctr = 0
			for k in subset:
			 	score += cat[i].loc[k, column]
			 	salary += cat[i].loc[k, 'Salary']
			 	players[ctr] = cat[i].loc[k, 'Player']
			 	ctr += 1
				ls[i][int(salary)].append([score, players])
		for j in xrange(slots):
			ls[i][j] = sorted(ls[i][j], key = lambda x: x[0], reverse = True)
			ls[i][j] = ls[i][j][:depth]

	# Dynamic programming merging of subproblems
	ls2 = []
	n_players = [players_per_category[0], players_per_category[1]]
	ls2.append(combine_layers(ls[0], ls[1], n_players, maximum_player_salary, minimum_player_salary, depth, slots))
	n_players = [players_per_category[2], players_per_category[3]]
	ls2.append(combine_layers(ls[2], ls[3], n_players, maximum_player_salary, minimum_player_salary, depth, slots))
	ls2.append(ls[4])


	n_players = [4,1]

	ls3 = []
	ls3.append(combine_layers(ls2[1], ls2[2], n_players, maximum_player_salary, minimum_player_salary, 40, slots))
	ls3.append(ls2[0])

	n_players = [5,4]
	final_linups = combine_layers(ls3[0], ls3[1], n_players, maximum_player_salary, minimum_player_salary, 200, slots)

	# looks through linupes that spend 45000 or more to pick the global optimal lineups
	lineups = []
	for i in xrange(minimum_total_salary, cap+1):
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
	bl.to_csv('data/' + file_name + '_best_linups.csv', index = False)

def optimize_lineups():
	file_names = find_fd_filenames()
	for f in file_names:
		# Get data for slate
		slate_id, slate_df = get_slate_df(f)

		# Filter columns we are intersted in
		slate_df = slate_df[['Player', 'PlayerID', 'Id', 'Score', 'Variance', 'Salary', 'Team', 'Position']]
		optimal_lineup_test(slate_df, 'Score', 0.3, [2,2,2,2,1], str(slate_id))


if __name__ == "__main__":
	return
