
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
import threading
import time
import copy
import Function_support as FS
import KEYS_support as key



class ViewModel:

    def __init__(self):
        self.setCurrentFeature('')
        self.setCurrentResponses({})
        self.setSelectedResponses([])

    """FUNCTIONS"""
    def resetFeature(self):
        self.setCurrentFeature('')
        self.setSelectedResponses([])

    """GETTERS"""
    def getCurrentFeature(self):
        return self.__currentFeature

    def getCurrentResponses(self):
        return self.__currentResponses

    def getSelectedResponses(self):
        return self.__selectedResponses

    """SETTERS"""
    def setCurrentFeature(self, value):
        self.__currentFeature = value

    def setCurrentResponses(self, value):
        self.__currentResponses = value

    def setSelectedResponses(self, value):
        self.__selectedResponses = value




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

    def __getFeatureResponses(self, featureID):
        featureList = self.getFeatureDescription()
        hasKey = FS.checkKey(featureList, featureID)

        if hasKey:
            responses = featureList[featureID][key.RESPONSES]
            print "Key found"
        else:
            responses = {}

        return responses

    """BUTTON FUNCTIONS"""
    def confirmFeatureSelect(self, evt):
        print "confirmFeatureSelect"
        self.startThread(evt)
        return "break"

    def resetFeatureSelect(self, evt):
        print "resetFeatureSelect"
        return "break"

    def queryFeature(self, featureID):
        # featureID = self.viewModel.getCurrentFeature()
        print "featureID " + str(featureID)
        self.viewModel.setCurrentFeature(featureID)
        responses = self.__getFeatureResponses(featureID)

        # Update contents of listbox
        self.viewModel.setCurrentResponses(responses)
        return responses

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

    # THREADING TEST FUNCTIONS
    def startThread(self, evt):
        if not self.isProcessing:
            self.isProcessing = True
            if not (self.winProgressBar is None):
                self.onProgressBarClose()

            self.winProgressBar = Tk()
            self.winProgressBar.protocol("WM_DELETE_WINDOW", self.onProgressBarClose)
            self.varProgressBar = 0
            [self.pbProgressBar, self.lblProgressBar] = self.initProgressBar(self.winProgressBar)

            ThreadedTask(self.winProgressBar, self.pbProgressBar, self.lblProgressBar, self.varProgressBar).start()
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


class ThreadedTask(threading.Thread):
    def __init__(self, winProgress, prog_bar, prog_text, prog_val):
        threading.Thread.__init__(self)
        self.winProgress = winProgress
        self.prog_bar = prog_bar
        self.prog_text = prog_text
        self.prog_val = prog_val
        self.count = 0

    def run(self):
        try:
            # self.prog_bar.start()
            while self.count < 100:
                self.count += 1
                # self.prog_bar.after(1, self.process_queue)
                self.process_queue()
                time.sleep(0.01)


        finally:
            self.prog_text["text"] = "COMPLETE"

    def process_queue(self):
        self.prog_val = float(self.count)
        self.prog_bar["value"] = self.prog_val
        self.prog_text["text"] = self.prog_val
        # self.prog_bar.start()
        # print str(self.prog_val)


