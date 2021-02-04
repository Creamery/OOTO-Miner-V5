
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"

'''
    This script contains all calls to the various Automated Mining
    Modules. It is also the script that is called when the Run button
    is clicked in the AM tab.
    [Candy]
'''

import os
import time
# Uploader support for converting read dataset
import __Loader_support as LS
import __RFE_support as RFES
import __Filter_support as FILS
import __CrossProcess_support as CPS
import __CrossProcess_MP_support as CMPS
import __Depth_support as DS
import _UIConstants_support as UICS
import _AMVariables_support as AMVS


def loaderModule():
    df_raw_dataset, df_dataset, ftr_names, pd_raw_dataset = LS.loadInput()  # Can add parameters
    return df_raw_dataset, df_dataset, ftr_names, pd_raw_dataset

def rfeModule(df_raw_dataset, ftr_names, pd_raw_dataset, controller):
    controller.updateModuleProgress(0, UICS.FIRST_MESSAGE_SPACE + "[ Starting Automated OOTO Miner] ")  # 1
    # time.sleep(1)

    dict_rfe = RFES.performRFE(df_raw_dataset, ftr_names, pd_raw_dataset, controller)
    return dict_rfe

def filterModule(dict_rfe, controller):
    i = 1
    print("SSFs:")
    text = "RFE Chosen SSFs:"
    controller.getAMController().addToConsoleAll(text + "\n")
    for key, value in dict_rfe.items():
        text = "SSF" + str(i) + " - " + str(value)
        print(text)
        i = i + 1
        controller.getAMController().addToConsoleAll(text + "\n")
        controller.getAMController().addToConsoleInput(text + "\n")

    # Takes the dictionary and converts it to the correct format for Crossing (e.g. ["b5:a", "b5:b"])
    extracted_cross_filters = FILS.extractCrossFilters(dict_rfe, controller)

    # NOTE: CROSS is the collection of SSFs
    CROSS = FILS.processLVLs(extracted_cross_filters)  # Returns the filter list for each level

    return CROSS


def crossProcessModule(df_dataset, np_CROSS, depth, controller):
    dict_significant_results = CMPS.crossProcessOptimized(df_dataset, np_CROSS, depth, controller)
    return dict_significant_results




def runAutomatedMining(controller):

    text = "RUNNING Automated Mining\n"  # Show start message in console
    controller.getAMController().addToConsoleAll(text + "\n")

    text = "MAX CROSS: " + str(UICS.MAX_CROSS)  # Show MAX CROSS in console and input
    controller.getAMController().addToConsoleAll(text + "\n")
    controller.getAMController().addToConsoleInput(text + "\n")

    text = "MAX LEVEL: " + str(UICS.MAX_LEVEL) + "\n"  # Show MAX LEVEL in console and input
    controller.getAMController().addToConsoleAll(text + "\n")
    controller.getAMController().addToConsoleInput(text + "\n")

    df_raw_dataset, df_dataset, ftr_names, pd_raw_dataset = loaderModule()

    # Run STATIC depth mining (Loops based on MAX DEPTH)
    # dict_significant_results = runStaticDepthMining(df_raw_dataset, df_dataset, ftr_names, controller)

    # Depth mining that continues on until the p-value stops updating
    dict_significant_results = runMobileDepthMining(df_raw_dataset, df_dataset, ftr_names, pd_raw_dataset, controller)

    controller.isAMFinished()  # Enables the Check button (Call on completion of the last iteration)
    print("Automated Mining Finished...")

    str_depths = str(AMVS.getSingleton().getDepths())
    controller.getAMController().addToConsoleAll("\nTotal Depth: " + str_depths)
    print("Total Depth " + str_depths)

    str_run_time = str(AMVS.getSingleton().getTime())
    controller.getAMController().addToConsoleAll("\nAM Run time:\n" + str_run_time + " seconds\n")
    print("Mining Run Time: " + str_run_time + " seconds")

    AMVS.getSingleton().resetSingleton()
    return dict_significant_results



