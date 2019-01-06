import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
import preprocessNFL as pre

# teamStatNames = ['Yds','Yds/G','PYds','RYds','PTS/G']
# teamPassNames = ['PYds/A', 'Passer Rating']
# teamReceiveNames = ['ReYds', 'ReYds/G']

dfX = pre.cleanTrainingX()
dfY = pre.cleanTrainingY(dfX)
dfX.drop(['Winner', '@', 'Loser', 'PtsW', 'PtsL'], axis=1, inplace=True)
dfUnplayed = pre.getUnplayedGames()
dfPredict = pre.cleanPredictions()

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
# PTS/G
# Passer Rating
# Yds
# Yds/G
