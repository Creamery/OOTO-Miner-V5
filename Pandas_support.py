
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

import pandas as pd
import numpy as np

import csv
import os


"""
Load dataset into pandas data frame
"""
def loadDataset(pathDataset, featureNames):
    print("pathDataset (AM)")
    print(pathDataset)

    dataframe = pd.read_csv(pathDataset)
    dataframe.apply(pd.to_numeric)
    dataframe.columns = featureNames
    print(dataframe.head())


    # TODO Split the RFS parts of this function
    topFeatureCount = 3  # This is how many will be chosen
    # Convert DataFrame object to NumPy array for faster computation
    array = dataframe.values
    print(array)
    ftrCount = len(featureNames)
    ftrEndIndex = ftrCount - 1

    X = array[:, 0:ftrEndIndex]
    Y = array[:, ftrEndIndex]

    model = LogisticRegression(solver = 'liblinear', multi_class = 'auto')  # or lbfgs or liblinear
    rfe = RFE(model, topFeatureCount)  # The second parameter is the number of top features to select
    fit = rfe.fit(X, Y)

    for i in range(X.shape[1]):
        print('Column: %d, Selected %s, Rank: %.3f' % (i, rfe.support_[i], rfe.ranking_[i]))

    print("Num Features: %s" % (fit.n_features_))
    print("Selected Features: %s" % (fit.support_))
    print("Feature Ranking: %s" % (fit.ranking_))
