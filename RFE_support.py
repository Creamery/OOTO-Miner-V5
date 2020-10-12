import collections
# Recursive Feature Elimination
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression




def performRFE(df_raw_dataset, ftr_name):
    # Convert DataFrame object to NumPy array for faster computation
    array = df_raw_dataset.values
    print(array)
    ftrCount = len(ftr_name)
    ftrEndIndex = ftrCount - 1

    X = array[:, 0:ftrEndIndex]
    Y = array[:, ftrEndIndex]

    model = LogisticRegression(solver = 'liblinear', multi_class = 'auto')  # or lbfgs or liblinear
    rfe = RFE(model, 3)  # The second parameter is the number of top features to select
    fit = rfe.fit(X, Y)

    for i in range(X.shape[1]):
        print('Column: %d, Selected %s, Rank: %.3f' % (i, rfe.support_[i], rfe.ranking_[i]))

    print("Num Features: %s" % (fit.n_features_))
    print("Selected Features: %s" % (fit.support_))
    print("Feature Ranking: %s" % (fit.ranking_))

    dict_rfe = collections.OrderedDict()

    return dict_rfe










