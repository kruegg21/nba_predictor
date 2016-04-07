import urllib
from bs4 import BeautifulSoup
import pandas as pd
import helper_functions as hf

# gets player data from one url from basketballreference.com, each page only show 100 entries of player data
def get_page_data(url, feature_names):
	#load HTML data from page into pagetext 
	page = urllib.urlopen(url)
	pagetext = page.read()

	# make some soup
	soup = BeautifulSoup(pagetext, 'html.parser')

	# create empty DataFrame object
	df = pd.DataFrame(columns = feature_names, index = range(0,110))

	# scrape HTML tree
	row = 0
	for element in soup.find_all('tr'):
		column = 0;
		for subelement in element.find_all('td'):
			if(subelement.string is not None):
				df.iat[row,column] = subelement.string
			column += 1
		row += 1

	return df

# scrapes new data from basketballreference.com, beginning at starting_date "starting_date" and up until most recent available data
# exports player data to 'player_data_new.csv' and team data t0 'team_data_new.csv'

# dumps to 'player_data_new.csv' and 'team_data_new.csv'

def scrape_new_data(starting_date):
	# creates accumulator DataFrame to hold data (change feature names)
	feature_names = ['Rank','Player','Age','Pos','Date','Team','Home','Opp','Result','GS','MP','FG','FGA','FG%','2P','2PA','2P%',
					'3P','3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','GmSc']
	accumulator = pd.DataFrame(columns = feature_names)

	# scrape player data
	reached_starting_date = 0
	i = 0
	while reached_starting_date == 0:
		offset = i * 100
		url = "http://www.basketball-reference.com/play-index/pgl_finder.cgi?request=1&player_id=&match=game&year_min=2016&year_max=2016&age_min=0&age_max=99&team_id=&opp_id=&is_playoffs=N&round_id=&game_num_type=&game_num_min=&game_num_max=&game_month=&game_day=&game_location=&game_result=&is_starter=&is_active=&is_hof=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&is_dbl_dbl=&is_trp_dbl=&order_by=date_game&order_by_asc=&offset=" + str(offset)
		df = get_page_data(url, feature_names)

		print i

		# data cleaning 
		df = df.drop([0,1,2,3,4,5])
		df = df.drop(df[pd.isnull(df.Date)].index)

		### NEW ####
		# reindex
		n = len(df.index)
		df.index = range(0,n)

		# get date and turn starting date into numeric
		date = df.loc[n - 1].Date
		numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
			pd.to_datetime(pd.Series(starting_date))) / 86400000000000
		numeric_date = numeric_date.iloc[0]
		if (numeric_date < 0):
			reached_starting_date = 1
		else:
			i += 1

		if reached_starting_date:
			# remove all days past starting date from df
			for j in range(0,n):
				date = df.loc[j].Date
				numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
				pd.to_datetime(pd.Series(starting_date))) / 86400000000000
				numeric_date = numeric_date.iloc[0]
				if (numeric_date < 0):
					df = df.drop(j)

		### END NEW #### 

		accumulator = pd.concat([accumulator,df])
		accumulator.to_csv('DataSets/NewData/player_data_new.csv', index = False)

	# scrape team data
	# creates accumulator DataFrame to hold data (change feature names)
	feature_names = ['Rank','Date','Team','Home','Opp','Result','TeamMP','TeamFG','TeamFGA','TeamFG%',
					 'Team2P','Team2PA','Team2P%','Team3P','Team3PA','Team3P%','TeamFT','TeamFTA','TeamFT%',
					 'TeamPTS','OppFG','OppFGA','OppFG%','Opp2P','Opp2PA','Opp2P%','Opp3P','Opp3PA','Opp3P%',
					 'OppFT','OppFTA','OppFT%','OppPTS']
	accumulator = pd.DataFrame(columns = feature_names)

	reached_starting_date = 0
	i = 0
	while reached_starting_date == 0:
		offset = i * 100
		url = "http://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2016&year_max=2016&team_id=&opp_id=&is_range=N&is_playoffs=N&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=date_game&order_by_asc=&offset=" + str(offset)
		df = get_page_data(url, feature_names)

		print i
		# data cleaning 
		df = df.drop([0,1,2,3,4,5])
		df = df.drop(df[pd.isnull(df.Date)].index)

		### NEW ####
		# reindex
		n = len(df.index)
		df.index = range(0,n)

		# get date and turn starting date into numeric
		date = df.loc[n - 1].Date
		numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
			pd.to_datetime(pd.Series(starting_date))) / 86400000000000
		numeric_date = numeric_date.iloc[0]
		if (numeric_date < 0):
			reached_starting_date = 1
		else:
			i += 1

		if reached_starting_date:
			# remove all days past starting date from df
			for j in range(0,n):
				date = df.loc[j].Date
				numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
				pd.to_datetime(pd.Series(starting_date))) / 86400000000000
				numeric_date = numeric_date.iloc[0]
				if (numeric_date < 0):
					df = df.drop(j)
		accumulator = pd.concat([accumulator,df])

	td1 = accumulator

	feature_names = ['Rank','Date','Team','Home','Opp','Result','TeamMP','TeamORB','TeamDRB',
					'TeamTRB','OppORB','OppDRB','OppTRB']
	accumulator = pd.DataFrame(columns = feature_names)

	for i in range(0,50):
		offset = i * 100
		url = "http://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2016&year_max=2016&team_id=&opp_id=&is_range=N&is_playoffs=N&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=orb&order_by_asc=&offset=" + str(offset)
		df = get_page_data(url, feature_names)

		print i
		# data cleaning 
		df = df.drop([0,1,2,3,4,5])
		df = df.drop(df[pd.isnull(df.Date)].index)

		### NEW ####
		# reindex
		n = len(df.index)
		df.index = range(0,n)
		for j in range(0,n):
			date = df.loc[j].Date
			numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
			pd.to_datetime(pd.Series(starting_date))) / 86400000000000
			numeric_date = numeric_date.iloc[0]
			if (numeric_date < 0):
				df = df.drop(j)
		accumulator = pd.concat([accumulator,df])
	td2 = accumulator



	feature_names = ['Rank','Date','Team','Home','Opp','Result','TeamMP','TeamAST','TeamSTL',
					'TeamBLK','TeamTOV','TeamPF','OppAST','OppSTL','OppBLK','OppTOV','OppPF']
	accumulator = pd.DataFrame(columns = feature_names)

	for i in range(0,50):
		offset = i * 100
		url = "http://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2016&year_max=2016&team_id=&opp_id=&is_range=N&is_playoffs=N&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=ast&order_by_asc=&offset=" + str(offset)
		df = get_page_data(url, feature_names)

		print i
		# data cleaning 
		df = df.drop([0,1,2,3,4,5])
		df = df.drop(df[pd.isnull(df.Date)].index)

		### NEW ####
		# reindex
		n = len(df.index)
		df.index = range(0,n)
		for j in range(0,n):
			date = df.loc[j].Date
			numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
			pd.to_datetime(pd.Series(starting_date))) / 86400000000000
			numeric_date = numeric_date.iloc[0]
			if (numeric_date < 0):
				df = df.drop(j)
		accumulator = pd.concat([accumulator,df])
	td3 = accumulator

	feature_names = ['Rank','Date','Team','Home','Opp','Result','TeamMP','TeamORtg','TeamFTr',
					'Team3PAr','TeamTS%','TeameFG%','TeamFT/FGA','OppORtg','OppFTr','Opp3PAr',
					'OppTS%','OppeFG%','OppFT/FGA']
	accumulator = pd.DataFrame(columns = feature_names)

	for i in range(0,50):
		offset = i * 100
		url = "http://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2016&year_max=2016&team_id=&opp_id=&is_range=N&is_playoffs=N&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=off_rtg&order_by_asc=&offset=" + str(offset)
		df = get_page_data(url, feature_names)

		print i
		# data cleaning 
		df = df.drop([0,1,2,3,4,5])
		df = df.drop(df[pd.isnull(df.Date)].index)

		### NEW ####
		# reindex
		n = len(df.index)
		df.index = range(0,n)
		for j in range(0,n):
			date = df.loc[j].Date
			numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
			pd.to_datetime(pd.Series(starting_date))) / 86400000000000
			numeric_date = numeric_date.iloc[0]
			if (numeric_date < 0):
				df = df.drop(j)
		accumulator = pd.concat([accumulator,df])
	td4 = accumulator

	feature_names = ['Rank','Date','Team','Home','Opp','Result','TeamMP','TeamORB%','TeamTRB%',
					'OppORB%','OppTRB%']
	accumulator = pd.DataFrame(columns = feature_names)

	for i in range(0,50):
		offset = i * 100
		url = "http://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2016&year_max=2016&team_id=&opp_id=&is_range=N&is_playoffs=N&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=orb_pct&order_by_asc=&offset=" + str(offset)
		df = get_page_data(url, feature_names)

		print i
		# data cleaning 
		df = df.drop([0,1,2,3,4,5])
		df = df.drop(df[pd.isnull(df.Date)].index)

		### NEW ####
		# reindex
		n = len(df.index)
		df.index = range(0,n)
		for j in range(0,n):
			date = df.loc[j].Date
			numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
			pd.to_datetime(pd.Series(starting_date))) / 86400000000000
			numeric_date = numeric_date.iloc[0]
			if (numeric_date < 0):
				df = df.drop(j)
		accumulator = pd.concat([accumulator,df])
	td5 = accumulator


	feature_names = ['Rank','Date','Team','Home','Opp','Result','TeamMP','TeamAST%','TeamSTL%',
					'TeamBLK%','TeamTOV%','OppAST%','OppSTL%','OppBLK%','OppTOV%']
	accumulator = pd.DataFrame(columns = feature_names)

	for i in range(0,50):
		offset = i * 100
		url = "http://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2016&year_max=2016&team_id=&opp_id=&is_range=N&is_playoffs=N&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=gt&c1val=&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=ast_pct&order_by_asc=&offset=" + str(offset)
		df = get_page_data(url, feature_names)

		print i
		# data cleaning 
		df = df.drop([0,1,2,3,4,5])
		df = df.drop(df[pd.isnull(df.Date)].index)

		# reindex
		n = len(df.index)
		df.index = range(0,n)
		for j in range(0,n):
			date = df.loc[j].Date
			numeric_date = pd.to_numeric(pd.to_datetime(pd.Series(date)) - \
			pd.to_datetime(pd.Series(starting_date))) / 86400000000000
			numeric_date = numeric_date.iloc[0]
			if (numeric_date < 0):
				df = df.drop(j)
		accumulator = pd.concat([accumulator,df])
	td6 = accumulator

	team_data = hf.concat_team_data(td1,td2,td3,td4,td5,td6)

	team_data.to_csv('DataSets/NewData/team_data_new.csv')
