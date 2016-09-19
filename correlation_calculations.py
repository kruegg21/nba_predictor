import pandas as pd
import scipy as sc

# product of 'build_from_scratch.py'
# contains dates from 10-01-2000 to 02-11-2016
# USE THIS AS BENCHMARK FOR CORRELATION AND XGBOOST TRAINING ERROR
df = pd.read_csv('DataSets/FormattedData/formatted_final_data.csv')

print sc.stats.pearsonr(df['PTS'], df['L10PlayerPTSPerPossPlayed'])

# # correlation calculation
#
# # PTS Per Poss Played
# df2 = df[df.L10PlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L10PlayerPTSPerPossPlayed']]
# print df2.corr()
# # PTS : L10PlayerPTSPerPossPlayed -> 0.571704
#
# df2 = df[df.L20PlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L20PlayerPTSPerPossPlayed']]
# print df2.corr()
# # PTS : L20PlayerPTSPerPossPlayed -> 0.60367
#
# df2 = df[df.L30PlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L30PlayerPTSPerPossPlayed']]
# print df2.corr()
# # PTS : L30PlayerPTSPerPossPlayed -> 0.611936
#
# df2 = df[df.L40PlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L40PlayerPTSPerPossPlayed']]
# print df2.corr()
# # PTS : L40PlayerPTSPerPossPlayed -> 0.614417
#
# df2 = df[df.L50PlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L50PlayerPTSPerPossPlayed']]
# print df2.corr()
# # PTS : L50PlayerPTSPerPossPlayed -> 0.614366
# '''
#
# '''
# # Player PTS Per Possession
# df2 = df[df.L10PlayerPTSPerPoss != -999]
# df2 = df2[['PTS','L10PlayerPTSPerPoss']]
# print df2.corr()
# # PTS : L10PlayerPTSPerPoss -> 0.704837
#
# df2 = df[df.L20PlayerPTSPerPoss != -999]
# df2 = df2[['PTS','L20PlayerPTSPerPoss']]
# print df2.corr()
# # PTS : L20PlayerPTSPerPoss -> 0.703422
#
# df2 = df[df.L30PlayerPTSPerPoss != -999]
# df2 = df2[['PTS','L30PlayerPTSPerPoss']]
# print df2.corr()
# # PTS : L30PlayerPTSPerPoss -> 0.69763
#
# df2 = df[df.L40PlayerPTSPerPoss != -999]
# df2 = df2[['PTS','L40PlayerPTSPerPoss']]
# print df2.corr()
# # PTS : L40PlayerPTSPerPoss -> 0.692116
#
# df2 = df[df.L50PlayerPTSPerPoss != -999]
# df2 = df2[['PTS','L50PlayerPTSPerPoss']]
# print df2.corr()
# # PTS : L50PlayerPTSPerPoss -> 0.687067
# '''
#
# '''
# # Opp Given UP PTS Per Poss
# df2 = df[df.L2OppGivenUpTeamPTSPerPoss != -999]
# df2 = df2[['PTS','L2OppGivenUpTeamPTSPerPoss']]
# print df2.corr()
# # PTS : L2OppGivenUpTeamPTSPerPoss -> 0.020739
#
# df2 = df[df.L5OppGivenUpTeamPTSPerPoss != -999]
# df2 = df2[['PTS','L5OppGivenUpTeamPTSPerPoss']]
# print df2.corr()
# # PTS : L5OppGivenUpTeamPTSPerPoss -> 0.027335
#
# df2 = df[df.L10OppGivenUpTeamPTSPerPoss != -999]
# df2 = df2[['PTS','L10OppGivenUpTeamPTSPerPoss']]
# print df2.corr()
# # PTS : L10OppGivenUpTeamPTSPerPoss -> 0.032576
#
# df2 = df[df.L20OppGivenUpTeamPTSPerPoss != -999]
# df2 = df2[['PTS','L20OppGivenUpTeamPTSPerPoss']]
# print df2.corr()
# # PTS : L20OppGivenUpTeamPTSPerPoss -> 0.034892
#
# df2 = df[df.L30OppGivenUpTeamPTSPerPoss != -999]
# df2 = df2[['PTS','L30OppGivenUpTeamPTSPerPoss']]
# print df2.corr()
# # PTS : L30OppGivenUpTeamPTSPerPoss ->  0.034852
#
# df2 = df[df.L40OppGivenUpTeamPTSPerPoss != -999]
# df2 = df2[['PTS','L40OppGivenUpTeamPTSPerPoss']]
# print df2.corr()
# # PTS : L4OppGivenUpTeamPTSPerPoss -> 0.035021
#
# df2 = df[df.L50OppGivenUpTeamPTSPerPoss != -999]
# df2 = df2[['PTS','L50OppGivenUpTeamPTSPerPoss']]
# print df2.corr()
# # PTS : L50OppGivenUpTeamPTSPerPoss -> 0.034697
# '''
#
# '''
# # Expected Possession Adjusted Opponent Given Up PTS
# df2 = df[df.L1ExpOppGivenUpTeamPTS != -999]
# df2 = df2[['PTS','L1ExpOppGivenUpTeamPTS']]
# print df2.corr()
# # PTS : L1ExpOppGivenUpTeamPTS -> 0.024976
#
# df2 = df[df.L2ExpOppGivenUpTeamPTS != -999]
# df2 = df2[['PTS','L2ExpOppGivenUpTeamPTS']]
# print df2.corr()
# # PTS : L2ExpOppGivenUpTeamPTS -> 0.031914
#
# df2 = df[df.L5ExpOppGivenUpTeamPTS != -999]
# df2 = df2[['PTS','L5ExpOppGivenUpTeamPTS']]
# print df2.corr()
# # PTS : L5ExpOppGivenUpTeamPTS -> 0.040857
#
# df2 = df[df.L10ExpOppGivenUpTeamPTS != -999]
# df2 = df2[['PTS','L10ExpOppGivenUpTeamPTS']]
# print df2.corr()
# # PTS : L10ExpOppGivenUpTeamPTS -> 0.046938
#
# df2 = df[df.L20ExpOppGivenUpTeamPTS != -999]
# df2 = df2[['PTS','L20ExpOppGivenUpTeamPTS']]
# print df2.corr()
# # PTS : L20ExpOppGivenUpTeamPTS -> 0.049892
#
# df2 = df[df.L30ExpOppGivenUpTeamPTS != -999]
# df2 = df2[['PTS','L30ExpOppGivenUpTeamPTS']]
# print df2.corr()
# # PTS : L30ExpOppGivenUpTeamPTS -> 0.050062
#
# df2 = df[df.L40ExpOppGivenUpTeamPTS != -999]
# df2 = df2[['PTS','L40ExpOppGivenUpTeamPTS']]
# print df2.corr()
# # PTS : L40ExpOppGivenUpTeamPTS -> 0.050266
#
# df2 = df[df.L50ExpOppGivenUpTeamPTS != -999]
# df2 = df2[['PTS','L50ExpOppGivenUpTeamPTS']]
# print df2.corr()
# # PTS : L50ExpOppGivenUpTeamPTS -> 0.050064
# '''
#
# ##################################################################
# # df = pd.read_csv('starters.csv')
#
#
#
# '''
# df2 = df[df.L10FGAPerMin != -999]
# df2 = df2[['FGA','L10FGAPerMin']]
# # FGA : L10FGAPerMin -> 0.663413
#
# df2 = df[df.L20FGAPerMin != -999]
# df2 = df2[['FGA','L20FGAPerMin']]
# # FGA : L20FGAPerMin -> 0.66951
#
# df2 = df[df.L30FGAPerMin != -999]
# df2 = df2[['FGA','L30FGAPerMin']]
# # FGA : L30FGAPerMin -> 0.668512
#
# df2 = df[df.L40FGAPerMin != -999]
# df2 = df2[['FGA','L40FGAPerMin']]
# # FGA : L40FGAPerMin -> 0.66589
#
# df2 = df[df.L50FGAPerMin != -999]
# df2 = df2[['FGA','L50FGAPerMin']]
#
# # adjusted Usage score taking into account any
# # surplus or deficit in available Usage
# df2 = df[df.ExpectedL20FGAPerMin != -999]
# df2 = df2[['FGA','ExpectedL20FGAPerMin']]
# # FGA : ExpectedL20FGAPerMin -> 0.675007
# '''
#
# '''
# # correlation for opponent's defense versus 'one spot'
# df = pd.read_csv('PositionalDatasets/one_spot_full.csv')
#
# df2 = df[df.L5OppOneSpotPlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L5OppOneSpotPlayerPTSPerPossPlayed']]
# # PTS : L5OppOneSpotPlayerPTSPerPossPlayed -> 0.012921
#
# df2 = df[df.L10OppOneSpotPlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L10OppOneSpotPlayerPTSPerPossPlayed']]
# # PTS : L10OppOneSpotPlayerPTSPerPossPlayed -> 0.029531
#
# df2 = df[df.L20OppOneSpotPlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L20OppOneSpotPlayerPTSPerPossPlayed']]
# # PTS : L20OppOneSpotPlayerPTSPerPossPlayed -> 0.041
#
# df2 = df[df.L30OppOneSpotPlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L30OppOneSpotPlayerPTSPerPossPlayed']]
# # PTS : L30OppOneSpotPlayerPTSPerPossPlayed -> 0.040454
#
# df2 = df[df.L40OppOneSpotPlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L40OppOneSpotPlayerPTSPerPossPlayed']]
# # PTS : L40OppOneSpotPlayerPTSPerPossPlayed -> 0.043407
#
# df2 = df[df.L50OppOneSpotPlayerPTSPerPossPlayed != -999]
# df2 = df2[['PTS','L50OppOneSpotPlayerPTSPerPossPlayed']]
# # PTS : L50OppOneSpotPlayerPTSPerPossPlayed -> 0.048695
# '''
#
# '''
# df = pd.read_csv('PositionalDatasets/combined_positional_full.csv')
#
# print len(df.index)
# df2 = df[df.L10OppPositionalOverUnderPTS != -999]
# print len(df2.index)
# df2 = df2[['PTS','L10OppPositionalOverUnderPTS']]
# print df2.corr()
#
# print len(df.index)
# df2 = df[df.L20OppPositionalOverUnderPTS != -999]
# print len(df2.index)
# df2 = df2[['PTS','L20OppPositionalOverUnderPTS']]
# print df2.corr()
#
# print len(df.index)
# df2 = df[df.L30OppPositionalOverUnderPTS != -999]
# print len(df2.index)
# df2 = df2[['PTS','L30OppPositionalOverUnderPTS']]
# print df2.corr()
#
# print len(df.index)
# df2 = df[df.L40OppPositionalOverUnderPTS != -999]
# print len(df2.index)
# df2 = df2[['PTS','L40OppPositionalOverUnderPTS']]
# print df2.corr()
#
# print len(df.index)
# df2 = df[df.L50OppPositionalOverUnderPTS != -999]
# print len(df2.index)
# df2 = df2[['PTS','L50OppPositionalOverUnderPTS']]
# print df2.corr()
#
# # PTS : L5OppOneSpotPlayerPTSPerPossPlayed -> 0.012921
# '''
#
# col = 'L30'
#
# df = pd.read_csv('DataSets/starters_usage.csv')
# print len(df.index)
# df2 = df[df['Expected' + col + 'PercStartersShots'] != -999]
# print len(df2.index)
# df2 = df2[['PercStartersShots','Expected' + col + 'PercStartersShots']]
# # 0.771311
# print df2.corr()
#
# print len(df.index)
# df2 = df[df[col + 'PercStartersShots'] != -999]
# print len(df2.index)
# df2 = df2[['PercStartersShots',col + 'PercStartersShots']]
# print df2.corr()
