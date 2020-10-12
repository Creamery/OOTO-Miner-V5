import collections
# Recursive Feature Elimination
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

MAX_RANK = 3


def performRFE(df_raw_dataset, ftr_names):
    # Convert DataFrame object to NumPy array for faster computation

    array = df_raw_dataset.values
    print(array)
    ftrCount = len(ftr_names)
    ftrEndIndex = ftrCount - 1

    X = array[:, 0:ftrEndIndex]
    Y = array[:, ftrEndIndex]

    # TODO (Future) Double check selected features
    model = LogisticRegression(solver = 'liblinear', multi_class = 'auto')  # or lbfgs or liblinear
    rfe = RFE(model, MAX_RANK)  # The second parameter is the number of top features to select
    fit = rfe.fit(X, Y)

    # for i in range(X.shape[1]):
    #     print('Column: %d, Selected %s, Rank: %.3f' % (i, rfe.support_[i], rfe.ranking_[i]))

    # print("Num Features: %s" % (fit.n_features_))
    # print("Selected Features: %s" % (fit.support_))
    # print("Feature Ranking: %s" % (fit.ranking_))
    # print("Feature Names: ")

    dict_rfe = prepareDictResult(ftr_names, fit.ranking_)
    print(dict_rfe)
    return dict_rfe


def prepareDictResult(ftr_names, feat_rank):
    dict_rfe = collections.OrderedDict()
    for i_rank in range(MAX_RANK):
        rank = i_rank + 1
        print("Rank " + str(rank))

        indices = [i for i, x in enumerate(feat_rank) if x == rank]
        print(indices)
        list_rank = []
        for index in indices:
            feat_code = ftr_names[index]
            list_rank.append(feat_code)
        dict_rfe[rank] = list_rank

        print(str(len(ftr_names)))
        print(str(len(feat_rank)))

    return dict_rfe








