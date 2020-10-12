# For Ordered Dictionary
import collections

import os
import pandas as pd
import numpy as np


# Uploader support for converting read dataset
import Loader_support as LS
import Filter_support as FILS
import ChiSquare_support as CHIS

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_input = str(dir_path + "\\_input\\")
dir_output = str(dir_path + "\\_output\\")



# Load Variable Description
fln_varDesc = "Uniandes_VariableDescription (New).csv"
path_varDesc = str(dir_input + fln_varDesc)
dict_varDesc = LS.loadVarDesc(path_varDesc)


# Load Dataset
fln_dataset = "Uniandes_Dataset (New).csv"
path_dataset = str(dir_input + fln_dataset)
df_dataset = LS.loadDataset(path_dataset, dict_varDesc)
LS.exportDataset(df_dataset, "Output.csv", dir_output)





b1_input1 = "b1(1 2) b5(1)\\b1(1).csv"
b5_input1 = "b1(1 2) b5(1)\\b5(1).csv"

b1_input1_path = str(dir_input + b1_input1)
b5_input1_path = str(dir_input + b5_input1)


# print(b1_input1_path)
# print(b5_input1_path)


# load data
df_b1_original = pd.read_csv(b1_input1_path)
df_b5_original = pd.read_csv(b5_input1_path)

# Create a copy just in case; Do all alterations in copy
dataset1 = df_b1_original.copy(deep = True)
dataset2 = df_b5_original.copy(deep = True)


# Filter dataset 1
# Condition: b1 = 1
# dataset1


filters = []

# Sample Filters
filter1 = collections.OrderedDict()
filter1["s1"] = "a"

filter2 = collections.OrderedDict()


# Select dataframe rows with multiple conditions
# fObj[dfObj['Product'] == 'Apples']


# This is Chi Square -- K?!
from scipy.stats import chi2_contingency
from scipy.stats import chisquare
# val = chisquare([[266, 132], [309, 93]])
# print(val)

obs = np.array([[266, 132], [309, 93]])
out = chi2_contingency(obs)
print(out)

obs = np.array([[241, 154], [238, 164]])
out = chi2_contingency(obs)
print(out)

obs = np.array([[398, 0], [170, 232]])
out = chi2_contingency(obs)
print(out)


dict_filter1 = FILS.createFilter("b1", "a")
dict_filter1 = FILS.appendFilter(dict_filter1, "b5", "b")
# FILS.printFilter(dict_filter1)

# dict_filter1 = FILS.appendFilter(dict_filter1, "b5", "a")
# FILS.printFilter(dict_filter1)

df_dataset3 = df_dataset.copy(deep = True)

# filteredDatasets = FILS.applyFilter(dataset3, dict_filter1)
CHIS.chiSquare(df_dataset3, dict_filter1)
