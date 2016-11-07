from collections import defaultdict
from itertools import combinations, product
from optimal_lineups import get_slate_df
from helper import find_fd_filenames, timeit
import numpy as np
import pandas as pd

class player_set(object):
    def __init__(self, players):
        self.players = players
        self.player_ids = [player.PlayerID for player in self.players]
        self.score = np.sum([player.Score for player in self.players])
        self.cost = np.sum([player.Cost for player in self.players])
        self.n_players = len(players)
        self.teams = set(player.Team for player in self.players)
        self.games = set(tuple(sorted([player.Team, player.Opp])) for player in self.players)

    def get_lineup(self):
        lineup = [player for player in self.players] + [self.score] + \
                 [self.cost] + [id_ for id_ in self.player_ids]
        return lineup

    def __add__(self, other):
        players = self.players + other.players
        return player_set(players)

    def __repr__(self):
        players = [p.Player for p in self.players]
        return "Players: {} with score: {}".format(players, self.score)

    def __cmp__(self, other):
        return self.score > other.score

class partition(object):
    def __init__(self, one_player_score = None, two_player_score = None,
                 two_players = None, one_player = None):
        self.one_player_score = list()
        self.two_player_score = list()
        self.two_players = list()
        self.one_player = list()

        # if one_player_score:
        #     self.one_player_score.append(one_player_score)
        #
        # if two_player_score:
        #     self.two_player_score.append(two_player_score)
        #
        # if two_players:
        #     self.two_players.append(two_players)
        #
        # if one_player:
        #     self.one_player.append(one_player)



    def add(self, players, score):
        if len(players) == 2:
            self.two_players.append(players)
            self.two_player_score.append(score)
        else:
            self.one_player.append(players)
            self.one_player_score.append(score)

    def __repr__(self):
        # Two players
        if self.two_players:
            two_players = [(pair[0].Player, pair[1].Player) for pair in self.two_players]
            two_player_score = [truncate(score, 2) for score in self.two_player_score]

        if self.one_player:
            one_player = [pair[0].Player for pair in self.one_player]
            one_player_score = [truncate(score, 2) for score in self.one_player_score]

        if self.one_player_score:
            if self.two_player_score:
                return "Two players: {} with score: {}. One player: {} with score: {}." \
                        .format(two_players,
                                two_player_score,
                                one_player,
                                one_player_score)
            else:
                return "One player: {} with score: {}." \
                        .format(one_player,
                                one_player_score)
        else:
            return "Two players: {} with score: {}." \
                    .format(two_players,
                            two_player_score)

def make_partition(df, position):
    # Make partition_dictionary dictionary
    partition_dictionary = defaultdict(list)

    # Relevant columns
    relevant_columns = ['Player', 'PlayerID', 'Team', 'Opp', 'Score', 'Cost']

    # Select players in postion
    players = df[df.Position == position][relevant_columns]
    print "Number of {} is {}".format(position, len(players))

    if position != 'C':
        # Make combinations of 2
        for combination in combinations(players.index, 2):
            p1, p2 = combination
            two_players = (players.loc[p1, relevant_columns],
                           players.loc[p2, relevant_columns])
            p = player_set(two_players)
            partition_dictionary[p.cost].append(p)

    for index in players.index:
        one_player = (players.loc[index, relevant_columns],)
        p = player_set(one_player)
        partition_dictionary[p.cost].append(p)
    return partition_dictionary

@timeit
def combine_layers(layer1, layer2, position_pair, cost_cutoff):
    # Each layer is tuple with the position as the first entry and the
    # defaultdict of cost and lists player_set objects key value pairs
    position1, dict1 = layer1
    position2, dict2 = layer2

    partition_dict = defaultdict(list)
    print "Combining {} and {}".format(position1, position2)
    print "Position pair is {}".format(position_pair)

    for d in [dict1, dict2]:
        for cost, player_set_list in d.iteritems():
            if len(player_set_list) > 2:
                d[cost] = sorted(player_set_list,
                                     key = lambda player_set: player_set.score,
                                     reverse = True)[:2]

    for item1, item2 in product(dict1.items(), dict2.items()):
        cost1, player_set_list1 = item1
        cost2, player_set_list2 = item2

        # Get cost of new partition
        cost = cost1 + cost2

        if cost < cost_cutoff:
            if position1 in position_pair:
                player_set_list1 = [l for l in player_set_list1 if l.n_players == 2]
            elif "-" not in position1:
                player_set_list1 = [l for l in player_set_list1 if l.n_players == 1]
            else:
                pass

            if position2 in position_pair:
                player_set_list2 = [l for l in player_set_list2 if l.n_players == 2]
            elif "-" not in position2:
                player_set_list2 = [l for l in player_set_list2 if l.n_players == 1]
            else:
                pass

            for player_set1, player_set2 in product(player_set_list1, player_set_list2):
                partition_dict[cost].append(player_set1 + player_set2)
    return ("{}-{}".format(position1, position2), partition_dict)

