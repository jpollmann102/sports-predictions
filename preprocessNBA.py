import pandas as pd
import numpy as np

teamNames = ['Atlanta Hawks','Boston Celtics','Brooklyn Nets','Charlotte Hornets','Chicago Bulls',
            'Cleveland Cavaliers','Dallas Mavericks','Denver Nuggets','Detroit Pistons',
            'Golden State Warriors','Houston Rockets','Indiana Pacers','Los Angeles Clippers',
            'Los Angeles Lakers','Memphis Grizzlies','Miami Heat','Milwaukee Bucks',
            'Minnesota Timberwolves','New Orleans Pelicans','New York Knicks',
            'Oklahoma City Thunder','Orlando Magic','Philadelphia 76ers','Phoenix Suns',
            'Portland Trail Blazers','Sacramento Kings','San Antonio Spurs','Toronto Raptors',
            'Utah Jazz','Washington Wizards']

def getPlayedGames():
    schedule = ['nba_games_2019_october.csv','nba_games_2019_november.csv','nba_games_2019_december.csv',
                'nba_games_2019_january.csv','nba_games_2019_february.csv','nba_games_2019_march.csv',
                'nba_games_2019_april.csv']

    dfGames = pd.read_csv('data/nba/{}'.format(schedule[0]))

    for i in range(1, len(schedule)):
        dfTemp = pd.read_csv('data/nba/{}'.format(schedule[i]))
        dfGames.append(dfTemp)

    dfRet = dfGames[['Away','AwayPts','Home','HomePts']]

    return dfRet

def getUnplayedGames():
    schedule = ['nba_games_2019_october.csv','nba_games_2019_november.csv','nba_games_2019_december.csv',
                'nba_games_2019_january.csv','nba_games_2019_february.csv','nba_games_2019_march.csv',
                'nba_games_2019_april.csv']

    dfGames = pd.read_csv('data/nba/{}'.format(schedule[0]))

    for i in range(1, len(schedule)):
        dfTemp = pd.read_csv('data/nba/{}'.format(schedule[i]))
        dfGames = dfGames.append(dfTemp)

    dfRet = dfGames[dfGames['AwayPts'].isnull()]
    dfRet = dfRet[['Away','Home']]

    return dfRet

def cleanPredictions():

    dfTeamO = pd.read_csv('data/nba/nba_team_offense.csv')
    dfTeamD = pd.read_csv('data/nba/nba_team_defense.csv')
    dfTeamReb = pd.read_csv('data/nba/nba_team_rebounds.csv')

    teamOffenseNames = ['FG%','3P%','PPS','AFG%']
    teamDefenseNames = ['FG%','3P%','PPS','AFG%']
    teamReboundNames = ['ORPG','DRPG']

    stats = [dfTeamO, dfTeamD, dfTeamReb]
    teamStatsNames = [teamOffenseNames, teamDefenseNames]

    dfPredict = getUnplayedGames()

    for stat in stats:
        for i in range(0,len(stat)):
            stat.iloc[i, stat.columns.get_loc('Tm')] = teamNames[i]
        stat.sort_values(by=['Tm'], inplace=True)

    # divide home team by visitor team for each stat
    # > 1 means home is favored in stat
    # < 1 means visitor is favored in stat
    # for integer stats, subtract visitor team from home team

    dfPredictNames = ['Away','Home'] + teamOffenseNames + teamDefenseNames + teamReboundNames
    dfPredict = dfPredict.reindex(columns=dfPredictNames, fill_value=0.0)

    dfTemp = dfPredict
    for i in range(len(dfTemp.index)):
        first = dfTemp.iloc[i,dfTemp.columns.get_loc('Away')]
        second = dfTemp.iloc[i,dfTemp.columns.get_loc('Home')]

        firstIdx = dfTeamO.index[dfTeamO['Tm'] == first].tolist()
        firstIdx = firstIdx[0]
        secondIdx = dfTeamO.index[dfTeamO['Tm'] == second].tolist()
        secondIdx = secondIdx[0]

        for j in range(len(teamStatsNames)):
            for k in range(len(teamStatsNames[j])):
                awayStatO = dfTeamO.iloc[firstIdx,dfTeamO.columns.get_loc(teamStatsNames[j][k])]
                homeStatO = dfTeamO.iloc[secondIdx,dfTeamO.columns.get_loc(teamStatsNames[j][k])]
                awayStatD = dfTeamD.iloc[firstIdx,dfTeamD.columns.get_loc(teamStatsNames[j][k])]
                homeStatD = dfTeamD.iloc[secondIdx,dfTeamD.columns.get_loc(teamStatsNames[j][k])]
                valO = homeStatO / awayStatO
                valD = homeStatD / awayStatD
                dfPredict.iloc[i,dfPredict.columns.get_loc(teamStatsNames[j][k])] = valO - valD

        for name in teamReboundNames:
            awayStatReb = dfTeamReb.iloc[firstIdx,dfTeamReb.columns.get_loc(name)]
            homeStatReb = dfTeamReb.iloc[secondIdx,dfTeamReb.columns.get_loc(name)]
            valReb = homeStatReb - awayStatReb
            dfPredict.iloc[i,dfPredict.columns.get_loc(name)] = valReb

    dfPredict.drop(['Away','Home'], axis=1, inplace=True)
    return dfPredict

