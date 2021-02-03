

import collections
import numpy as np
import __Loader_support as LS
import __ChiSquare_support as CHIS
import _UIConstants_support as UICS
import _AMVariables_support as AMVS


def process(queue_flag, queue_return,
            depth, np_cross_filters,
            np_cross_datasets, queue_console,
            iterable):


    i_cross_type = iterable[0]
    i_cross_level = iterable[1]

    cross_type = np_cross_datasets[i_cross_type]  # Iterate through each CROSS TYPE
    # The variable cross_level is the list of dataframes
    cross_level = cross_type[i_cross_level]  # Iterate through each LEVEL
    len_cross_level = len(cross_level)

    list_level_ssfs = []
    list_all_ssfs = []
    list_ssfs = []
    dict_result_table_sig = collections.OrderedDict()

    str_current_cross = "[" + str(i_cross_type) + "][" + str(i_cross_level + 1) + "]"
    # Title for the current cross process
    str_title = UICS.SUB_MODULE_INDICATOR + "Processing CROSS" + str_current_cross  # LVL Pass 1
    # Update the progress bar about the current CROSS[type][level]
    # controller.updateModuleProgress(key, str_title)  # Pass 1 TODO
    # time.sleep(0.01)  # Sleep

    i_process_count = 0  # Process count for current CROSS[type][level]
    # np_level_ssfs = np.array(list_level_ssfs)

    for i_dataset_pairs in range(len_cross_level):
        dataset_pairs = cross_level[i_dataset_pairs]
        len_dataset_pairs = len(dataset_pairs)

        str_cross_level_length = str(len_cross_level)
        #  Description for the current cross process
        str_description = "         " + str_current_cross + " - " + str(
            i_dataset_pairs + 1) + " of " + str_cross_level_length
        # controller.updateModuleProgress(key, str_description)  # INNER PASS 1
        # queue_console.put(("A", "B"))

        for i_dataset_pair in range(len_dataset_pairs):

            dataset_pair = dataset_pairs[i_dataset_pair]

            dict_chi_square = CHIS.chiSquare(dataset_pair)
            # if dict_chi_square is None:
            #     print("dict_chi_square is NONE")
            # controller.updateModuleProgress(key, "Applying Chi-square")
            # time.sleep(0.01)

            df_processed_output, list_ssf, list_sig_output = CHIS.processChiSquareTable(dict_chi_square)

            # if df_processed_output is None:
            # print("df_processed_output is NONE")
            if df_processed_output is not None:
                # print("")
                # print(len(np_cross_filters[i_cross_type]))
                # print(i_cross_type)
                # print(len(np_cross_filters[i_cross_type][i_cross_level]))
                # print(i_cross_level)
                # print(len(np_cross_filters[i_cross_type][i_cross_level][i_dataset_pairs]))
                # print(i_dataset_pairs)
                # print("")
                dataset_pair_filter = np_cross_filters[i_cross_type][i_cross_level][i_dataset_pairs]

                if len(list_ssfs) == 0:
                    list_ssfs = list_ssf
                else:
                    list_ssfs = mergeAndFilter(list_ssfs, list_ssf)

                np_dataset_pair_filter = np.array(dataset_pair_filter)
                # list_chi_square_output.append([df_output, np_dataset_pair_filter])
                list_index = [i_cross_type, i_cross_level]

                # controller.updateModuleProgress(key, "Exporting Chi-square Table")
                # time.sleep(0.01)

                df_output, str_pair_name = LS.exportChiSquareTable(df_processed_output,
                                                                   np_dataset_pair_filter,
                                                                   depth, list_index)

                dict_result_table_sig = addToDictionaryResult(dict_result_table_sig, str_pair_name, list_sig_output)
            # else:
            # controller.updateModuleProgress(key, str_description)  # Pass 2
            # Add 1 to make up for the missed processes
            # print("DF OUTPUT IS NULL: Skipping Item")

        list_all_ssfs = mergeAndFilter(list_all_ssfs, list_ssfs)
        ssfs_filename = "SSFs - CROSS[" + str(i_cross_type) + "][" + str(i_cross_level + 1) + "].csv"
        LS.exportSSFs(list_ssfs, ssfs_filename, depth)

    queue_return.put(dict_result_table_sig)
    queue_flag.get()
    print("DONE")


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


