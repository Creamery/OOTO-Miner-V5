# For Ordered Dictionary
import collections

import os
import pandas as pd
import numpy as np


# Uploader support for converting read dataset
import Loader_support as LS
import Filter_support as FILS
import ChiSquare_support as CHIS
import CrossProcess_support as CPS

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


# CPS

# items = [
#     [["b1:a", "b1:b"], ["b5:a"]],
#     [["b1:a", "b5:b", "u3:a"], ["b2:b"]],
#     [["b5:a"], ["b1:a"]]
# ]
#
# for item in items:
#     print("Item")
#     print(item)
#     print("")
#     CPS.updateChecklist(item)

CPS.updateChecklist([["b1:b", "b1:a"], ["b5:a"]])
CPS.updateChecklist([["b1:b"], ["b5:a"]])
CPS.updateChecklist([["b1:b"], ["b5:a"]])
CPS.updateChecklist([["b1:a", "b1:b"], ["b5:a"]])
CPS.updateChecklist([["b5:a"], ["b1:a", "b1:b"]])
CPS.updateChecklist([["b5:a"], ["b1:b", "b1:a"]])


SSF_0 = ["b1:a", "b1:b",
         "u3:a", "u3:b"]

SSF_1 = ["b4:a", "b4:b"]

SSF_2 = ["t2:a", "t2:b"]


cross_filters = CPS.crossFilters(SSF_0, 3)
for item in cross_filters:
    CPS.printChecklist(item)




