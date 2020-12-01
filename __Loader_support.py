
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    This script handles all LOADER MODULE functions.
    It loads data from the _input and _output folders.
    
    The OUTPUT MODULE is integrated in this script as well
    (through export functions). This module exports to destinations
    within the _output folder.
    [Candy]
'''

import tkinter.messagebox as tkMessageBox

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
import glob
import os
import errno

# For exports
import __Filter_support as FILS
import _ChiSquare_support as CHIS
import _UIConstants_support as UICS

# For loadVarDesc()
ITEM_MARKER = "^"
FEAT_NAME = "Name"
OPTION_NAME = "OptionName"

# For loadSSFs()
import glob

# Paths

GL_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
GL_AM_INPUT_PATH = os.path.dirname(os.path.realpath(__file__)) + str("\\_input\\")
GL_AM_OUTPUT_PATH = os.path.dirname(os.path.realpath(__file__)) + str("\\_output\\AM\\")
GL_AM_EXCEL_OUTPUT_PATH = os.path.dirname(os.path.realpath(__file__)) + str("\\_output\\AM\\UI Results\\")
GL_AM_EXCEL_FOLDER_NAME = str("UI Results")
GL_MM_OUTPUT_PATH = os.path.dirname(os.path.realpath(__file__)) + str("\\_output\\MM\\")
PICKLE_TITLE_NAME = "Pickle Result - "

RESULT_COLNAMES = ["Feature", "DoF", "P Value", "Chi Square", "Observed", "Expected", "IsSignificant"]

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
        exportDataset(df_dataset, "Converted Dataset.csv")

    # print(df_dataset[key])

    return df_raw_dataset, df_dataset

def loadFeatureNames(path_FeatureNames):
    file = open(path_FeatureNames, 'rt')
    ftr_names = file.read()
    ftr_names = ftr_names.strip().split(',')
    return ftr_names

def exportDataset(df_dataset, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + filename)
    checkDirectory(path_export)
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
    checkDirectory(path_export)
    with open(path_export, 'w') as file:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(file, dict_data.keys())
        w.writeheader()
        w.writerow(dict_data)

def exportList(list_data, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + filename)
    with open(path_export, 'w') as file:
        wr = csv.writer(file, quoting = csv.QUOTE_ALL)
        wr.writerow(list_data)

def exportSSFs(list_ssfs, filename, depth, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + "\\" + UICS.STRING_SSFS_FOLDER + str(depth) +"\\")
    checkDirectory(path_export)
    path_export = path_export + filename
    with open(path_export, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerows(list_ssfs)

'''
    Loads the folder containing all SSF CSV files and
    concatenates the contents into a dataframe with
    columns of [feature, chi].
    
    It also sorts the dataframe contents by the chi
    column values.
