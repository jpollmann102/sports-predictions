import pandas as pd
import numpy as np

teamNames = ['Arizona Cardinals','Atlanta Falcons','Baltimore Ravens','Buffalo Bills','Carolina Panthers','Chicago Bears','Cincinnati Bengals',
            'Cleveland Browns','Dallas Cowboys','Denver Broncos','Detroit Lions','Green Bay Packers','Houston Texans','Indianapolis Colts',
            'Jacksonville Jaguars','Kansas City Chiefs','Los Angeles Chargers','Los Angeles Rams','Miami Dolphins','Minnesota Vikings',
            'New York Giants','New York Jets','New England Patriots','New Orleans Saints','Oakland Raiders','Philadelphia Eagles',
            'Pittsburgh Steelers','San Francisco 49ers','Seattle Seahawks','Tampa Bay Buccaneers','Tennessee Titans','Washington Redskins']

def getUnplayedGames():
    dfGames = pd.read_csv('data/nfl/nfl_games_2018.csv')
    dfRet = dfGames[dfGames['PtsW'].isnull()]
    dfRet = dfRet[['Winner','@','Loser']]

    return dfRet


def cleanPredictions(week):
    dfTeamO = pd.read_csv('data/nfl/nfl_team_offense.csv')
    dfTeamD = pd.read_csv('data/nfl/nfl_team_defense.csv')
    dfTeamPassO = pd.read_csv('data/nfl/nfl_team_pass_offense.csv')
    dfTeamPassD = pd.read_csv('data/nfl/nfl_team_pass_defense.csv')
    dfTeamRushO = pd.read_csv('data/nfl/nfl_team_rush_offense.csv')
    dfTeamRushD = pd.read_csv('data/nfl/nfl_team_rush_defense.csv')
    dfTeamReceiveO = pd.read_csv('data/nfl/nfl_team_receiving_offense.csv')
    dfTeamReceiveD = pd.read_csv('data/nfl/nfl_team_receiving_defense.csv')

    teamStatNames = ['Yds/G','PYds/G','RYds/G','PTS/G']
    teamPassNames = ['Percentage','PYds/A','Passer Rating']
    teamRushNames = ['RYds/A']
    teamReceiveNames = ['Average','ReYds/G']

    statsO = [dfTeamO, dfTeamPassO, dfTeamRushO, dfTeamReceiveO]
    statsD = [dfTeamD, dfTeamPassD, dfTeamRushD, dfTeamReceiveD]
    teamStatsNames = [teamStatNames, teamPassNames, teamRushNames, teamReceiveNames]

    dfGames = pd.read_csv('data/nfl/nfl_games_2018.csv')
    dfPredict = dfGames[dfGames['PtsW'].isnull()]
    dfPredict = dfPredict[['Winner','Loser']]

    # change team names to match
    # note that these are not alphabetized due to naming conventions of input files
    # the final dataframes are sorted correctly

    for stat in statsO:
        for i in range(0,len(stat)):
            stat.iloc[i, stat.columns.get_loc('Tm')] = teamNames[i]
        stat.sort_values(by=['Tm'], inplace=True)

    for stat in statsD:
        for i in range(0,len(stat)):
            stat.iloc[i, stat.columns.get_loc('Tm')] = teamNames[i]
        stat.sort_values(by=['Tm'], inplace=True)

    # divide home team by visitor team for each stat
    # > 1 means home is favored in stat
    # < 1 means visitor is favored in stat
    # for integer stats, subtract visitor team from home team

    dfPredictNames = ['Winner','Loser'] + teamStatNames + teamPassNames + teamRushNames + teamReceiveNames
    dfPredict = dfPredict.reindex(columns=dfPredictNames, fill_value=0.0)

    dfTemp = dfPredict
    for i in range(len(dfTemp.index)):
        first = dfTemp.iloc[i,dfTemp.columns.get_loc('Winner')]
        second = dfTemp.iloc[i,dfTemp.columns.get_loc('Loser')]

        firstIdx = dfTeamO.index[dfTeamO['Tm'] == first].tolist()
        firstIdx = firstIdx[0]
        secondIdx = dfTeamO.index[dfTeamO['Tm'] == second].tolist()
        secondIdx = secondIdx[0]

        for j in range(len(teamStatsNames)):
            for k in range(len(teamStatsNames[j])):
                winnerStatO = statsO[j].iloc[firstIdx,statsO[j].columns.get_loc(teamStatsNames[j][k])]
                loserStatO = statsO[j].iloc[secondIdx,statsO[j].columns.get_loc(teamStatsNames[j][k])]
                winnerStatD = statsD[j].iloc[firstIdx,statsD[j].columns.get_loc(teamStatsNames[j][k])]
                loserStatD = statsD[j].iloc[secondIdx,statsD[j].columns.get_loc(teamStatsNames[j][k])]
                valO = winnerStatO - loserStatO
                valD = winnerStatD - loserStatD
                dfPredict.iloc[i,dfPredict.columns.get_loc(teamStatsNames[j][k])] = valO - valD

    dfPredict.drop(['Winner','Loser'], axis=1, inplace=True)
    return dfPredict

