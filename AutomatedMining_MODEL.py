
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"

'''
    This script is referenced by the AutomatedMining_View
    to know what data to show.
    [Candy]
'''


try:
    from Tkinter import *
except ImportError:
    from _tkinter import *

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

from collections import OrderedDict
import copy
import Function_support as FS
from Keys_support import Dataset as KSD
import _Widget_support as WS
import _MODULE_SystematicFiltering as SF
import Pandas_support as PS


class AutomatedMining_Model:

    def __init__(self):
        self.viewModel = ViewModel()

        self.isProcessing = False
        self.winProgressBar = None
        self.pbProgressBar = None
        self.AMController = None
        self.__systematicFiltering = None

        self.__resetFeatureDescription()
        self.__resetDatasets()

    def readFeatures(self, features):
        self.__resetFeatureDescription()
        self.__setFeatureDescriptionRaw(features)
        for feature in features:
            code = feature[KSD.CODE]
            description = feature[KSD.DESCRIPTION]
            responses = feature[KSD.RESPONSES]
            dictResponses = self.__parseResponses(responses)


            featureDescription = {KSD.DESCRIPTION: description, KSD.RESPONSES: dictResponses}
            self.getFeatureDescription()[code] = featureDescription

        # formally set feature description to sort alphabetically
        self.__setFeatureDescription(self.getFeatureDescription())

    """
    Feature names for pandas data frame
    """
    def readFeatureNames(self, features):
        featureNames = [dItem[KSD.CODE] for dItem in features]
        self.__setFeatureNames(featureNames)
        print("FEATURE Names----")
        print(self.getFeatureNames())
        print(type(self.getFeatureNames()))

    """
    Changes the format of responses to a dictionary of the form :
    { 'a': { 'Code': [], 'Description': [] } }
    """

    def __parseResponses(self, responses):
        dictResponses = {}

        for response in responses:
            group = response[KSD.GROUP]
            if not(str(group).strip() == '-1'):
                code = response[KSD.CODE]
                description = response[KSD.DESCRIPTION]


                entry = dictResponses.setdefault(group, OrderedDict({KSD.CODE: [], KSD.DESCRIPTION: []}))
                entry[KSD.CODE].append(code)
                entry[KSD.DESCRIPTION].append(description)

        dictResponses = WS.AlphabeticalDict(dictResponses)  # sort keys alphabetically
        return dictResponses


    def readDataset(self, dirPopulation):
        PS.loadDataset(dirPopulation, self.getFeatureNames())



    def __resetFeatureDescription(self):
        self.__setFeatureDescription({})
        self.__setFeatureDescriptionRaw({})

    def __resetDatasets(self):
        self.__setPopulationDataset({KSD.SAMPLES: [], KSD.FEATURE_LIST: {}})
        self.__setDatasetA({KSD.SAMPLES: [], KSD.FEATURE_LIST: {}})
        self.__setDatasetB({KSD.SAMPLES: [], KSD.FEATURE_LIST: {}})

        # self.tests = []
        # self.datasetCountA = len(self.datasetA['Data'])
        # self.datasetCountB = len(self.datasetB['Data'])

        # TODO
        # self.labelQueryDataACount.configure(text = self.getDatasetCountA())
        # self.labelQueryDataBCount.configure(text = self.getDatasetCountB())
        # self.queryResetDatasetA(None)
        # self.queryResetDatasetB(None)


    """Returns a list of feature values"""
    def __getFeatureQuery(self, queryString):
        featureList = self.getFeatureDescription()

        queryStringKeys = []
        for featureKey in featureList.keys():
            # print(str(featureKey) + " vs " + queryString)
            # print("find returns : " + str(str(featureKey).find(queryString)))
            if str(featureKey).find(queryString) > -1:  # if key contains string
                queryStringKeys.append(featureKey)


        # queryFeatureList = [featureList[x] for x in queryStringKeys]
        queryFeatureList = {key: value for key, value in featureList.items() if key in queryStringKeys}
        queryFeatureList = WS.AlphabeticalDict(queryFeatureList)

        return queryFeatureList

    def __getFeatureResponses(self, featureID):
        featureList = self.getFeatureDescription()
        hasKey = FS.checkKey(featureList, featureID)

        if hasKey:
            response = featureList[featureID][KSD.RESPONSES]
            # print "Key found"
        else:
            response= {}

        self.viewModel.setCurrentResponse(response)
        return response

    """BUTTON FUNCTIONS"""
    def confirmFeatureSelect(self):
        selectedFeatureIndices = self.viewModel.getSelectedFeatureIndices()

        confirmedFeatures = [self.viewModel.getCurrentQueryFeatureList().items()[index] for index in selectedFeatureIndices]
        confirmedFeatures = WS.AlphabeticalDict(confirmedFeatures)

        updatedFeatures = WS.MergedDict(self.viewModel.getConfirmedFeatures(), confirmedFeatures)

        # update viewModel's confirmed features with the currently selected features
        self.viewModel.setConfirmedFeatures(updatedFeatures)

        return self.viewModel.getConfirmedFeatures()


    def runSystematicFiltering(self, root):
        self.__systematicFiltering = SF.SystematicFiltering(root, self.AMController)

    def setAMController(self, controller):
        self.AMController = controller

    def queryFeature(self, featureID):
        self.viewModel.setQueryFeatureList(featureID)
        queryFeatureList = self.__getFeatureQuery(featureID)
        # responses = self.__getFeatureResponses(featureID)

        # Update contents of listbox
        self.viewModel.setQueryFeatureList(queryFeatureList)
        # self.viewModel.setCurrentResponses(responses)
        return queryFeatureList

    def queryFeatureResponses(self, featureID):
        self.viewModel.setQueryFeatureList(featureID)
        response = self.__getFeatureResponses(featureID)

        # Update contents of listbox
        self.viewModel.setCurrentResponse(response)
        return response

    def resetFeatureSelect(self):
        return "break"

    def resetConfirmedFeatures(self):
        confirmedFeatureList = self.viewModel.getConfirmedFeatures()
        selectedIndices = self.viewModel.getSelectedConfirmedFeatureIndices()

        selectedFeatures = [self.viewModel.getConfirmedFeatures().items()[index] for index in selectedIndices]
        selectedFeatures = WS.AlphabeticalDict(selectedFeatures)

        updatedFeatureList = WS.SubtractedDict(confirmedFeatureList, selectedFeatures)

        self.viewModel.setConfirmedFeatures(updatedFeatureList)
        self.viewModel.setSelectedConfirmedFeatureIndices([])

        return self.viewModel.getConfirmedFeatures()


    """GETTERS"""
    # returns the formatted feature description used for UI data retrieval
    def getFeatureDescription(self):
        return self.__featureDescription

    # returns the raw feature description, as directly read from the CSV
    def getFeatureDescriptionRaw(self):
        return self.__featureDescriptionRaw

    def getPopulationDataset(self):
        return self.__populationDataset

    def getDatasetA(self):
        return self.__datasetA

    def getDatasetB(self):
        return self.__datasetB

    def getCountDatasetA(self):
        count = len(self.getDatasetA()['Data'])
        return count

    def getCountDatasetB(self):
        count = len(self.getDatasetB()['Data'])
        return count

    def getFeatureNames(self):
        return self.__featureNames

    """SETTERS"""
    def __setFeatureDescription(self, value):
        # sort alphabetically before setting feature description
        self.__featureDescription = WS.AlphabeticalDict(value)

    def __setFeatureDescriptionRaw(self, value):
        self.__featureDescriptionRaw = value

    def __setPopulationDataset(self, value):
        self.__populationDataset = OrderedDict(value)

    def __setDatasetA(self, value):
        self.__datasetA = OrderedDict(value)

    def __setDatasetB(self, value):
        self.__datasetB = OrderedDict(value)

    def __setFeatureNames(self, value):
        self.__featureNames = value


    """UPDATERS"""
    def updateSelectedFeatureResponse(self, selectedItem):
        featureID = self.extractFeatureID(selectedItem)
        response = {}

        if not (featureID == '-1'):
            response = self.getFeatureDescription()[featureID][KSD.RESPONSES]

        self.viewModel.setCurrentResponse(response)

        return response

    def updateConfirmedFeatureResponse(self, selectedItem):
        featureID = self.extractFeatureID(selectedItem)
        response = {}

        if not (featureID == '-1'):
            response = self.getFeatureDescription()[featureID][KSD.RESPONSES]

        self.viewModel.setConfirmedCurrentResponse(response)

        return response

    def extractFeatureID(self, selectedItem):
        featureId = str(selectedItem).strip()[0:2]
        return featureId