'''
def loadSSFs(foldername, path = GL_AM_OUTPUT_PATH):
    path = str(path + "\\" + foldername +"\\")
    checkDirectoryExistence(path)

    # Get all CSV filenames in folder
    csv_filenames = glob.glob(path + "/*.csv")
    df_result = None

    for name in csv_filenames:
        if df_result is None:
            df_result = pd.read_csv(name, header = None, usecols = [0, 1], names=["feature", "chi"])
        else:
            df = pd.read_csv(name, header = None, usecols = [0, 1], names=["feature", "chi"])
            pd.concat([df_result, df])

    df_result = df_result.sort_values(["chi"], ascending = (False))
    return df_result

def export2DList(list_ssfs, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + filename)
    with open(path_export, 'w') as file:
        writer = csv.writer(file)
        for i in list_ssfs:
            writer.writerows(i)


def exportUIResultDictionary(dict_results, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + "UI Results\\")
    checkDirectory(path_export)
    path_export = path_export + filename
    for df_name, df in dict_results.items():
        if df is not None:
            final_path = path_export + " - " + df_name + ".csv"
            df.to_csv(final_path)

def exportPickleResultDictionary(dict_results, filename, path = GL_AM_OUTPUT_PATH):
    path_export = str(path + "Pickle Results\\")
    checkDirectory(path_export)
    path_export = path_export + filename
    path_export = path_export.replace("\\", "/")
    with open(path_export + '.pkl', 'wb') as file:
        pickle.dump(dict_results, file, pickle.HIGHEST_PROTOCOL)


def checkExcelFileExistence(filename, path = GL_AM_OUTPUT_PATH):
    path_import = str(path + filename)
    if checkDirectoryExistence(path_import):  # Check directory existence
        return True
    return False

def checkCSVFileExistence(filename, path = GL_AM_OUTPUT_PATH):
    path_import = str(path + filename)
    if checkDirectoryExistence(path_import):  # Check directory existence
        return True
    return False

def checkCSVFileExistence(full_path):
    if checkDirectoryExistence(full_path):  # Check directory existence
        return True
    return False

def loadCSVResultDictionary(filename = "UI Results\\", path = GL_AM_OUTPUT_PATH):
    # path_import = str(path + "Pickle Results\\")
    path_import = str(path + filename)
    checkDirectoryExistence(path_import)

    excelFiles = glob.glob(path_import + "*.csv")
    dict_output = collections.OrderedDict(())
    for excelFile in excelFiles:
        with open(excelFile, mode = 'r') as infile:

            key = os.path.splitext(os.path.basename(excelFile))[0]
            key = key.replace("UI Result - ", "")
            dict_table = collections.OrderedDict()

            reader = csv.reader(infile)
            i_row = 0
            ref_row = None  # The row reference for keys
            for row in reader:
                if i_row is not 0:  # Skip the first row since its the feature names
                    i_column = 0
                    for value in row:
                        dict_table[ref_row[i_column]].append(value)
                        i_column = i_column + 1

                else:  # This initializes the table keys using row 0's values
                    i_value = 0
                    for value in row:
                        dict_table[value.strip()] = []
                        i_value = i_value + 1
                    ref_row = row
                i_row = i_row + 1

            dict_output[key] = dict_table

    return dict_output



def loadInput():

    # Load Variable Description
    path_varDesc = UICS.PATH_VARDESC
    if UICS.PATH_VARDESC is None:
        fln_varDesc = "Uniandes_VariableDescription (New).csv"
        path_varDesc = str(GL_AM_INPUT_PATH + fln_varDesc)
    dict_varDesc = loadVarDesc(path_varDesc)

    # Load Dataset
    path_dataset = UICS.PATH_DATASET
    if UICS.PATH_DATASET is None:
        fln_dataset = "Uniandes_Dataset (New).csv"
        path_dataset = str(GL_AM_INPUT_PATH + fln_dataset)
    df_raw_dataset, df_dataset = loadDataset(path_dataset, dict_varDesc)
    # LS.exportDataset(df_dataset, "Output.csv", dir_output)

    # Load Feature Names
    path_ftr_names = UICS.PATH_FTRNAMES
    if path_ftr_names is None:
        path_ftr_names = locateFeatureNamesFile(path_dataset)

    # if not checkCSVFileExistence(path_ftr_names):  # If file does not exist, show an error message
    #     tkMessageBox.showerror("FEATURE NAMES FILE NOT FOUND", "Please make sure that the file you entered is correct.")

    ftr_names = loadFeatureNames(path_ftr_names)

    return df_raw_dataset, df_dataset, ftr_names

'''
    Attempts to locate the missing feature names file by searching the assumed values.
'''
def locateFeatureNamesFile(path_dataset):
    # Try to find the file by assuming it is the dataset name + "_FeatureNames"
    file_name = path_dataset.split("/")
    i_end_file_name = len(file_name) - 1
    file_name = file_name[i_end_file_name][:-4]
    # The feature names file is assumed to be the dataset name + "_FeatureNames
    ftr_file_path = file_name + "_FeatureNames.csv"

    # if not checkCSVFileExistence(ftr_file_path):  # If the assumed name still doesn't exist
    #     fln_ftrNames = "Uniandes_FeatureNames.csv"
    #     path_ftrNames = str(GL_AM_INPUT_PATH + fln_ftrNames)

    return ftr_file_path



