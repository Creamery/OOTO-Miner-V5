
# Recursive Feature Elimination
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

import pandas as pd
import numpy as np

import csv
import os


# set directories and paths
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_input = str(dir_path + "\\_input\\")

print(dir_input)

ftrName_input = "Uniandes_FeatureNames.csv"
dtsetName_input = "Uniandes_Dataset.csv"
vrblDesc_input = "Uniandes_VariableDescription.csv"

pathFtrName_input = str(dir_input + ftrName_input)
pthDtsetName_input = str(dir_input + dtsetName_input)
pthVrblDesc_input = str(dir_input + vrblDesc_input)

print(pathFtrName_input)



# load feature names

file = open(pathFtrName_input, 'rt')
ftrName = file.read()
ftrName = ftrName.strip().split(',')

print(ftrName)
    

# url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
# names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
# dataframe = pd.read_csv(url, names = names)
# print(dataframe.head())

# dataframe = pd.read_csv(pthDtsetName_input, names = ftrName)
dataframe = pd.read_csv(pthDtsetName_input)
dataframe.apply(pd.to_numeric)
dataframe.columns = ftrName
print(dataframe.head())


# Convert DataFrame object to NumPy array for faster computation
array = dataframe.values
ftrCount = len(ftrName)
ftrEndIndex = ftrCount - 1

X = array[:,0:ftrEndIndex]
Y = array[:,ftrEndIndex]

model = LogisticRegression(solver = 'liblinear', multi_class = 'auto') # or lbfgs or liblinear
rfe = RFE(model, 3) # The second parameter is the number of top features to select
fit = rfe.fit(X, Y)
print("Num Features: %s" % (fit.n_features_))
print("Selected Features: %s" % (fit.support_))
print("Feature Ranking: %s" % (fit.ranking_))



















