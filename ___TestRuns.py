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



filters = []

# Sample Filters
dict_filter1 = FILS.createFilter("b1", "a")
dict_filter1 = FILS.appendFilter(dict_filter1, "b5", "b")
# FILS.printFilter(dict_filter1)
# dict_filter1 = FILS.appendFilter(dict_filter1, "b5", "a")
# FILS.printFilter(dict_filter1)

df_dataset3 = df_dataset.copy(deep = True)

# filteredDatasets = FILS.applyFilter(dataset3, dict_filter1)
dict_chi_square = CHIS.chiSquare(df_dataset3, dict_filter1)
df_chi_square_output = CHIS.processChiSquareTable(dict_chi_square)
LS.exportChiSquareTable(df_chi_square_output, "Dictionary Chi Square Values.csv", LS.GL_OUTPUT_PATH)



















