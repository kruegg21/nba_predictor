import pandas as pd

# Rank
# Player
# Age
# Pos
# Date
# Team
# GS
# MP
# FG
# FGA
# FG%
# 2P
# 2PA
# 2P%
# 3P
# 3PA
# 3P%
# FT
# FTA
# FT%
# ORB
# DRB
# TRB
# AST
# STL
# BLK
# TOV
# PF
# PTS
# GmSc
# PlayerGameNumber
# NumPos
# FanDuelScore
# L1PlayerPTS
# L2PlayerPTS
# L3PlayerPTS
# L5PlayerPTS
# L10PlayerPTS
# L20PlayerPTS
# L30PlayerPTS
# L40PlayerPTS
# L50PlayerPTS
# L1PlayerAST
# L2PlayerAST
# L3PlayerAST
# L5PlayerAST
# L10PlayerAST
# L20PlayerAST
# L30PlayerAST
# L40PlayerAST
# L50PlayerAST
# L1PlayerDRB
# L2PlayerDRB
# L3PlayerDRB
# L5PlayerDRB
# L10PlayerDRB
# L20PlayerDRB
# L30PlayerDRB
# L40PlayerDRB
# L50PlayerDRB
# L1PlayerTRB
# L2PlayerTRB
# L3PlayerTRB
# L5PlayerTRB
# L10PlayerTRB
# L20PlayerTRB
# L30PlayerTRB
# L40PlayerTRB
# L50PlayerTRB
# L1PlayerSTL
# L2PlayerSTL
# L3PlayerSTL
# L5PlayerSTL
# L10PlayerSTL
# L20PlayerSTL
# L30PlayerSTL
# L40PlayerSTL
# L50PlayerSTL
# L1PlayerTOV
# L2PlayerTOV
# L3PlayerTOV
# L5PlayerTOV
# L10PlayerTOV
# L20PlayerTOV
# L30PlayerTOV
# L40PlayerTOV
# L50PlayerTOV
# L1PlayerORB
# L2PlayerORB
# L3PlayerORB
# L5PlayerORB
# L10PlayerORB
# L20PlayerORB
# L30PlayerORB
# L40PlayerORB
# L50PlayerORB
# L1PlayerBLK
# L2PlayerBLK
# L3PlayerBLK
# L5PlayerBLK
# L10PlayerBLK
# L20PlayerBLK
# L30PlayerBLK
# L40PlayerBLK
# L50PlayerBLK
# L1PlayerMP
# L2PlayerMP
# L3PlayerMP
# L5PlayerMP
# L10PlayerMP
# L20PlayerMP
# L30PlayerMP
# L40PlayerMP
# L50PlayerMP
# PTSPerMP
# ASTPerMP
# TRBPerMP
# DRBPerMP
# ORBPerMP
# STLPerMP
# BLKPerMP
# TOVPerMP
# L1PlayerPTSPerMP
# L2PlayerPTSPerMP
# L3PlayerPTSPerMP
# L5PlayerPTSPerMP
# L10PlayerPTSPerMP
# L20PlayerPTSPerMP
# L30PlayerPTSPerMP
# L40PlayerPTSPerMP
# L50PlayerPTSPerMP
# L1PlayerASTPerMP
# L2PlayerASTPerMP
# L3PlayerASTPerMP
# L5PlayerASTPerMP
# L10PlayerASTPerMP
# L20PlayerASTPerMP
# L30PlayerASTPerMP
# L40PlayerASTPerMP
# L50PlayerASTPerMP
# L1PlayerDRBPerMP
# L2PlayerDRBPerMP
# L3PlayerDRBPerMP
# L5PlayerDRBPerMP
# L10PlayerDRBPerMP
# L20PlayerDRBPerMP
# L30PlayerDRBPerMP
# L40PlayerDRBPerMP
# L50PlayerDRBPerMP
# L1PlayerTRBPerMP
# L2PlayerTRBPerMP
# L3PlayerTRBPerMP
# L5PlayerTRBPerMP
# L10PlayerTRBPerMP
# L20PlayerTRBPerMP
# L30PlayerTRBPerMP
# L40PlayerTRBPerMP
# L50PlayerTRBPerMP
# L1PlayerSTLPerMP
# L2PlayerSTLPerMP
# L3PlayerSTLPerMP
# L5PlayerSTLPerMP
# L10PlayerSTLPerMP
# L20PlayerSTLPerMP
# L30PlayerSTLPerMP
# L40PlayerSTLPerMP
# L50PlayerSTLPerMP
# L1PlayerTOVPerMP
# L2PlayerTOVPerMP
# L3PlayerTOVPerMP
# L5PlayerTOVPerMP
# L10PlayerTOVPerMP
# L20PlayerTOVPerMP
# L30PlayerTOVPerMP
# L40PlayerTOVPerMP
# L50PlayerTOVPerMP
# L1PlayerORBPerMP
# L2PlayerORBPerMP
# L3PlayerORBPerMP
# L5PlayerORBPerMP
# L10PlayerORBPerMP
# L20PlayerORBPerMP
# L30PlayerORBPerMP
# L40PlayerORBPerMP
# L50PlayerORBPerMP
# L1PlayerBLKPerMP
# L2PlayerBLKPerMP
# L3PlayerBLKPerMP
# L5PlayerBLKPerMP
# L10PlayerBLKPerMP
# L20PlayerBLKPerMP
# L30PlayerBLKPerMP
# L40PlayerBLKPerMP
# L50PlayerBLKPerMP
# NumericDate_x
# TeamMP
# TeamFG
# TeamFGA
# TeamFG%
# Team2P
# Team2PA
# Team2P%
# Team3P
# Team3PA
# Team3P%
# TeamFT
# TeamFTA
# TeamFT%
# TeamPTS
# OppFG
# OppFGA
# OppFG%
# Opp2P
# Opp2PA
# Opp2P%
# Opp3P
# Opp3PA
# Opp3P%
# OppFT
# OppFTA
# OppFT%
# OppPTS
# TeamORB
# TeamDRB
# TeamTRB
# OppORB
# OppDRB
# OppTRB
# TeamAST
# TeamSTL
# TeamBLK
# TeamTOV
# TeamPF
# OppAST
# OppSTL
# OppBLK
# OppTOV
# OppPF
# TeamORtg
# TeamFTr
# Team3PAr
# TeamTS%
# TeameFG%
# TeamFT/FGA
# OppORtg
# OppFTr
# Opp3PAr
# OppTS%
# OppeFG%
# OppFT/FGA
# TeamORB%
# TeamTRB%
# OppORB%
# OppTRB%
# TeamAST%
# TeamSTL%
# TeamBLK%
# TeamTOV%
# OppAST%
# OppSTL%
# OppBLK%
# OppTOV%
# TeamGameNumber
# OppGameNumber
# Overtime
# B2B
# B2BHome
# B2BAway
# TeamPossessions
# Pace
# TeamPTSPerPoss
# OppPTSPerPoss
# TeamASTPerPoss
# OppASTPerPoss
# TeamORBPerPoss
# OppORBPerPoss
# TeamDRBPerPoss
# OppDRBPerPoss
# TeamTRBPerPoss
# OppTRBPerPoss
# TeamSTLPerPoss
# OppSTLPerPoss
# TeamBLKPerPoss
# OppBLKPerPoss
# TeamTOVPerPoss
# OppTOVPerPoss
# AdjTeamPTS
# AdjTeamAST
# AdjTeamDRB
# AdjTeamORB
# AdjTeamTRB
# AdjTeamSTL
# AdjTeamTOV
# AdjTeamBLK
# L1OppGivenUpTeamASTPerPoss
# L2OppGivenUpTeamASTPerPoss
# L3OppGivenUpTeamASTPerPoss
# L5OppGivenUpTeamASTPerPoss
# L10OppGivenUpTeamASTPerPoss
# L20OppGivenUpTeamASTPerPoss
# L30OppGivenUpTeamASTPerPoss
# L40OppGivenUpTeamASTPerPoss
# L50OppGivenUpTeamASTPerPoss
# L1OppGivenUpTeamDRBPerPoss
# L2OppGivenUpTeamDRBPerPoss
# L3OppGivenUpTeamDRBPerPoss
# L5OppGivenUpTeamDRBPerPoss
# L10OppGivenUpTeamDRBPerPoss
# L20OppGivenUpTeamDRBPerPoss
# L30OppGivenUpTeamDRBPerPoss
# L40OppGivenUpTeamDRBPerPoss
# L50OppGivenUpTeamDRBPerPoss
# L1OppGivenUpTeamORBPerPoss
# L2OppGivenUpTeamORBPerPoss
# L3OppGivenUpTeamORBPerPoss
# L5OppGivenUpTeamORBPerPoss
# L10OppGivenUpTeamORBPerPoss
# L20OppGivenUpTeamORBPerPoss
# L30OppGivenUpTeamORBPerPoss
# L40OppGivenUpTeamORBPerPoss
# L50OppGivenUpTeamORBPerPoss
# L1OppGivenUpTeamTRBPerPoss
# L2OppGivenUpTeamTRBPerPoss
# L3OppGivenUpTeamTRBPerPoss
# L5OppGivenUpTeamTRBPerPoss
# L10OppGivenUpTeamTRBPerPoss
# L20OppGivenUpTeamTRBPerPoss
# L30OppGivenUpTeamTRBPerPoss
# L40OppGivenUpTeamTRBPerPoss
# L50OppGivenUpTeamTRBPerPoss
# L1OppGivenUpTeamSTLPerPoss
# L2OppGivenUpTeamSTLPerPoss
# L3OppGivenUpTeamSTLPerPoss
# L5OppGivenUpTeamSTLPerPoss
# L10OppGivenUpTeamSTLPerPoss
# L20OppGivenUpTeamSTLPerPoss
# L30OppGivenUpTeamSTLPerPoss
# L40OppGivenUpTeamSTLPerPoss
# L50OppGivenUpTeamSTLPerPoss
# L1OppGivenUpTeamBLKPerPoss
# L2OppGivenUpTeamBLKPerPoss
# L3OppGivenUpTeamBLKPerPoss
# L5OppGivenUpTeamBLKPerPoss
# L10OppGivenUpTeamBLKPerPoss
# L20OppGivenUpTeamBLKPerPoss
# L30OppGivenUpTeamBLKPerPoss
# L40OppGivenUpTeamBLKPerPoss
# L50OppGivenUpTeamBLKPerPoss
# L1OppGivenUpTeamTOVPerPoss
# L2OppGivenUpTeamTOVPerPoss
# L3OppGivenUpTeamTOVPerPoss
# L5OppGivenUpTeamTOVPerPoss
# L10OppGivenUpTeamTOVPerPoss
# L20OppGivenUpTeamTOVPerPoss
# L30OppGivenUpTeamTOVPerPoss
# L40OppGivenUpTeamTOVPerPoss
# L50OppGivenUpTeamTOVPerPoss
# L1OppGivenUpAdjTeamPTS
# L2OppGivenUpAdjTeamPTS
# L3OppGivenUpAdjTeamPTS
# L5OppGivenUpAdjTeamPTS
# L10OppGivenUpAdjTeamPTS
# L20OppGivenUpAdjTeamPTS
# L30OppGivenUpAdjTeamPTS
# L40OppGivenUpAdjTeamPTS
# L50OppGivenUpAdjTeamPTS
# L1OppGivenUpAdjTeamAST
# L2OppGivenUpAdjTeamAST
# L3OppGivenUpAdjTeamAST
# L5OppGivenUpAdjTeamAST
# L10OppGivenUpAdjTeamAST
# L20OppGivenUpAdjTeamAST
# L30OppGivenUpAdjTeamAST
# L40OppGivenUpAdjTeamAST
# L50OppGivenUpAdjTeamAST
# L1OppGivenUpAdjTeamORB
# L2OppGivenUpAdjTeamORB
# L3OppGivenUpAdjTeamORB
# L5OppGivenUpAdjTeamORB
# L10OppGivenUpAdjTeamORB
# L20OppGivenUpAdjTeamORB
# L30OppGivenUpAdjTeamORB
# L40OppGivenUpAdjTeamORB
# L50OppGivenUpAdjTeamORB
# L1OppGivenUpAdjTeamDRB
# L2OppGivenUpAdjTeamDRB
# L3OppGivenUpAdjTeamDRB
# L5OppGivenUpAdjTeamDRB
# L10OppGivenUpAdjTeamDRB
# L20OppGivenUpAdjTeamDRB
# L30OppGivenUpAdjTeamDRB
# L40OppGivenUpAdjTeamDRB
# L50OppGivenUpAdjTeamDRB
# L1OppGivenUpAdjTeamTRB
# L2OppGivenUpAdjTeamTRB
# L3OppGivenUpAdjTeamTRB
# L5OppGivenUpAdjTeamTRB
# L10OppGivenUpAdjTeamTRB
# L20OppGivenUpAdjTeamTRB
# L30OppGivenUpAdjTeamTRB
# L40OppGivenUpAdjTeamTRB
# L50OppGivenUpAdjTeamTRB
# L1OppGivenUpAdjTeamSTL
# L2OppGivenUpAdjTeamSTL
# L3OppGivenUpAdjTeamSTL
# L5OppGivenUpAdjTeamSTL
# L10OppGivenUpAdjTeamSTL
# L20OppGivenUpAdjTeamSTL
# L30OppGivenUpAdjTeamSTL
# L40OppGivenUpAdjTeamSTL
# L50OppGivenUpAdjTeamSTL
# L1OppGivenUpAdjTeamTOV
# L2OppGivenUpAdjTeamTOV
# L3OppGivenUpAdjTeamTOV
# L5OppGivenUpAdjTeamTOV
# L10OppGivenUpAdjTeamTOV
# L20OppGivenUpAdjTeamTOV
# L30OppGivenUpAdjTeamTOV
# L40OppGivenUpAdjTeamTOV
# L50OppGivenUpAdjTeamTOV
# L1OppGivenUpAdjTeamBLK
# L2OppGivenUpAdjTeamBLK
# L3OppGivenUpAdjTeamBLK
# L5OppGivenUpAdjTeamBLK
# L10OppGivenUpAdjTeamBLK
# L20OppGivenUpAdjTeamBLK
# L30OppGivenUpAdjTeamBLK
# L40OppGivenUpAdjTeamBLK
# L50OppGivenUpAdjTeamBLK
# L1OppPace
# L2OppPace
# L3OppPace
# L5OppPace
# L10OppPace
# L20OppPace
# L30OppPace
# L40OppPace
# L50OppPace
# L1TeamPace
# L2TeamPace
# L3TeamPace
# L5TeamPace
# L10TeamPace
# L20TeamPace
# L30TeamPace
# L40TeamPace
# L50TeamPace
# L10PaceTot
# L20PaceTot
# L30PaceTot
# L40PaceTot
# L50PaceTot
# NumericDate_y
# Result
# Home
# Opp
# PlayerPTSPerPoss
# PlayerASTPerPoss
# PlayerTRBPerPoss
# PlayerDRBPerPoss
# PlayerORBPerPoss
# PlayerBLKPerPoss
# PlayerSTLPerPoss
# PlayerTOVPerPoss
# L1PlayerPTSPerPoss
# L2PlayerPTSPerPoss
# L3PlayerPTSPerPoss
# L5PlayerPTSPerPoss
# L10PlayerPTSPerPoss
# L20PlayerPTSPerPoss
# L30PlayerPTSPerPoss
# L40PlayerPTSPerPoss
# L50PlayerPTSPerPoss
# L1PlayerASTPerPoss
# L2PlayerASTPerPoss
# L3PlayerASTPerPoss
# L5PlayerASTPerPoss
# L10PlayerASTPerPoss
# L20PlayerASTPerPoss
# L30PlayerASTPerPoss
# L40PlayerASTPerPoss
# L50PlayerASTPerPoss
# L1PlayerDRBPerPoss
# L2PlayerDRBPerPoss
# L3PlayerDRBPerPoss
# L5PlayerDRBPerPoss
# L10PlayerDRBPerPoss
# L20PlayerDRBPerPoss
# L30PlayerDRBPerPoss
# L40PlayerDRBPerPoss
# L50PlayerDRBPerPoss
# L1PlayerTRBPerPoss
# L2PlayerTRBPerPoss
# L3PlayerTRBPerPoss
# L5PlayerTRBPerPoss
# L10PlayerTRBPerPoss
# L20PlayerTRBPerPoss
# L30PlayerTRBPerPoss
# L40PlayerTRBPerPoss
# L50PlayerTRBPerPoss
# L1PlayerORBPerPoss
# L2PlayerORBPerPoss
# L3PlayerORBPerPoss
# L5PlayerORBPerPoss
# L10PlayerORBPerPoss
# L20PlayerORBPerPoss
# L30PlayerORBPerPoss
# L40PlayerORBPerPoss
# L50PlayerORBPerPoss
# L1PlayerSTLPerPoss
# L2PlayerSTLPerPoss
# L3PlayerSTLPerPoss
# L5PlayerSTLPerPoss
# L10PlayerSTLPerPoss
# L20PlayerSTLPerPoss
# L30PlayerSTLPerPoss
# L40PlayerSTLPerPoss
# L50PlayerSTLPerPoss
# L1PlayerBLKPerPoss
# L2PlayerBLKPerPoss
# L3PlayerBLKPerPoss
# L5PlayerBLKPerPoss
# L10PlayerBLKPerPoss
# L20PlayerBLKPerPoss
# L30PlayerBLKPerPoss
# L40PlayerBLKPerPoss
# L50PlayerBLKPerPoss
# L1PlayerTOVPerPoss
# L2PlayerTOVPerPoss
# L3PlayerTOVPerPoss
# L5PlayerTOVPerPoss
# L10PlayerTOVPerPoss
# L20PlayerTOVPerPoss
# L30PlayerTOVPerPoss
# L40PlayerTOVPerPoss
# L50PlayerTOVPerPoss
# L1ExpPlayerPTS
# L2ExpPlayerPTS
# L3ExpPlayerPTS
# L5ExpPlayerPTS
# L10ExpPlayerPTS
# L20ExpPlayerPTS
# L30ExpPlayerPTS
# L40ExpPlayerPTS
# L50ExpPlayerPTS
# L1ExpPlayerAST
# L2ExpPlayerAST
# L3ExpPlayerAST
# L5ExpPlayerAST
# L10ExpPlayerAST
# L20ExpPlayerAST
# L30ExpPlayerAST
# L40ExpPlayerAST
# L50ExpPlayerAST
# L1ExpPlayerTRB
# L2ExpPlayerTRB
# L3ExpPlayerTRB
# L5ExpPlayerTRB
# L10ExpPlayerTRB
# L20ExpPlayerTRB
# L30ExpPlayerTRB
# L40ExpPlayerTRB
# L50ExpPlayerTRB
# L1ExpPlayerORB
# L2ExpPlayerORB
# L3ExpPlayerORB
# L5ExpPlayerORB
# L10ExpPlayerORB
# L20ExpPlayerORB
# L30ExpPlayerORB
# L40ExpPlayerORB
# L50ExpPlayerORB
# L1ExpPlayerDRB
# L2ExpPlayerDRB
# L3ExpPlayerDRB
# L5ExpPlayerDRB
# L10ExpPlayerDRB
# L20ExpPlayerDRB
# L30ExpPlayerDRB
# L40ExpPlayerDRB
# L50ExpPlayerDRB
# L1ExpPlayerSTL
# L2ExpPlayerSTL
# L3ExpPlayerSTL
# L5ExpPlayerSTL
# L10ExpPlayerSTL
# L20ExpPlayerSTL
# L30ExpPlayerSTL
# L40ExpPlayerSTL
# L50ExpPlayerSTL
# L1ExpPlayerBLK
# L2ExpPlayerBLK
# L3ExpPlayerBLK
# L5ExpPlayerBLK
# L10ExpPlayerBLK
# L20ExpPlayerBLK
# L30ExpPlayerBLK
# L40ExpPlayerBLK
# L50ExpPlayerBLK
# L1ExpPlayerTOV
# L2ExpPlayerTOV
# L3ExpPlayerTOV
# L5ExpPlayerTOV
# L10ExpPlayerTOV
# L20ExpPlayerTOV
# L30ExpPlayerTOV
# L40ExpPlayerTOV
# L50ExpPlayerTOV
# L1ExpOppGivenUpTeamPTS
# L2ExpOppGivenUpTeamPTS
# L3ExpOppGivenUpTeamPTS
# L5ExpOppGivenUpTeamPTS
# L10ExpOppGivenUpTeamPTS
# L20ExpOppGivenUpTeamPTS
# L30ExpOppGivenUpTeamPTS
# L40ExpOppGivenUpTeamPTS
# L50ExpOppGivenUpTeamPTS
# L1ExpOppGivenUpTeamAST
# L2ExpOppGivenUpTeamAST
# L3ExpOppGivenUpTeamAST
# L5ExpOppGivenUpTeamAST
# L10ExpOppGivenUpTeamAST
# L20ExpOppGivenUpTeamAST
# L30ExpOppGivenUpTeamAST
# L40ExpOppGivenUpTeamAST
# L50ExpOppGivenUpTeamAST
# L1ExpOppGivenUpTeamTRB
# L2ExpOppGivenUpTeamTRB
# L3ExpOppGivenUpTeamTRB
# L5ExpOppGivenUpTeamTRB
# L10ExpOppGivenUpTeamTRB
# L20ExpOppGivenUpTeamTRB
# L30ExpOppGivenUpTeamTRB
# L40ExpOppGivenUpTeamTRB
# L50ExpOppGivenUpTeamTRB
# L1ExpOppGivenUpTeamORB
# L2ExpOppGivenUpTeamORB
# L3ExpOppGivenUpTeamORB
# L5ExpOppGivenUpTeamORB
# L10ExpOppGivenUpTeamORB
# L20ExpOppGivenUpTeamORB
# L30ExpOppGivenUpTeamORB
# L40ExpOppGivenUpTeamORB
# L50ExpOppGivenUpTeamORB
# L1ExpOppGivenUpTeamDRB
# L2ExpOppGivenUpTeamDRB
# L3ExpOppGivenUpTeamDRB
# L5ExpOppGivenUpTeamDRB
# L10ExpOppGivenUpTeamDRB
# L20ExpOppGivenUpTeamDRB
# L30ExpOppGivenUpTeamDRB
# L40ExpOppGivenUpTeamDRB
# L50ExpOppGivenUpTeamDRB
# L1ExpOppGivenUpTeamSTL
# L2ExpOppGivenUpTeamSTL
# L3ExpOppGivenUpTeamSTL
# L5ExpOppGivenUpTeamSTL
# L10ExpOppGivenUpTeamSTL
# L20ExpOppGivenUpTeamSTL
# L30ExpOppGivenUpTeamSTL
# L40ExpOppGivenUpTeamSTL
# L50ExpOppGivenUpTeamSTL
# L1ExpOppGivenUpTeamBLK
# L2ExpOppGivenUpTeamBLK
# L3ExpOppGivenUpTeamBLK
# L5ExpOppGivenUpTeamBLK
# L10ExpOppGivenUpTeamBLK
# L20ExpOppGivenUpTeamBLK
# L30ExpOppGivenUpTeamBLK
# L40ExpOppGivenUpTeamBLK
# L50ExpOppGivenUpTeamBLK
# L1ExpOppGivenUpTeamTOV
# L2ExpOppGivenUpTeamTOV
# L3ExpOppGivenUpTeamTOV
# L5ExpOppGivenUpTeamTOV
# L10ExpOppGivenUpTeamTOV
# L20ExpOppGivenUpTeamTOV
# L30ExpOppGivenUpTeamTOV
# L40ExpOppGivenUpTeamTOV
# L50ExpOppGivenUpTeamTOV
# PosMetric
# FGAPerMin
# L1FGAPerMin
# L2FGAPerMin
# L3FGAPerMin
# L5FGAPerMin
# L10FGAPerMin
# L20FGAPerMin
# L30FGAPerMin
# L40FGAPerMin
# L50FGAPerMin
# PercTeamShots
# L1PercTeamShots
# L2PercTeamShots
# L3PercTeamShots
# L5PercTeamShots
# L10PercTeamShots
# L20PercTeamShots
# L30PercTeamShots
# L40PercTeamShots
# L50PercTeamShots
# BucketedMin
# L1ExpMinAdjPTS
# L2ExpMinAdjPTS
# L3ExpMinAdjPTS
# L5ExpMinAdjPTS
# L10ExpMinAdjPTS
# L20ExpMinAdjPTS
# L30ExpMinAdjPTS
# L40ExpMinAdjPTS
# L50ExpMinAdjPTS
# L1ExpMinAdjAST
# L2ExpMinAdjAST
# L3ExpMinAdjAST
# L5ExpMinAdjAST
# L10ExpMinAdjAST
# L20ExpMinAdjAST
# L30ExpMinAdjAST
# L40ExpMinAdjAST
# L50ExpMinAdjAST
# L1ExpMinAdjDRB
# L2ExpMinAdjDRB
# L3ExpMinAdjDRB
# L5ExpMinAdjDRB
# L10ExpMinAdjDRB
# L20ExpMinAdjDRB
# L30ExpMinAdjDRB
# L40ExpMinAdjDRB
# L50ExpMinAdjDRB
# L1ExpMinAdjORB
# L2ExpMinAdjORB
# L3ExpMinAdjORB
# L5ExpMinAdjORB
# L10ExpMinAdjORB
# L20ExpMinAdjORB
# L30ExpMinAdjORB
# L40ExpMinAdjORB
# L50ExpMinAdjORB
# L1ExpMinAdjTRB
# L2ExpMinAdjTRB
# L3ExpMinAdjTRB
# L5ExpMinAdjTRB
# L10ExpMinAdjTRB
# L20ExpMinAdjTRB
# L30ExpMinAdjTRB
# L40ExpMinAdjTRB
# L50ExpMinAdjTRB
# L1ExpMinAdjSTL
# L2ExpMinAdjSTL
# L3ExpMinAdjSTL
# L5ExpMinAdjSTL
# L10ExpMinAdjSTL
# L20ExpMinAdjSTL
# L30ExpMinAdjSTL
# L40ExpMinAdjSTL
# L50ExpMinAdjSTL
# L1ExpMinAdjBLK
# L2ExpMinAdjBLK
# L3ExpMinAdjBLK
# L5ExpMinAdjBLK
# L10ExpMinAdjBLK
# L20ExpMinAdjBLK
# L30ExpMinAdjBLK
# L40ExpMinAdjBLK
# L50ExpMinAdjBLK
# L1ExpMinAdjTOV
# L2ExpMinAdjTOV
# L3ExpMinAdjTOV
# L5ExpMinAdjTOV
# L10ExpMinAdjTOV
# L20ExpMinAdjTOV
# L30ExpMinAdjTOV
# L40ExpMinAdjTOV
# L50ExpMinAdjTOV
# L2OppGivenUpTeamPTSPerPoss
# L3OppGivenUpTeamPTSPerPoss
# L5OppGivenUpTeamPTSPerPoss
# L10OppGivenUpTeamPTSPerPoss
# L20OppGivenUpTeamPTSPerPoss
# L30OppGivenUpTeamPTSPerPoss
# L40OppGivenUpTeamPTSPerPoss
# L50OppGivenUpTeamPTSPerPoss

