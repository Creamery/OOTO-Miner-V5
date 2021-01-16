__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    The CROSS PROCESSING MODULE. This script handles the application
    of generated filters from the FILTERING MODULE to the given dataset.

    This is also the script where the CHI-SQUARE MODULE is called.
    It applies chi-square to the generated filtered datasets and
    calls the LOADER MODULE to export the results into a table.
    [Candy]
'''

import numpy as np
import time
import collections

import __Loader_support as LS
import __Filter_support as FILS
import _ChiSquare_support as CHIS
import _UIConstants_support as UICS
import _AMVariables_support as AMVS

# Multiprocessing Scripts
from multiprocessing import Pool
from functools import partial
import __CrossProcess_MP_process as CPMPP



'''
    Optimized Cross Process
'''
def crossProcessOptimized(df_dataset, np_CROSS, depth, controller):
    key = UICS.KEY_PRE_CROSS_MODULE  # Key for progress bar

    controller.updateModuleProgress(key, UICS.MODULE_INDICATOR + "Starting CROSS PROCESS MODULE")  # 1
    # time.sleep(0.01)  # Sleep

    # Generate datasets as dictated by filters
    # NOTE:
    #   np_dataset_pairs[type]                      - A list of cross types
    #   np_dataset_pairs[type][level]               - A list of levels within the list of cross types
    #   np_dataset_pairs[type][level][0]            - A list of dataset pairs (list) within the list of levels
    #   np_dataset_pairs[0][0][0][0]                - The contents of the list containing the dataset pairs
    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Extracting Datasets by Filter")  # 2
    # time.sleep(0.01)  # Sleep
    np_cross_datasets, np_cross_filters = extractDatasets(df_dataset, np_CROSS)  # TODO (Future) Try to optimize

    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Successfully Extracted Datasets")  # 3
    # time.sleep(0.01)  # Sleep

    len_cross_datasets = int(UICS.MAX_CROSS)  # len(np_cross_datasets)
    len_cross_types = int(UICS.MAX_LEVEL)  # UICS.MAX_CROSS  # len(cross_type)
    # len_cross_level = UICS.MAX_LEVEL  # len(cross_level)

    list_cross_ssfs = []
    dict_result_table_sig = collections.OrderedDict()

    print("Processing - Please Wait... (Average Runtime for ALL Features - 8 minutes")

    controller.updateModuleProgress(key,
                                    UICS.SUB_MODULE_INDICATOR + "Starting Cross Process : This might take some time...")  # 4
    # time.sleep(0.01)  # Sleep

    # Prepare to update progress bar with the second half of the CROSS PROCESS MODULE
    key = UICS.KEY_CROSS_MODULE  # Key for progress bar

    # Compute the total process of this section according to the computed cross type and level count
    # Compute for one pass at Level (See line commented with "LVL Pass 1")
    UICS.CROSS_MAX_PROCESS_COUNT = computeMaxCrossLevelCount(np_cross_datasets, len_cross_datasets, len_cross_types)
    # Multiply by 2 since you will record each pass (1) then update for exporting the table (1)
    data_filter_process_count = computeMaxProcessCount(np_cross_datasets, len_cross_datasets, len_cross_types)
    data_filter_process_count = data_filter_process_count  # * 2
    UICS.CROSS_MAX_PROCESS_COUNT = UICS.CROSS_MAX_PROCESS_COUNT + data_filter_process_count
    list_level_ssfs = None

    start_time = time.time()

    pool_size = len_cross_datasets*len_cross_types
    iterable = [1, 2, 3, 4, 5]
    count_process = 5
    pool = Pool(processes = count_process)

    a = "hi"
    b = "there"

    func = partial(CPMPP.process, a, b)
    pool.map_async(func, iterable)

    # Apply Chi-square on all dataset pairs in the list np_dataset_pairs
    for i_cross_type in range(len_cross_datasets):  # TODO (Future) Find the best way to partition this
        cross_type = np_cross_datasets[i_cross_type]  # Iterate through each CROSS TYPE

        for i_cross_level in range(len_cross_types):
            print("")
            # TODO Call a process for the given cross type and level


    # TODO While all processes are not yet done

    pool.close()
    pool.join()


    run_time = (time.time() - start_time)
    AMVS.getSingleton().updateTime(run_time)  # Update Singleton's run time
    print("--- %s seconds ---" % run_time)
    str_runtime = "\nCross Process Time:\n" + str(run_time) + " seconds"
    controller.getAMController().addToConsoleAll(str_runtime + "\n")

    print("Processing Complete")
    LS.exportOutputModuleResults(dict_result_table_sig, len_cross_datasets,
                                 len_cross_types, controller)

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


def computeMaxCrossLevelCount(np_cross_datasets, len_cross_datasets, len_cross_types):
    process_count = 0

    for i_cross_type in range(len_cross_datasets):
        cross_type = np_cross_datasets[i_cross_type]  # Iterate through each CROSS TYPE

        for i_cross_level in range(len_cross_types):
            cross_level = cross_type[i_cross_level]  # Iterate through each LEVEL

            process_count = process_count + 1  # Count the number of pass per levels

    return process_count


def mergeUnique(list1, list2):
    # in_first = set(list1)
    # in_second = set(list2)
    # in_second_but_not_in_first = in_second - in_first
    # merged_list = list1 + list(in_second_but_not_in_first)
    merged_list = list(set(list1) | set(list2))
    # merged_list = np.unique(list1 + list2)
    return merged_list


'''
    Merges unique first entries (index 0) of the list.
    It then keeps the higher value of similar entries
    for the second element  (index 1).
