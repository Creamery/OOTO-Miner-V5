import pprint
import itertools
import numpy as np
import copy
import collections

PP = pprint.PrettyPrinter(indent = 4)
OPTION_CODES = [":a", ":b"]  # TODO (Future) confirm this
MAX_LEVEL = 3  # The maximum level to process
MAX_FILTER_ELEMENTS = 2  # TODO (Future) Check if this needs to be increased (this is the number of group comparisons in a filter)

# CHECKLISTS = np.fromiter(Checklist, list)
CHECKLISTS = [None] * MAX_LEVEL
'''
 Level is from 1 to 3. It is also the number of groups the function produces.
 It then groups each resulting cross_options into pairs, which results in cross_filters.
'''
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

    # TODO [PRINT: Amount of reduced values for paper]
    ctr_Raw = 0
    ctr_Filtered = 0

    for i in range(end_index):
        # print("I IS " + str(i))
        item_1 = list_combination[i]
        for j in range(end_index):
            counter = i + (j + 1)
            if counter <= end_index:
                # print("J IS " + str(counter))
                item_2 = list_combination[counter]
                cross = []
                cross.append(item_1)
                cross.append(item_2)
                if updateChecklist(cross, level):
                    cross_filters.append(cross)
                    ctr_Filtered = ctr_Filtered + 1

                ctr_Raw = ctr_Raw + 1

    # Remove the extra details from the array, i.e. "dtype"
    list_cross_filters = []
    for item in cross_filters:
        item = [list(i) for i in item]
        list_cross_filters.append(item)
    np_list_cross_filters = np.array(list_cross_filters)
    print("RAW " + str(ctr_Raw))
    print("ACCEPTED " + str(ctr_Filtered))
    return np_list_cross_filters


'''
 Returns N SSFs, which is decided by RFES.MAX_RANK. In the current program, MAX_RANK = 3.
 The input dict_rfe contains:
 OrderedDict([(1, ['b1', 'u4', 'p10']), (2, ['p11']), (3, ['s6'])])
'''
def extractFilters(dict_rfe):
    # print(dict_rfe)
    list_feat_codes = []
    for key, value in dict_rfe.items():
        list_feat_codes.append(value)  # Sample Contents: [[b1, u4, p10],[p11],[s6]]
    list_feat_codes = np.array(list_feat_codes)
    extracted_filters = convertToCrossFilters(list_feat_codes)

    return extracted_filters


'''
 Convert array of feature codes (i.e. ['b1', 'u3']) to cross filter input
 (i.e. ["b1:a", "b1:b",
        "u3:a", "u3:b"])
'''
def convertToCrossFilters(list_feat_codes):
    CROSS = []

    for feature_codes in list_feat_codes:
        SSF = []
        for feature_code in feature_codes:
            for option_code in OPTION_CODES:
                str_feature_code = str(feature_code + option_code)
                SSF.append(str_feature_code)
        # print(SSF)
        SSF = np.array(SSF)
        CROSS.append(SSF)

    CROSS = np.array(CROSS)
    return CROSS

# TODO PRINT [Log values for paper]
'''
 Processes an array of SSFs. The length must be equal to MAX_LEVEL defined at the top of this script.
 Returns LVL[types][levels] where types = 0-2 and levels = 1-3
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
            print "TYPE {0} LVL {1}".format(i_type, level)

            np_filter = crossFilters(SSF, level)
            # np_filter = np.array(filter)
            LVL[i_type][i_level] = np_filter  # TODO Lessen dimensions
            print("")  # TODO Remove if you are not gonna print here anymore

    LVL = np.array(LVL)

    # LVLs.append(LVL)
    # PP.pprint(LVL)
    return LVL

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
 Returns True if list_cross is already in the finished list (CHECKLIST) and False otherwise
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
                    # if count_match == 1:
                    #     match_1_ci = cross_item
                    #     match_1_chi = checklist_item
                    # elif count_match == 2:
                    #     match_2_ci = cross_item
                    #     match_2_chi = checklist_item

                    # If all entries in a group match, return True
                    if count_match == MAX_FILTER_ELEMENTS:
                        isIn = True

                        # print("CHECK CHECKLIST")
                        # print(match_1_ci)
                        # print(match_1_chi)
                        # print("")
                        # print(match_2_ci)
                        # print(match_2_chi)
                        # print("")

                        return isIn

    return isIn


def printChecklist(Checklist):
    PP.pprint(Checklist)
