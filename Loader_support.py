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

# For loadDataset()
import pandas as pd


# For exports
import Filter_support as FILS
import ChiSquare_support as CHIS
import os
import errno

# For loadVarDesc()
ITEM_MARKER = "^"
FEAT_NAME = "Name"
OPTION_NAME = "OptionName"

# Paths
GL_OUTPUT_PATH = os.path.dirname(os.path.realpath(__file__)) + str("\\_output\\")

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

def exportDataset(df_dataset, filename, path = GL_OUTPUT_PATH):
    path_export = str(path + filename)
    df_dataset.to_csv(path_export, index = False, sep = ",")

def exportDataFrame(df_dataset, filename, path = GL_OUTPUT_PATH):
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
def exportChiSquareTable(df_output, filter, list_index = None, path = GL_OUTPUT_PATH):

    np_filters = FILS.extractFilter(filter)  # Returns an Numpy array of dictionaries per filter element

    str_filename = str("Result Table - CROSS")
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
            options = dict_filter[feat_code]

            i_option = 0
            len_options = len(options)
            for option in options:
                i_option = i_option + 1
                str_filename = str_filename + "[" + str(option)
                if isLastElement(i_option, len_options):
                    str_filename = str_filename + "]"
                else:
                    str_filename = str_filename + ", "

            # If last feat code, add .csv or VS?
            if isLastElement(i_feat_code, len_dict_filter):  # If last element in filter group
                if isLastElement(i_dict_filter, len_np_filters):  # Check first if it is the last element overall (i.e. last filter group)
                    str_filename = str_filename + ".csv"  # If yes, add .csv
                else:  # Else, add " VS "
                    str_filename = str_filename + " VS "

    print("Export: " + str_filename)
    print("")


    output_path = path + "\\Result Tables\\"
    checkDirectory(output_path)

    if list_index is not None:
        specific_path = output_path + "\\CROSS" + str_type + " LVL" + str_level + "\\"
        checkPath(specific_path)
        output_path = specific_path

    exportDataFrame(df_output, str_filename, output_path)
    return df_output

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

def checkPath(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def printDictionary(oDict):
    print(json.dumps(oDict, indent = 4))

def exportDictionary(dict_data, filename, path = GL_OUTPUT_PATH):
    print("Exported Dictionary")
    path_export = str(path + filename)
    with open(path_export, 'wb') as file:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(file, dict_data.keys())
        w.writeheader()
        w.writerow(dict_data)

def exportList(list_data, filename, path = GL_OUTPUT_PATH):
    path_export = str(path + filename)
    with open(path_export, 'wb') as file:
        wr = csv.writer(file, quoting = csv.QUOTE_ALL)
        wr.writerow(list_data)





