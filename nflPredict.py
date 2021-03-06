import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import preprocessNFL as pre
import scraper as sc
import sys

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import classification_report

if(len(sys.argv) < 2):
    print("Please include the week and if you should scrape (Y/N)")
    sys.exit()

scrape = sys.argv[1]

if scrape == 'Y' or scrape == 'y':
    sc.scrapeAllNFL()

# def meanAbsolutePercentageError(yTrue, yPredict):
#     yTrue, yPredict = np.array(yTrue), np.array(yPredict)
#     return np.mean(np.abs((yTrue - yPredict) / yTrue)) * 100

dfX = pre.cleanTrainingX()
dfY = pre.cleanTrainingY(dfX)

dfX.drop(['Winner', '@', 'Loser', 'PtsW', 'PtsL'], axis=1, inplace=True)

# best 4 features are:
# PTS/G
# Passer Rating
# Yds
# Yds/G
# features = ['PTS/G', 'Passer Rating', 'Yds', 'Yds/G']
# dfX = dfX[features]

xTrain, xTest, yTrain, yTest = train_test_split(dfX.values, dfY.values, test_size=0.2, random_state=1)

logreg = LogisticRegression(solver='lbfgs', max_iter=4000)
logreg.fit(xTrain, np.ravel(yTrain, order='C'))
score = logreg.score(xTest, yTest)
print("\nAccuracy for predicting the winner with logistic regression was: {:.2f}%".format(score * 100))

dfUnplayed = pre.getUnplayedGames()
dfUnplayed.columns = ['Away','@','Home']
dfPredict = pre.cleanPredictions()
# dfPredict = dfPredict[features]
print(dfPredict)

predictions = logreg.predict(dfPredict)
print(dfUnplayed)
print("\nLogistic regression predictions:\n")
print(predictions)

# lowest 37, highest 186 with feature selection
# lowest 19, highest 93 without feature selection
hiddenSize = 56
clf = MLPClassifier(hidden_layer_sizes=(hiddenSize), max_iter=4000)
clf.fit(xTrain, np.ravel(yTrain, order='C'))
predictions = clf.predict(xTest)
print("\nNeural network report w/ {} hidden nodes:".format(hiddenSize))
print("High f1 scores are good\n")
print(classification_report(yTest,predictions))
predictions = clf.predict(dfPredict)
print(dfUnplayed)
print("\nNeural network predictions:\n")
print(predictions)