# AM MODEL class that contains the functions and variables utilized by the UI/VIEW
class ViewModel:

    def __init__(self):
        # feature select
        self.__currentQueryFeatureList = {}
        self.__currentResponse = {}
        self.__selectedFeatureIndices = []
        self.__prevSelectedFeatures = []

        # confirmed feature select
        self.__confirmedFeatures = {}
        self.__confirmedCurrentResponse = {}
        self.__selectedConfirmedFeatureIndices = []
        self.__prevSelectedConfirmedFeatures = []

    """FUNCTIONS"""
    def resetFeature(self):
        self.setQueryFeatureList('')
        self.setSelectedFeatureIndices([])

    """GETTERS"""
    # region feature select getters
    def getCurrentQueryFeatureList(self):
        return self.__currentQueryFeatureList

    def getCurrentResponse(self):
        return self.__currentResponse

    def getSelectedFeatureIndices(self):
        return self.__selectedFeatureIndices

    def getPrevSelectedFeatures(self):
        return self.__prevSelectedFeatures
    # endregion feature select getters

    # region confirmed features getters
    def getConfirmedFeatures(self):
        return self.__confirmedFeatures

    def getConfirmedCurrentResponse(self):
        return self.__confirmedCurrentResponse

    def getSelectedConfirmedFeatureIndices(self):
        return self.__selectedConfirmedFeatureIndices

    def getPrevSelectedConfirmedFeatures(self):
        return self.__prevSelectedConfirmedFeatures
    # endregion confirmed feature getters

    """SETTERS"""
    # region feature select setters
    def setQueryFeatureList(self, value):
        self.__currentQueryFeatureList = value

    def setCurrentResponse(self, value):
        self.__currentResponse = value

    def setSelectedFeatureIndices(self, value):
        self.__selectedFeatureIndices = value

    def setPrevSelectedFeatures(self, value):
        self.__prevSelectedFeatures = value
    # endregion feature select setters

    # region confirmed features setters
    def setConfirmedFeatures(self, value):
        self.__confirmedFeatures = value

    def setConfirmedCurrentResponse(self, value):
        self.__confirmedCurrentResponse = value

    def setSelectedConfirmedFeatureIndices(self, value):
        self.__selectedConfirmedFeatureIndices = value

    def setPrevSelectedConfirmedFeatures(self, value):
        self.__prevSelectedConfirmedFeatures = value
    # endregion confirmed features setters

    """UPDATERS"""
    # region feature select updaters
    def updateSelectedFeatures(self, listbox, newSelectedFeatureIndices):
        self.updatePrevSelectedFeatures()
        self.setSelectedFeatureIndices(newSelectedFeatureIndices)

        if self.getPrevSelectedFeatures():  # if not empty
            # compare last selectionlist with new list and extract the difference
            changedSelection = set(self.getPrevSelectedFeatures()).symmetric_difference(set(newSelectedFeatureIndices))
            self.setPrevSelectedFeatures(newSelectedFeatureIndices)
        else:
            # if empty, assign current selection
            self.setPrevSelectedFeatures(newSelectedFeatureIndices)
            changedSelection = newSelectedFeatureIndices


        if len(changedSelection) > 0:
            index = int(list(changedSelection)[0])
            if index in listbox.curselection():
                lastSelectedIndex = listbox.get(index)
            else:
                lastSelectedIndex = -1
        else:
            lastSelectedIndex = -1

        return lastSelectedIndex

    def updatePrevSelectedFeatures(self):
        self.__prevSelectedFeatures = self.getSelectedFeatureIndices()
    # endregion feature select updaters

    def updateConfirmedSelectedFeatures(self, listbox, newSelectedFeatureIndices):
        # self.updatePrevSelectedConfirmedFeatures()
        self.setSelectedConfirmedFeatureIndices(newSelectedFeatureIndices)

        if self.getPrevSelectedConfirmedFeatures():  # if not empty
            # compare last selectionlist with new list and extract the difference
            changedSelection = set(self.getPrevSelectedConfirmedFeatures()).symmetric_difference(set(newSelectedFeatureIndices))
            self.setPrevSelectedConfirmedFeatures(newSelectedFeatureIndices)
        else:
            # if empty, assign current selection
            self.setPrevSelectedConfirmedFeatures(newSelectedFeatureIndices)
            changedSelection = newSelectedFeatureIndices

        if len(changedSelection) > 0:
            index = int(list(changedSelection)[0])
            if index in listbox.curselection():
                lastSelectedIndex = listbox.get(index)
            else:
                lastSelectedIndex = -1
        else:
            lastSelectedIndex = -1

        return lastSelectedIndex

    def updatePrevSelectedConfirmedFeatures(self):
        self.__prevSelectedConfirmedFeatures = self.getSelectedConfirmedFeatureIndices()
