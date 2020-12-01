
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019, 2021 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    This script provides functions relating to
    depth processing.
    [Candy]
'''

import __Loader_support as LS
import _UIConstants_support as UICS

def loadPreviousSSFs(depth):
    foldername = UICS.STRING_SSFS_FOLDER + str(depth)
    df_SSFs = LS.loadSSFs(foldername)

    print(df_SSFs)

    return df_SSFs




