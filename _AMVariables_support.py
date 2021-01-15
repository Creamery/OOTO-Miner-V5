
import numpy as np

class _Singleton:
    _instance = None
    llistSSFs = []
    ctr_Accepted = 0
    time_run = 0
    total_depths = 0

    # Contents will be in the form of FN1 VS FN2 (i.e. 'b1 VS b2')
    npFeaturePairs = np.empty([0, 1], dtype = object)  # 0 rows, 1 column

    def updateSSFsList(self, input):
        self.llistSSFs.append(input)

    def getLlSSFs(self):
        return self.llistSSFs

    def updateFeaturePairs(self, llFeature_pair):
        str_featPair = self.convertPairToString(llFeature_pair)
        # print(str_featPair)
        self.npFeaturePairs = np.append(self.npFeaturePairs, np.array([[str_featPair]]), axis = 0)

    '''
        This function returns true if the list of features
        have been paired before.
    '''
    def isFeaturePairParsed(self, llFeature_pair):
        str_pair = self.convertPairToString(llFeature_pair)
        if str_pair in self.npFeaturePairs[:, 0]:  # Go through all the rows of the first column and check if the string exists
            # print(str(str_pair) + " is here.")
            return True
        return False

    def getFeaturePairs(self):
        return self.npFeaturePairs

    '''
        llFeature_pair takes the form of [[pair_1], [pair_2]] (or a cross), where
        pairs 1 and 2 are the number of features that a dataset is filtered
        with.
        
        The features within a pair have an option attached (i.e. b1:a).
    '''
    def convertPairToString(self, llFeature_pair):
        feat_sep = "|"
        len_feat_sep = len(feat_sep)

        pair_sep = " VS "
        len_pair_sep = len(pair_sep)

        str_pairs = ""

        # Concatenate the features in the form of: b1:a|b2:a|b3:a VS c1:a|c2:a|c3:a
        for pair in llFeature_pair:  # For each item in a feature pair, do the following:

            str_feat = ""
            for feat in pair:  # For each element in a pair, separate it with feat_sep (|)
                str_feat = str_feat + str(feat) + feat_sep

            str_feat = str_feat[:-len_feat_sep]  # Remove the last occurrence of '|'
            str_pairs = str_pairs + str_feat + pair_sep

        str_featPair = str_pairs[:-len_pair_sep]  # Remove the last occurrence of ' VS '
        return str_featPair

    def addCtrAccepted(self):
        self.ctr_Accepted = self.ctr_Accepted + 1

    def resetCtrAccepted(self):
        self.ctr_Accepted = 0

    def getCtrAccepted(self):
        return self.ctr_Accepted

    def updateTime(self, new_time_set):
        self.time_run = self.time_run + new_time_set

    def getTime(self):
        return self.time_run

    def resetTime(self):
        self.time_run = 0

    def setDepths(self, depths):
        self.total_depths = depths

    def getDepths(self):
        return self.total_depths

    def resetDepths(self):
        self.total_depths = 0


def getSingleton():
    if _Singleton._instance is None:
        _Singleton._instance = _Singleton()
    return _Singleton._instance