'''
    Mine data according to the p-value.
    The miner continues until p-value stops updating.
'''
def runMobileDepthMining(df_raw_dataset, df_dataset, ftr_names, pd_raw_dataset, controller):
    singleton = AMVS.getSingleton()  # A Singleton class is used
    dict_significant_results = None
    isUpdating = True
    hasPrevSSFs = True
    i_depth = 0
    curr_depth = 0

    while isUpdating:  # Keep looping until the stop criteria are met
        curr_depth = i_depth + 1
        singleton.resetCtrAccepted()

        print("Starting DEPTH: " + str(curr_depth))
        # Select SSFs, if first iteration, use RFE, else load the generated SSFs of the previous depth
        if i_depth == 0:
            print("Loading SEED SSFs...")
            # dict_ranked_features = rfeModule(df_raw_dataset, ftr_names, controller)
            dict_ranked_features = UICS.SEED_SSFS
            AMVS.getSingleton().updateDictSSFs(dict_ranked_features)
            print("-- Successfully Loaded SEED SSFs --")

            print("Extracting RFE Features")
            rfe_features = rfeModule(df_raw_dataset, ftr_names, pd_raw_dataset, controller)
            print("-- Successfully Determined RFE Features --")
            print(rfe_features)

            print("")

        else:
            print("Extracting SSFs from Previous Depth [" + str(i_depth) + "]...")
            # Load the previous SSFs and consolidate. The current depth
            # indicates the PREVIOUS SSF folder.
            df_SSFs = DS.loadPreviousSSFs(i_depth)
            print("df_SSFs")
            print(df_SSFs)


            if df_SSFs is None:  # If there were no previously loaded SSFs, stop updating TODO: check if this can be determined earlier
                hasPrevSSFs = False
                isUpdating = False
                dict_ranked_features = None
                print("-- Failed to Locate Previous SSFs --")
            else:
                # Partition the extracted SSFs to 3 Ranks
                dict_new_ranked_features = DS.rankSSFs(df_SSFs)
                # Merge the new SSFs with the old SSFs
                AMVS.getSingleton().updateDictSSFs(dict_new_ranked_features)
                print("RANK")
                dict_ranked_features = AMVS.getSingleton().getDictSSFs()
                print(dict_ranked_features)
                print("-- Successfully Extracted Previous SSFs --")

        if hasPrevSSFs:
            print("Starting Filtering...")
            np_cross = filterModule(dict_ranked_features, controller)
            print("-- Filtering Finished --")
            print("")

            print("Starting Cross Process...")
            dict_significant_results = crossProcessModule(df_dataset, np_cross, curr_depth, controller)
            print("-- Cross Process Finished --")


            list_SSFs = getSSFsList(dict_ranked_features)
            print(list_SSFs)
            # if isConstantSSFs(list_SSFs):  # Stop mining if the current list of SSFs have been parsed before
            if singleton.isConstantSSFs(list_SSFs):  # Stop mining if the current list of SSFs have been parsed before
                isUpdating = False
            elif singleton.getCtrAccepted() == 0:  # Mark mining as finished when there are no more accepted values
                isUpdating = False

            print(singleton.getCtrAccepted())

            i_depth = i_depth + 1
            # print(dict_significant_results)
            # list_SSFs = getSSFsList(dict_ranked_features)
            # if isConstantSSFs(list_SSFs):  # Stop mining if the current list of SSFs have been parsed before
            #     isUpdating = False
            # if hasNoNewPairs():  # Stop mining if the significant results have all been parsed before
            #     isUpdating = False

            # singleton.updateSSFsList(list_SSFs)
            # print(list_SSFs)
            # print("")
            # print(singleton.getLlSSFs())
            # print("")

    AMVS.getSingleton().setDepths(i_depth - 1)  # Log total number of depths
    return dict_significant_results


'''
    Converts the values in the SSFs dictionary to a list.
'''
def getSSFsList(dict_SSFs):
    list_SSFs = []

    for key, value in dict_SSFs.items():
        list_SSFs.append(value)

    return list_SSFs

'''
    This function checks if the SSFs have been parsed
    before. If so, it returns True.
'''
def isConstantSSFs(list_currSSFs):
    singleton = AMVS.getSingleton()
    llist_prevSSFs = singleton.getLlSSFs()  # Get the list of all parsed SSFs (from all depths) via the Singleton class
    state = False

    for SSFs in llist_prevSSFs:
        # Check if all items in the current SSFs list are contained
        # in any previously parsed SSFs list
        state = isListsMatch(SSFs, list_currSSFs)
        if state:  # If there's a match, stop looping and return 'state'
            break

    return state


'''
    This function checks if all items in list2 are in list1.
'''
def isListsMatch(list1, list2):

    # len_list1 = len(list1)
    # len_list2 = len(list2)

    # if len_list1 > len_list2:
    #     list_A = list1
    #     list_B = list2
    # else:
    #     list_A = list2
    #     list_B = list1

    # Checks if all elements of list2 is in list1
    isMatch = all(item in list1 for item in list2)

    return isMatch



'''
    Mine data according to the value of MAX DEPTH.
    MAX DEPTH is declared in the UICS script.
'''
def runStaticDepthMining(df_raw_dataset, df_dataset, ftr_names, pd_raw_dataset, controller):
    depth = UICS.MAX_DEPTH
    start_depth = UICS.getStartDepth()  # Getting it this way will subtract 1 from the value, to be used as an index
    dict_significant_results = None

    for i_depth in range(start_depth, depth):  # TODO: Fix this so that it will stop according to the change in p-value
        curr_depth = i_depth + 1

        print("Starting DEPTH: " + str(curr_depth) + " of " + str(depth))
        # Select SSFs, if first iteration, use RFE, else load the generated SSFs of the previous depth
        if i_depth == 0:
            print("Starting RFE...")
            dict_ranked_features = rfeModule(df_raw_dataset, ftr_names, pd_raw_dataset, controller)
            print("-- RFE Finished --")
            print("")

        else:
            print("Extracting SSFs from Previous Depth [" + str(i_depth) + "]...")
            # Load the previous SSFs and consolidate. The current depth
            # indicates the PREVIOUS SSF folder.
            df_SSFs = DS.loadPreviousSSFs(i_depth)
            # Partition the extracted SSFs to 3 Ranks
            dict_ranked_features = DS.rankSSFs(df_SSFs)
            print("-- Successfully Extracted Previous SSFs --")


        print("Starting Filtering...")
        np_cross = filterModule(dict_ranked_features, controller)
        print("-- Filtering Finished --")
        print("")

        print("Starting Cross Process...")
        dict_significant_results = crossProcessModule(df_dataset, np_cross, curr_depth, controller)
        print("-- Cross Process Finished --")

    return dict_significant_results