##################################################################
# product of 'build_from_scratch.py'
# contains dates from 10-01-2000 to 02-11-2016
# USE THIS AS BENCHMARK FOR CORRELATION AND XGBOOST TRAINING ERROR
'''
df = pd.read_csv('formatted_final_data.csv')

# correlation calculation

# PTS Per Poss Played
df2 = df[df.L10PlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L10PlayerPTSPerPossPlayed']]
print df2.corr()
# PTS : L10PlayerPTSPerPossPlayed -> 0.571704

df2 = df[df.L20PlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L20PlayerPTSPerPossPlayed']]
print df2.corr()
# PTS : L20PlayerPTSPerPossPlayed -> 0.60367

df2 = df[df.L30PlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L30PlayerPTSPerPossPlayed']]
print df2.corr()
# PTS : L30PlayerPTSPerPossPlayed -> 0.611936

df2 = df[df.L40PlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L40PlayerPTSPerPossPlayed']]
print df2.corr()
# PTS : L40PlayerPTSPerPossPlayed -> 0.614417

df2 = df[df.L50PlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L50PlayerPTSPerPossPlayed']]
print df2.corr()
# PTS : L50PlayerPTSPerPossPlayed -> 0.614366
'''

'''
# Player PTS Per Possession
df2 = df[df.L10PlayerPTSPerPoss != -999]
df2 = df2[['PTS','L10PlayerPTSPerPoss']]
print df2.corr()
# PTS : L10PlayerPTSPerPoss -> 0.704837

df2 = df[df.L20PlayerPTSPerPoss != -999]
df2 = df2[['PTS','L20PlayerPTSPerPoss']]
print df2.corr()
# PTS : L20PlayerPTSPerPoss -> 0.703422

df2 = df[df.L30PlayerPTSPerPoss != -999]
df2 = df2[['PTS','L30PlayerPTSPerPoss']]
print df2.corr()
# PTS : L30PlayerPTSPerPoss -> 0.69763

df2 = df[df.L40PlayerPTSPerPoss != -999]
df2 = df2[['PTS','L40PlayerPTSPerPoss']]
print df2.corr()
# PTS : L40PlayerPTSPerPoss -> 0.692116

df2 = df[df.L50PlayerPTSPerPoss != -999]
df2 = df2[['PTS','L50PlayerPTSPerPoss']]
print df2.corr()
# PTS : L50PlayerPTSPerPoss -> 0.687067
'''

