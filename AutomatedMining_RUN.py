
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
import __Depth_support as DS
import _UIConstants_support as UICS


def loaderModule():
    df_raw_dataset, df_dataset, ftr_names = LS.loadInput()  # Can add parameters
    return df_raw_dataset, df_dataset, ftr_names

def rfeModule(df_raw_dataset, ftr_names, controller):
    controller.updateModuleProgress(0, UICS.FIRST_MESSAGE_SPACE + "[ Starting Automated OOTO Miner] ")  # 1
    time.sleep(1)

    dict_rfe = RFES.performRFE(df_raw_dataset, ftr_names, controller)
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
    dict_significant_results = CPS.crossProcessOptimized(df_dataset, np_CROSS, depth, controller)
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

    df_raw_dataset, df_dataset, ftr_names = loaderModule()

    # Run STATIC depth mining (Loops based on MAX DEPTH)
    # dict_significant_results = runStaticDepthMining(df_raw_dataset, df_dataset, ftr_names, controller)

    # Depth mining that continues on until the p-value stops updating
    dict_significant_results = runMobileDepthMining(df_raw_dataset, df_dataset, ftr_names, controller)

    controller.isAMFinished()  # Enables the Check button (Call on completion of the last iteration)
    print("Automated Mining Finished...")



    return dict_significant_results



'''
    Mine data according to the p-value.
    The miner continues until p-value stops updating.
'''
def runMobileDepthMining(df_raw_dataset, df_dataset, ftr_names, controller):
    depth = UICS.MAX_DEPTH
    i_depth = UICS.getStartDepth()  # Getting it this way will subtract 1 from the value, to be used as an index
    dict_significant_results = None

    for _ in range(i_depth, depth):  # TODO: Fix this so that it will stop according to the change in p-value
        curr_depth = i_depth + 1

        print("Starting DEPTH: " + str(curr_depth) + " of " + str(depth))
        # Select SSFs, if first iteration, use RFE, else load the generated SSFs of the previous depth
        if i_depth == 0:
            print("Starting RFE...")
            dict_ranked_features = rfeModule(df_raw_dataset, ftr_names, controller)
            print("-- RFE Finished --")
            print("")

        else:
            print("Extracting SSFs from Previous Depth [" + str(i_depth) + "]...")
            # Load the previous SSFs and consolidate. The current depth
            # indicates the PREVIOUS SSF folder.
            dict_ranked_features = DS.loadPreviousSSFs(i_depth)
            print("-- Successfully Extracted Previous SSFs --")


        print("Starting Filtering...")
        np_cross = filterModule(dict_ranked_features, controller)
        print("-- Filtering Finished --")
        print("")

        print("Starting Cross Process...")
        dict_significant_results = crossProcessModule(df_dataset, np_cross, curr_depth, controller)
        print("-- Cross Process Finished --")

    return dict_significant_results



'''
    Mine data according to the value of MAX DEPTH.
    MAX DEPTH is declared in the UICS script.
'''
def runStaticDepthMining(df_raw_dataset, df_dataset, ftr_names, controller):
    depth = UICS.MAX_DEPTH
    i_depth = UICS.getStartDepth()  # Getting it this way will subtract 1 from the value, to be used as an index
    dict_significant_results = None

    for _ in range(i_depth, depth):
        curr_depth = i_depth + 1

        print("Starting DEPTH: " + str(curr_depth) + " of " + str(depth))
        # Select SSFs, if first iteration, use RFE, else load the generated SSFs of the previous depth
        if i_depth == 0:
            print("Starting RFE...")
            dict_ranked_features = rfeModule(df_raw_dataset, ftr_names, controller)
            print("-- RFE Finished --")
            print("")

        else:
            print("Extracting SSFs from Previous Depth [" + str(i_depth) + "]...")
            # Load the previous SSFs and consolidate. The current depth
            # indicates the PREVIOUS SSF folder.
            dict_ranked_features = DS.loadPreviousSSFs(i_depth)
            print("-- Successfully Extracted Previous SSFs --")


        print("Starting Filtering...")
        np_cross = filterModule(dict_ranked_features, controller)
        print("-- Filtering Finished --")
        print("")

        print("Starting Cross Process...")
        dict_significant_results = crossProcessModule(df_dataset, np_cross, curr_depth, controller)
        print("-- Cross Process Finished --")

    return dict_significant_results



