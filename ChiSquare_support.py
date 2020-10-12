
import collections
import json  # For pretty print
import numpy as np
from scipy.stats import chi2_contingency

import Filter_support as FILS
import Loader_support as LS

# Chi-square Dictionary Keys
CHI_SQUARE = "ChiSquare"
P_VALUE = "PValue"
DOF = "DoF"
EXPECTED = "Expected"


def chiSquare(df_dataset, filter):
    # print(filteredDatasets[0].columns)
    # for df_dataset in filteredDatasets:  # For each dataset in filteredDatasets
    #     print(df_dataset.columns())

    # Get the "table form" from the dataset (i.e. the necessary values)
    list_tables = extractTables(df_dataset, filter)

    len_dict_tables = len(list_tables)
    df_table = list_tables[0]
    list_table_values = []
    list_feat_code = []

    # Match up the values for the table
    for feat_code, value in df_table.items():  # For each column in filteredDatasets, also don't remove "value", it treats it as an entry otherwise

        list_join = []
        list_feat_code.append(feat_code)
        for i in range(0, len_dict_tables):
            df_table = list_tables[i]
            list_item = df_table[feat_code]
            list_join.append(list_item)
        list_table_values.append(list_join)


    # Then apply Chi-square and store in a dictionary
    dict_chi_square = collections.OrderedDict()
    i_feat_code = 0
    for item in list_table_values:
        print("item")
        print(item)
        observed = np.array(item)
        chi_stat, p, dof, expected = chi2_contingency(observed)


        feat_code = list_feat_code[i_feat_code]
        dict_chi_details = collections.OrderedDict()  # Ordered Dictionary that will hold the Chi-square return values

        # Fill in dictionary details
        dict_chi_details[CHI_SQUARE] = chi_stat
        dict_chi_details[P_VALUE] = p
        dict_chi_details[DOF] = dof
        dict_chi_details[EXPECTED] = expected

        dict_chi_square[feat_code] = dict_chi_details  # Add details to main dictionary



        i_feat_code = i_feat_code + 1
    print(dict_chi_square)

    return dict_chi_square

'''
Goes through each filtered dataset (usually 2, e.g. [ b1 - Male | b5 - Urban])
and extracts the table by counting the occurrences of "a" and "b" per feature code.
The actual summation is done in "extractTable()".
'''
def extractTables(df_dataset, filter):
    filteredDatasets = FILS.applyFilter(df_dataset, filter)
    list_tables = []
    for filteredDataset in filteredDatasets:  # Iterate through each filtered dataset
        dict_table = extractTable(filteredDataset)  # Then extract the values needed for Chi-square
        list_tables.append(dict_table)
        printTable(dict_table)
    return list_tables


# TODO (Future) Make this scalable (the "a" and "b")
def extractTable(df_filteredDataset):
    dict_table = collections.OrderedDict()
    for feat_code in df_filteredDataset.columns:  # For each column in filteredDatasets

        # print("Feature: " + feat_code)
        a_sum = len(df_filteredDataset
                    [df_filteredDataset[feat_code].str.contains("a", na = False)])
        b_sum = len(df_filteredDataset
                    [df_filteredDataset[feat_code].str.contains("b", na = False)])  # 2nd param to avoid NaN

        dict_table[feat_code] = []
        dict_table[feat_code].append(a_sum)  # Append the 2 values
        dict_table[feat_code].append(b_sum)

        # print("A sum " + str(a_sum))
        # print("B sum " + str(b_sum))
        # print("")
    return dict_table


def printTable(oDict):
    print(json.dumps(oDict, indent = 4))
