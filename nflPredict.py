import pandas as pd
import tensorflow as tf
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

from scipy.stats import poisson, skellam

# teamStatsFile = 'csv/nfl_team_stats_2016_2016.csv'
gameStatsFile = 'csv/nfl_game_stats_2016_2016.csv'
season17File = 'csv/nfl_game_stats_2017_2018.csv'

# def processRawTeamStats(teamStatsCSV):
#     # processes the file containing team data.
#     names = ['PF_Off', 'Yds_Off', 'Ply_Off', 'Y_Per_P_Off', 'TO_Off', 'FL_Off', '1stD_Off', 'Cmp_Off', 'Att_Off',
#                 'TD_Off', 'Int_Off', 'NY_Per_A_Off', 'Y_Per_A_Off', 'Pen_Off', '1stPy_Off', 'Sc_Perc_Off',
#                 'TO_Perc_Off', 'EXP_Off', 'Cmp_POff', 'Att_POff', 'Cmp_Perc_Off', 'Yds_POff', 'TD_POff',
#                 'TD_Perc_Off', 'Int_POff', 'Int_Perc_Off', 'Lng', 'Y_Per_A_POff', 'AY_Per_A_Off', 'Y_Per_C_Off',
#                 'Y_Per_G_Off', 'Rate_Off', 'Sk_Off', 'NY_Per_A_POff', 'ANY_Per_A_Off', 'Sk_Perc_Off', '4QC', 'GWD',
#                 'EXP_POff', 'PF_Def', 'Yds_Def', 'Ply_Def', 'Y_Per_P_Def', 'TO_Def', 'FL_Def', '1stD_Def',
#                 'Cmp_Def', 'Att_Def', 'TD_Def', 'Int_Def', 'NY_Per_A_Def', 'Y_Per_A_Def', 'Pen_Def', '1stPy_Def',
#                 'Sc_Perc_Def', 'TO_Perc_Def', 'EXP_Def', 'Cmp_PDef', 'Att_PDef', 'Cmp_Perc_Def', 'Yds_PDef',
#                 'TD_PDef', 'TD_Perc_Def', 'Int_PDef', 'Int_Perc_Def', 'Y_Per_A_PDef', 'AY_Per_A_Def', 'Y_Per_C_Def',
#                 'Y_Per_G_Def', 'Rate_Def', 'Sk_Def', 'NY_Per_A_PDef', 'ANY_Per_A_Def', 'Sk_Perc_Def', 'EXP_PDef']
#
#     data = pd.read_csv(teamStatsCSV, names=names, header=0)
#     return data

def processRawGameStats(gameStatsCSV):
    # processes the file containing game data
    names = ['Visitor_Team', 'Visitor_Team_PTS', 'Home_Team', 'Home_Team_PTS']

    data = pd.read_csv(gameStatsCSV, names=names, header=0)
    return data

def processSeasonFile(seasonCSV):
    # processes the file containing a season's games and results
    names = ['Visitor_Team', 'Visitor_Team_PTS', 'Home_Team', 'Home_Team_PTS']

    data = pd.read_csv(seasonCSV, names=names, header=0)
    return data

def printAvgScores(games):
    out = games[['Home_Team', 'Visitor_Team', 'Home_Team_PTS', 'Visitor_Team_PTS']]
    print(out.mean())

# dfTeamStats = processRawTeamStats(teamStatsFile)
dfGameStats = processRawGameStats(gameStatsFile)
dfSeasonStats = processSeasonFile(season17File)

dfGameStats = dfGameStats[['Home_Team', 'Visitor_Team', 'Home_Team_PTS', 'Visitor_Team_PTS']]
dfSeasonScores = dfSeasonStats[['Home_Team_PTS', 'Visitor_Team_PTS']]
dfSeasonStats = dfSeasonStats[['Home_Team', 'Visitor_Team']]

scoreModelData = pd.concat([dfGameStats[['Home_Team', 'Visitor_Team', 'Home_Team_PTS']].assign(home=1).rename(
                            columns={'Home_Team':'team', 'Visitor_Team':'opponent', 'Home_Team_PTS':'score'}),
                            dfGameStats[['Visitor_Team', 'Home_Team', 'Visitor_Team_PTS']].assign(home=0).rename(
                            columns={'Visitor_Team':'team', 'Home_Team':'opponent', 'Visitor_Team_PTS':'score'})])

poissonModel = smf.glm(formula="score ~ home + team + opponent", data=scoreModelData, family=sm.families.Poisson()).fit()

def simulateGame(footModel, home, away, maxScore=55):
    if gameStatsFile.__contains__('2000') or gameStatsFile.__contains__('2012'):
        if home == 'Los Angeles Rams': home = 'St. Louis Rams'
        if away == 'Los Angeles Rams': away = 'St. Louis Rams'
    if home == 'Los Angeles Chargers': home = 'San Diego Chargers'
    if away == 'Los Angeles Chargers': away = 'San Diego Chargers'
    homeScoreAvg = footModel.predict(pd.DataFrame(data={'team':home, 'opponent':away, 'home':1}, index=[1])).values[0]
    awayScoreAvg = footModel.predict(pd.DataFrame(data={'team':away, 'opponent':home, 'home':0}, index=[1])).values[0]

    teamPrediction = [[poisson.pmf(i, teamAvg) for i in range(0, maxScore + 1)] for teamAvg in [homeScoreAvg, awayScoreAvg]]

    return np.outer(np.array(teamPrediction[0]), np.array(teamPrediction[1]))

