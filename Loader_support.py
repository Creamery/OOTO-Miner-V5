__author__ = ["Candy Espulgar"]

__copyright__ = "Copyright 2020, TE3D House | 2020, Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga | Neil Buckley"]
__version__ = "3.0"

# For loadVarDesc()
import json  # For pretty print
import collections
import csv
from csv import reader
import numpy as np
import pickle
import time

# For loadDataset()
import pandas as pd
import os
import errno


# For exports
import Filter_support as FILS
import ChiSquare_support as CHIS
import UIConstants_support as UICS

# For loadVarDesc()
ITEM_MARKER = "^"
FEAT_NAME = "Name"
OPTION_NAME = "OptionName"

# Paths
GL_AM_INPUT_PATH = os.path.dirname(os.path.realpath(__file__)) + str("\\_input\\")
GL_AM_OUTPUT_PATH = os.path.dirname(os.path.realpath(__file__)) + str("\\_output\\AM\\")
GL_MM_OUTPUT_PATH = os.path.dirname(os.path.realpath(__file__)) + str("\\_output\\MM\\")
PICKLE_TITLE_NAME = "Pickle Result - "

# NOTE: Arrays start at 0
def loadVarDesc(path_variableDesc):
    dict_varDesc = collections.OrderedDict()

    # Open file in read mode
    with open(path_variableDesc, "r") as obj_varDesc:
        read_varDesc = reader(obj_varDesc)
        
        for row in read_varDesc:
            row_id = row[0].strip()

        
            # Create a new dict entry if you see the Item Marker (^)
            if row_id == ITEM_MARKER:
                
                feat_code = row[1].strip()
                feat_name = row[2].strip()
                
                item = collections.OrderedDict()  # The item values/options, i.e. 1, 2
                dict_option_names = collections.OrderedDict()  # The option names, i.e. "Mostly True"

                item[FEAT_NAME] = feat_name
                item[OPTION_NAME] = dict_option_names

                dict_varDesc[feat_code] = item

                # print(feat_code + " - " + feat_name)
                
            # If not New Entry, continue adding to Item
            else:
                feat_val = row[1].strip()  # Ex. In Gender, 1 or 2
                feat_eval = row[0].strip()  # Equivalent value (i.e. "a" or "b")
                item[feat_val] = feat_eval

                dict_option_names[feat_val] = row[2].strip()

        # printDictionary(dict_option_names)
    return dict_varDesc

'''
Loads the dataset and makes necessary replacements according
to the Variable Description File.
'''
def loadDataset(path_dataset, dict_varDesc):
    # Load file as dataframe
    df_dataset = pd.read_csv(path_dataset)
    df_raw_dataset = df_dataset.copy(deep = True)
    # printDictionary(dict_varDesc)

    # Replace each column value with their equivalent letter based on dict_varDesc (Variable Description File)
    for feat_code, feat_dict in dict_varDesc.items():
        item = dict_varDesc[feat_code]  # For each entry in dict_varDesc
        option_values = []  # Will hold the original option values in the dataset
        option_new_values = []  # Will hold the values to replace the options

        for item_code, item_value in item.items():  # Parse each key and value in that item
            if item_code != FEAT_NAME and item_code != OPTION_NAME:  # If the key does not contain "Name", replace the dataset values
                option_values.append(int(item_code))
                option_new_values.append(item[item_code])  # The value that the option should be. i.e "a"

        df_dataset[feat_code] = df_dataset[feat_code].replace(option_values, option_new_values)
        # df_dataset[key] = df_dataset[key].replace([1, 2], ["a", "b"])

    # print(df_dataset[key])

    return df_raw_dataset, df_dataset

def loadFeatureNames(path_FeatureNames):
    file = open(path_FeatureNames, 'rt')
    ftr_names = file.read()
    ftr_names = ftr_names.strip().split(',')
    return ftr_names

def exportDataset(df_dataset, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + filename)
    df_dataset.to_csv(path_export, index = False, sep = ",")

def exportDataFrame(df_dataset, filename, path = GL_AM_OUTPUT_PATH):
    # print("Export Dataframe")
    path_export = str(path + filename)
    df_dataset.to_csv(path_export, index = False, sep = ",")



