import pandas as pd

# For loadVarDesc()
import json  # For pretty print
import collections
from csv import reader


# For load() types
TYPE_VARDESC = 1
TYPE_DATASET = 2

# For loadVarDesc()
ITEM_MARKER = "^"
FEAT_NAME = "Name"


def load(load_type, path):
    if(load_type == TYPE_VARDESC):
        loadVarDesc(path)
    else:
        print("ERROR: TYPE_VARDESC Not Found")


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


                
        printDictionary(dict_varDesc)
    return dict_varDesc


def printDictionary(oDict):
    print(json.dumps(oDict, indent = 4))


# REMOVE    
def readFeatures(variableDescription, itemMarker):
        
    global features_gl
    features_gl = FS.readFeatures(variableDescription, itemMarker)
    if (len(features_gl)) <= 0: # Invalid variable description file
        return False
    else:
        return True

        
