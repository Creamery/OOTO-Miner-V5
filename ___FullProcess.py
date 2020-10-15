


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
    print("SSF0:")
    LS.printDictionary(dict_rfe)
    print("")
    # Takes the dictionary and converts it to the correct format for Crossing (e.g. ["b5:a", "b5:b"])
    extracted_cross_filters = FILS.extractCrossFilters(dict_rfe)

    # NOTE: CROSS is the collection of SSFs
    CROSS = FILS.processLVLs(extracted_cross_filters)  # Returns the filter list for each level

    # print(LVL)
    # print("")
    # print(CROSS[0][0])
    # print("")
    # print(CROSS[0][1])
    # print("")
    # print(CROSS[0][2])

    # cross_filters = CPS.crossFilters(SSF_0, 1)


    # for item in cross_filters:
    #     CPS.updateChecklist(item)
    # CPS.updateChecklist([["b5:a"], ["b1:b", "b1:a"]])
    # print(CPS.CHECKLIST)
    return CROSS

def crossProcessModule(df_dataset, np_CROSS):
    CPS.crossProcess(df_dataset, np_CROSS)











df_raw_dataset, df_dataset, ftr_names = loaderModule()

dict_rfe = rfeModule(df_raw_dataset, ftr_names)

# Returns the filter list for each level (np_cross[type][level]
# where level starts from 1 (subtracted when retrieved)
np_cross = filterModule(dict_rfe)

crossProcessModule(df_dataset, np_cross)