@timeit
def add_wildcard(partition_dict, slate_df, total_salary):
    p = partition_dict[1]
    final_lineups = defaultdict(list)
    relevant_columns = ['Player', 'PlayerID', 'Team', 'Opp', 'Score', 'Cost']
    players = slate_df[relevant_columns]
    n_lineups = 0
    for cost, lineups in p.iteritems():
        n_lineups += len(lineups)
        for lineup in lineups:
            # Constraints
            lineup_player_ids = lineup.player_ids
            remaining_salary = total_salary - cost

            # Filter out players already in lineup
            possible_players = players[~players['PlayerID'].isin(lineup_player_ids) & \
                                       (players.Cost <= remaining_salary)]

            # Get best player to add
            index = possible_players['Score'].argmax()
            lineup_set = lineup + player_set((players.iloc[index],))
            final_lineups[lineup_set.cost].append(lineup_set)
    return final_lineups

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def reduce(function, iterable, initializer=None, a1=None, a2=None):
    it = iter(iterable)
    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')
    accum_value = initializer
    for x in it:
        accum_value = function(accum_value, x, a1, a2)
    return accum_value

def pprint(partition_dict):
    if type(partition_dict.keys()[0]) == 'str':
        for key1, item1 in partition_dict.iteritems():
            print "{}".format(key1)
            for key2, item2 in sorted(item1.iteritems()):
                print "\t{}".format(key2)
                for item3 in item2:
                    print "\t\t{}".format(item3)
                print "\n"
    else:
        for key2, item2 in sorted(partition_dict.iteritems()):
            print "{}".format(key2)
            for item3 in item2:
                print "\t{}".format(item3)
            print "\n"

if __name__ == "__main__":
    min_price = 3500
    step_size = 100
    max_price = 10000
    total_salary = 60000

    file_names = find_fd_filenames()
    for f in file_names:
        # Get data for slate
        slate_id, slate_df = get_slate_df(f)

        # Filter columns we are intersted in
        slate_df = slate_df[['Player', 'PlayerID', 'Id', 'Score', 'Variance',
        					 'Salary', 'Team', 'Position', 'Opponent']]

        slate_df.rename(columns = {'Opponent': 'Opp', 'Salary': 'Cost'},
                        inplace = True)

        # Make partition objects
        partition_dict = dict()
        positions = ['PG', 'SG', 'SF', 'PF', 'C']
        for position in positions:
            partition_dict[position] = make_partition(slate_df, position)

        # Position pair represents the two positions we are picking 2 players for
        # using the G/F wildcards
        lineups = []
        for position_pair in product(['PG', 'SG'], ['PF', 'SF']):
            # Order in more efficient way possible
            not_position_pair = list(set(['PG', 'SG', 'PF', 'SF']) - set(position_pair))
            partition_tuples = [(position_pair[0], partition_dict[position_pair[0]]),
                                (position_pair[1], partition_dict[position_pair[1]]),
                                (not_position_pair[0], partition_dict[not_position_pair[0]]),
                                (not_position_pair[1], partition_dict[not_position_pair[1]]),
                                ('C', partition_dict['C'])]

            # Combine layers
            lineups = []
            lineup_dict = reduce(combine_layers, partition_tuples, None, position_pair, total_salary - min_price)
            lineup_dict = add_wildcard(lineup_dict, slate_df, total_salary)
            for cost, lineup_list in lineup_dict.iteritems():
                for lineup in lineup_list:
                    lineups.append(lineup.get_lineup())
            lineups_df = pd.DataFrame(lineups, columns = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7',
                                                          'P8', 'Score', 'Cost', 'ID1', 'ID2', 'ID3',
                                                          'ID4', 'ID5', 'ID6', 'ID7', 'ID8'])
            lineups_df.to_csv('whatever.csv')
