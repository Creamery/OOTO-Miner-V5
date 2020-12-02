
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019, 2021 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    This script provides functions relating to
    depth processing.
    [Candy]
'''
import collections
import numpy as np

import __Loader_support as LS
import _UIConstants_support as UICS

def loadPreviousSSFs(depth):
    foldername = UICS.STRING_SSFS_FOLDER + str(depth)
    df_SSFs = LS.loadSSFs(foldername)
    # print(df_SSFs)

    # Partition the extracted SSFs to 3 Ranks
    dict_ranked_ssfs = rankSSFs(df_SSFs)
    # print(dict_ranked_ssfs)

    return dict_ranked_ssfs

def rankSSFs(df_SSFs):
    col_feat = UICS.COL_SSFS_FEAT
    col_chi = UICS.COL_SSFS_CHI

    df_chi = df_SSFs[col_chi]
    list_chi = df_chi.values.tolist()
    # Create and initialize a dictionary of ranked SSFs
    dict_ranked_ssfs = collections.OrderedDict()
    dict_ranked_ssfs[1] = []  # There are better, extendable ways to do this, but
    dict_ranked_ssfs[2] = []  # the program really requires just 3 ranks
    dict_ranked_ssfs[3] = []

    cutoff_rank1 = np.percentile(list_chi, UICS.SSF_PERCENTILE_2)  # Rank 1 should have the higher set of chi values
    cutoff_rank2 = np.percentile(list_chi, UICS.SSF_PERCENTILE_1)

    for index in df_chi.index:
        feat = df_SSFs[col_feat][index]
        chi = df_SSFs[col_chi][index]

        # Check which percentile it belongs
        if chi >= cutoff_rank1:  # Append to Rank 1
            dict_ranked_ssfs[1].append(feat)
            # print(feat + " " + str(chi))

        elif chi >= cutoff_rank2:  # Append to Rank 2
            dict_ranked_ssfs[2].append(feat)

        else:  # Everything else, append to Rank 3
            dict_ranked_ssfs[3].append(feat)

    return dict_ranked_ssfs

