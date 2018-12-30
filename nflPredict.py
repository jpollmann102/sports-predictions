import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
# from math import exp

if(len(sys.argv) < 2):
    print("Please include the file name for predictions you'd like to run")
    sys.exit()

predictFile = sys.argv[1]

def meanAbsolutePercentageError(yTrue, yPredict):
    yTrue, yPredict = np.array(yTrue), np.array(yPredict)
    return np.mean(np.abs((yTrue - yPredict) / yTrue)) * 100


# Keys for team offense file
# PF: points scored by team
# Y/P: yards per play
# FL: fumbles lost
# NY/A: net yards gained per pass attempt
# RY/A: net yards gained per rush attempt
# Sc%: percent of drives scored

# read in data




dfTeamsO2018 = pd.read_csv('data/nfl_week17_team_offense_2018.csv', header=0, float_precision='round_trip')
dfTeamsD2018 = pd.read_csv('data/nfl_week17_team_defense_2018.csv', header=0, float_precision='round_trip')
dfTeamsO2017 = pd.read_csv('data/nfl_team_offense_2017.csv', header=0, float_precision='round_trip')
dfTeamsD2017 = pd.read_csv('data/nfl_team_defense_2017.csv', header=0, float_precision='round_trip')
dfGames2017 = pd.read_csv('data/nfl_games_training_2017.csv', header=0)
dfGames2018 = pd.read_csv('data/nfl_games_training_2018.csv', header=0)

dfWeekP = pd.read_csv('predict/{}'.format(predictFile), header=0)

# these are the features of interest from the teams file
# Okeys = ['Y/P','TO','PYds','PTD','Int','RYds','RTD','OPenYds','Sc%','OTO%']
# Dkeys = ['OY/P','FTO','OPYds','OPTD','FInt','ORYds','ORTD','DPenYds','OSc%','DTO%']
# Wkeys = ['WY/P','WTO','WPYds','WPTD','WInt','WRYds','WRTD','WPenYds','WSc%','WTO%','WOY/P','WFTO','WOPYds','WOPTD','WFInt','WORYds','WORTD','WDPenYds','WOSc%','WDTO%']
# Lkeys = ['LY/P','LTO','LPYds','LPTD','LInt','LRYds','LRTD','LPenYds','LSc%','LTO%','LOY/P','LFTO','LOPYds','LOPTD','LFInt','LORYds','LORTD','LDPenYds','LOSc%','LDTO%']
Wkeys = ['WPYds','WRYds','WSc%','WTO%','WFTO','WOPYds','WORYds','WOSc%','WDTO%']
Lkeys = ['LPYds','LRYds','LSc%','LTO%','LFTO','LOPYds','LORYds','LOSc%','LDTO%']
Okeys = ['PYds', 'RYds', 'Sc%', 'OTO%']
Dkeys = ['FTO', 'OPYds', 'ORYds', 'OSc%', 'DTO%']
WOkeys = ['WPYds', 'WRYds', 'WSc%', 'WTO%']
WDkeys = ['WFTO', 'WOPYds', 'WORYds', 'WOSc%', 'WDTO%']
LOkeys = ['LPYds', 'LRYds', 'LSc%', 'LTO%']
LDkeys = ['LFTO', 'LOPYds', 'LORYds', 'LOSc%', 'LDTO%']

reversedKeys = LOkeys + LDkeys + WOkeys + WDkeys

# append each game from the season with the teams' stats
dfGames2018 = pd.concat([dfGames2018, pd.DataFrame(0, index=np.arange(len(dfGames2018)), columns=Wkeys)], axis=1)
dfGames2018 = pd.concat([dfGames2018, pd.DataFrame(0, index=np.arange(len(dfGames2018)), columns=Lkeys)], axis=1)
dfGames2017 = pd.concat([dfGames2017, pd.DataFrame(0, index=np.arange(len(dfGames2017)), columns=Wkeys)], axis=1)
dfGames2017 = pd.concat([dfGames2017, pd.DataFrame(0, index=np.arange(len(dfGames2017)), columns=Lkeys)], axis=1)
dfWeekP = pd.concat([dfWeekP, pd.DataFrame(0, index=np.arange(len(dfWeekP)), columns=Wkeys)], axis=1)
dfWeekP = pd.concat([dfWeekP, pd.DataFrame(0, index=np.arange(len(dfWeekP)), columns=Lkeys)], axis=1)

