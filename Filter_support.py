
import json  # For pretty print
import collections

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
    filteredDataset = df_dataset
    print("Apply Filter")
    return filteredDataset



def printFilter(oDict):
    print(json.dumps(oDict, indent = 4))




