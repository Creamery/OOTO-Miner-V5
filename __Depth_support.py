
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
    col_feat = UICS.COL_SSFS_FEAT
    col_chi = UICS.COL_SSFS_CHI

    df_chi = df_SSFs[col_chi]
    list_chi = df_chi.values.tolist()
    len_list = len(list_chi)
    # print(list_chi)

    percentile = 0.333
    for index in df_chi.index:
        feat = df_SSFs[col_feat][index]
        chi = df_SSFs[col_chi][index]

        # i_chi = list_chi.index(chi)  # The index of the current chi value
        if chi > list_chi[int(len_list * percentile)]:
            print(feat + " " + str(chi))
        # Check which percentile it belongs

    return df_SSFs