homeTeams = dfSeasonStats.loc[:, "Home_Team"]
awayTeams = dfSeasonStats.loc[:, "Visitor_Team"]
homeScores = dfSeasonScores.loc[:, "Home_Team_PTS"]
awayScores = dfSeasonScores.loc[:, "Visitor_Team_PTS"]

def simulateSeason(footModel, homeTeams, awayTeams, printGames=True):
    numGames = 256
    correct = 0
    lineWins = 0
    perfectScorePredictions = 0
    perfectGamePredictions = 0
    closeScorePredictions = 0
    closeGamePredictions = 0
    avgLineError = 0
    for i in range(0, numGames - 1):
        game = simulateGame(footModel, homeTeams[i], awayTeams[i])
        homeW = np.sum(np.tril(game, -1))
        awayW = np.sum(np.triu(game, 1))
        tie = np.sum(np.diag(game))

        scoreProb = max(map(max, game))
        homeS, awayS = np.where(game == scoreProb)

        homeScore = homeS[0]
        awayScore = awayS[0]

        HpredVSreal = abs(homeScore - homeScores[i])
        ApredVSreal = abs(awayScore - awayScores[i])

        if homeScores[i] > awayScores[i]:
            realW = homeTeams[i]
            realL = awayTeams[i]
            actualLine = homeScores[i] - awayScores[i]
        else:
            realW = awayTeams[i]
            realL = homeTeams[i]
            actualLine = awayScores[i] - homeScores[i]

        if homeW > awayW:
            predictedW = homeTeams[i]
        else:
            predictedW = awayTeams[i]

        if realW == predictedW:
            correct = correct + 1

        winningScore = max(homeScore, awayScore)
        if winningScore == homeScore:
            losingScore = awayScore
        else:
            losingScore = homeScore

        HscorePercentError = (HpredVSreal / homeScores[i])
        AscorePercentError = (ApredVSreal / awayScores[i])

        predictedLine = winningScore - losingScore

        if(actualLine < predictedLine): lineWins += 1

        lineError = (abs(predictedLine - actualLine) / actualLine) * 100

        avgLineError += lineError

        if HscorePercentError == 0 or AscorePercentError == 0:
            perfectScorePredictions += 1

        if HscorePercentError < .1 or AscorePercentError < .1:
            closeScorePredictions += 1

        if HscorePercentError == 0 and AscorePercentError == 0:
            perfectGamePredictions += 1

        if HscorePercentError < .1 and AscorePercentError < .1:
            closeGamePredictions += 1

        if printGames:
            print("{} @ {}".format(homeTeams[i], awayTeams[i]))
            print("\n")
            print("{0} chance to win: {1:.2f}".format(homeTeams[i], homeW * 100))
            print("{0} chance to win: {1:.2f}".format(awayTeams[i], awayW * 100))
            print("Chance of a tie: {:.2f}".format(tie * 100))
            print("\n")
            print("Predicted winner: {}".format(predictedW))
            print("Predicted score: {}: {} @ {}: {}".format(homeTeams[i], homeScore, awayTeams[i], awayScore))
            print("Predicted line: {} - {:.2f}".format(predictedW, predictedLine))
            print("\n")
            print("Actual results:")
            print("{}: {} @ {}: {}".format(homeTeams[i], homeScores[i], awayTeams[i], awayScores[i]))
            print("{} predicted score error: {:.2f}".format(homeTeams[i], HscorePercentError * 100))
            print("{} predicted score error: {:.2f}".format(awayTeams[i], AscorePercentError * 100))
            print("Actual line: {} - {}".format(realW, actualLine))
            print("Line error: {:.2f}".format(lineError))
            print("Winner prediction correct: {}".format(realW == predictedW))
            print("---------------------------------------------------------")
            print("\n")

    percentCorrectWinners = (correct / numGames) * 100
    percentCloseScores = (closeScorePredictions / numGames) * 100
    percentCloseGames = (closeGamePredictions / numGames) * 100
    percentPerfectScores = (perfectScorePredictions / numGames) * 100
    percentPerfectGames = (perfectGamePredictions / numGames) * 100
    avgLineError /= numGames
    return percentCorrectWinners, lineWins, percentPerfectScores, percentPerfectGames, percentCloseScores, percentCloseGames, avgLineError

percentCorrect, lineWins, percentPerfectScores, percentPerfectGames, percentCloseScores, percentCloseGames, avgLineError = simulateSeason(poissonModel, homeTeams, awayTeams, printGames=False)
print("The winner prediction accuracy was: {:.2f}".format(percentCorrect))
print("Percent of time one team's score was predicted: {:.2f}".format(percentPerfectScores))
print("Percent of time one team's score was predicted within 10%: {:.2f}".format(percentCloseScores))
print("Percent of time both teams' scores were predicted: {:.2f}".format(percentPerfectGames))
print("Percent of time both teams' scores were predicted within 10%: {:.2f}".format(percentCloseGames))
print("The average line error was: {:.2f}".format(avgLineError))
print("The number of line wins was: {}".format(lineWins))
