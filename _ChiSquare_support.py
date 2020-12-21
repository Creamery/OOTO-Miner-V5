
import collections
import json  # For pretty print
import numpy as np
from scipy.stats import chi2_contingency
import pandas as pd

import time
import __Filter_support as FILS
import __Loader_support as LS
import _UIConstants_support as UICS

# Chi-square Dictionary Keys
CHI_SQUARE = "ChiSquare"
P_VALUE = "PValue"
DOF = "DoF"
OBSERVED = "Observed"
EXPECTED = "Expected"

DATASET_EXPORT_COUNTER = 1

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
    np_tables = extractTables(np_dataset_pairs)  # np_tables is an np array of dataframes
    # print(np_tables)

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
                dict_chi_details[OBSERVED] = observed
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


    This function returns an updated dict_result_table (as passed in the paremeter)
    that records all dataset pairings (e.g. b1[a] VS b2[b]) as keys and their equivalent
    table results [Feature, DoF, P Value, Chi Square, Is Significant] as values.
    
'''
def processChiSquareTable(dict_chi_square):

    list_output = []  # Will contain the properly formatted data for the dataframe
    list_significant = []  # Will contain the list of features marked as significant
    list_significant_output = []  # Will contain the properly formatted data for the dataframe

    # The order will be: [feat_code, dof, p_value, chi_square, is_significant]
    list_headers = ["Feature", "DoF", "P Value", "Chi Square", "Observed", "Expected", "Is Significant"]

    for feat_code, value in dict_chi_square.items():

        row = []
        dof = value[DOF]
        p_value = round(value[P_VALUE], 6)
        chi_square = round(value[CHI_SQUARE], 6)

        observed = value[OBSERVED]
        observed = str(observed[0]).strip() + " ; " + str(observed[1]).strip()
        expected = value[EXPECTED]
        expected = str(expected[0]).strip() + " ; " + str(expected[1]).strip()


        isSignificant = 0
        if p_value < UICS.P_CUTOFF:
            isSignificant = 1

        row.append(feat_code)
        row.append(dof)
        row.append(p_value)
        row.append(chi_square)
        row.append(observed)
        row.append(expected)
        row.append(isSignificant)

        list_output.append(row)

        if isSignificant == 1:  # If feat_code is marked significant, store to be returned as a list later
            sig_row = []
            sig_out_row = []

            sig_row.append(feat_code)
            sig_row.append(chi_square)
            list_significant.append(sig_row)

            sig_out_row.append(feat_code)
            sig_out_row.append(dof)
            sig_out_row.append(p_value)
            sig_out_row.append(chi_square)
            sig_out_row.append(observed)
            sig_out_row.append(expected)
            sig_out_row.append(isSignificant)
            list_significant_output.append(sig_out_row)


    if len(list_output) > 0:
        df_output = pd.DataFrame(np.array(list_output), columns = list_headers)
        pd.Index(list_headers)  # Set index as headers

        # Set the dataframe columns as correct
        df_output["DoF"] = df_output["DoF"].astype(int)
        df_output["P Value"] = df_output["P Value"].astype(float)
        df_output["Chi Square"] = df_output["Chi Square"].astype(float)
        df_output["Is Significant"] = df_output["Is Significant"].astype(int)
        df_output = df_output.sort_values(by = "Chi Square", ascending = False)

    else:
        df_output = None

    if len(list_significant_output) > 0:
        df_significant_output = pd.DataFrame(np.array(list_significant_output), columns = list_headers)
        pd.Index(list_headers)  # Set index as headers

        # Set the dataframe columns as correct
        df_significant_output["DoF"] = df_significant_output["DoF"].astype(int)
        df_significant_output["P Value"] = df_significant_output["P Value"].astype(float)
        df_significant_output["Chi Square"] = df_significant_output["Chi Square"].astype(float)
        df_significant_output["Is Significant"] = df_significant_output["Is Significant"].astype(int)
        df_significant_output = df_significant_output.sort_values(by = "Chi Square", ascending = False)

    else:
        df_significant_output = None

    # np_significant = np.array(list_significant)
    return df_output, list_significant, df_significant_output


'''
Goes through each filtered dataset (usually 2, e.g. [ b1 - Male | b5 - Urban])
and extracts the table by counting the occurrences of "a" and "b" per feature code.
The actual summation is done in "extractTable()".
'''
def extractTables(np_dataset_pair):
    list_tables = []
    for dataset in np_dataset_pair:  # Iterate through each filtered dataset
        df_table = extractContingencyTable(dataset)  # Then extract the values needed for Chi-square
        list_tables.append(df_table)

        # LS.exportDictionary(dict_table, "Dataset Result " + str(DATASET_EXPORT_COUNTER) + ".csv", LS.GL_AM_OUTPUT_PATH + "Datasets\\")
        # DATASET_EXPORT_COUNTER = DATASET_EXPORT_COUNTER + 1
        # printTable(dict_table)

    # print(list_tables)
    # np_tables = np.array(list_tables)
    np_tables = list_tables
    return np_tables


# TODO (Future) Make this scalable (the "a" and "b")
def extractContingencyTable(df_filtered_dataset):

    # dict_table = collections.OrderedDict()
    # column_names = []
    df_table = pd.DataFrame()

    for feat_code in df_filtered_dataset.columns:  # For each column in df_filtered_dataset
        counts = df_filtered_dataset[feat_code].value_counts()
        key_counts = counts.keys().tolist()

        a_count = getOptionsCount("a", counts, key_counts)
        b_count = getOptionsCount("b", counts, key_counts)

        df_table[feat_code] = [a_count, b_count]  # The feat_code in df_table is a column of a_counts, b_counts

    return df_table


'''
    Get the counts of the specified str_option based on the counts list.
    This function checks whether the option is present, if not, it returns
    a count of 0.
'''
def getOptionsCount(str_option, counts, key_counts):

    try:  # Try to search for the index of str_option in key_counts
        index = key_counts.index(str_option)
        option_count = counts[index]  # If the index exists, get its corresponding count in counts

    except ValueError:  # If str_option does not exist, the count for it is 0
        option_count = 0

    return option_count


def printTable(oDict):
    print(json.dumps(oDict, indent = 4))