'''
# Opp Given UP PTS Per Poss
df2 = df[df.L2OppGivenUpTeamPTSPerPoss != -999]
df2 = df2[['PTS','L2OppGivenUpTeamPTSPerPoss']]
print df2.corr()
# PTS : L2OppGivenUpTeamPTSPerPoss -> 0.020739 

df2 = df[df.L5OppGivenUpTeamPTSPerPoss != -999]
df2 = df2[['PTS','L5OppGivenUpTeamPTSPerPoss']]
print df2.corr()
# PTS : L5OppGivenUpTeamPTSPerPoss -> 0.027335

df2 = df[df.L10OppGivenUpTeamPTSPerPoss != -999]
df2 = df2[['PTS','L10OppGivenUpTeamPTSPerPoss']]
print df2.corr()
# PTS : L10OppGivenUpTeamPTSPerPoss -> 0.032576 

df2 = df[df.L20OppGivenUpTeamPTSPerPoss != -999]
df2 = df2[['PTS','L20OppGivenUpTeamPTSPerPoss']]
print df2.corr()
# PTS : L20OppGivenUpTeamPTSPerPoss -> 0.034892

df2 = df[df.L30OppGivenUpTeamPTSPerPoss != -999]
df2 = df2[['PTS','L30OppGivenUpTeamPTSPerPoss']]
print df2.corr()
# PTS : L30OppGivenUpTeamPTSPerPoss ->  0.034852

df2 = df[df.L40OppGivenUpTeamPTSPerPoss != -999]
df2 = df2[['PTS','L40OppGivenUpTeamPTSPerPoss']]
print df2.corr()
# PTS : L4OppGivenUpTeamPTSPerPoss -> 0.035021  

df2 = df[df.L50OppGivenUpTeamPTSPerPoss != -999]
df2 = df2[['PTS','L50OppGivenUpTeamPTSPerPoss']]
print df2.corr()
# PTS : L50OppGivenUpTeamPTSPerPoss -> 0.034697
'''

