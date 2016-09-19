import pandas as pd
import numexpr as ne
import time
import numpy as np
import helper_functions as hf
import xgboost as xgb
import final_score as fs
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import get_averages as ga
import variance_functions as vf

# SMALL TEST DF
df = pd.DataFrame(data = [['Stephen Curry',1,30,10,'SAC','2011-01-01',0.1],
						  ['Stephen Curry',2,25,0,'GSW','2011-01-01',0.2],
						  ['Stephen Curry',3,32,6.2,'GSW','2011-01-01',0.15],
						  ['Stephen Curry',4,31,9,'GSW','2011-01-01',0.12],
						  ['Stephen Curry',5,31,10,'GSW','2011-01-01',0.13],
						  ['Stephen Curry',6,31,11,'GSW','2011-01-01',0.15],
						  ['Steve Nash',1,21,12,'PHX','2011-01-01',0.16],
						  ['Steve Nash',2,19,13,'PHX','2011-01-01',0.18],
						  ['Steve Nash',3,17,19,'PHX','2011-01-01',0.20],
						  ['Steve Nash',4,23,9,'PHX','2011-01-01',0.50]],
				  columns = ['Player','PlayerGameNumber','PTS','AST','Team','Date','Usg'])


df = hf.calculate_team_change(df, 'Player')

print df


###########################################################################
# CODE SNIPPETS

# SORT
'''
df = df.sort_values(by = ['Player', 'PlayerGameNumber'])
df.index = xrange(len(df.index))
'''

# ELIMINATE 'AST' COLUMN IF IT EXISTS IN DF
'''
if 'AST' in df.columns:
	df = df.drop('AST', 1)
'''

# GROUP BY 
'''
grouped = df.groupby(['Team','Date'])
for i in grouped:
	print i[1]
'''

# ADD SHIFTED COLUMN
# example shifts by 1
'''
df['ShiftedColumn'] = df['ColumnToShift'].shift(1)
'''
###########################################################################
