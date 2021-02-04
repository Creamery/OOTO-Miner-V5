
import numpy as np
import collections
import __Loader_support as LS

class _Singleton:
    _instance = None

    dict_SSFs = None
    llistSSFs = []
    ctr_Accepted = 0
    time_run = 0
    total_depths = 0
    # Contents will be in the form of FN1 VS FN2 (i.e. 'b1 VS b2')
    npFeaturePairs = np.empty([0, 1], dtype = object)  # 0 rows, 1 column

    # Text outputs
    text_contextPerDepth = ""
    text_frequencyCounts = ""

    # Frerquency count variables
    freq_loaderModule = 0
    time_loaderModule = 0

    freq_rfeModule = 0
    time_rfeModule = 0

    freq_filterModule = 0
    time_filterModule = 0
    freqTotal_filterModule = 0
    timeTotal_filterModule = 0

    freq_crossProcessModule = 0
    time_crossProcessModule = 0
    freqSingleProcess_crossProcessModule = 0

    freqTotal_crossProcessModule = 0
    freqTotalSingleProcess_crossProcessModule = 0
    timeTotal_crossProcessModule = 0

    freq_chiSquareModule = 0
    time_chiSquareModule = 0

    freq_outputModule = 0
    time_outputModule = 0

    freq_total = 0  # Frequency regardless of module
    run_total = 0  # Run time regardless of module

    def resetSingleton(self):
        dict_SSFs = None
        llistSSFs = []
        ctr_Accepted = 0
        time_run = 0
        total_depths = 0
        # Contents will be in the form of FN1 VS FN2 (i.e. 'b1 VS b2')
        npFeaturePairs = np.empty([0, 1], dtype = object)  # 0 rows, 1 column

        # Text outputs
        text_contextPerDepth = ""
        text_frequencyCounts = ""
        # Frerquency count variables
        freq_loaderModule = 0
        time_loaderModule = 0

        freq_rfeModule = 0
        time_rfeModule = 0

        freq_filterModule = 0
        time_filterModule = 0

        freq_crossProcessModule = 0
        time_crossProcessModule = 0
        freqSingleProcess_crossProcessModule = 0

        freq_chiSquareModule = 0
        time_chiSquareModule = 0

        freq_outputModule = 0
        time_outputModule = 0

        freq_total = 0  # Frequency regardless of module
        run_total = 0  # Run time regardless of module

    def isConstantSSFs(self, listSSFs):
        if all(item in self.llistSSFs for item in listSSFs):  # Returns True if list 1 has all elements of list 2
            return True
        else:
            return False

    def updateDictSSFs(self, new_dict, curr_depth):
        print("Existing SSFs is:")
        print(self.dict_SSFs)
        print("")

        print("Inserting this dict to existing SSFs:")
        print(new_dict)
        print("")

        print("Current list SSFs:")
        print(self.llistSSFs)
        print("")

        if self.dict_SSFs is None:
            self.dict_SSFs = new_dict
            for key, value in self.dict_SSFs.items():
                self.llistSSFs.extend(value)

        else:
            for key in new_dict.keys():

                if key in self.dict_SSFs.keys():
                    newList = new_dict[key]
                    cleanNewList = [x for x in newList if x not in self.llistSSFs]
                    self.llistSSFs.extend(cleanNewList)  # Add the contents of the new list to the entire list of SSFs

                    # Merge the two lists
                    mergedList = self.dict_SSFs[key] + cleanNewList
                    # Remove duplicates via Set
                    uniqueList = list(set(mergedList))
                    uniqueList.sort()

                    self.dict_SSFs[key] = uniqueList

                else:
                    newList = new_dict[key]
                    newList.sort()
                    cleanList = [x for x in newList if x not in self.llistSSFs]
                    self.llistSSFs.extend(cleanList)  # Add the contents of the new list to the entire list of SSFs
                    self.dict_SSFs[key] = cleanList  # newList

        print("New SSFs are:")
        print(self.dict_SSFs)
        self.updateContextPerDepthText(self.dict_SSFs, curr_depth)


    def updateContextPerDepthText(self, currDictContextFeatures, depth):
        self.text_contextPerDepth = self.text_contextPerDepth + "DEPTH " + str(depth) + "\n"
        for key, value in currDictContextFeatures.items():
            strList = self.convertListToString(value)
            text = str(key) + ": " + strList + "\n"
            self.text_contextPerDepth = self.text_contextPerDepth + text

        self.text_contextPerDepth = self.text_contextPerDepth + "\n\n"  # Add spaces for next entry

    def convertListToString(self, inputList):
        str_output = ""
        list_delimiter = ", "
        len_list_delimiter = len(list_delimiter)

        for element in inputList:
            str_output = str_output + str(element) + list_delimiter

        str_output = str_output[:-len_list_delimiter]  # Remove the last occurrence of ", "
        return str_output

    def getDictSSFs(self):
        return self.dict_SSFs

    def getLlSSFs(self):
        return self.llistSSFs


    def printAllTextData(self):

        self.printContextFeaturesPerDepth()
        self.printSalientFeaturesText()  # Print the complete SSF list regardless of depth
        self.printFrequencyCountsText()

    def printContextFeaturesPerDepth(self, filename = "LOG - Context Features Per Depth"):
        LS.exportTextFile(filename, self.text_contextPerDepth)

    def printSalientFeaturesText(self, filename = "LOG - All Salient Features"):
        text_data = ""
        for feature in self.llistSSFs:
            text_data = text_data + str(feature) + "\n"
        LS.exportTextFile(filename, text_data)

    def printFrequencyCountsText(self, filename = "LOG - Frequency Counts Per Module"):
        text_data = "\n"
        text_data = text_data + "Loader Module Summary\n"
        text_data = text_data + "\tFrequency: " + str(self.freq_loaderModule) + "\n"
        text_data = text_data + "\tTime: " + str(self.time_loaderModule) + " seconds\n\n"

        text_data = text_data + "Filter Module Summary\n"
        text_data = text_data + "\tTotal Frequency: " + str(self.freqTotal_filterModule) + "\n"
        text_data = text_data + "\tTotal Time: " + str(self.timeTotal_filterModule) + " seconds\n\n"

        text_data = text_data + "Cross Process Module Summary\n"
        text_data = text_data + "\tTotal Frequency: " + str(self.freqTotal_crossProcessModule) + "\n"
        text_data = text_data + "\tTotal Highest Frequency for a Single Process: " + str(self.freqTotalSingleProcess_crossProcessModule) + "\n"
        text_data = text_data + "\tTotal Time: " + str(self.timeTotal_crossProcessModule) + " seconds\n\n"


        text_data = text_data + "\n\nCross Process Module by Depth\n"
        text_data = text_data + self.text_frequencyCounts

        LS.exportTextFile(filename, text_data)



    def updateFrequencyCountsText(self, curr_depth):
        text_data = "\tDepth " + str(curr_depth) + "\n"

        text_data = text_data + "\t\tFilter Module\n"
        text_data = text_data + "\t\t\tFrequency: " + str(self.freq_filterModule) + "\n"
        text_data = text_data + "\t\t\tTime: " + str(self.time_filterModule) + " seconds\n\n"


        text_data = text_data + "\t\tCross Process Module\n"
        text_data = text_data + "\t\t\tFrequency: " + str(self.freq_crossProcessModule) + "\n"
        text_data = text_data + "\t\t\tHighest Single Process Frequency: " + str(self.freqSingleProcess_crossProcessModule) + "\n"
        text_data = text_data + "\t\t\tTime: " + str(self.time_crossProcessModule) + " seconds\n\n\n"

        self.text_frequencyCounts = self.text_frequencyCounts + text_data

        # Add values to constant variables to get totals
        self.freqTotal_filterModule = self.freqTotal_filterModule + self.freq_filterModule
        self.timeTotal_filterModule = self.timeTotal_filterModule + self.time_filterModule

        self.freqTotal_crossProcessModule = self.freqTotal_crossProcessModule + self.freq_crossProcessModule
        self.freqTotalSingleProcess_crossProcessModule = self.freqTotalSingleProcess_crossProcessModule + self.freqSingleProcess_crossProcessModule
        self.timeTotal_crossProcessModule = self.timeTotal_crossProcessModule + self.time_crossProcessModule

    def updateFrequency_LoaderModule(self, frequency_count, run_time):
        self.freq_loaderModule = frequency_count
        self.time_loaderModule = run_time

    def updateFrequency_RfeModule(self, frequency_count, run_time):
        self.freq_rfeModule = frequency_count
        self.time_rfeModule = run_time

    def updateFrequency_FilterModule(self, frequency_count, run_time):
        self.freq_filterModule = frequency_count
        self.time_filterModule = run_time

    def updateFrequency_CrossProcessModule(self, frequency_count, highest_process_frequency, run_time):
        self.freq_crossProcessModule = frequency_count
        self.freqSingleProcess_crossProcessModule = highest_process_frequency  # The highest frequency by a single process
        self.time_crossProcessModule = run_time

    def updateFrequency_ChiSquareModule(self, frequency_count, run_time):
        self.freq_chiSquareModule = frequency_count
        self.time_chiSquareModule = run_time

    def updateFrequency_OutputModule(self, frequency_count, run_time):
        self.freq_outputModule = frequency_count
        self.time_outputModule = run_time




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