'''
    Prints the Chi-square dictionary results. Makes the necessary
    adjustments so that it will properly display in CSV.
    
    The 2nd parameter is a single filter (with 2 filter elements).
    Filename is extracted within the function.
    
    The 3rd parameter contains the [type, level] value used for the filename.
    This function exports the Chi-square Result Table.
    
'''
def exportChiSquareTable(df_output, filter, list_index = None, path = GL_AM_OUTPUT_PATH):

    np_filters = FILS.extractFilter(filter)  # Returns an Numpy array of dictionaries per filter element
    # print(np_filters)
    # print("")
    str_filename = str("Result Table - CROSS")
    str_pair_name = ""

    if list_index is not None:
        i_type = list_index[0]
        i_level = list_index[1] + 1
        str_type = str("[" + str(i_type) + "]")
        str_level = str("[" + str(i_level)+ "]")

        str_filename = str_filename + str_type  # Add [type] to filename
        str_filename = str_filename + str_level + " - "  # Add [level] to filename

    i_dict_filter = 0
    for dict_filter in np_filters:

        i_feat_code = 0
        len_dict_filter = len(dict_filter)

        i_dict_filter = i_dict_filter + 1
        len_np_filters = len(np_filters)
        for feat_code in dict_filter:
            i_feat_code = i_feat_code + 1
            str_filename = str_filename + (str(feat_code))
            str_pair_name = str_pair_name + str(feat_code)
            options = dict_filter[feat_code]

            i_option = 0
            len_options = len(options)
            for option in options:
                i_option = i_option + 1
                str_filename = str_filename + "[" + str(option)
                str_pair_name = str_pair_name + "(" + str(option)
                if isLastElement(i_option, len_options):
                    str_filename = str_filename + "]"
                    str_pair_name = str_pair_name + ")"
                else:
                    str_filename = str_filename + ", "
                    str_pair_name = str_pair_name + ", "

            # If last feat code, add .csv or VS?
            if isLastElement(i_feat_code, len_dict_filter):  # If last element in filter group
                if isLastElement(i_dict_filter, len_np_filters):  # Check first if it is the last element overall (i.e. last filter group)
                    str_filename = str_filename + ".csv"  # If yes, add .csv
                else:  # Else, add " VS "
                    str_filename = str_filename + UICS.STRING_VS
                    str_pair_name = str_pair_name + UICS.STRING_VS


    # print("Export: " + str_filename)
    # print("")


    output_path = path + "\\Result Tables\\"
    checkDirectory(output_path)

    if list_index is not None:
        specific_path = output_path + "\\CROSS" + str_type + " LVL" + str_level + "\\"
        checkPath(specific_path)
        output_path = specific_path

    exportDataFrame(df_output, str_filename, output_path)
    return df_output, str_pair_name

'''
    The final output call made by the OUTPUT MODULE. It exports the recorded
    result tables as excel files separated by CROSS[type][level].
    
    It also outputs a single pickle file that consolidates all significant
    feature code comparisons.
'''
def exportOutputModuleResults(dict_result_table_sig, len_cross_datasets, len_cross_types, controller):
    key = UICS.KEY_OUTPUT_MODULE
    controller.updateModuleProgress(key, UICS.MODULE_INDICATOR + "Starting OUTPUT MODULE")  # 1
    time.sleep(0.01)
    controller.updateModuleProgress(key,  UICS.SUB_MODULE_INDICATOR + "Exporting UI Results")  # 2

    exportUIResultDictionary(dict_result_table_sig, "UI Result")
    controller.updateModuleProgress(key,  UICS.SUB_MODULE_INDICATOR + "Successfully Exported UI Results")  # 3
    time.sleep(0.01)

    str_pickle_filename = PICKLE_TITLE_NAME = "CROSS[" + str(len_cross_datasets - 1) + "][" + str(len_cross_types) + "]"

    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Creating Pickle Save File")  # 4
    time.sleep(0.01)

    exportPickleResultDictionary(dict_result_table_sig, str_pickle_filename)
    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Successfully Created Pickle Save File")  # 5
    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "File Saved as \"" + str_pickle_filename + "\"")  # 6
    time.sleep(0.01)

    controller.updateModuleProgress(100, UICS.FIRST_MESSAGE_SPACE + "[ Finished Automated OOTO Miner] ")  # 1
    # loaded_pickle = LS.loadPickleResultDictionary(str_pickle_filename)
    # print(loaded_pickle.keys())


