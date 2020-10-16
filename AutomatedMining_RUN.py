
import os
# Uploader support for converting read dataset
import Loader_support as LS
import RFE_support as RFES
import Filter_support as FILS
import CrossProcess_support as CPS


def rfeModule(df_raw_dataset, ftr_names):
    dict_rfe = RFES.performRFE(df_raw_dataset, ftr_names)
    return dict_rfe

def filterModule(dict_rfe):
    i = 1
    print("SSFs:")
    for key, value in dict_rfe.items():
        print "SSF" + str(i) + " - " + str(value)
        i = i + 1

    # Takes the dictionary and converts it to the correct format for Crossing (e.g. ["b5:a", "b5:b"])
    extracted_cross_filters = FILS.extractCrossFilters(dict_rfe)

    # NOTE: CROSS is the collection of SSFs
    CROSS = FILS.processLVLs(extracted_cross_filters)  # Returns the filter list for each level

    return CROSS


def crossProcessModule(df_dataset, np_CROSS):
    dict_significant_results = CPS.crossProcess(df_dataset, np_CROSS)
    return dict_significant_results



def runAutomatedMining(df_raw_dataset, df_dataset, ftr_names):
    # df_raw_dataset, df_dataset, ftr_names = loaderModule()

    print("Starting RFE...")
    dict_rfe = rfeModule(df_raw_dataset, ftr_names)
    print("-- RFE Finished --")
    print("")

    # Returns the filter list for each level (np_cross[type][level]
    # where level starts from 1 (subtracted when retrieved)
    print("Starting Filtering...")
    np_cross = filterModule(dict_rfe)
    print("-- Filtering Finished --")
    print("")

    print("Starting Cross Process...")
    dict_significant_results = crossProcessModule(df_dataset, np_cross)
    print("-- Cross Process Finished --")

    return dict_significant_results