'''
# Expected Possession Adjusted Opponent Given Up PTS
df2 = df[df.L1ExpOppGivenUpTeamPTS != -999]
df2 = df2[['PTS','L1ExpOppGivenUpTeamPTS']]
print df2.corr()
# PTS : L1ExpOppGivenUpTeamPTS -> 0.024976

df2 = df[df.L2ExpOppGivenUpTeamPTS != -999]
df2 = df2[['PTS','L2ExpOppGivenUpTeamPTS']]
print df2.corr()
# PTS : L2ExpOppGivenUpTeamPTS -> 0.031914

df2 = df[df.L5ExpOppGivenUpTeamPTS != -999]
df2 = df2[['PTS','L5ExpOppGivenUpTeamPTS']]
print df2.corr()
# PTS : L5ExpOppGivenUpTeamPTS -> 0.040857

df2 = df[df.L10ExpOppGivenUpTeamPTS != -999]
df2 = df2[['PTS','L10ExpOppGivenUpTeamPTS']]
print df2.corr()
# PTS : L10ExpOppGivenUpTeamPTS -> 0.046938 

df2 = df[df.L20ExpOppGivenUpTeamPTS != -999]
df2 = df2[['PTS','L20ExpOppGivenUpTeamPTS']]
print df2.corr()
# PTS : L20ExpOppGivenUpTeamPTS -> 0.049892

df2 = df[df.L30ExpOppGivenUpTeamPTS != -999]
df2 = df2[['PTS','L30ExpOppGivenUpTeamPTS']]
print df2.corr()
# PTS : L30ExpOppGivenUpTeamPTS -> 0.050062

df2 = df[df.L40ExpOppGivenUpTeamPTS != -999]
df2 = df2[['PTS','L40ExpOppGivenUpTeamPTS']]
print df2.corr()
# PTS : L40ExpOppGivenUpTeamPTS -> 0.050266

df2 = df[df.L50ExpOppGivenUpTeamPTS != -999]
df2 = df2[['PTS','L50ExpOppGivenUpTeamPTS']]
print df2.corr()
# PTS : L50ExpOppGivenUpTeamPTS -> 0.050064
'''

