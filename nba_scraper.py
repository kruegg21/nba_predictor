import warnings
warnings.filterwarnings("ignore")
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
from helper import *
from read_write import read_team_data

def scrape():
    most_recent_date = read_team_data().Date.max().strftime('%Y-%m-%d')
    scrape_new_data(most_recent_date, only_team = False)

def get_page_data(url, feature_names):
	# Load HTML data from page into pagetext
	page = urllib.urlopen(url)
	pagetext = page.read()

	# Make some soup
	soup = BeautifulSoup(pagetext, 'html.parser')

	# Create empty DataFrame object
	df = pd.DataFrame(columns = feature_names, index = range(0,110))

	# Scrape HTML tree
	row = 0
	for element in soup.find_all('tr'):
		column = 0;
		for subelement in element.find_all('td'):
			if(subelement.string is not None):
				df.iat[row,column] = subelement.string
			column += 1
		row += 1

	return df

def get_season(dt):
	season = dt.year
	if dt.month > 9:
		season += 1
	return season

@timeit
def scrape_new_data(most_recent_date, only_team = False):
    feature_names = ['Player','Age','Pos','Date','Team','Home','Opp',
    				 'Result','GS','MP','FG','FGA','FG%','2P','2PA','2P%','3P',
    				 '3PA','3P%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL',
    				 'BLK','TOV','PF','PTS','GmSc']
    accumulator = pd.DataFrame(columns = feature_names)

    # Turn most_recent_date into datetime
    most_recent_date = datetime.strptime(most_recent_date, "%Y-%m-%d")

    # Scrape Player Data
    if not only_team:
        reached_most_recent_date = False
        i = 0
        while not reached_most_recent_date :
            offset = i * 100
            url = "http://www.basketball-reference.com/play-index/pgl_finder.cgi?" + \
            	  "request=1" + \
            	  "&player_id=" + \
            	  "&match=game" + \
            	  "&year_min=2016" + \
            	  "&year_max=2017" + \
            	  "&age_min=0" + \
            	  "&age_max=99" + \
            	  "&team_id=" + \
            	  "&opp_id=" + \
            	  "&is_playoffs=N" + \
            	  "&round_id=" + \
            	  "&game_num_type=" + \
            	  "&game_num_min=" + \
            	  "&game_num_max=" + \
            	  "&game_month=" + \
            	  "&game_day=" + \
                  "&game_location=" + \
            	  "&game_result=" + \
            	  "&is_starter=" + \
            	  "&is_active=" + \
            	  "&is_hof=" + \
            	  "&pos_is_g=Y" + \
            	  "&pos_is_gf=Y" + \
            	  "&pos_is_f=Y" + \
            	  "&pos_is_fg=Y" + \
            	  "&pos_is_fc=Y" + \
            	  "&pos_is_c=Y" + \
            	  "&pos_is_cf=Y" + \
            	  "&c1stat=" + \
            	  "&c1comp=gt" + \
            	  "&c1val=" + \
            	  "&c2stat=" + \
            	  "&c2comp=gt" + \
            	  "&c2val=" + \
            	  "&c3stat=" + \
            	  "&c3comp=gt" + \
            	  "&c3val=" + \
            	  "&c4stat=" + \
            	  "&c4comp=gt" + \
            	  "&c4val=" + \
            	  "&is_dbl_dbl=" + \
            	  "&is_trp_dbl=" + \
            	  "&order_by=date_game" + \
            	  "&order_by_asc=N" + \
            	  "&offset=" + str(offset)

            # Put data from page into DataFrame
            df = get_page_data(url, feature_names)

            # Data Cleaning
            df = df[pd.notnull(df.Player)]

            # Turn date into datetime and choose
            df['Date'] = pd.to_datetime(df.Date)
            date = df.Date.min()
            print date
            print most_recent_date

            if (date <= most_recent_date):
            	reached_most_recent_date = True
            else:
            	i += 1

            if reached_most_recent_date:
            	df = df.drop(df[df.Date <= most_recent_date].index)

            accumulator = pd.concat([accumulator,df])
            accumulator.to_csv('Data/new_player_data.csv', index = False)

    print "Finished scraping player data"

    # Scrape Team Data
    """
    Scraping team data requires getting the data from an entire season because
    some of the data categores are not sorted chronologically.
    """

    # Use 'most_recent_date' to determine season
    season = '2017'
    # get_season(most_recent_date)

    team_data = pd.DataFrame()
    order_by_list = ['date_game', 'orb', 'ast', 'off_rtg']
    feature_names = [['Date','Team','Home','Opp','Result','TeamMP',
    				  'TeamFG','TeamFGA','TeamFG%','Team2P','Team2PA','Team2P%',
    				  'Team3P','Team3PA','Team3P%','TeamFT','TeamFTA','TeamFT%',
    				  'TeamPTS','OppFG','OppFGA','OppFG%','Opp2P','Opp2PA',
    				  'Opp2P%','Opp3P','Opp3PA','Opp3P%','OppFT','OppFTA',
    				  'OppFT%','OppPTS'],
    				 ['Date','Team','Home','Opp','Result','TeamMP',
    				  'TeamORB','TeamDRB','TeamTRB','OppORB','OppDRB','OppTRB'],
    				 ['Date','Team','Home','Opp','Result','TeamMP',
    				  'TeamAST','TeamSTL','TeamBLK','TeamTOV','TeamPF','OppAST',
    				  'OppSTL','OppBLK','OppTOV','OppPF'],
    				 ['Date','Team','Home','Opp','Result','TeamMP',
    			  	  'TeamORtg','TeamFTr','Team3PAr','TeamTS%','TeameFG%',
    			  	  'TeamFT/FGA','OppORtg','OppFTr','Opp3PAr','OppTS%',
    				  'OppeFG%','OppFT/FGA'],
    				 ['Date','Team','Home','Opp','Result','TeamMP',
    				  'TeamAST%','TeamSTL%','TeamBLK%','TeamTOV%','OppAST%',
    				  'OppSTL%','OppBLK%','OppTOV%'],
    				 ['Date','Team','Home','Opp','Result','TeamMP',
    			  	  'TeamORB%','TeamTRB%','OppORB%','OppTRB%']]
    for order, fn in zip(order_by_list, feature_names):
        accumulator = pd.DataFrame(columns = fn)
        reached_end_of_season = False
        i = 0
        while not reached_end_of_season:
            offset = i * 100
            url = "http://www.basketball-reference.com/play-index/tgl_finder.cgi?" + \
            "request=1" + \
            "&player=" + \
            "&match=game" + \
            "&lg_id=NBA" + \
            "&year_min=" + str(season) + \
            "&year_max=" + str(season) + \
            "&team_id=" + \
            "&opp_id=" + \
            "&is_range=N" + \
            "&is_playoffs=N" + \
            "&round_id=" + \
            "&best_of=" + \
            "&team_seed=" + \
            "&opp_seed=" + \
            "&team_seed_cmp=eq" + \
            "&opp_seed_cmp=eq" + \
            "&game_num_type=team" + \
            "&game_num_min=" + \
            "&game_num_max=" + \
            "&game_month=" + \
            "&game_location=" + \
            "&game_result=" + \
            "&is_overtime=" + \
            "&c1stat=" + \
            "&c1comp=gt" + \
            "&c1val=" + \
            "&c2stat=" + \
            "&c2comp=gt" + \
            "&c2val=" + \
            "&c3stat=" + \
            "&c3comp=gt" + \
            "&c3val=" + \
            "&c4stat=" + \
            "&c4comp=gt" + \
            "&c4val=" + \
            "&order_by=" + order + \
            "&order_by_asc=" + \
            "&offset=" + str(offset)

            df = get_page_data(url, fn)

            # Data Cleaning
            df = df[pd.notnull(df.Team)]
            if df.empty:
            	reached_end_of_season = True
            else:
            	i += 1

            accumulator = pd.concat([accumulator,df])
        if team_data.empty:
        	team_data = accumulator
        else:
        	team_data = team_data.merge(accumulator, on = ['Date', 'Team', 'Home',
        												   'Result', 'TeamMP', 'Opp'])
    team_data.to_csv('Data/new_team_data.csv', index = False)