def addToDictionaryResult(dict_result, key, value):
    if key not in dict_result.keys():
        dict_result[key] = value

    return dict_result

def isLastElement(index, length):
    if index == length:
        return True
    else:
        return False

def checkDirectory(output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        try:
            os.makedirs(os.path.dirname(output_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def checkDirectoryExistence(output_path):
    if not os.path.exists(os.path.dirname(output_path)):  # If path does not exist, return false
        try:
            return False
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    else:
        return True  # Else return true

def checkPath(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def printDictionary(oDict):
    print(json.dumps(oDict, indent = 4))

def exportDictionary(dict_data, filename, path = GL_AM_OUTPUT_PATH):
    print("Exported Dictionary")
    path_export = str(path + filename)
    with open(path_export, 'wb') as file:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(file, dict_data.keys())
        w.writeheader()
        w.writerow(dict_data)

def exportList(list_data, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + filename)
    with open(path_export, 'wb') as file:
        wr = csv.writer(file, quoting = csv.QUOTE_ALL)
        wr.writerow(list_data)

def exportSSFs(list_ssfs, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + "\\SSFs\\")
    checkDirectory(path_export)
    path_export = path_export + filename
    with open(path_export, 'wb') as file:
        for feat_code in list_ssfs:
            file.write(str(feat_code) + "\n")


def export2DList(list_ssfs, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + filename)
    with open(path_export, 'wb') as file:
        writer = csv.writer(file)
        for i in list_ssfs:
            writer.writerows(i)


def exportUIResultDictionary(dict_results, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + "UI Results\\")
    checkDirectory(path_export)
    path_export = path_export + filename
    for df_name, df in dict_results.items():
        if df is not None:
            final_path = path_export + " - " + df_name + ".xlsx"
            df.to_excel(final_path)

def exportPickleResultDictionary(dict_results, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + "Pickle Results\\")
    checkDirectory(path_export)
    path_export = path_export + filename
    path_export = path_export.replace("\\", "/")
    with open(path_export + '.pkl', 'wb') as file:
        pickle.dump(dict_results, file, pickle.HIGHEST_PROTOCOL)


def checkPickleFileExistence(filename, path = GL_AM_OUTPUT_PATH):
    path_import = str(path + "Pickle Results\\")
    if checkDirectoryExistence(path_import):  # Check directory existence
        path_import = path_import + filename + ".pkl"
        path_import = path_import.replace("\\", "/")
        print(path_import)

        return os.path.isfile(path_import)  # Check file existence
        # return checkDirectoryExistence(path_import)
    return False



def loadPickleResultDictionary(filename, path = GL_AM_OUTPUT_PATH):
    path_import = str(path + "Pickle Results\\")
    checkDirectoryExistence(path_import)
    path_import = path_import + filename
    path_import = path_import.replace("\\", "/")

    with open(path_import + '.pkl', 'rb') as file:
        return pickle.load(file)


def loadInput(path_varDesc = None, path_dataset = None, path_ftrNames = None):
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # dir_input = str(dir_path + "\\_input\\")
    # dir_output = str(dir_path + "\\_output\\")

    # Load Variable Description
    if path_varDesc is None:
        fln_varDesc = "Uniandes_VariableDescription (New).csv"
        path_varDesc = str(GL_AM_INPUT_PATH + fln_varDesc)

    dict_varDesc = loadVarDesc(path_varDesc)


    # Load Dataset
    if path_dataset is None:
        fln_dataset = "Uniandes_Dataset (New).csv"
        path_dataset = str(GL_AM_INPUT_PATH + fln_dataset)
    df_raw_dataset, df_dataset = loadDataset(path_dataset, dict_varDesc)
    # LS.exportDataset(df_dataset, "Output.csv", dir_output)

    if path_ftrNames is None:
        fln_ftrNames = "Uniandes_FeatureNames.csv"
        path_ftrNames = str(GL_AM_INPUT_PATH + fln_ftrNames)
    ftr_names = loadFeatureNames(path_ftrNames)

    return df_raw_dataset, df_dataset, ftr_names







