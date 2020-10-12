
import collections
import json  # For pretty print
import numpy as np
from scipy.stats import chi2_contingency

import Filter_support as FILS


def chiSquare(df_dataset, filter):
    # print(filteredDatasets[0].columns)
    # for df_dataset in filteredDatasets:  # For each dataset in filteredDatasets
    #     print(df_dataset.columns())

    # Get the "table form" from the dataset (i.e. the necessary values)
    list_tables = extractTables(df_dataset, filter)

    len_dict_tables = len(list_tables)
    df_table = list_tables[0]
    list_table_values = []

    # Match up the values for the table
    for feat_code, value in df_table.items():  # For each column in filteredDatasets, also don't remove "value", it treats it as an entry otherwise

        list_join = []
        for i in range(0, len_dict_tables):
            df_table = list_tables[i]
            list_item = df_table[feat_code]
            list_join.append(list_item)
        list_table_values.append(list_join)

    # Then apply Chi-square
    for item in list_table_values:
        print("item")
        print(item)
        observed = np.array(item)
        output = chi2_contingency(observed)
        print("chi-square")
        print(output)
        print("")

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
