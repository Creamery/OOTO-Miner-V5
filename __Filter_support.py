
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    The FILTERING MODULE. This script generates the filters required
    by the CROSS PROCESS MODULE in the Automated Mining System.
    [Candy]
'''

import pprint
import itertools
import numpy as np
import copy
import collections
import time
from numba import jit

import _UIConstants_support as UICS
import _AMVariables_support as AMVS

PP = pprint.PrettyPrinter(indent = 4)
OPTION_CODES = [":a", ":b"]  # TODO (Future) confirm this
MAX_LEVEL = 3  # The maximum level to process
MAX_FILTER_ELEMENTS = 2  # TODO (Future) Check if this needs to be increased (this is the number of group comparisons in a filter)




# CHECKLISTS = np.fromiter(Checklist, list)
CHECKLISTS = [None] * MAX_LEVEL
'''
    Level is from 1 to 3. It is also the number of groups the function produces.
    It then groups each resulting cross_options into pairs, which results in cross_filters.
    
    Sample output;
    [ [['b1:b']['b1:a']]
      [['p11:b']['p11:a']]
      [['p10:a']['p10:b']] ]
      
    [ [['b1:b' 'p10:b' 'p11:a']['b1:b' 'p10:a' 'p11:a']]
      <...>
      [['b1:a' 'p10:b' 'p11:b']['b1:a' 'p10:a' 'p11:b']] ]
