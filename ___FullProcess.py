


import os
# Uploader support for converting read dataset
import Loader_support as LS
import RFE_support as RFES
import Filter_support as FILS
import CrossProcess_support as CPS

def loaderModule():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_input = str(dir_path + "\\_input\\")
    dir_output = str(dir_path + "\\_output\\")

    # Load Variable Description
    fln_varDesc = "Uniandes_VariableDescription (New).csv"
    path_varDesc = str(dir_input + fln_varDesc)
    dict_varDesc = LS.loadVarDesc(path_varDesc)


    # Load Dataset
    fln_dataset = "Uniandes_Dataset (New).csv"
    path_dataset = str(dir_input + fln_dataset)
    df_raw_dataset, df_dataset = LS.loadDataset(path_dataset, dict_varDesc)
    # LS.exportDataset(df_dataset, "Output.csv", dir_output)

    fln_ftrNames = "Uniandes_FeatureNames.csv"
    path_ftrNames = str(dir_input + fln_ftrNames)
    ftr_names = LS.loadFeatureNames(path_ftrNames)

    return df_raw_dataset, df_dataset, ftr_names

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




df_raw_dataset, df_dataset, ftr_names = loaderModule()

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



