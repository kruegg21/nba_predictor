import pandas as pd
import itertools
from collections import Counter

# looks at slate information and finds lineup permutations for 'slate' 

# 1. Reads position specific player lists from 'SlateList' folder
# 2. Creates combinations for all lineups
# 3. Filters the possible lineups based on the following rules
#	a) No more than 4 players from one team
#	b) Minimum of 3 teams represented
#	c) Cost does not exceed 'maximum_cost'
#	d) Cost does is not less than 'minimum_cost'
# 4. Dumps the lineups that pass the filter into 'perm_lineups.csv'

# PRINTS THE NUMBER OF POSSIBLE 
def lineup_permutations(slate, maximum_cost, minimum_cost):
	pg = pd.read_csv('SlateLists/' + slate + '_pg_list.csv')
	sg = pd.read_csv('SlateLists/' + slate + '_sg_list.csv')
	sf = pd.read_csv('SlateLists/' + slate + '_sf_list.csv')
	pf = pd.read_csv('SlateLists/' + slate + '_pf_list.csv')
	c = pd.read_csv('SlateLists/' + slate + '_c_list.csv')

	print pg
	print sg
	print sf
	print pf
	print c

	pg_options = [x for x in itertools.combinations(pg.index, 2)]
	sg_options = [x for x in itertools.combinations(sg.index, 2)]
	sf_options = [x for x in itertools.combinations(sf.index, 2)]
	pf_options = [x for x in itertools.combinations(pf.index, 2)]

	comb = [x for x in itertools.product(pg_options,sg_options,sf_options,pf_options,c.index)]

	print "NUMBER OF LINEUPS WITHOUT FILTERING"
	print len(comb)
	num_lineups = 0
	lineups = []
	for i in comb:
		team = []
		cost = pg.loc[i[0][0],'Cost']
		cost += pg.loc[i[0][1],'Cost']
		score = pg.loc[i[0][0],'Score']
		score += pg.loc[i[0][1],'Score']
		team.append(pg.loc[i[0][0],'Team'])
		team.append(pg.loc[i[0][1],'Team'])

		cost += sg.loc[i[1][0],'Cost']
		cost += sg.loc[i[1][1],'Cost']
		score += sg.loc[i[1][0],'Score']
		score += sg.loc[i[1][1],'Score']
		team.append(sg.loc[i[1][0],'Team'])
		team.append(sg.loc[i[1][1],'Team'])

		cost += sf.loc[i[2][0],'Cost']
		cost += sf.loc[i[2][1],'Cost']
		score += sf.loc[i[2][0],'Score']
		score += sf.loc[i[2][1],'Score']
		team.append(sf.loc[i[2][0],'Team'])
		team.append(sf.loc[i[2][1],'Team'])

		cost += pf.loc[i[3][0],'Cost']
		cost += pf.loc[i[3][1],'Cost']
		score += pf.loc[i[3][0],'Score']
		score += pf.loc[i[3][1],'Score']
		team.append(pf.loc[i[3][0],'Team'])
		team.append(pf.loc[i[3][1],'Team'])

		cost += c.loc[i[4],'Cost']
		score += c.loc[i[4],'Score']
		team.append(c.loc[i[4],'Team'])

		max_players_on_team = Counter(team).most_common(1)[0][1]
		print max_players_on_team
		print team
		print '\n'
		number_of_teams = len(Counter(team))

		if (cost <= maximum_cost) & (cost > minimum_cost) & (max_players_on_team < 4) & (number_of_teams > 2):
			lineups.append([score, pg.loc[i[0][0],'Player'], pg.loc[i[0][1],'Player'], sg.loc[i[1][0],'Player'],
								   sg.loc[i[1][1],'Player'], sf.loc[i[2][0],'Player'], sf.loc[i[2][1],'Player'],
								   pf.loc[i[3][0],'Player'], pf.loc[i[3][1],'Player'], c.loc[i[4],'Player'],
								   pg.loc[i[0][0],'Id'], pg.loc[i[0][1],'Id'], sg.loc[i[1][0],'Id'],
								   sg.loc[i[1][1],'Id'], sf.loc[i[2][0],'Id'], sf.loc[i[2][1],'Id'],
								   pf.loc[i[3][0],'Id'], pf.loc[i[3][1],'Id'], c.loc[i[4],'Id']])
			num_lineups += 1

	lineups = sorted(lineups, key = lambda x: x[0], reverse = True)

	print "NUMBER OF LINEUPS AFTER FILTERING"
	print num_lineups

	bl = pd.DataFrame(lineups, columns = ['Score','Player1','Player2','Player3','Player4','Player5','Player6','Player7','Player8','Player9',
										  'PG1','PG2','SG1','SG2','SF1','SF1','PF1','PF2','C'])
	bl.to_csv('perm_lineups.csv', index = False)

lineup_permutations('late', 60000, 54000)