def cleanTrainingX():

    dfTeamO = pd.read_csv('data/nba/nba_team_offense.csv')
    dfTeamD = pd.read_csv('data/nba/nba_team_defense.csv')
    dfTeamReb = pd.read_csv('data/nba/nba_team_rebounds.csv')

    teamOffenseNames = ['FG%','3P%','PPS','AFG%']
    teamDefenseNames = ['FG%','3P%','PPS','AFG%']
    teamReboundNames = ['ORPG','DRPG']

    teamStatsNames = [teamOffenseNames, teamDefenseNames]
    stats = [dfTeamO, dfTeamD, dfTeamReb]

    dfX = getPlayedGames()
    dfX.drop(['AwayPts','HomePts'], axis=1, inplace=True)

    for stat in stats:
        for i in range(0,len(stat)):
            stat.iloc[i, stat.columns.get_loc('Tm')] = teamNames[i]
        stat.sort_values(by=['Tm'], inplace=True)

    # divide home team by visitor team for each stat
    # > 1 means home is favored in stat
    # < 1 means visitor is favored in stat
    # for integer stats, subtract visitor team from home team

    dfXNames = ['Away','Home'] + teamOffenseNames + teamDefenseNames + teamReboundNames
    dfX = dfX.reindex(columns=dfXNames, fill_value=0.0)

    dfTemp = dfX
    for i in range(len(dfTemp.index)):
        first = dfTemp.iloc[i,dfTemp.columns.get_loc('Away')]
        second = dfTemp.iloc[i,dfTemp.columns.get_loc('Home')]

        firstIdx = dfTeamO.index[dfTeamO['Tm'] == first].tolist()
        firstIdx = firstIdx[0]
        secondIdx = dfTeamO.index[dfTeamO['Tm'] == second].tolist()
        secondIdx = secondIdx[0]

        for j in range(len(teamStatsNames)):
            for k in range(len(teamStatsNames[j])):
                awayStatO = dfTeamO.iloc[firstIdx,dfTeamO.columns.get_loc(teamStatsNames[j][k])]
                homeStatO = dfTeamO.iloc[secondIdx,dfTeamO.columns.get_loc(teamStatsNames[j][k])]
                awayStatD = dfTeamD.iloc[firstIdx,dfTeamD.columns.get_loc(teamStatsNames[j][k])]
                homeStatD = dfTeamD.iloc[secondIdx,dfTeamD.columns.get_loc(teamStatsNames[j][k])]
                valO = homeStatO / awayStatO
                valD = homeStatD / awayStatD
                dfX.iloc[i,dfX.columns.get_loc(teamStatsNames[j][k])] = valO - valD

        for name in teamReboundNames:
            awayStatReb = dfTeamReb.iloc[firstIdx,dfTeamReb.columns.get_loc(name)]
            homeStatReb = dfTeamReb.iloc[secondIdx,dfTeamReb.columns.get_loc(name)]
            valReb = homeStatReb - awayStatReb
            dfX.iloc[i,dfX.columns.get_loc(name)] = valReb

    dfX.drop(['Away','Home'], axis=1, inplace=True)
    return dfX

def cleanTrainingY():
    dfX = getPlayedGames()
    scores = dfX[['AwayPts']]
    dfOut = pd.DataFrame().reindex_like(scores)
    for i in range(len(dfX)):
        if dfX.iloc[i,1] > dfX.iloc[i,3]:
            # Winner is the away team
            dfOut.iloc[i,0] = 0
        else:
            dfOut.iloc[i,0] = 1

    return dfOut
