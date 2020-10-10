# For Ordered Dictionary
import collections

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
    
# dataframe = pd.read_csv(pthDtsetName_input, names = ftrName)
dataframe = pd.read_csv(pthDtsetName_input)
dataframe.apply(pd.to_numeric)
dataframe.columns = ftrName
print(dataframe.head())






# Filters -------------------------------------------------------
dataframe1 = dataframe.copy(deep = True)
dataframe2 = dataframe.copy(deep = True)

# Initialize filters as ordered dictionaries
filter1 = collections.OrderedDict()
filter2 = collections.OrderedDict()
filter1['b1'] = 1
filter1['b5'] = 1
filter2['b5'] = 1

filters = []  # Might NOT need this
filters.append(filter1)
filters.append(filter2)
print(filters)

# Iterate through each filter and prepare a dataset accordingly
for key, value in filter1.items():
    print(str(key))
    print(value)
    dataframe1 = dataframe1[dataframe1[str(key)] == value]


# Output to CSV
dir_output = str(dir_path + "\\_output\\")
dataframe1.to_csv(dir_output + '\\dataframe1.csv', index = False)








'''
# Convert DataFrame object to NumPy array for faster computation
array = dataframe.values
print(array)
ftrCount = len(ftrName)
ftrEndIndex = ftrCount - 1

X = array[:,0:ftrEndIndex]
Y = array[:,ftrEndIndex]

model = LogisticRegression(solver = 'liblinear', multi_class = 'auto') # or lbfgs or liblinear
rfe = RFE(model, 3) # The second parameter is the number of top features to select
fit = rfe.fit(X, Y)

for i in range(X.shape[1]):
	print('Column: %d, Selected %s, Rank: %.3f' % (i, rfe.support_[i], rfe.ranking_[i]))

	
print("Num Features: %s" % (fit.n_features_))
print("Selected Features: %s" % (fit.support_))
print("Feature Ranking: %s" % (fit.ranking_))
'''


















