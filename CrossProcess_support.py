import pprint
import itertools
import numpy as np
import copy
import time
import collections

import Loader_support as LS
import Filter_support as FILS
import ChiSquare_support as CHIS
import UIConstants_support as UICS

'''
The main function to call.
Applies necessary functions to output a printable chi-square comparison table. 
'''
def crossProcess(df_dataset, np_CROSS, controller):
    key = UICS.KEY_PRE_CROSS_MODULE  # Key for progress bar
    i_key = 1  # Iterator for progress bar

    controller.updateModuleProgress(key, i_key, "Starting CROSS PROCESS MODULE")  # 1
    i_key = i_key + 1
    time.sleep(0.01)

    # Generate datasets as dictated by filters
    # NOTE:
    #   np_dataset_pairs[type]                      - A list of cross types
    #   np_dataset_pairs[type][level]               - A list of levels within the list of cross types
    #   np_dataset_pairs[type][level][0]            - A list of dataset pairs (list) within the list of levels
    #   np_dataset_pairs[0][0][0][0]                - The contents of the list containing the dataset pairs
    controller.updateModuleProgress(key, i_key, "Extracting Datasets by Filter")  # 2
    i_key = i_key + 1
    time.sleep(0.01)

    np_cross_datasets, np_cross_filters = extractDatasets(df_dataset, np_CROSS)  # TODO (Future) Try to optimize

    controller.updateModuleProgress(key, i_key, "Successfully Extracted Datasets")  # 3
    i_key = i_key + 1
    time.sleep(0.01)

    len_cross_datasets = int(UICS.MAX_CROSS)  # len(np_cross_datasets)
    len_cross_types = int(UICS.MAX_LEVEL)  # UICS.MAX_CROSS  # len(cross_type)
    # len_cross_level = UICS.MAX_LEVEL  # len(cross_level)

    list_cross_ssfs = []
    dict_result_table_sig = collections.OrderedDict()

    print("Processing - Please Wait... (Average Runtime for ALL Features - 8 minutes")

    controller.updateModuleProgress(key, i_key, "Starting Cross Process : This might take some time...")  # 4
    time.sleep(0.01)


    # Prepare to update progress bar with the second half of the CROSS PROCESS MODULE
    key = UICS.KEY_CROSS_MODULE  # Key for progress bar
    i_key = 1  # Iterator for progress bar

    # Compute the total process of this section according to the computed cross type and level count
    UICS.CROSS_MAX_PROCESS_COUNT = computeMaxProcessCount(np_cross_datasets, len_cross_datasets, len_cross_types)
    # Multiply by 3 since you will record each pass once, then update twice more; One for Chi-square
    # and the other for exporting the table
    UICS.CROSS_MAX_PROCESS_COUNT = UICS.CROSS_MAX_PROCESS_COUNT * 3
    UICS.CROSS_MAX_PROCESS_COUNT = UICS.CROSS_MAX_PROCESS_COUNT + i_key
    print("CPM Count " + str(UICS.CROSS_MAX_PROCESS_COUNT / 3))

    start_time = time.time()
    # Apply Chi-square on all dataset pairs in the list np_dataset_pairs
    for i_cross_type in range(len_cross_datasets):  # TODO (Future) Find the best way to partition this
        cross_type = np_cross_datasets[i_cross_type]  # Iterate through each CROSS TYPE

        for i_cross_level in range(len_cross_types):
            # print("CROSS[" + str(i_cross_type) + "][" + str(i_cross_level + 1) + "]: " + str(i_cross_level + 1) + " out of "+ str(len_cross_types))

            # The variable cross_level is the list of dataframes
            cross_level = cross_type[i_cross_level]  # Iterate through each LEVEL
            len_cross_level = len(cross_level)

            list_level_ssfs = []
            list_all_ssfs = []
            list_ssfs = []
            # np_level_ssfs = np.array(list_level_ssfs)
            for i_dataset_pairs in range(len_cross_level):
                dataset_pairs = cross_level[i_dataset_pairs]
                len_dataset_pairs = len(dataset_pairs)

                # Title for the current cross process
                str_title = "Processing CROSS[" + str(i_cross_type) + "][" + str(i_cross_level) + "]"
                # Update the progress bar about the current CROSS[type][level]
                controller.updateModuleProgress(key, i_key, str_title)
                i_key = i_key + 1
                time.sleep(0.01)

                str_dataset_length = str(len_dataset_pairs)
                for i_dataset_pair in range(len_dataset_pairs):
                    #  Description for the current cross process
                    str_description = "     " + str(i_dataset_pair) + " of " + str_dataset_length
                    controller.updateModuleProgress(key, i_key, str_description)
                    i_key = i_key + 1

                    dataset_pair = dataset_pairs[i_dataset_pair]

                    dict_chi_square = CHIS.chiSquare(dataset_pair)

                    controller.updateModuleProgress(key, i_key, "Applying Chi-square")
                    i_key = i_key + 1
                    # time.sleep(0.01)
                    df_processed_output, list_ssf, list_sig_output = CHIS.processChiSquareTable(dict_chi_square)

                    if df_processed_output is not None:
                        dataset_pair_filter = np_cross_filters[i_cross_type][i_cross_level][i_dataset_pairs]

                        if len(list_ssfs) == 0:
                            list_ssfs = list_ssf
                        else:
                            list_ssfs = mergeUnique(list_ssfs, list_ssf)


                        np_dataset_pair_filter = np.array(dataset_pair_filter)
                        # list_chi_square_output.append([df_output, np_dataset_pair_filter])
                        list_index = [i_cross_type, i_cross_level]

                        controller.updateModuleProgress(key, i_key, "Exporting Chi-square Table")
                        i_key = i_key + 1
                        # time.sleep(0.01)
                        # TODO Printing
                        df_output, str_pair_name = LS.exportChiSquareTable(df_processed_output,
                                                                           np_dataset_pair_filter,
                                                                           list_index)

                        dict_result_table_sig = addToDictionaryResult(dict_result_table_sig, str_pair_name, list_sig_output)
                    else:
                        i_key = i_key + 2  # Add 2 to make up for the missed processes
                        # print("DF OUTPUT IS NULL: Skipping Item")


                list_all_ssfs = mergeUnique(list_all_ssfs, list_ssfs)
                ssfs_filename = "SSFs - CROSS[" + str(i_cross_type) + "][" + str(i_cross_level) + "].csv"
                LS.exportSSFs(list_ssfs, ssfs_filename)




            list_level_ssfs.append(list_all_ssfs)  # Store SSF list

        list_cross_ssfs.append(list_level_ssfs)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Processing Complete")
    LS.exportUIResultDictionary(dict_result_table_sig, "UI Result")
    return dict_result_table_sig

