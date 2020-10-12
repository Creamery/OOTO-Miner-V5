import pprint

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
            print("")
            print("MATCH")

    return isIn


def printChecklist(Checklist):
    PP.pprint(Checklist)








