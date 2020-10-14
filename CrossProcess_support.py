import pprint
import itertools
import numpy as np
import copy
import time

import Filter_support as FILS
import ChiSquare_support as CHIS
import Loader_support as LS


'''
The main function to call.
Applies necessary functions to output a printable chi-square comparison table. 
'''
def crossProcess(df_dataset, np_CROSS):
    # Generate datasets as dictated by filters
    # NOTE:
    #   np_dataset_pairs[0]             - A list of cross types
    #   np_dataset_pairs[0][0]          - A list of levels within the list of cross types
    #   np_dataset_pairs[0][0][0]       - A list of dataset pairs (list) within the list of levels
    #   np_dataset_pairs[0][0][0][0]    - The contents of the list containing the dataset pairs
    np_cross_datasets = extractDatasets(df_dataset, np_CROSS)  # TODO (Future) Try to optimize


    # print(len(np_dataset_pairs))


    start_time = time.time()
    file_counter = 0

    np_cross_datasets = np_cross_datasets[0:]  # TODO Find a good way to partition this
    # Apply Chi-square on all dataset pairs in the list np_dataset_pairs
    for cross_type in np_cross_datasets:
        for cross_level in cross_type:  # The variable cross_level is the list of dataframes
            for dataset_pair in cross_level:
                dict_chi_square = CHIS.chiSquare(dataset_pair)
                df_output = CHIS.processChiSquareTable(dict_chi_square)  # TODO Printing
                LS.exportDataFrame(df_output, "chi-" + str(file_counter) + ".csv")  # TODO Printing
                file_counter = file_counter + 1

    print("--- %s seconds ---" % (time.time() - start_time))

    # CHIS.printTable(dict_chi_square)



def extractDatasets(df_dataset, np_CROSS):
    list_cross_type = []
    list_level = []

    # Filter datasets according to filters
    for np_cross_type in np_CROSS:  # np_cross_type[type]
        for np_level in np_cross_type:  # np_cross_type[type][level]
            for list_filter in np_level:  # [["b1:a", "b2:b"], ["u3:b", "b5:b]]
                df_filtered_dataset = df_dataset.copy(deep = True)  # TODO OPTIMIZE to proceed
                np_dataset_pair = FILS.applyFilter(df_filtered_dataset, list_filter)  # Dataset A & B
                # list_dataset_pairs.append(np_dataset_pair)
                list_level.append(np_dataset_pair)  # List of dataset pairs (list) in a level
            list_cross_type.append(list_level)  # List of levels (list) of dataset pairs

    list_cross_type = np.array(list_cross_type)

    return list_cross_type








