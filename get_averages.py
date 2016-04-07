import pandas as pd
# takes a data frame and a list of columns and gets the last
# 1, 2, 3, 5, 10, 20, 30, 40 and 50 day averages for each game

# requires the data frame to be sorted on 'sorted_column'
# and 'date'

def get_averages(data_frame, column, mid_column_name, sorted_column, day_list, ft):
	print "GETTING AVERAGES FOR"
	print column
	# MUST GROUP BY PLAYER TO GET ACCURATE AVERAGES
	for i in day_list:
		# get stat column
		col = data_frame.loc[:,column]

		# get rolling mean (includes the day of stat, so this
		# must be shifted to create the correct window)
		col = pd.rolling_mean(col, i)
		# shift rolling mean
		col.fillna(-999, inplace = True)
		col = pd.Series(col.iloc[:-1])
		col = pd.Series(-999).append(col)
		col.index = xrange(len(col.index))

		# check for spill over
		col[data_frame.loc[:,sorted_column] <= i] = -999

		# reindex to remedy index change made during shift
		col.index = xrange(len(col.index))

		# add to data frame
		data_frame["L" + str(i) + mid_column_name + column] = col
		
 	return data_frame

def get_lagged_variables(df, column, mid_column_name, sorted_column):
	day_list = [1,2,3,4]
	for i in day_list:
		col = df.loc[:,column]
		col = pd.Series(col.iloc[:-i])
		col = pd.Series([-999] * i).append(col)
		col.index = xrange(len(col.index))

		# check for spill over
		col[df.loc[:,sorted_column] <= i] = -999

		# reindex to remedy index change made during shift
		col.index = xrange(len(col.index))

		# add to data frame
		df[str(i) + "GamesAgo" + mid_column_name + column] = col
	return df

# gets sum of 'stat' in 'n' row chunks in 'df' 
# used to find team aggregates for a particular game
def get_team_aggregates(df, stat, n):
	col = pd.rolling_mean(df.loc[:,stat], n) * n
	col = col[[n*x - 1 for x in xrange(1,(len(col)/n)+1)]]
	col.index = xrange(len(col.index))

	return col












