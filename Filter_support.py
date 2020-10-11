
import json  # For pretty print
import collections
import Loader_support as LS

def createFilter(feat_key, option):
    dict_filter = collections.OrderedDict()
    dict_filter[feat_key] = []
    dict_filter[feat_key].append(option)
    return dict_filter

def appendFilter(dict_filter, feat_key, option):
    if feat_key in dict_filter:  # If key in filter, append to that entry's array
        (dict_filter[feat_key]).append(option)

    else:  # If key not in filter, add a new entry and array, then append option
        dict_filter[feat_key] = []
        dict_filter[feat_key].append(option)

    return dict_filter

def applyFilter(df_dataset, dict_filter):
    filteredDatasets = []

    for key, options in dict_filter.items():
        filteredDataset = df_dataset.copy(deep = True)
        filteredDataset = filteredDataset[filteredDataset[key].isin(options)]
        # print(LS.GL_OUTPUT_PATH)
        LS.exportDataset(filteredDataset, str(key + ".csv"), LS.GL_OUTPUT_PATH)
    print("Apply Filter")
    return filteredDatasets



def printFilter(oDict):
    print(json.dumps(oDict, indent = 4))