##################################################################


# df = pd.read_csv('starters.csv')



'''
df2 = df[df.L10FGAPerMin != -999]
df2 = df2[['FGA','L10FGAPerMin']]
# FGA : L10FGAPerMin -> 0.663413 

df2 = df[df.L20FGAPerMin != -999]
df2 = df2[['FGA','L20FGAPerMin']]
# FGA : L20FGAPerMin -> 0.66951

df2 = df[df.L30FGAPerMin != -999]
df2 = df2[['FGA','L30FGAPerMin']]
# FGA : L30FGAPerMin -> 0.668512

df2 = df[df.L40FGAPerMin != -999]
df2 = df2[['FGA','L40FGAPerMin']]
# FGA : L40FGAPerMin -> 0.66589

df2 = df[df.L50FGAPerMin != -999]
df2 = df2[['FGA','L50FGAPerMin']]

# adjusted Usage score taking into account any
# surplus or deficit in available Usage
df2 = df[df.ExpectedL20FGAPerMin != -999]
df2 = df2[['FGA','ExpectedL20FGAPerMin']]
# FGA : ExpectedL20FGAPerMin -> 0.675007
'''

'''
# correlation for opponent's defense versus 'one spot'
df = pd.read_csv('PositionalDatasets/one_spot_full.csv')

df2 = df[df.L5OppOneSpotPlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L5OppOneSpotPlayerPTSPerPossPlayed']]
# PTS : L5OppOneSpotPlayerPTSPerPossPlayed -> 0.012921

df2 = df[df.L10OppOneSpotPlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L10OppOneSpotPlayerPTSPerPossPlayed']]
# PTS : L10OppOneSpotPlayerPTSPerPossPlayed -> 0.029531

df2 = df[df.L20OppOneSpotPlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L20OppOneSpotPlayerPTSPerPossPlayed']]
# PTS : L20OppOneSpotPlayerPTSPerPossPlayed -> 0.041

df2 = df[df.L30OppOneSpotPlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L30OppOneSpotPlayerPTSPerPossPlayed']]
# PTS : L30OppOneSpotPlayerPTSPerPossPlayed -> 0.040454

df2 = df[df.L40OppOneSpotPlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L40OppOneSpotPlayerPTSPerPossPlayed']]
# PTS : L40OppOneSpotPlayerPTSPerPossPlayed -> 0.043407

df2 = df[df.L50OppOneSpotPlayerPTSPerPossPlayed != -999]
df2 = df2[['PTS','L50OppOneSpotPlayerPTSPerPossPlayed']]
# PTS : L50OppOneSpotPlayerPTSPerPossPlayed -> 0.048695 
'''