'''
def crossFilters(filters, level):
    singleton = AMVS.getSingleton()

    # Get possible combinations of options (in filters parameter)
    combination = list(itertools.combinations(filters, level))
    set_combination = set(combination)
    list_combination = []

    for item in set_combination:
        list_item = np.asarray(item)
        list_combination.append(list_item)

    # list_combination = [val for sublist in list_combination for val in sublist]
    list_combination = np.array(list_combination)
    len_list_combination = len(list_combination)
    cross_filters = []

    end_index = len_list_combination - 1

    # TODO [PRINT: Amount of reduced values for paper]
    ctr_Raw = 0
    ctr_Valid = 0
    ctr_Purged = 0
    ctr_Filtered = 0

    for i in range(end_index):
        item_1 = list_combination[i]
        for j in range(end_index):
            counter = i + (j + 1)
            if counter <= end_index:
                item_2 = list_combination[counter]
                cross = [item_1, item_2]  # Sample content: [array(['b1:a', 'p11:b'], dtype='<U5'), array(['b1:a', 'p11:a'], dtype='<U5')]

                if validComparison(cross):  # Only proceed if cross is VALID; FMI check notes above function
                    if updateChecklist(cross, level):
                        if not purgedCross(cross):  # Remove repeating pairs
                            # cross_filters.append(cross)
                            # print(cross)
                            ctr_Purged = ctr_Purged + 1
                            if not singleton.isFeaturePairParsed(cross):  # Don't include previously parsed pairs (from previous depths)
                                cross_filters.append(cross)  # Append a filter to cross_filters
                                singleton.updateFeaturePairs(cross)
                                singleton.addCtrAccepted()
                                # print("Added:")
                                # print(cross)
                                # print("Singleton contents:")
                                # print(singleton.getFeaturePairs())
                                ctr_Filtered = ctr_Filtered + 1

                    ctr_Valid = ctr_Valid + 1
                ctr_Raw = ctr_Raw + 1



    # Remove the extra details from the array, i.e. "dtype"
    list_cross_filters = []
    for item in cross_filters:
        item = [list(i) for i in item]
        list_cross_filters.append(item)
    np_list_cross_filters = np.array(list_cross_filters)

    # print(np_list_cross_filters)
    print("")
    print("RAW " + str(ctr_Raw))
    print("VALID " + str(ctr_Valid))
    print("PURGED " + str(ctr_Purged))
    print("ACCEPTED " + str(ctr_Filtered))
    print("")

    frequency_count = end_index * end_index
    return np_list_cross_filters, frequency_count


'''
    Checks if there is a filter element that contains ['feat_code:a', 'feat_code:b']
    and removes it (a and b under the same feature code is the same as sampling the
    entire dataset.
'''
def purgedCross(cross):
    isPurged = False
    # st = st[:-1]
    for filter_element in cross:
        # Remove last letter of each entry inside filter_element (i.e. 'a' and 'b')
        clean_filter_element = [x[:-1] for x in filter_element]

        # Statement returns true of there is a duplicate in clean_filter_element
        if len(clean_filter_element) != len(set(clean_filter_element)):
            # if duplicate exists, set isPurged to True and return
            isPurged = True
            return isPurged
    return isPurged



'''
    Returns N SSFs, which is decided by RFES.MAX_RANK. In the current program, MAX_RANK = 3.
    The input dict_rfe contains:
    OrderedDict([(1, ['b1', 'u4', 'p10']), (2, ['p11']), (3, ['s6'])])
'''
def extractCrossFilters(dict_rfe, controller):
    # print(dict_rfe)
    list_feat_codes = []
    for key, value in dict_rfe.items():
        list_feat_codes.append(value)  # Sample Contents: [[b1, u4, p10],[p11],[s6]]
    list_feat_codes = np.array(list_feat_codes)
    extracted_filters = convertToCrossFilters(list_feat_codes, controller)

    frequency_count = len(dict_rfe.keys())
    return extracted_filters, frequency_count


'''
    Convert array of feature codes (i.e. ['b1', 'u3']) to cross filter input
    (i.e. ["b1:a", "b1:b",
           "u3:a", "u3:b"])
'''
def convertToCrossFilters(list_feat_codes, controller):
    key = UICS.KEY_FILTERING_MODULE

    CROSS = []
    controller.updateModuleProgress(key, UICS.MODULE_INDICATOR + "Starting FILTER MODULE")  # 1
    # time.sleep(0.01)


    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Creating SSF Array")  # 2
    # time.sleep(0.01)

    for feature_codes in list_feat_codes:
        SSF = []
        for feature_code in feature_codes:
            for option_code in OPTION_CODES:
                str_feature_code = str(feature_code + option_code)
                SSF.append(str_feature_code)
        # print(SSF)
        SSF = np.array(SSF)
        CROSS.append(SSF)

    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Successfully Created SSF Array")  # 3
    # time.sleep(0.01)

    CROSS = np.array(CROSS)  # Sample contents: [array(['b1:a', 'b1:b', 'p10:a', 'p10:b', 'p11:a', 'p11:b'], dtype='<U5')
                             # array(['p5:a', 'p5:b'], dtype='<U4') array(['p9:a', 'p9:b'], dtype='<U4')]

    return CROSS

# TODO PRINT [Log values for paper]
'''
    Processes an array of SSFs. The length must be equal to MAX_LEVEL defined at the top of this script.
    Returns LVL[types][levels] where types = 0-2 and levels = 1-3
'''
def processLVLs(CROSS):

    len_CROSS = len(CROSS)
    frequency_count = 0

    # LVLs = []
    LVL = [[0 for x in range(len_CROSS)] for y in range(MAX_LEVEL)]  # Initialize matrix (2D Array)

    for i_type in range(len_CROSS):  # SSFs 0, 1, 2
        if i_type > 0:  # Process the union of the current SSF and the previous SSF
            SSF = unionSSF(CROSS[i_type-1], CROSS[i_type])
        else:
            SSF = CROSS[i_type]

        for i_level in range(MAX_LEVEL):  # For each SSF, process level 3x (or MAX_LEVEL times)
            level = i_level + 1
            # print "TYPE {0} LVL {1}".format(i_type, level)

            np_filter, frequency_count = crossFilters(SSF, level)
            # print(np_filter)

            LVL[i_type][i_level] = np_filter  # TODO Lessen dimensions
            # print(np_filter)
            # print("")  # TODO Remove if you are not gonna print here anymore
        # print("")
    LVL = np.array(LVL)

    frequency_count = frequency_count + (len_CROSS * MAX_LEVEL)
    # LVLs.append(LVL)
    # PP.pprint(LVL)

    return LVL, frequency_count


'''
    Creates and returns a list that is a union of the 2 (Numpy array) parameters.
'''
def unionSSF(SSF_1, SSF_2):
    SSF_1_copy = copy.deepcopy(SSF_1)
    SSF_2_copy = copy.deepcopy(SSF_2)
    # SSF_union = SSF_1_copy + SSF_2_copy
    SSF_union = np.concatenate((SSF_1_copy, SSF_2_copy))
    SSF_union = np.array(SSF_union)
    return SSF_union

'''
    Takes in a filter in the form of a list of lists (llist_cross).
    This function only accepts filters with ONE varying option per
    list contained within it. The varying option must also be under
    the same feature.
    
    For example: [[b1:a, b2:a, b3:a] VS [b1:a, b2:a, b3:b]] is VALID since
    only the third element (under the same feature) has a different option.
    
    BUT [[b1:a, b2:a, b3:a] VS [b1:a, b2:b, b3:b]] is NOT VALID because two
    elements under the same feature have different options.
    
    If the different option between the two inner lists happened to be
    "b3:a" and "b4:a" respectively, it should also NOT be accepted, since the
    two options are under different features, and is considered to be an
    invalid comparison.    
'''
def validComparison(llist_cross):
    len_cross = len(llist_cross)
    if len_cross > 0:  # Check incase llist_cross is empty, though that should really not happen
        item_1 = llist_cross[0]
        for i in range(1, len_cross):  # Start at the second element, which is index 1
            item_2 = llist_cross[i]
            list_diff = list(set(item_1) - set(item_2))
            len_diff = len(list_diff)
            # print("")
            # print(item_1)
            # print(item_2)
            # print(list_diff)
            # print(len_diff)

            # If at least one list difference is not equal to the allowed difference, return False
            if len_diff != UICS.ALLOWED_DIFFERENCE:
                return False
            else:  # Check if the different elements are under the same feature
                list_unique = set(item_1) ^ set(item_2)  # Perform XOR to get uncommon elements between the two lists
                # print(list_unique)
                prev_feat = None
                for item in list_unique:
                    str_item = item.strip()
                    split_item = str_item.split(UICS.SPLIT_SYMBOL)  # Split the element by the colon (:)
                    feat_key = split_item[0]
                    # option = split_item[1]

                    if prev_feat is None:
                        prev_feat = feat_key
                    else:
                        if prev_feat != feat_key:
                            return False  # If at least one of the elements do not belong to the same feature, return False

        return True  # If the loop ends without exceeding the allowed difference, return True
    return False


'''
    Updates the list of finished feature pairs.
    The list follows the form of [[filters], [filters]].
    An example is shown below:
    checklist[
        [["b1:a"], [b5:a"]],
        [["b1:a"], [b5:b"]],
    ]
    Returns TRUE if the output is accepted, and False otherwise.
    
    NOTE: Actual appearance when a checklist entry (list_cross) is printed
    [array(['p11:a'], dtype='<U5'), array(['p11:b'], dtype='<U5')]
    [array(['b1:a', 'p10:b'], dtype='<U5'), array(['p10:a', 'p10:b'], dtype='<U5')]
'''
def updateChecklist(list_cross, level):
    # When updating, check if list_cross is already in checklist
    if checkChecklist(list_cross, level) is False:  # If not, append to checklist
        appendChecklist(list_cross, level)
        return True
    else:
        return False


'''
    Algorithm requires level to be from 1-3, hence the index subtraction
'''
def getChecklist(level):
    i_level = level - 1
    if CHECKLISTS[i_level]:
        np_checklist = np.array(CHECKLISTS[i_level])
        return np_checklist
    else:
        CHECKLISTS[i_level] = []
    return CHECKLISTS[i_level]

def appendChecklist(list_cross, level):
    np.append(CHECKLISTS[level - 1], list_cross)


'''
    Parameter list_cross contains something of the form of:
    [[filters], [filters]]
    Returns True if list_cross is already in the finished list
    (CHECKLIST) and False otherwise
'''
def checkChecklist(list_cross, level):
    isIn = False
    np_list_cross = np.array(list_cross)
    # if len(getChecklist(level)) < 0:
    for checklist_items in getChecklist(level):
        # match_1_ci = []
        # match_2 = []
        count_match = 0
        np_checklist_items = checklist_items

        for cross_item in np_list_cross:
            np_cross_item = np.array(cross_item)
            for checklist_item in np_checklist_items:
                np_checklist_item = np.array(checklist_item)
                # If all items in the array matches the other, return True
                if collections.Counter(np_cross_item) == collections.Counter(np_checklist_item):
                    count_match = count_match + 1


                    # If all entries in a group match, return True
                    if count_match == MAX_FILTER_ELEMENTS:
                        isIn = True
                        return isIn

    return isIn


def printChecklist(Checklist):
    PP.pprint(Checklist)


'''
FUNCTIONS FOR APPLYING FILTERS
'''

'''
    This function accepts a single filter and applies it to the dataset.
    It then returns the filtered dataset.
    A filter should be in the following format:
    [["b1:a", "b5:b"], ["b3:a", "u3:b]]
    
    The function returns the 2 datasets (dataset A and B) to be compared.
'''
def applyFilter(df_dataset, list_filter):
    df_filtered_dataset = df_dataset.copy(deep = True)
    list_results = []
    np_filter_dict = extractFilter(list_filter)  # An np dictionary filter has 2 dictionaries

    # print("DICT FILTER")
    # print(np_filter_dicts[0])
    for dict_filter in np_filter_dict:  # For each part of the filter (i.e. 1 dictionary)
        df_result = filterDataset(df_filtered_dataset, dict_filter)
        list_results.append(df_result)


    # This approach fixes the value error as opposed to the commented approach
    np_filtered_dataset_pair = np.empty(MAX_FILTER_ELEMENTS, dtype = object)
    np_filtered_dataset_pair[:] = [list_results]
    # np_filtered_dataset_pair = np.array(list_results)
    return np_filtered_dataset_pair


'''
    Extracts the filter, where a filter is of the format [["b1:a", "b5:b"], ["b3:a", "u3:b]].
    Filters are assumed to have 2 sets of conditions.
    TODO: Assumes filters have 2 sets of conditions
    
    This function returns a list (np_filters) of dictionaries that contain the dictionary form
    of the filters. For a 2-element filter, it will return a 2-element list (where an element
    is a dictionary).
'''
def extractFilter(filter):
    list_filters = []
    # print("FILTER")
    for filter_element in filter:  # A single filter part, e.g. ["b1:a", "u3:b" ]
        dict_filter = collections.OrderedDict()
        # print("FILTER ELEMENT")
        for element in filter_element:
            # print("ELEMENT")
            split_item = element.split(UICS.SPLIT_SYMBOL)
            feat_key = split_item[0]
            option = split_item[1]

            # Check if the key has already been added. If not, add the key first
            if feat_key not in dict_filter:
                dict_filter[feat_key] = []

            dict_filter[feat_key].append(option)

        list_filters.append(dict_filter)

    np_filters = np.array(list_filters)

    return np_filters


'''
    Applies a a dict_filter on a dataset and returns the filtered dataset.
    To be used on only 1 filter.
'''
def filterDataset(df_dataset, dict_filter):
    df_filtered_dataset = df_dataset.copy(deep = True)

    for key, options in dict_filter.items():
        # Returns all rows that satisfy the array of conditions
        df_filtered_dataset = df_filtered_dataset[df_filtered_dataset[key].isin(options)]

    return df_filtered_dataset







