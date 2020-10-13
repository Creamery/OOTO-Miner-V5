import pprint
import itertools
import numpy as np
import copy

import Filter_support as FILS

def crossProcess(df_dataset, np_CROSS):

    # Generate datasets as dictated by filters
    np_dataset_pairs = extractDatasets(df_dataset, np_CROSS)

    print(np_dataset_pairs)



def extractDatasets(df_dataset, np_CROSS):
    list_dataset_pairs = []
    # Filter datasets according to filters
    for np_cross_type in np_CROSS:  # np_cross_type[type]
        for np_level in np_cross_type:  # np_cross_type[type][level]
            for list_filter in np_level:  # [["b1:a", "b2:b"], ["u3:b", "b5:b]]
                df_filtered_dataset = df_dataset.copy(deep = True)  # TODO (Future) Can be optimized
                np_filtered_datasets = FILS.applyFilter(df_filtered_dataset, list_filter)  # Dataset A & B
                list_dataset_pairs.append(np_filtered_datasets)

    np_dataset_pairs = np.array(list_dataset_pairs)
    return np_dataset_pairs








