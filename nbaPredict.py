import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import preprocessNBA as pre
import scraper as sc
import sys

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import classification_report

if(len(sys.argv) < 2):
    print("Please include if you should scrape (Y/N)")
    sys.exit()

scrape = sys.argv[1]

if scrape == 'Y' or scrape == 'y':
    sc.scrapeAllNBA()

# def meanAbsolutePercentageError(yTrue, yPredict):
#     yTrue, yPredict = np.array(yTrue), np.array(yPredict)
#     return np.mean(np.abs((yTrue - yPredict) / yTrue)) * 100

dfX = pre.cleanTrainingX()
dfY = pre.cleanTrainingY()

# features = ['PYds/A', 'Average', 'RYds/G', 'PTS/G']
# dfX = dfX[features]

xTrain, xTest, yTrain, yTest = train_test_split(dfX.values, dfY.values, test_size=0.1, random_state=1)

logreg = LogisticRegression(solver='lbfgs')
logreg.fit(xTrain, np.ravel(yTrain, order='C'))
score = logreg.score(xTest, yTest)
print("\nAccuracy for predicting the winner with logistic regression was: {:.2f}%".format(score * 100))

dfUnplayed = pre.getUnplayedGames()
dfPredict = pre.cleanPredictions()
# dfPredict = dfPredict[features]

predictions = logreg.predict(dfPredict)
print(dfUnplayed)
print("\nLogistic regression predictions:\n")
print(predictions)

# lowest 6, highest 26
# it seems 12 and 7 are the best hidden sizes
clf = MLPClassifier(hidden_layer_sizes=(5), max_iter=4000)
clf.fit(xTrain, np.ravel(yTrain, order='C'))
predictions = clf.predict(xTest)
print("\nNeural network report:")
print("High f1 scores are good\n")
print(classification_report(yTest,predictions))
predictions = clf.predict(dfPredict)
print(dfUnplayed)
print("\nNeural network predictions:\n")
print(predictions)