'''


def mergeAndFilter(list1, list2):
    dict1 = collections.defaultdict(list)

    for e in list1 + list2:
        dict1[e[0]].append(e[1])

    merged_list = list()

    for key, value in dict1.items():
        max_value = []
        max_value.append(max(value))
        merged_list.append([key] + max_value)

    return merged_list


def addToDictionaryResult(dict_result, key, value):
    if key not in dict_result.keys():
        dict_result[key] = value

    return dict_result


def extractDatasets(df_dataset, np_CROSS):  # TODO: Optimize this

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
                # print("Starting : df_filtered_dataset = df_dataset.copy")
                df_filtered_dataset = df_dataset.copy(deep = True)  # TODO OPTIMIZE to proceed

                # print("Starting : np_dataset_pair = FILS.applyFilter")
                np_dataset_pair = FILS.applyFilter(df_filtered_dataset, list_filter)  # [datasetA, datasetB] | Length: 2

                # list_dataset_pairs.append(np_dataset_pair)
                # print("Starting : list_pairs.append(np_dataset_pair)")
                list_pairs.append(
                    np_dataset_pair)  # List of dataset pairs (list) in a level [ [datasetA, datasetB], [<...>] ]

                # print("Starting : list_pairs_filter.append(list_filter)")
                list_pairs_filter.append(list_filter)

            # print("Starting : list_level.append(list_pairs)")
            list_level.append(list_pairs)
            # print("Starting : list_level_filter.append(list_pairs_filter)")
            list_level_filter.append(list_pairs_filter)

        # print("Starting : list_cross_type.append(list_level)")
        list_cross_type.append(list_level)  # List of levels (list) of dataset pairs
        # print("Starting : list_cross_type_filter.append(list_level_filter)")
        list_cross_type_filter.append(list_level_filter)  # List of levels filters equivalent to list_cross_type

    # print("Starting : np_list_cross_type = np.array(list_cross_type))")
    np_list_cross_type = np.array(list_cross_type)
    # list_cross_type_filter = np.array(list_cross_type_filter)

    # print("")
    # print("")
    # print("")

    return np_list_cross_type, list_cross_type_filter








