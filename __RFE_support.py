
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"

'''
    The RFE MODULE.
    Applies Recursive Feature Elimination (RFE) to the original dataset in
    order to extract the first set of SSFs.
    [Candy]
'''

import collections
from sklearn.feature_selection import RFE  # Recursive Feature Elimination
from sklearn.linear_model import LogisticRegression
import _UIConstants_support as UICS
from sklearn import datasets
import time


'''
    <!> ENTRY: The function called by the automated mining process.
    
    Returns a dictionary containing the Rankings as keys (1-3) and
    an array of the feature codes under that ranking.
'''
def performRFE(df_raw_dataset, ftr_names, pd_raw_dataset, controller):
    key = UICS.KEY_RFE_MODULE  # For progress bar

    # Convert DataFrame object to NumPy array for faster computation
    array = df_raw_dataset.values
    # print(array)
    # ftrCount = len(ftr_names)
    # ftrEndIndex = ftrCount - 1

    # X = array[:, 0:ftrEndIndex]
    # Y = array[:, ftrEndIndex]

    ftrCount = len(ftr_names)
    ftrEndIndex = ftrCount - 1

    X = array[:, 0:ftrCount]
    Y = array[:, ftrEndIndex]
    print(X)

    controller.updateModuleProgress(key, UICS.MODULE_INDICATOR + "Starting RFE MODULE")  # 1
    # time.sleep(0.01)

    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Extracting Features")  # 2
    # time.sleep(0.01)

    model = LogisticRegression(solver = 'liblinear', multi_class = 'auto')  # or lbfgs or liblinear
    # rfe = RFE(model, UICS.MAX_RANK)  # The second parameter is the number of top features to select
    rfe = RFE(model, UICS.MAX_RANK)  # The second parameter is the number of top features to select
    fit = rfe.fit(X, Y)

    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Successfully Extracted Features")  # 3
    # time.sleep(0.01)


    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Preparing RFE Results")  # 4
    # time.sleep(0.01)

    dict_rfe = prepareDictResult(ftr_names, fit.ranking_)
    print("Complete RFE Ranking")
    # print(fit.ranking_)

    # Summarize all features
    for i in range(X.shape[1]):
        # print('Column: %d, Feature:%s, Selected %s, Rank: %.3f' % (i, ftr_names[i], rfe.support_[i], rfe.ranking_[i]))
        print('Column: %d, Feature:%s, Rank: %.3f' % (i, ftr_names[i], rfe.ranking_[i]))
    # for i in range(len(fit.ranking_)):
    #     print("Rank " + str(i+1) + " | " + str(fit.ranking_[i]) + " | " + "Column: " + str(rfe.support_[i]))

    controller.updateModuleProgress(key, UICS.SUB_MODULE_INDICATOR + "Successfully Created Result Dictionary")  # 5
    # time.sleep(0.01)

    return dict_rfe


def prepareDictResult(ftr_names, feat_rank):
    dict_rfe = collections.OrderedDict()
    for i_rank in range(UICS.MAX_RANK):
        rank = i_rank + 1
        # print("Rank " + str(rank))

        indices = [i for i, x in enumerate(feat_rank) if x == rank]
        # print(indices)
        list_rank = []
        for index in indices:
            feat_code = ftr_names[index]
            list_rank.append(feat_code)
        dict_rfe[rank] = list_rank

        # print(str(len(ftr_names)))
        # print(str(len(feat_rank)))

    return dict_rfe








