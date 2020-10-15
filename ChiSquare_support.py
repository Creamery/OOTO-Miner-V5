
import collections
import json  # For pretty print
import numpy as np
from scipy.stats import chi2_contingency
import pandas as pd

import time
import Filter_support as FILS
import Loader_support as LS

# Chi-square Dictionary Keys
CHI_SQUARE = "ChiSquare"
P_VALUE = "PValue"
DOF = "DoF"
EXPECTED = "Expected"

P_CUTOFF = 0.01

'''
    Performs Chi-square on the selected dataset based on the filter.
    Filters are at most 2 datasets.
    
    The parameter is a list of dataset pairs (filtered datasets).
'''
def chiSquare(np_dataset_pairs):
    # start_time = time.time()

    # print(filteredDatasets[0].columns)
    # for df_dataset in filteredDatasets:  # For each dataset in filteredDatasets
    #     print(df_dataset.columns())

    dict_chi_square = {}  # Just for initialization

    # Get the "table form" from the dataset (i.e. the necessary values)
    np_tables = extractTables(np_dataset_pairs)
    # print(np_tables)


    df_table = np_tables[0]

    for dataset in np_dataset_pairs:  # Iterate through each dataset pair in np_filtered_datasets
        len_dict_tables = len(np_tables)
        df_table = np_tables[0]
        list_table_values = []
        list_feat_code = []


        # Match up the values for the table
        for feat_code, value in df_table.items():  # For each column in filteredDatasets; Also don't remove "value", it treats it as an entry otherwise

            list_join = []
            list_feat_code.append(feat_code)
            for i in range(0, len_dict_tables):
                df_table = np_tables[i]
                list_item = df_table[feat_code]
                list_join.append(list_item)
            list_table_values.append(list_join)

        # LS.exportList(list_table_values, "res.csv")


        # Then apply Chi-square and store in a dictionary
        dict_chi_square = collections.OrderedDict()
        i_feat_code = 0
        for item in list_table_values:
            # print("item")
            # print(item)
            observed = np.array(item)
            # observed = pd.crosstab(item[0], item[1])
            # print(type(observed))
            # print(observed)
            if [0, 0] not in observed:
                chi_stat, p, dof, expected = chi2_contingency(observed, correction = False)


                feat_code = list_feat_code[i_feat_code]
                dict_chi_details = collections.OrderedDict()  # Ordered Dictionary that will hold the Chi-square return values

                # Fill in dictionary details
                dict_chi_details[CHI_SQUARE] = chi_stat
                dict_chi_details[P_VALUE] = p
                dict_chi_details[DOF] = dof
                dict_chi_details[EXPECTED] = expected

                dict_chi_square[feat_code] = dict_chi_details  # Add details to main dictionary


            i_feat_code = i_feat_code + 1
        # print(dict_chi_square)

    # print("--- %s seconds ---" % (time.time() - start_time))
    return dict_chi_square



'''
Processes the Chi-square dictionary results into a table-like dataframe.
Makes the necessary adjustments so that it will properly display in CSV.
The headers are: ["Feature", "DoF", "P Value", "Chi Square", "Is Significant"]

This function returns a data frame containing the formatted output as well
as a Numpy array of significant features.
'''
def processChiSquareTable(dict_chi_square):

    list_output = []  # Will contain the properly formatted data for the dataframe
    list_significant = []  # Will contain the list of features marked as significant

    # The order will be: [feat_code, dof, p_value, chi_square, is_significant]
    list_headers = ["Feature", "DoF", "P Value", "Chi Square", "Is Significant"]

    for feat_code, value in dict_chi_square.items():

        row = []
        chi_square = round(value[CHI_SQUARE], 6)
        p_value = round(value[P_VALUE], 6)
        dof = value[DOF]
        isSignificant = 0
        if p_value < P_CUTOFF:
            isSignificant = 1

        row.append(feat_code)
        row.append(dof)
        row.append(p_value)
        row.append(chi_square)
        row.append(isSignificant)

        list_output.append(row)
    if len(list_output) > 0:
        df_output = pd.DataFrame(np.array(list_output), columns = list_headers)
        pd.Index(list_headers)  # Set index as headers

        # Set the dataframe columns as correct
        df_output["DoF"] = df_output["DoF"].astype(int)
        df_output["P Value"] = df_output["P Value"].astype(float)
        df_output["Chi Square"] = df_output["Chi Square"].astype(float)
        df_output["Is Significant"] = df_output["Is Significant"].astype(int)
        df_output = df_output.sort_values(by = "Chi Square", ascending = False)

        if isSignificant > 0:  # If feat_code is marked significant, store to be returned as a list later
            list_significant.append(feat_code)
    else:
        df_output = None

    np_significant = np.array(list_significant)
    return df_output, np_significant


'''
Goes through each filtered dataset (usually 2, e.g. [ b1 - Male | b5 - Urban])
and extracts the table by counting the occurrences of "a" and "b" per feature code.
The actual summation is done in "extractTable()".
'''
def extractTables(np_dataset_pair):
    list_tables = []
    for dataset in np_dataset_pair:  # Iterate through each filtered dataset
        dict_table = extractContingencyTable(dataset)  # Then extract the values needed for Chi-square
        list_tables.append(dict_table)
        # printTable(dict_table)
    np_tables = np.array(list_tables)
    return np_tables


# TODO (Future) Make this scalable (the "a" and "b")
def extractContingencyTable(df_filtered_dataset):
    dict_table = collections.OrderedDict()
    for feat_code in df_filtered_dataset.columns:  # For each column in df_filtered_dataset

        # print("Feature: " + feat_code)
        a_sum = len(df_filtered_dataset
                    [df_filtered_dataset[feat_code].str.contains("a", na = False)])
        b_sum = len(df_filtered_dataset
                    [df_filtered_dataset[feat_code].str.contains("b", na = False)])  # 2nd param to avoid NaN

        dict_table[feat_code] = []
        dict_table[feat_code].append(a_sum)  # Append the 2 values
        dict_table[feat_code].append(b_sum)

        # print("A sum " + str(a_sum))
        # print("B sum " + str(b_sum))
        # print("")
    return dict_table


def printTable(oDict):
    print(json.dumps(oDict, indent = 4))