# get lengths
numTeams = len(dfTeamsO2018.index)
numGames = len(dfGames2017.index)
numPGames = len(dfWeekP.index)

# get keys
dfTempO2018 = dfTeamsO2018[Okeys]
dfTempD2018 = dfTeamsD2018[Dkeys]
dfTempO2017 = dfTeamsO2017[Okeys]
dfTempD2017 = dfTeamsD2017[Dkeys]

# fill in prediction dataframe
for i in range(0,numPGames):
    pWinner = dfWeekP.at[i,'Winner']
    pLoser = dfWeekP.at[i,'Loser']

    pwinnerIdx = dfTeamsO2018.index[dfTeamsO2018['Tm'] == pWinner].tolist()
    ploserIdx = dfTeamsO2018.index[dfTeamsO2018['Tm'] == pLoser].tolist()

    pwinnerOStats = dfTempO2018.iloc[pwinnerIdx[0],:]
    ploserOStats = dfTempO2018.iloc[ploserIdx[0],:]
    pwinnerDStats = dfTempD2018.iloc[pwinnerIdx[0],:]
    ploserDStats = dfTempD2018.iloc[ploserIdx[0],:]

    for j in range(0,len(pwinnerOStats)):
        dfWeekP.at[i,WOkeys[j]] = pwinnerOStats[j]
        dfWeekP.at[i,LOkeys[j]] = ploserOStats[j]

    for j in range(0,len(pwinnerDStats)):
        dfWeekP.at[i,WDkeys[j]] = pwinnerDStats[j]
        dfWeekP.at[i,LDkeys[j]] = ploserDStats[j]

# indices to be filled starts at 8
# fill in values for the team stats
for i in range(0,numGames):
    # for every game
    # get the winner and loser

    # do the 2017 games
    winner17 = dfGames2017.at[i,'Winner']
    loser17 = dfGames2017.at[i,'Loser']

    # get index of winner and loser
    winner17Idx = dfTeamsO2017.index[dfTeamsO2017['Tm'] == winner17].tolist()
    loser17Idx = dfTeamsO2017.index[dfTeamsO2017['Tm'] == loser17].tolist()

    # get the winner and loser stats from team stats
    winnerOStats17 = dfTempO2017.iloc[winner17Idx[0],:]
    loserOStats17 = dfTempO2017.iloc[loser17Idx[0],:]
    winnerDStats17 = dfTempD2017.iloc[winner17Idx[0],:]
    loserDStats17 = dfTempD2017.iloc[loser17Idx[0],:]

    winnerStats17 = winnerOStats17.append(winnerDStats17)
    loserStats17 = loserOStats17.append(loserDStats17)

    if i < len(dfGames2018.index):
        # if we can do the 2018 games, do them

        winner = dfGames2018.at[i,'Winner']
        loser = dfGames2018.at[i,'Loser']

        # get index of winner and loser
        winnerIdx = dfTeamsO2018.index[dfTeamsO2018['Tm'] == winner].tolist()
        loserIdx = dfTeamsO2018.index[dfTeamsO2018['Tm'] == loser].tolist()

        # get the winner and loser stats from team stats
        winnerOStats = dfTempO2018.iloc[winnerIdx[0],:]
        loserOStats = dfTempO2018.iloc[loserIdx[0],:]
        winnerDStats = dfTempD2018.iloc[winnerIdx[0],:]
        loserDStats = dfTempD2018.iloc[loserIdx[0],:]

        # for both teams
        # fill in values
        for j in range(0,len(winnerOStats)):
            dfGames2018.at[i,WOkeys[j]] = winnerOStats[j]
            dfGames2018.at[i,LOkeys[j]] = loserOStats[j]
            dfGames2017.at[i,WOkeys[j]] = winnerOStats17[j]
            dfGames2017.at[i,LOkeys[j]] = loserOStats17[j]


        for j in range(0,len(winnerDStats)):
            dfGames2018.at[i,WDkeys[j]] = winnerDStats[j]
            dfGames2018.at[i,LDkeys[j]] = loserDStats[j]
            dfGames2017.at[i,WDkeys[j]] = winnerDStats17[j]
            dfGames2017.at[i,LDkeys[j]] = loserDStats17[j]
    else:
        # for both teams
        # fill in values
        for j in range(0,len(winnerOStats)):
            dfGames2017.at[i,WOkeys[j]] = winnerOStats17[j]
            dfGames2017.at[i,LOkeys[j]] = loserOStats17[j]

        for j in range(0,len(winnerDStats)):
            dfGames2017.at[i,WDkeys[j]] = winnerDStats17[j]
            dfGames2017.at[i,LDkeys[j]] = loserDStats17[j]