'''
df = pd.read_csv('PositionalDatasets/combined_positional_full.csv')

print len(df.index)
df2 = df[df.L10OppPositionalOverUnderPTS != -999]
print len(df2.index)
df2 = df2[['PTS','L10OppPositionalOverUnderPTS']]
print df2.corr()

print len(df.index)
df2 = df[df.L20OppPositionalOverUnderPTS != -999]
print len(df2.index)
df2 = df2[['PTS','L20OppPositionalOverUnderPTS']]
print df2.corr()

print len(df.index)
df2 = df[df.L30OppPositionalOverUnderPTS != -999]
print len(df2.index)
df2 = df2[['PTS','L30OppPositionalOverUnderPTS']]
print df2.corr()

print len(df.index)
df2 = df[df.L40OppPositionalOverUnderPTS != -999]
print len(df2.index)
df2 = df2[['PTS','L40OppPositionalOverUnderPTS']]
print df2.corr()

print len(df.index)
df2 = df[df.L50OppPositionalOverUnderPTS != -999]
print len(df2.index)
df2 = df2[['PTS','L50OppPositionalOverUnderPTS']]
print df2.corr()

# PTS : L5OppOneSpotPlayerPTSPerPossPlayed -> 0.012921
'''

df = pd.read_csv('usage_set.csv')
print len(df.index)
df2 = df[df['ExpectedL20Usg%'] != -999]
print len(df2.index)
df2 = df2[['FGA','ExpectedL20Usg%']]
print df2.corr()

print len(df.index)
df2 = df[df['L20Usg%'] != -999]
print len(df2.index)
df2 = df2[['FGA','L20Usg%']]
print df2.corr()



