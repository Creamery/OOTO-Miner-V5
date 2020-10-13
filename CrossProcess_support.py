import pprint
import itertools
import numpy as np
import copy
import RFE_support as RFES

CHECKLIST = []
PP = pprint.PrettyPrinter(indent = 4)
OPTION_CODES = [":a", ":b"]  # TODO (Future) confirm this
MAX_LEVEL = 3  # The maximum level to process

'''
Updates the list of finished feature pairs.
The list follows the form of [[filters], [filters]].
An example is shown below:
checklist[
    [["b1:a", "b1:b"], ["b5:a"]],
    [["b1:a"], [b5:a"]],
    [["b1:a"], [b5:b"]],
]
Returns TRUE if the output is accepted, and False otherwise.
'''
def updateChecklist(list_cross):
    # When updating, check if list_cross is already in checklist
    if checkChecklist(list_cross) is False:  # If not, append to checklist
        CHECKLIST.append(list_cross)
        return True
    else:
        return False
'''
 Parameter list_cross contains something of the form of:
 [[filters], [filters]]
'''
def checkChecklist(list_cross):
    isIn = False
    for checklist_items in CHECKLIST:
        len_checklist_item = len(checklist_items)

        count_match = 0
        for cross_item in list_cross:
            for checklist_item in checklist_items:
                if all(x in cross_item for x in checklist_item):
                    count_match = count_match + 1
                    # print("cross: ")
                    # print(cross_item)
                    # print("check: ")
                    # print(checklist_item)
                    # print("")
        # print("Match COUNT: " + str(count_match))
        if count_match == len_checklist_item:
            isIn = True

    return isIn


def printChecklist(Checklist):
    PP.pprint(Checklist)

# Level is from 1 to 3. It is also the number of groups the function produces.
# It then groups each resulting cross_options into pairs, which results in cross_filters.
def crossFilters(filters, level):
    # Get possible combinations of options (in filters parameter)
    combination = list(itertools.combinations(filters, level))
    set_combination = set(combination)
    list_combination = []

    for item in set_combination:
        list_item = np.asarray(item)
        list_combination.append(list_item)

    # list_combination = [val for sublist in list_combination for val in sublist]

    len_list_combination = len(list_combination)
    cross_filters = []

    end_index = len_list_combination - 1
    for i in range(end_index):
        # print("I IS " + str(i))
        item_1 = list_combination[i]
        for j in range(end_index):
            counter = i + (j + 1)
            if counter <= (end_index):
                # print("J IS " + str(counter))
                item_2 = list_combination[counter]
                cross = []
                cross.append(item_1)
                cross.append(item_2)
                cross_filters.append(cross)

    # Remove the extra details from the array, i.e. "dtype"
    list_cross_filters = []
    for item in cross_filters:
        item = [list(i) for i in item]
        list_cross_filters.append(item)
    return list_cross_filters

'''
Returns N SSFs, which is decided by RFES.MAX_RANK. In the current program, MAX_RANK = 3.
'''
def extractCROSS(dict_rfe):
    # print(dict_rfe)
    list_feat_codes = []
    for key, value in dict_rfe.items():
        list_feat_codes.append(value)

    CROSS = convertToCrossFilter(list_feat_codes)
    return CROSS
'''
Processes an array of SSFs. The length must be equal to MAX_LEVEL defined at the top of this script.
'''
def processLVLs(CROSS):
    len_CROSS = len(CROSS)
    # LVLs = []
    LVL = [[0 for x in range(len_CROSS)] for y in range(MAX_LEVEL)]  # Initialize matrix (2D Array)

    for i_type in range(len_CROSS):  # SSFs 0, 1, 2
        if i_type > 0:  # Process the union of the current SSF and the previous SSF
            SSF = unionSSF(CROSS[i_type-1], CROSS[i_type])
        else:
            SSF = CROSS[i_type]

        for i_level in range(MAX_LEVEL):  # For each SSF, process level 3x (or MAX_LEVEL times)
            level = i_level + 1
            # print(level)
            LVL[i_type][i_level] = crossFilters(SSF, level)
        # LVLs.append(LVL)
    PP.pprint(LVL)  # TODO Lessen dimensions

'''
Creates and returns a list that is a union of the 2 parameters.
'''
def unionSSF(SSF_1, SSF_2):
    SSF_1_copy = copy.deepcopy(SSF_1)
    SSF_2_copy = copy.deepcopy(SSF_2)
    SSF_union = SSF_1_copy + SSF_2_copy
    return SSF_union
'''
Convert array of feature codes (i.e. ['b1', 'u3']) to cross filter input
(i.e. ["b1:a", "b1:b",
       "u3:a", "u3:b"])
'''
def convertToCrossFilter(list_feat_codes):
    SSFs = []

    for feature_codes in list_feat_codes:
        SSF = []
        for feature_code in feature_codes:
            for option_code in OPTION_CODES:
                str_feature_code = str(feature_code + option_code)
                SSF.append(str_feature_code)
        # print(SSF)
        SSFs.append(SSF)
    return SSFs

