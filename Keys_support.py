
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    Dataset key support for the original Manual
    Mining System.
    [Candy]
'''

# dataset keys
class Dataset:
    SAMPLES = 'Samples'
    CODE = 'Code'
    DESCRIPTION = 'Description'
    RESPONSES = 'Responses'
    GROUP = 'Group'
    FEATURE_LIST = 'FeatureList'

    def __init__(self):
        pass

# SSF keys
class SSF:
    FEATURES = "Features"
    FEAT_CODE = "Feature_Code"  # 'featureID' = [1, 3]
    FEAT_GROUP = "Feature_Group"  # 'featureID' = 'a'
    FEAT_GROUP_CODE = "Feature_Group_Code"  # 'featureID' = ('a', [1, 3])
    # GROUP_CODE = "Group_Code"  # 'a' = [1, 3]

    def __init__(self):
        pass
