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
    np_cross_datasets, np_cross_filters = extractDatasets(df_dataset, np_CROSS)  # TODO (Future) Try to optimize


    # print(len(np_dataset_pairs))


    start_time = time.time()
    file_counter = 0



    len_cross_datasets = len(np_cross_datasets)
    len_cross_types = 1  # len(cross_type)
    len_cross_level = 1  # len(cross_level)
    list_chi_square_table = []
    list_chi_square_output = []

    # Apply Chi-square on all dataset pairs in the list np_dataset_pairs
    for i_cross_type in range(len_cross_datasets):  # TODO Find a good way to partition this
        cross_type = np_cross_datasets[i_cross_type]
        for i_cross_level in range(len_cross_types):  # The variable cross_level is the list of dataframes
            cross_level = cross_type[i_cross_level]
            for i_dataset_pair in range(len_cross_level):
                dataset_pair = cross_level[i_dataset_pair]
                dict_chi_square = CHIS.chiSquare(dataset_pair)
                df_output = CHIS.processChiSquareTable(dict_chi_square)  # TODO Printing

                dataset_pair_filter = np_cross_filters[i_cross_type][i_cross_level]
                np_dataset_pair_filter = np.array(dataset_pair_filter)

                # list_chi_square_output.append([df_output, np_dataset_pair_filter])
                LS.exportChiSquareTable(df_output, dataset_pair_filter)  # TODO Printing

                file_counter = file_counter + 1



    # np_cross_datasets = np_cross_datasets[0:]  # TODO Find a good way to partition this
    # # Apply Chi-square on all dataset pairs in the list np_dataset_pairs
    # for cross_type in np_cross_datasets:
    #     for cross_level in cross_type:  # The variable cross_level is the list of dataframes
    #         for dataset_pair in cross_level[0:]:
    #             dict_chi_square = CHIS.chiSquare(dataset_pair)
    #             df_output = CHIS.processChiSquareTable(dict_chi_square)  # TODO Printing
    #             LS.exportDataFrame(df_output, "chi-" + str(file_counter) + ".csv")  # TODO Printing
    #             file_counter = file_counter + 1

    print("--- %s seconds ---" % (time.time() - start_time))

    # CHIS.printTable(dict_chi_square)



def extractDatasets(df_dataset, np_CROSS):
    list_cross_type = []
    list_level = []

    list_cross_type_filter = []
    list_level_filter = []

    # Filter datasets according to filters
    for np_cross_type in np_CROSS:  # np_cross_type[type]
        for np_level in np_cross_type:  # np_cross_type[type][level]
            for list_filter in np_level:  # [["b1:a", "b2:b"], ["u3:b", "b5:b]]
                df_filtered_dataset = df_dataset.copy(deep = True)  # TODO OPTIMIZE to proceed
                np_dataset_pair = FILS.applyFilter(df_filtered_dataset, list_filter)  # Dataset A & B
                # list_dataset_pairs.append(np_dataset_pair)
                list_level.append(np_dataset_pair)  # List of dataset pairs (list) in a level
                list_level_filter.append(list_filter)
            list_cross_type.append(list_level)  # List of levels (list) of dataset pairs
            list_cross_type_filter.append(list_level_filter)  # List of levels filters equivalent to list_cross_type

    list_cross_type = np.array(list_cross_type)
    # list_cross_type_filter = np.array(list_cross_type_filter)

    return list_cross_type, list_cross_type_filter








