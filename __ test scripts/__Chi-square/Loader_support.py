

# For loadVarDesc()
import json  # For pretty print
import collections
from csv import reader

# For loadDataset()
import pandas as pd
import tabulate
from tabulate import tabulate


# For loadVarDesc()
ITEM_MARKER = "^"
FEAT_NAME = "Name"



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
                
                item = collections.OrderedDict()
                item[FEAT_NAME] = feat_name
                
                dict_varDesc[feat_code] = item

                # print(feat_code + " - " + feat_name)
                
            # If not New Entry, continue adding to Item
            else:
                feat_val = row[1].strip()  # Ex. In Gender, 1 or 2
                feat_eval = row[0].strip()  # Equivalent value (i.e. "a" or "b")
                item[feat_val] = feat_eval

                item_name = str(FEAT_NAME + feat_val)
                item[item_name] = row[2].strip()


                
        # printDictionary(dict_varDesc)
    return dict_varDesc


def loadDataset(path_dataset, dict_varDesc):
    # Load file as dataframe
    df_dataset = pd.read_csv(path_dataset)
    key = "b1"
    df_dataset[key] = df_dataset[key].replace([1, 2], ["a", "b"])
    print(df_dataset[key])
    # print(tabulate(df_dataset, headers = 'keys', tablefmt = 'psql'))

def printDictionary(oDict):
    print(json.dumps(oDict, indent = 4))















        
