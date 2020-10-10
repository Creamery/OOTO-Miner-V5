# For Ordered Dictionary
import collections

import os
import pandas as pd
import numpy as np


# Uploader support for converting read dataset
import Loader_support as LS

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_input = str(dir_path + "\\_input\\")


# Load Variable Description
fln_varDesc = "Uniandes_VariableDescription.csv"
path_varDesc = str(dir_input + fln_varDesc)
LS.load(LS.TYPE_VARDESC, path_varDesc)


dataset_input = "Uniandes_Dataset.csv"






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
dataset1


filters = []

# Sample Filters
filter1 = collections.OrderedDict()
filter1["s1"] = "a"

filter2 = collections.OrderedDict()


# Select dataframe rows with multiple conditions
# fObj[dfObj['Product'] == 'Apples']



