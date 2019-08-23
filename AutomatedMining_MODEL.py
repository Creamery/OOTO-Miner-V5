
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
import KEYS_support as key
from CrossProcessThread import CrossProcessThread

class ViewModel:

    def __init__(self):
        self.setQueryFeatureList('')
        self.setCurrentResponse({})
        self.setSelectedFeatures([])
        self.setPrevSelectedFeatures([])

    """FUNCTIONS"""
    def resetFeature(self):
        self.setQueryFeatureList('')
        self.setSelectedFeatures([])

    """GETTERS"""
    def getCurrentFeature(self):
        return self.__currentQueryFeatureList

    def getCurrentResponse(self):
        return self.__currentResponse

    def getSelectedFeatures(self):
        return self.__selectedFeatures

    def getPrevSelectedFeatures(self):
        return self.__prevSelectedFeatures

    """SETTERS"""
    def setQueryFeatureList(self, value):
        self.__currentQueryFeatureList = value

    def setCurrentResponse(self, value):
        self.__currentResponse = value

    def setSelectedFeatures(self, value):
        self.__selectedFeatures = value

    def setPrevSelectedFeatures(self, value):
        self.__prevSelectedFeatures = value

    """UPDATERS"""

    def updateSelectedFeatures(self, listbox, newSelectedFeatures):
        self.updatePrevSelectedFeatures()
        self.setSelectedFeatures(newSelectedFeatures)

        # w = evt.widget
        if self.getPrevSelectedFeatures():  # if not empty
            # compare last selectionlist with new list and extract the difference
            changedSelection = set(self.getPrevSelectedFeatures()).symmetric_difference(set(newSelectedFeatures))
            self.setPrevSelectedFeatures(newSelectedFeatures)
        else:
            # if empty, assign current selection
            self.setPrevSelectedFeatures(newSelectedFeatures)
            changedSelection = newSelectedFeatures

        if len(changedSelection) > 0:
            index = int(list(changedSelection)[0])
            lastSelectedIndex = listbox.get(index)
        else:
            lastSelectedIndex = -1
        print('ls '+ str(lastSelectedIndex))
        return lastSelectedIndex


    def updatePrevSelectedFeatures(self):
        self.__prevSelectedFeatures = self.getSelectedFeatures()