'''
    Pre-compute the number of processes under the CROSS loop.
'''
def computeMaxProcessCount(np_cross_datasets, len_cross_datasets, len_cross_types):
    process_count = 0

    for i_cross_type in range(len_cross_datasets):
        cross_type = np_cross_datasets[i_cross_type]  # Iterate through each CROSS TYPE

        for i_cross_level in range(len_cross_types):
            cross_level = cross_type[i_cross_level]  # Iterate through each LEVEL
            len_cross_level = len(cross_level)

            for i_dataset_pairs in range(len_cross_level):
                process_count = process_count + 1  # Count the number of dataset pairs

    return process_count

def mergeUnique(list1, list2):
    # in_first = set(list1)
    # in_second = set(list2)
    # in_second_but_not_in_first = in_second - in_first
    # merged_list = list1 + list(in_second_but_not_in_first)
    merged_list = list(set(list1) | set(list2))
    # merged_list = np.unique(list1 + list2)
    return merged_list


def addToDictionaryResult(dict_result, key, value):

    if key not in dict_result.keys():
        dict_result[key] = value

    return dict_result

def extractDatasets(df_dataset, np_CROSS):

    list_cross_type = []
    list_cross_type_filter = []

    # Filter datasets according to filters
    for np_cross_type in np_CROSS:  # np_cross_type[type] | Runs: 3; Per run length: 3

        list_level = []
        list_level_filter = []
        # np_cross_type[type][level] | Runs: 3; Per run length:
        # 1-[15, 66, 28] 2-[58, 276, 496] 3-[6, 6, 0]
        # Run length is the number of dataset pairs per level
        for np_level in np_cross_type:  # Runs: 3 per Cross Type

            list_pairs = []
            list_pairs_filter = []
            # [["b1:a", "b2:b"], ["u3:b", "b5:b]]
            # Runs: 1-[15, 66, 28] 2-[58, 276, 496] 3-[6, 6, 0];
            # Per run length: 2 (which is [filterA, filterB]
            for list_filter in np_level:
                df_filtered_dataset = df_dataset.copy(deep = True)  # TODO OPTIMIZE to proceed
                np_dataset_pair = FILS.applyFilter(df_filtered_dataset, list_filter)  # [datasetA, datasetB] | Length: 2

                # list_dataset_pairs.append(np_dataset_pair)
                list_pairs.append(np_dataset_pair)  # List of dataset pairs (list) in a level [ [datasetA, datasetB], [<...>] ]
                list_pairs_filter.append(list_filter)
            list_level.append(list_pairs)
            list_level_filter.append(list_pairs_filter)
        list_cross_type.append(list_level)  # List of levels (list) of dataset pairs
        list_cross_type_filter.append(list_level_filter)  # List of levels filters equivalent to list_cross_type


    np_list_cross_type = np.array(list_cross_type)
    # list_cross_type_filter = np.array(list_cross_type_filter)


    return np_list_cross_type, list_cross_type_filter








