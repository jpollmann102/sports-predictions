import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
import preprocess as pre

# teamStatNames = ['Yds/G','PYds/G','RYds/G','PTS/G']
# teamPassNames = ['Percentage','PYds/A','Passer Rating']
# teamRushNames = ['RYds/A']
# teamReceiveNames = ['Average','ReYds/G']
# teamStatsNames = [teamStatNames, teamPassNames, teamRushNames, teamReceiveNames]

dfX = pre.cleanTrainingX(16)
dfY = pre.cleanTrainingY(dfX)
dfX.drop(['Winner', '@', 'Loser', 'PtsW', 'PtsL'], axis=1, inplace=True)
dfUnplayed = pre.getUnplayedGames()
dfPredict = pre.cleanPredictions(16)

X = dfX.values
Y = dfY.values

# feature extraction
test = SelectKBest(score_func=f_classif, k=4)
fit = test.fit(X,Y)

# summarize scores
np.set_printoptions(precision=3)
print(fit.scores_)
features = fit.transform(X)
print(features[0:5,:])

# best 4 features are:
# PYds/A
# Average Reception Yards
# Passer Rating
# RYds/G