class AutomatedMining_Model:

    def __init__(self):
        self.viewModel = ViewModel()

        self.isProcessing = False
        self.winProgressBar = None
        self.pbProgressBar = None

        self.__resetFeatureDescription()
        self.__resetDatasets()



    def readFeatures(self, features):
        self.__resetFeatureDescription()

        for feature in features:
            code = feature[key.CODE]
            description = feature[key.DESCRIPTION]
            responses = feature[key.RESPONSES]
            dictResponses = self.parseResponses(responses)


            featureDescription = {}
            featureDescription[key.DESCRIPTION] = description
            featureDescription[key.RESPONSES] = dictResponses

            self.getFeatureDescription()[code] = featureDescription

    """
    Change the format of responses to a dictionary of the form :
    { 'a': { 'Code': [], 'Description': [] } }
    """
    def parseResponses(self, responses):
        dictResponses = {}

        for response in responses:
            group = response[key.GROUP]
            if not(str(group).strip() == '-1'):
                code = response[key.CODE]
                description = response[key.DESCRIPTION]


                entry = dictResponses.setdefault(group, OrderedDict({key.CODE: [], key.DESCRIPTION: []}))
                entry[key.CODE].append(code)
                entry[key.DESCRIPTION].append(description)

        dictResponses = OrderedDict(sorted(dictResponses.items()))  # sort keys alphabetically
        return dictResponses


    def readDataset(self, dataset):
        self.__resetDatasets()

        # Append SAMPLES
        for record in dataset:
            orderedRecord = OrderedDict(sorted(record.items()))  # sort keys alphabetically
            self.getPopulationDataset()[key.SAMPLES].append(orderedRecord)
            self.getDatasetA()[key.SAMPLES].append(orderedRecord)
            self.getDatasetB()[key.SAMPLES].append(orderedRecord)

        # Set FEATURE_LIST
        self.getPopulationDataset()[key.FEATURE_LIST] = self.getFeatureDescription()
        self.getDatasetA()[key.FEATURE_LIST] = copy.deepcopy(self.getFeatureDescription())
        self.getDatasetB()[key.FEATURE_LIST] = copy.deepcopy(self.getFeatureDescription())
        print "getPopulationDataset[key.SAMPLES]"
        # print str(type(self.getPopulationDataset()[key.SAMPLES][0]))
        # print str(self.getPopulationDataset()[key.SAMPLES])


    def __resetFeatureDescription(self):
        self.__setFeatureDescription({})

    def __resetDatasets(self):
        self.__setPopulationDataset({key.SAMPLES: [], key.FEATURE_LIST: {}})
        self.__setDatasetA({key.SAMPLES: [], key.FEATURE_LIST: {}})
        self.__setDatasetB({key.SAMPLES: [], key.FEATURE_LIST: {}})

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
            print(str(featureKey) + " vs " + queryString)
            print("find returns : " + str(str(featureKey).find(queryString)))
            if str(featureKey).find(queryString) > -1: # if key contains string
                queryStringKeys.append(featureKey)


        # queryFeatureList = [featureList[x] for x in queryStringKeys]
        queryFeatureList = {key: value for key, value in featureList.items() if key in queryStringKeys}
        queryFeatureList = OrderedDict(sorted(queryFeatureList.items()))
        print(str(queryFeatureList))
        return queryFeatureList

    def __getFeatureResponses(self, featureID):
        featureList = self.getFeatureDescription()
        hasKey = FS.checkKey(featureList, featureID)

        if hasKey:
            response = featureList[featureID][key.RESPONSES]
            print "Key found"
        else:
            responses = {}

        self.setCurrentResponse(response)
        return response

    """BUTTON FUNCTIONS"""
    def confirmFeatureSelect(self, evt):
        print "confirmFeatureSelect"
        # self.startThread(evt)  # TODO
        return "break"

    def confirmConfirmedFeatures(self, evt):
        print "confirmConfirmedFeatures"
        return "break"

    def resetFeatureSelect(self, evt):
        print "resetFeatureSelect"
        return "break"

    def queryFeature(self, featureID):
        # featureID = self.viewModel.getCurrentFeature()
        print "featureID " + str(featureID)

        self.viewModel.setQueryFeatureList(featureID)
        queryFeatureList = self.__getFeatureQuery(featureID)
        # responses = self.__getFeatureResponses(featureID)

        # Update contents of listbox
        self.viewModel.setQueryFeatureList(queryFeatureList)
        # self.viewModel.setCurrentResponses(responses)
        return queryFeatureList

    def queryFeatureResponses(self, featureID):
        # featureID = self.viewModel.getCurrentFeature()
        print "featureID " + str(featureID)

        self.viewModel.setQueryFeatureList(featureID)
        response = self.__getFeatureResponses(featureID)

        # Update contents of listbox
        self.viewModel.setCurrentResponse(response)
        return response

    """GETTERS"""
    def getFeatureDescription(self):
        return self.__featureDescription

    def getPopulationDataset(self):
        return self.__populationDataset

    def getDatasetA(self):
        return self.__datasetA

    def getDatasetB(self):
        return self.__datasetA

    def getCountDatasetA(self):
        count = len(self.getDatasetA()['Data'])
        return count

    def getCountDatasetB(self):
        count = len(self.getDatasetB()['Data'])
        return count

    """SETTERS"""
    def __setFeatureDescription(self, value):
        self.__featureDescription = OrderedDict(value)

    def __setPopulationDataset(self, value):
        self.__populationDataset = OrderedDict(value)

    def __setDatasetA(self, value):
        self.__datasetA = OrderedDict(value)

    def __setDatasetB(self, value):
        self.__datasetB = OrderedDict(value)

    """UPDATERS"""
    def updateSelectedFeatureResponse(self, selectedItem):
        featureID = self.extractFeatureID(selectedItem)
        response = {}
        print "featureID is " + str(featureID)
        if not (featureID == '-1'):
            response = self.getFeatureDescription()[featureID][key.RESPONSES]
            self.viewModel.setCurrentResponse(response)

        return response

    def extractFeatureID(self, selectedItem):
        featureId = str(selectedItem).strip()[0:2]
        print str(featureId)
        return featureId


    # THREADING TEST FUNCTIONS
    def startThread(self, evt):
        if not self.isProcessing:
            self.isProcessing = True
            if not (self.winProgressBar is None):
                self.onProgressBarClose()

            self.winProgressBar = Toplevel()  # Tk() TODO add parent
            self.winProgressBar.protocol("WM_DELETE_WINDOW", self.onProgressBarClose)
            self.varProgressBar = 0
            [self.pbProgressBar, self.lblProgressBar] = self.initProgressBar(self.winProgressBar)

            crossProcess = CrossProcessThread(self.winProgressBar, self.pbProgressBar,
                                              self.lblProgressBar, self.varProgressBar)
            crossProcess.start()
        else:
            print ("isProcessing")

    def initProgressBar(self, parentFrame):
        progBar = ttk.Progressbar(
            parentFrame, orient = "horizontal",
            length = 300, variable = self.varProgressBar)

        progBar.pack(side = TOP)
        progText = Label(progBar)
        progText.place(relx = 0, rely = 0, relh = 1)
        return progBar, progText

    def onProgressBarClose(self):
        # if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        #     self.winProgressBar.destroy()
        #     self.winProgressBar = None
        #     self.isProcessing = False
        self.winProgressBar.destroy()
        self.winProgressBar = None
        self.isProcessing = False