################################################################################
#              Code below is used for predicting the winning team              #
################################################################################

# put together the 2017 and 2018 games
dfGames = dfGames2018.append(dfGames2017)

firstTeams = dfWeekP.iloc[:,0]
secondTeams = dfWeekP.iloc[:,1]
# get list of winning scores
yW = dfGames.iloc[:,2]
# get list of losing scores
yL = dfGames.iloc[:,3]
# get list of features to test
# Xw = dfGames[WOkeys].join(dfGames[LDkeys])
# Xl = dfGames[LOkeys].join(dfGames[WDkeys])
Xw = pd.concat([dfGames[WOkeys], dfGames[LDkeys]], axis=1)
Xl = pd.concat([dfGames[LOkeys], dfGames[WDkeys]], axis=1)

predictXW = pd.concat([dfWeekP[WOkeys], dfWeekP[LDkeys]], axis=1)
predictXL = pd.concat([dfWeekP[LOkeys], dfWeekP[WDkeys]], axis=1)

# not useful for linear regression:
# rushing yards
# passing yards
# yard per play

# plt.figure(1)
# plt.plot(dfGames['PtsW'], dfGames['WOSc%'], 'ro')
# plt.ylabel('Winning Points')
# plt.xlabel('Opposition Defense Rating')
# plt.figure(2)
# plt.plot(dfGames['PtsL'], dfGames['LOSc%'], 'o')
# plt.ylabel('Losing Points')
# plt.xlabel('Opposition Defense Rating')
# plt.show()

xwTrain, xwTest, ywTrain, ywTest = train_test_split(Xw, yW, random_state=0)
xlTrain, xlTest, ylTrain, ylTest = train_test_split(Xl, yL, random_state=0)

# scaler = StandardScaler()
#
# scaler.fit(xwTrain)
# xwTrain = scaler.transform(xwTrain)
# xwTest = scaler.transform(xwTest)
#
# scaler.fit(xlTrain)
# xlTrain = scaler.transform(xlTrain)
# xlTest = scaler.transform(xlTest)

clfW = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(30,30,30), random_state=1, max_iter=500)
clfL = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(30,30,30), random_state=1, max_iter=500)
clfW.fit(xwTrain, ywTrain)
clfL.fit(xlTrain, ylTrain)

predictionsW = clfW.predict(predictXW)
predictionsL = clfL.predict(predictXL)

# print(classification_report(ywTest, predictionsW))
# print(classification_report(ylTest, predictionsL))

# print("Training size: {}".format(len(xwTrain)))
# logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')
# logregW = LogisticRegression()
# logregL = LogisticRegression()
#
# logregW.fit(xwTrain, ywTrain)
# logregL.fit(xlTrain, ylTrain)
#
# predictionsW = logregW.predict(predictXW)
# predictionsL = logregL.predict(predictXL)

# print("\nThe training set is:\n")
# print(dfWeekP)

# predictions = logreg.predict(predictX)
# print("\nThe real winners were:\n")
# print(yTest)
# print("\nThe predicted first team scores are:\n")
# print("\n{}".format(predictionsW))
# # score = logregW.score(xwTest, ywTest)
# # print("\nAccuracy for predicting the winning score was: {:.2f}%".format(score * 100))
#
# print("\nThe predicted second team scores are:\n")
# print("\n{}".format(predictionsL))
# score = logregL.score(xlTest, ylTest)
# print("\nAccuracy for predicting the secon score was: {:.2f}%".format(score * 100))

for i in range(len(predictionsW)):
    if predictionsW[i] > predictionsL[i]:
        print("Winner of the {:2} game is {:22} by a score of {} to {:3}, line of {}".format(i + 1, firstTeams[i], predictionsW[i], predictionsL[i], predictionsW[i] - predictionsL[i]))
    else:
        print("Winner of the {:2} game is {:22} by a score of {} to {:3}, line of {}".format(i + 1, secondTeams[i], predictionsL[i], predictionsW[i], predictionsL[i] - predictionsW[i]))
