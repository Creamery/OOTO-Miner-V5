import pprint
import itertools
import numpy as np

CHECKLIST = []
PP = pprint.PrettyPrinter(indent = 4)

'''
Updates the list of finished feature pairs.
The list follows the form of [[filters], [filters]].
An example is shown below:
checklist[
    [["b1:a", "b1:b"], ["b5:a"]],
    [["b1:a"], [b5:a"]],
    [["b1:a"], [b5:b"]],
]
'''
def updateChecklist(list_cross):
    # When updating, check if list_cross is already in checklist
    if checkChecklist(list_cross) is False:  # If not, append to checklist
        CHECKLIST.append(list_cross)
    # printChecklist(CHECKLIST)
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

    print(list_combination)

    len_list_combination = len(list_combination)
    cross_filters = []
    PP.pprint(list_combination)

    end_index = len_list_combination - 1
    for i in range(end_index):
        print("I IS " + str(i))
        item_1 = list_combination[i]
        for j in range(end_index):
            # counter = i + j + 1 - i
            counter = i + (j + 1)
            if counter <= (end_index):
                print("J IS " + str(counter))
                item_2 = list_combination[counter]
                cross = []
                cross.append(item_1)
                cross.append(item_2)
                cross_filters.append(cross)

    print(len(cross_filters))
    for item in cross_filters:
        PP.pprint(item)






    # PP.pprint(cross_filters)

    # # Extract the values
    # cross_options = []
    # for item in set_combination:
    #     for option in item:
    #         print(option)
    #         cross_options.append(option)
    #     print("")
    #
    # # Then recombine the values as unique pairs (combinations) to one another
    # cross_filters = list(itertools.combinations(cross_options, 2))
    # # set_cross_filters = set(cross_filters)
    # return cross_filters