def cleanTrainingX(week):
    dfTeamO = pd.read_csv('data/nfl/nfl_team_offense.csv')
    dfTeamD = pd.read_csv('data/nfl/nfl_team_defense.csv')
    dfTeamPassO = pd.read_csv('data/nfl/nfl_team_pass_offense.csv')
    dfTeamPassD = pd.read_csv('data/nfl/nfl_team_pass_defense.csv')
    dfTeamRushO = pd.read_csv('data/nfl/nfl_team_rush_offense.csv')
    dfTeamRushD = pd.read_csv('data/nfl/nfl_team_rush_defense.csv')
    dfTeamReceiveO = pd.read_csv('data/nfl/nfl_team_receiving_offense.csv')
    dfTeamReceiveD = pd.read_csv('data/nfl/nfl_team_receiving_defense.csv')

    teamStatNames = ['Yds/G','PYds/G','RYds/G','PTS/G']
    teamPassNames = ['Percentage','PYds/A','Passer Rating']
    teamRushNames = ['RYds/A']
    teamReceiveNames = ['Average','ReYds/G']

    statsO = [dfTeamO, dfTeamPassO, dfTeamRushO, dfTeamReceiveO]
    statsD = [dfTeamD, dfTeamPassD, dfTeamRushD, dfTeamReceiveD]
    teamStatsNames = [teamStatNames, teamPassNames, teamRushNames, teamReceiveNames]

    dfGames = pd.read_csv('data/nfl/nfl_games_2018.csv')
    dfGames.sort_values(by=['@'], inplace=True)
    dfGames.dropna(subset=['PtsW'], inplace=True)
    dfX = dfGames.iloc[:((int(week) - 1) * 16)]

    # change team names to match
    # note that these are not alphabetized due to naming conventions of input files
    # the final dataframes are sorted correctly

    for stat in statsO:
        for i in range(0,len(stat)):
            stat.iloc[i, stat.columns.get_loc('Tm')] = teamNames[i]
        stat.sort_values(by=['Tm'], inplace=True)

    for stat in statsD:
        for i in range(0,len(stat)):
            stat.iloc[i, stat.columns.get_loc('Tm')] = teamNames[i]
        stat.sort_values(by=['Tm'], inplace=True)

    # subtract home team by visitor team for each stat
    # > 0 means home is favored in stat
    # < 0 means visitor is favored in stat

    # example for offense:
    # Jaguars @ Giants, +30.7 Yds/G means Giants average 30.7 more yards per game than Jaguars
    # example for defense:
    # Jaguars @ Giants, -6.5 Yds/G means Giants allow 6.5 less yards per game on defense than Jaguars
    # so to compare:
    # Jaguars @ Giants, Giants average 30.7 more yards per game, and give up 6.5 less, for a total of 37.2 more yards than Jaguars

    dfxNames = ['Winner','@','Loser','PtsW','PtsL'] + teamStatNames + teamPassNames + teamRushNames + teamReceiveNames
    dfX = dfX.reindex(columns=dfxNames, fill_value=0.0)

    dfTemp = dfX
    for i in range(len(dfTemp.index)):
        first = dfTemp.iloc[i,dfTemp.columns.get_loc('Winner')]
        second = dfTemp.iloc[i,dfTemp.columns.get_loc('Loser')]

        firstIdx = dfTeamO.index[dfTeamO['Tm'] == first].tolist()
        firstIdx = firstIdx[0]
        secondIdx = dfTeamO.index[dfTeamO['Tm'] == second].tolist()
        secondIdx = secondIdx[0]

        for j in range(len(teamStatsNames)):
            for k in range(len(teamStatsNames[j])):
                winnerStatO = statsO[j].iloc[firstIdx,statsO[j].columns.get_loc(teamStatsNames[j][k])]
                loserStatO = statsO[j].iloc[secondIdx,statsO[j].columns.get_loc(teamStatsNames[j][k])]
                winnerStatD = statsD[j].iloc[firstIdx,statsD[j].columns.get_loc(teamStatsNames[j][k])]
                loserStatD = statsD[j].iloc[secondIdx,statsD[j].columns.get_loc(teamStatsNames[j][k])]
                valO = winnerStatO - loserStatO
                valD = winnerStatD - loserStatD
                dfX.iloc[i,dfX.columns.get_loc(teamStatsNames[j][k])] = valO - valD

    return dfX

def cleanTrainingY(dfX):
    winningScores = dfX[['PtsW']]
    dfOut = pd.DataFrame().reindex_like(winningScores)
    for i in range(len(dfX)):
        if dfX.iloc[i,1] == '@':
            # Winner is the away team
            dfOut.iloc[i,0] = 0
        else:
            dfOut.iloc[i,0] = 1

    return dfOut
