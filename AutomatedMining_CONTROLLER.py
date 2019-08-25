#! /usr/bin/env python

"""
{Description}

"""

__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019, TE3D House"
__credits__ = ["Arnulfo Azcarraga"]
__version__ = "3.0"

import tkMessageBox
import copy
import SampleVsPopulation as svp
import SampleVsSample as svs
import ChiTest as ct
import os
from collections import Counter

import Tkinter as tk

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

import math
import Color_support
import Icon_support
import UI_support
import PIL.Image
import PIL.ImageTk
import CONSTANTS as const
import Function_support as FS

import _MODULE_SystematicFiltering as SF

class AutomatedMining_Controller:

    def __init__(self, view, model, root = None):
        self.root = root
        self.view = view
        self.model = model
        self.dictWidgetPlace = {}
        self.populationDataset = []

        self.populationDatasetOriginalA = {'Data': [], 'Filter Features': []}
        self.populationDatasetOriginalB = {'Data': [], 'Filter Features': []}
        self.datasetA = {'Data': [], 'Filter Features': []}
        self.datasetB = {'Data': [], 'Filter Features': []}

        self.tests = []
        self.datasetCountA = 0
        self.datasetCountB = 0


        self.arrQueryCriticalValue = None
        self.arrQueryCriticalValueMapping = None


        self.configureViewBindings()

        # self.configureTestTabBindings()
        # self.initializeVariables()

    def configureViewBindings(self):
        button = self.view.getBtnConfirmFeatureSelect()
        button.bind('<Button-1>', self.confirmFeatureSelect)

        button = self.view.getBtnConfirmConfirmedFeatures()
        button.bind('<Button-1>', self.model.confirmConfirmedFeatures)

        button = self.view.getBtnResetFeatureSelect()
        button.bind('<Button-1>', self.model.resetFeatureSelect)

        button = self.view.getBtnQueryFeatureList()
        button.bind('<Button-1>', self.queryFeatureID)

        listbox = self.view.getLbListFeatureSelect()
        listbox.bind('<<ListboxSelect>>', self.selectFeature)

        # TODO Entry Change

    def confirmFeatureSelect(self, event):
        self.systematicFiltering = SF.SystematicFiltering(self.root)
        self.model.confirmFeatureSelect(event)

        return "break"

    def queryFeatureID(self, event):
        print "queryFeatureID"
        # get featureID from entry widget
        featureID = self.view.getEntryQueryFeatureList().get()

        queryFeatureList = self.model.queryFeature(featureID)

        self.view.updateLbListFeatureSelect(queryFeatureList)

    def selectFeature(self, event):
        listbox = event.widget
        selectedItems = listbox.curselection()

        lastSelectedItem = self.model.viewModel.updateSelectedFeatures(listbox, selectedItems)
        # lastSelectedItem = listbox.get(lastSelectedIndex)

        response = self.model.updateSelectedFeatureResponse(lastSelectedItem)
        self.view.updateLbListFeatureDetails(response)

    def setArrQueryCriticalValue(self, arrayValue):
        self.arrQueryCriticalValue = arrayValue

    def setArrQueryCriticalValueMapping(self, arrayValue):
        self.arrQueryCriticalValueMapping = arrayValue

    def initializeVariables(self):
        # Selected UI for MM
        self.selectOptionZTest(None)
        self.showConsoleScreen(None, self.listConsoleScreen)  # Click ALL type

        global queryType
        queryType = self.comboQueryTest.get()

        self.populationDir = ""

        # Button state variables (This is used instead of directly disabling buttons to keep their appearance)
        self.buttonQueryFeature_state = DISABLED

        self.hasUploadedVariableDescription = False
        self.hasUploadedPopulation = False

        self.isReadyDatasetA = False
        self.isReadyDatasetB = False
        self.checkIfDatasetReady()
        self.resetDatasetContents()

    def resetDatasetContents(self):
        # self.populationDataset = []
        self.populationDatasetOriginalA = {'Data': [], 'Filter Features': []}
        self.populationDatasetOriginalB = {'Data': [], 'Filter Features': []}
        self.datasetA = {'Data': [], 'Filter Features': []}
        self.datasetB = {'Data': [], 'Filter Features': []}

        self.tests = []
        self.datasetCountA = len(self.datasetA['Data'])
        self.datasetCountB = len(self.datasetB['Data'])

        self.labelQueryDataACount.configure(text = self.getDatasetCountA())
        self.labelQueryDataBCount.configure(text = self.getDatasetCountB())

        self.queryResetDatasetA(None)
        self.queryResetDatasetB(None)

    def readFeatures(self, variableDescription, itemMarker):
        features = FS.readFeatures(variableDescription, itemMarker)
        if (len(features)) <= 0:
            return False
        else:
            self.model.readFeatures(features)
            # print "FEATURES " + str(features)
            return True

    def uploadDataset(self, dataset):
        self.model.readDataset(dataset)

        # TODO Show the total samples of the unaltered dataset
        # self.datasetCountA = len(self.datasetA['Data'])
        # self.datasetCountB = len(self.datasetB['Data'])
        # self.datasetCountA = 0
        # self.datasetCountB = 0

        # TODO return
        # self.labelQueryDataACount.configure(text = self.getDatasetCountA())
        # self.labelQueryDataBCount.configure(text = self.getDatasetCountB())

        print "UPLOADED"
        return True

    def configureTestTabBindings(self):

        # GENERAL
        self.dictConsoleScreens = self.view.getDictConsoleScreens()

        # LABEL FRAMES
        self.labelOverlayFilterListData = self.view.getLabelOverlayFilterListData()
        self.labelFrameFilterListData = self.view.getLabelFrameFilterListData()
        self.labelFilterStripes = self.view.getLabelFilterStripes()
        self.labelQuerySetDataStatusA = self.view.getLabelQuerySetDataStatusA()
        self.labelQuerySetDataStatusB = self.view.getLabelQuerySetDataStatusB()
        self.labelQuerySetDataStripesA = self.view.getLabelQuerySetDataStripesA()
        self.labelQuerySetDataStripesB = self.view.getLabelQuerySetDataStripesB()

        # LABELS
        self.labelQueryDataA = self.view.getLabelQueryDataA()
        self.labelQueryDataB = self.view.getLabelQueryDataB()
        self.labelQueryDataFeatureName = self.view.getLabelQueryDataFeatureName()
        self.listQueryDataA = self.view.getListQueryDataA()
        self.listQueryDataB = self.view.getListQueryDataB()

        self.labelQueueCount = self.view.getLabelQueueCount()
        self.labelConsoleScreenTaskBar = self.view.getLabelConsoleScreenTaskBar()

        self.labelQueryDataACount = self.view.getLabelQueryDataACount()
        self.labelQueryDataBCount = self.view.getLabelQueryDataBCount()

        # LISTBOXES
        self.listQuerySetDataA = self.view.getListQuerySetDataA()
        self.listQuerySetDataB = self.view.getListQuerySetDataB()

        # SPINBOXES
        self.spinBoxQueryZConfidence = self.view.getSpinBoxQueryZConfidence()

        # ENTRIES
        self.entryQueryFeature = self.view.getEntryQueryFeature()
        self.entryQuerySetDataA = self.view.getEntryQuerySetDataA()
        self.entryQuerySetDataB = self.view.getEntryQuerySetDataB()

        # BUTTONS

        self.labelFrameProcessZTest = self.view.getLabelFrameProcessZTest()
        self.labelFrameProcessChiSquare = self.view.getLabelFrameProcessChiSquare()

        self.buttonQuerySetDataA = self.view.getButtonQuerySetDataA()
        self.buttonQuerySetDataA.bind('<Button-1>', self.querySetDataA)
        self.buttonQuerySetDataB = self.view.getButtonQuerySetDataB()
        self.buttonQuerySetDataB.bind('<Button-1>', self.querySetDataB)

        self.buttonQueryAddFilterA = self.view.getButtonQueryAddFilterA()
        self.buttonQueryAddFilterA.bind('<Button-1>', self.queryAddFilterA)
        self.buttonQueryAddFilterB = self.view.getButtonQueryAddFilterB()
        self.buttonQueryAddFilterB.bind('<Button-1>', self.queryAddFilterB)

        self.buttonQueryFeature = self.view.getButtonQueryFeature()
        self.buttonQueryFeature.bind('<Button-1>', self.querySetFeature)
        # self.buttonQueryFeature.configure(command = self.querySetFeature)
        # self.buttonQueryFeatureA.bind('<Button-1>', self.querySetFeatureA)
        # self.buttonQueryFeatureB.bind('<Button-1>', self.querySetFeatureB)

        self.buttonQueryZTest = self.view.getButtonQueryZTest()
        self.buttonQueryZTest.bind('<Button-1>', self.queryZTest)  # Run Z-test Sample vs Sample
        self.buttonQueryZTestSvP = self.view.getButtonQueryZTestSvP()
        self.buttonQueryZTestSvP.bind('<Button-1>', self.querySVP)  # Run Z-test Sample vs Population

        self.buttonQueue = self.view.getButtonQueue()
        self.buttonQueue.bind('<Button-1>', self.queue)  # Enqueue Subset-pairs

        self.buttonClearQueue = self.view.getButtonClearQueue()
        self.buttonClearQueue.bind('<Button-1>', self.clearQueue)
        self.buttonTestQueue = self.view.getButtonTestQueue()
        self.buttonTestQueue.bind('<Button-1>', self.testQueue)  # Run Miner Button

        self.buttonQueryResetFilterA = self.view.getButtonQueryResetFilterA()
        self.buttonQueryResetFilterA.bind('<Button-1>', self.queryResetDatasetA)

        self.buttonQueryResetFilterB = self.view.getButtonQueryResetFilterB()
        self.buttonQueryResetFilterB.bind('<Button-1>', self.queryResetDatasetB)

        # Test option buttons
        self.buttonChooseChiSquare = self.view.getButtonChooseChiSquare()
        self.buttonChooseChiSquare.bind('<Button-1>', self.selectOptionChiSquare)

        self.buttonChooseZTest = self.view.getButtonChooseZTest()
        self.buttonChooseZTest.bind('<Button-1>', self.selectOptionZTest)

        # Console buttons
        self.buttonConsoleAll = self.view.getButtonConsoleAll()
        self.buttonConsoleAll.bind("<Button-1>", lambda event: self.showConsoleScreen(event, self.listConsoleScreen))

        self.buttonConsoleZTest = self.view.getButtonConsoleZTest()
        self.buttonConsoleZTest.bind("<Button-1>",
                                     lambda event: self.showConsoleScreen(event, self.listConsoleZTestScreen))

        self.buttonConsoleChiSquare = self.view.getButtonConsoleChiSquare()
        self.buttonConsoleChiSquare.bind("<Button-1>",
                                         lambda event: self.showConsoleScreen(event, self.listConsoleChiSquareScreen))

        self.buttonConsoleQueue = self.view.getButtonConsoleQueue()
        self.buttonConsoleQueue.bind("<Button-1>",
                                     lambda event: self.showConsoleScreen(event, self.listConsoleQueueScreen))
        # self.buttonConsoleAll.bind('<Button-1>', self.showConsoleScreen(self.listConsoleScreen))
        # self.buttonConsoleZTest.bind('<Button-1>', self.showConsoleScreen(self.listConsoleZTestScreen))
        # self.buttonConsoleChiSquare.bind('<Button-1>', self.showConsoleScreen(self.listConsoleChiSquareScreen))
        # self.buttonConsoleQueue.bind('<Button-1>', self.showConsoleScreen(self.listConsoleQueueScreen))

        # FOCUS IN / OUT

        self.listConsoleScreen = self.view.getListConsoleScreen()
        self.listConsoleScreen.bind("<ButtonRelease>",
                                    lambda event: self.selectConsoleEntry(event, self.listConsoleScreen))

        self.listConsoleZTestScreen = self.view.getListConsoleZTestScreen()
        self.listConsoleZTestScreen.bind("<ButtonRelease>",
                                         lambda event: self.selectConsoleEntry(event, self.listConsoleZTestScreen))

        self.listConsoleChiSquareScreen = self.view.getListConsoleChiSquareScreen()
        self.listConsoleChiSquareScreen.bind("<ButtonRelease>", lambda event: self.selectConsoleEntry(event,
                                                                                                      self.listConsoleChiSquareScreen))

        self.listConsoleQueueScreen = self.view.getListConsoleQueueScreen()
        self.listConsoleQueueScreen.bind("<ButtonRelease>",
                                         lambda event: self.selectConsoleEntry(event, self.listConsoleQueueScreen))

        # ENTER / LEAVE
        self.buttonQuerySetDataA.bind("<Enter>", self.enterRightArrowPlainIcon)
        self.buttonQuerySetDataA.bind("<Leave>", self.leaveRightArrowPlainIcon)

        self.buttonQuerySetDataB.bind("<Enter>", self.enterRightArrowPlainIcon)
        self.buttonQuerySetDataB.bind("<Leave>", self.leaveRightArrowPlainIcon)
        # self.buttonQuerySetDataB.bind("<Enter>", lambda event, iconSize =  Icon_support.SELECT_ICO_SIZE_BUTTONS: self.enterRightArrowIcon(event, Icon_support.SELECT_ICO_SIZE_BUTTONS))
        # self.buttonQuerySetDataB.bind("<Leave>", self.leaveRightArrowIcon(Icon_support.SELECT_ICO_SIZE_BUTTONS))

        self.buttonQueryAddFilterA.bind("<Enter>", self.enterCheckIcon)
        self.buttonQueryAddFilterA.bind("<Leave>", self.leaveCheckIcon)

        self.buttonQueryAddFilterB.bind("<Enter>", self.enterCheckIcon)
        self.buttonQueryAddFilterB.bind("<Leave>", self.leaveCheckIcon)

        # self.buttonQueryFeature.bind("<Enter>", self.enterRightArrowPlainIcon)
        self.buttonQueryFeature.bind("<Leave>", self.leaveRightArrowPlainIcon)
        self.buttonQueryFeature.bind("<Enter>",
                                     lambda event: self.enterRightArrowPlainIcon(event, self.buttonQueryFeature_state))
        self.buttonQueryFeature.bind("<Leave>",
                                     lambda event: self.leaveRightArrowPlainIcon(event, self.buttonQueryFeature_state))

        self.buttonQueryZTest.bind("<Enter>", self.enterCheckIcon)
        self.buttonQueryZTest.bind("<Leave>", self.leaveCheckIcon)

        self.buttonQueue.bind("<Enter>", self.enterAddIcon)
        self.buttonQueue.bind("<Leave>", self.leaveAddIcon)
        # self.buttonQueue.bind("<Enter>", self.enterDownArrowIcon)
        # self.buttonQueue.bind("<Leave>", self.leaveDownArrowIcon)

        self.buttonClearQueue.bind("<Enter>", self.enterCrossIcon)
        self.buttonClearQueue.bind("<Leave>", self.leaveCrossIcon)

        self.buttonTestQueue.bind("<Enter>", self.enterRightArrowIcon)
        self.buttonTestQueue.bind("<Leave>", self.leaveRightArrowIcon)

        self.buttonQueryResetFilterA.bind("<Enter>", self.enterCrossIcon)
        self.buttonQueryResetFilterA.bind("<Leave>", self.leaveCrossIcon)

        self.buttonQueryResetFilterB.bind("<Enter>", self.enterCrossIcon)
        self.buttonQueryResetFilterB.bind("<Leave>", self.leaveCrossIcon)

        # LISTBOX
        self.listQuerySetDataA = self.view.getListQuerySetDataA()
        self.listQuerySetDataA.bind('<<ListboxSelect>>', self.querySelectDataValuesA)
        self.listQuerySetDataB = self.view.getListQuerySetDataB()
        self.listQuerySetDataB.bind('<<ListboxSelect>>', self.querySelectDataValuesB)

        self.listQueryDataA = self.view.getListQueryDataA()
        self.listQueryDataA.bind('<<ListboxSelect>>', self.setFocusFeatureValues)
        self.listQueryDataB = self.view.getListQueryDataB()
        self.listQueryDataB.bind('<<ListboxSelect>>', self.setFocusFeatureValues)

        # MOUSEWHEEL
        self.listQueryDataA.bind("<MouseWheel>", self.scrollFilterListBox)
        self.listQueryDataB.bind("<MouseWheel>", self.scrollFilterListBox)

        # COMBOBOX
        self.comboQueryTest = self.view.getComboQueryTest()
        self.comboQueryTest.bind('<<ComboboxSelected>>', self.querySetType)

    ''' --> Elements under the TEST ("TEST") TAB (2) <-- '''
    # region

    '''SELECT HEADER'''

    # region

    def setFocusFeatureValues(self, event):  ### TODO Add checker if listbox is not empty
        listBox = event.widget
        selectedItems = listBox.curselection()
        FS.setFocusFeatureValues(self.listQueryDataA, self.datasetA, selectedItems, self.labelQueryDataA, False)
        FS.setFocusFeatureValues(self.listQueryDataB, self.datasetB, selectedItems, self.labelQueryDataB, True)

    ''' Initial (SELECT) query for DATA A '''

    def querySetDataA(self, event):

        # CLEAR sample count
        self.queryResetDatasetA(event)
        # CLEAR filter feature box first
        self.queryResetFilterDetails(event)

        try:
            # findFeature(self.entryQuerySetDataA.get(), self.listQuerySetDataA, self.datasetA, "Dataset_Feature")
            self.findFeature(self.entryQuerySetDataA.get(), self.listQuerySetDataA, self.datasetA,
                             self.populationDatasetOriginalA, True, "Dataset_Feature")
        except NameError:
            tkMessageBox.showerror("Error: No features",
                                   "Features not found. Please upload your variable description file.")
        return "break"

    '''
    Finds the feature and displays its responses.

    If the feature being searched is the one that will be focused on for Z-Test between
    two samples, it will also display all of the proportions, frequencies and total for each value of that 
    feature
    '''

    # def findFeature(entryFeat, listFeat, dataset, *args):
    def findFeature(self, entryFeat, listFeat, dataset, populationDatasetOriginal, isPrintingError = False, *args):
        global features
        # Here is how to get the value from entryFeatA
        featCode = entryFeat
        print "Entered feature code: " + featCode
        arrTempItems = []
        found = False
        hasFocusFeature = False
        # Get proper list of features from initial variable description
        for feature in features:
            if feature['Code'] == featCode:
                found = True
                for arg in args:
                    if arg == "Dataset_Feature":
                        dataset['Feature'] = copy.deepcopy(feature)
                        populationDatasetOriginal['Feature'] = copy.deepcopy(feature)

                    if arg == "Focus_Feature":
                        dataset['Focus Feature'] = copy.deepcopy(feature)
                        populationDatasetOriginal['Focus Feature'] = copy.deepcopy(feature)
                        hasFocusFeature = True
                for response in feature['Responses']:
                    tempResp = response['Code'] + " - " + response['Description']
                    arrTempItems.append(tempResp)
                break
        if not found and isPrintingError:
            tkMessageBox.showerror("Error: Feature not found", "Feature not found in Variable Descriptor. Try again.")

        # Getting the proportions and frequencies of each value (including invalid values) in the focus feature
        if hasFocusFeature == True:
            arrTempItems = []
            dataset['ColumnData'] = []
            populationDatasetOriginal['ColumnData'] = []
            for record in dataset['Data']:
                dataset['ColumnData'].append(record[featCode])
                populationDatasetOriginal['ColumnData'].append(record[featCode])
            c = Counter(dataset['ColumnData'])  # Counts the number of occurrences of each value of the focus feature

            countN = len(dataset['ColumnData'])  # N is the size of the dataset
            countn = 0  # n is the total number of values where their group is not -1

            notInGroupNega1 = []  # List that keeps track of the values whose group is not -1
            presentInData = []  # List of values that occurred at least once in the data

            for response in dataset['Focus Feature']['Responses']:
                for val in c:
                    if val == response['Code']:
                        presentInData.append(val)
                        if response['Group'] != '-1':
                            notInGroupNega1.append(val)
                            countn = countn + int(c[val])
                        break
            '''
                reminderN = "N = Total no. of records"
                remindern = "n = Total no. of records where Group is not -1\n"
                header = "Freq | p/N | p/n | Group | Code | Description"

                arrTempItems.append(reminderN)
                arrTempItems.append(remindern)
                arrTempItems.append(header)
                '''
            for response in dataset['Focus Feature']['Responses']:
                countP = 0
                print 'Value: ' + response['Code']
                print 'Frequency: ' + str(countP)
                print 'n:' + str(countn)
                print 'N:' + str(countN)

                if response['Code'] in presentInData:  # If the value has occurred in the data
                    countP = int(c[response['Code']])

                proportionOverN = round(countP / float(countN) * 100.0, 2)
                proportionOvern = round(countP / float(countn) * 100.0, 2)

                if response['Code'] not in notInGroupNega1:  # If the value is an invalid value or its group/class is -1
                    proportionOvern = proportionOvern * 0

                tempResp = str(format(countP, '04')) + " | " + str(format(proportionOverN, '05')) + "%(N) | " + str(
                    format(proportionOvern, '05')) + "%(n) | "
                isValidResponse = False
                for val in c:
                    if val == response['Code']:
                        isValidResponse = True
                        tempResp = tempResp + response['Group'] + " | " + response['Code'] + " | " + response[
                            'Description']
                        break
                if not isValidResponse:
                    if response['Code'] not in presentInData:
                        tempResp = tempResp + response['Group'] + " | " + response['Code'] + " | " + response[
                            'Description']
                    else:
                        tempResp = tempResp + "-1" + " | " + response['Code'] + " | " + "INVALID VALUE"
                arrTempItems.append(tempResp)

        listFeat.delete(0, END)
        for A in arrTempItems:
            listFeat.insert(END, A)

    ''' Initial (SELECT) query for DATA B '''

    def querySetDataB(self, event):
        # CLEAR sample count
        self.queryResetDatasetB(event)

        # CLEAR filter feature box first
        self.queryResetFilterDetails(event)
        try:
            # findFeature(self.entryQuerySetDataB.get(), self.listQuerySetDataB, self.datasetB, "Dataset_Feature")
            self.findFeature(self.entryQuerySetDataB.get(), self.listQuerySetDataB, self.datasetB,
                             self.populationDatasetOriginalB, True, "Dataset_Feature")

        except NameError:
            tkMessageBox.showerror("Error: No features",
                                   "Features not found. Please upload your variable description file.")
        return "break"

    def queryResetDatasetA(self, event):
        self.isReadyDatasetA = False  # When a dataset is reset, it is not ready
        self.checkIfDatasetReady()  # Update dataset status accordingly
        self.setDatasetStripeReady(False, self.labelQuerySetDataStripesA)

        self.buttonQueryResetFilterA.configure(relief = FLAT)

        self.datasetA = self.resetDataset()
        self.entryQuerySetDataA.configure(text = '')
        self.entryQueryFeature.configure(text = '')
        self.labelQuerySetDataStatusA.configure(
            text = UI_support.SELECT_STATUS_NO_DATA_TEXT,
            background = Color_support.SELECT_LISTBOX_STATUS_BG,
            foreground = Color_support.SELECT_LISTBOX_STATUS_FG
        )

        # self.labelFrameQueryDataA.configure(text = "Dataset A") ### TODO
        # self.labelQuerySetDataStatusA.configure(text = UI_support.LBL_SELECT_NO_DATA)

        # if self.datasetA['Data'] is []:

        self.datasetCountA = 0  # len(self.datasetA['Data'])
        self.labelQueryDataACount.configure(text = self.getDatasetCountA())
        # self.labelQueryDataACount.configure(text = "" + str(len(self.datasetA['Data']))) ### TODO

        # Empty FILTER details of BOTH A and B
        self.queryResetFilterDetails(event)
        self.listQuerySetDataA.delete(0, END)

        return "break"

    def queryResetDatasetB(self, event):
        self.isReadyDatasetB = False  # When a dataset is reset, it is not ready
        self.checkIfDatasetReady()  # Update dataset status accordingly
        self.setDatasetStripeReady(False, self.labelQuerySetDataStripesB)

        self.buttonQueryResetFilterB.configure(relief = FLAT)
        self.datasetB = self.resetDataset()
        self.entryQuerySetDataB.configure(text = '')
        self.entryQueryFeature.configure(text = '')

        # self.labelFrameQueryDataB.configure(text = "Dataset B")
        self.labelQuerySetDataStatusB.configure(
            text = UI_support.SELECT_STATUS_NO_DATA_TEXT,
            background = Color_support.SELECT_LISTBOX_STATUS_BG,
            foreground = Color_support.SELECT_LISTBOX_STATUS_FG
        )

        # if self.datasetB['Data'] is []:
        self.datasetCountB = 0  # len(self.datasetB['Data'])
        self.labelQueryDataBCount.configure(text = self.getDatasetCountB())

        # Empty FILTER details of BOTH A and B
        self.queryResetFilterDetails(event)
        self.listQuerySetDataB.delete(0, END)

        return "break"

    def querySelectDataValuesA(self, event):
        self.isReadyDatasetA = False  # When a listbox element is de/selected, mark the dataset as not ready
        self.checkIfDatasetReady()  # Update dataset status accordingly
        self.setDatasetStripeReady(False, self.labelQuerySetDataStripesA)

        # self.datasetCountA = selectDatasetValues(event, self.datasetA, self.populationDataset)

        # Do search in populationDatasetOriginal, not filtered dataset A
        # selectDatasetValues(event, self.datasetA)
        self.datasetCountA = FS.selectDatasetValues(event, self.populationDatasetOriginalA)

        print ("Pop Dataset A" + str(len(self.populationDatasetOriginalA['Data'])))
        print ("Dataset A" + str(len(self.datasetA['Data'])))

        self.labelQueryDataACount.configure(text = self.getDatasetCountA())

    def querySelectDataValuesB(self, event):
        self.isReadyDatasetB = False  # When a listbox element is de/selected, mark the dataset as not ready
        self.checkIfDatasetReady()  # Update dataset status accordingly
        self.setDatasetStripeReady(False, self.labelQuerySetDataStripesB)

        # self.datasetCountB = selectDatasetValues(event, self.datasetB, self.populationDataset)

        # Do search in populationDatasetOriginal, not filtered dataset B
        # self.datasetCountB = selectDatasetValues(event, self.datasetB)
        self.datasetCountB = FS.selectDatasetValues(event, self.populationDatasetOriginalB)

        print ("Pop Dataset B" + str(len(self.populationDatasetOriginalB['Data'])))
        print ("Dataset B" + str(len(self.datasetB['Data'])))

        self.labelQueryDataBCount.configure(text = self.getDatasetCountB())

    def queryResetFilterDetails(self, event):
        # Empty FILTER details of BOTH A and B
        self.labelQueryDataA.configure(text = UI_support.SELECT_STATUS_NO_DATA_TEXT)
        self.listQueryDataA.delete(0, END)

        self.labelQueryDataB.configure(text = UI_support.SELECT_STATUS_NO_DATA_TEXT)
        self.listQueryDataB.delete(0, END)

        self.labelQueryDataFeatureName.configure(
            text = UI_support.FILTER_STATUS_NO_FEATURE_TEXT,
        )

    # endregion

    '''FILTER HEADER'''
    # region

    ''' Simultaneously scrolls the FILTER listbox A and B'''

    def scrollFilterListBox(self, event):  # To simultaneously scroll Filter listbox A and B
        self.listQueryDataA.yview("scroll", event.delta, "units")
        self.listQueryDataB.yview("scroll", event.delta, "units")
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"

    def queryAddFilterA(self, event):
        self.isReadyDatasetA = False
        self.buttonQueryAddFilterA.configure(relief = FLAT)
        print ("LEN (Prev) IS " + str(len(self.datasetA['Data'])))
        print ("Dataset A COUNT IS " + str(self.datasetCountA))

        # If the dataset is empty, do not push through with filtering.
        if len(self.datasetA['Data']) <= 0:
            tkMessageBox.showerror("Error: Empty dataset",
                                   "Dataset is empty. Please check if you uploaded your population dataset")
            # CLEAR filter feature box
            self.queryResetFilterDetails(event)

        # If there are 0 samples in the selection, do not push through with filtering
        elif self.datasetCountA <= 0:
            tkMessageBox.showerror("Error: No samples selected for A",
                                   "You must have at least 1 sample in your selection.")
            # CLEAR filter feature box
            self.queryResetFilterDetails(event)
            self.labelQuerySetDataStatusA.configure(
                text = UI_support.SELECT_STATUS_NO_DATA_TEXT,
                background = Color_support.SELECT_LISTBOX_STATUS_BG,
                foreground = Color_support.SELECT_LISTBOX_STATUS_FG
            )
            # return -1

        else:
            # CLEAR filter feature box first
            self.queryResetFilterDetails(event)
            self.isReadyDatasetA = True
            self.checkIfDatasetReady()
            self.datasetA = copy.deepcopy(self.populationDatasetOriginalA)

            # Filter the data given the feature inputted and its values selected
            try:
                new_data = FS.filterDataset(self.datasetA, self.datasetA['Feature'],
                                            self.datasetA['Feature']['Selected Responses'])
                # new_data = filterDataset(self.populationDatasetOriginalA, self.populationDatasetOriginalA['Feature'], self.populationDatasetOriginalA['Feature']['Selected Responses'])
            except KeyError:
                tkMessageBox.showerror("Error: No selected responses",
                                       "You did not select any responses. Please select at least one.")
                # return -1
                return "break"

            # Add the feature to the dataset's filtered features
            self.datasetA['Filter Features'].append(self.datasetA['Feature'])
            # self.populationDatasetOriginalA['Filter Features'].append(self.datasetA['Feature'])

            # Assign the new set of filtered data
            self.datasetA['Data'] = new_data
            # self.populationDatasetOriginalA['Data'] = new_data

            if (queryType == 'Sample vs Sample'):
                queryStrFilterA = ''
                # queryStrFilterA = 'Dataset A'
            else:
                # queryStrFilterA = 'Population'
                queryStrFilterA = ''

            # Write the breadcrumb trail of the features and values the dataset was filtered by
            for i in range(0, len(self.datasetA['Filter Features'])):
                # queryStrFilterA = queryStrFilterA + "->" + self.datasetA['Filter Features'][i]['Code']
                queryStrFilterA = " [ " + self.datasetA['Filter Features'][i]['Code'] + " | "
                for j in range(0, len(self.datasetA['Filter Features'][i]['Selected Responses'])):
                    # if j == 0:
                    #     queryStrFilterA = queryStrFilterA + " [ "
                    queryStrFilterA = queryStrFilterA + self.datasetA['Filter Features'][i]['Selected Responses'][j][
                        'Code'] + " "
                    if j == (len(self.datasetA['Filter Features'][i]['Selected Responses']) - 1):
                        queryStrFilterA = queryStrFilterA + "]"

            # self.labelFrameQueryDataA.configure(text = queryStrFilterA) ### TODO
            self.labelQuerySetDataStatusA.configure(
                text = UI_support.LBL_SELECT_READY + "" + queryStrFilterA,
                background = Color_support.SELECT_LISTBOX_STATUS_READY_BG,
                foreground = Color_support.SELECT_LISTBOX_STATUS_READY_FG
            )
            self.setDatasetStripeReady(True, self.labelQuerySetDataStripesA)
        print ("LEN (After) IS " + str(len(self.datasetA['Data'])))
        print ("Dataset A COUNT IS " + str(self.datasetCountA))
        print ("")
        return "break"

    def queryAddFilterB(self, event):
        self.isReadyDatasetB = False

        self.buttonQueryAddFilterB.configure(relief = FLAT)
        print ("LEN (Prev) IS " + str(len(self.datasetA['Data'])))
        print ("Dataset B COUNT IS " + str(self.datasetCountB))

        # If the dataset is empty, do not push through with filtering.
        if len(self.datasetB['Data']) <= 0:
            tkMessageBox.showerror("Error: Empty dataset",
                                   "Dataset is empty. Please check if you uploaded your population dataset")
            # CLEAR filter feature box
            self.queryResetFilterDetails(event)


        # If there are 0 samples in the selection, do not push through with filtering
        elif self.datasetCountB <= 0:
            tkMessageBox.showerror("Error: No samples selected for B",
                                   "You must have at least 1 sample in your selection.")
            # CLEAR filter feature box
            self.queryResetFilterDetails(event)

            self.labelQuerySetDataStatusB.configure(
                text = UI_support.SELECT_STATUS_NO_DATA_TEXT,
                background = Color_support.SELECT_LISTBOX_STATUS_BG,
                foreground = Color_support.SELECT_LISTBOX_STATUS_FG
            )
            # return -1

        else:
            # CLEAR filter feature box first
            self.queryResetFilterDetails(event)
            self.isReadyDatasetB = True
            self.checkIfDatasetReady()
            self.datasetB = copy.deepcopy(self.populationDatasetOriginalB)

            # Filter the data given the feature inputted and its values selected

            try:
                new_data = FS.filterDataset(self.datasetB, self.datasetB['Feature'],
                                            self.datasetB['Feature']['Selected Responses'])
            except KeyError:
                tkMessageBox.showerror("Error: No selected responses",
                                       "You did not select any responses. Please select at least one.")
                # return -1
                return "break"

            # Add the feature to the dataset's filtered features
            self.datasetB['Filter Features'].append(self.datasetB['Feature'])

            # Assign the new set of filtered data
            self.datasetB['Data'] = new_data

            if (queryType == 'Sample vs Sample'):  ### TODO
                queryStrFilterB = ''
            else:
                queryStrFilterB = ''

            # Write the breadcrumb trail of the features and values the dataset was filtered by
            for i in range(0, len(self.datasetB['Filter Features'])):
                # queryStrFilterB = queryStrFilterB + "->" + self.datasetB['Filter Features'][i]['Code']
                queryStrFilterB = " [ " + self.datasetB['Filter Features'][i]['Code'] + " | "
                for j in range(0, len(self.datasetB['Filter Features'][i]['Selected Responses'])):
                    # if j == 0:
                    #     queryStrFilterB = queryStrFilterB + "("
                    queryStrFilterB = queryStrFilterB + self.datasetB['Filter Features'][i]['Selected Responses'][j][
                        'Code'] + " "
                    if j == (len(self.datasetB['Filter Features'][i]['Selected Responses']) - 1):
                        queryStrFilterB = queryStrFilterB + "]"

            # Concat the Filter String Here
            # self.labelFrameQueryDataB.configure(text = queryStrFilterB)
            self.labelQuerySetDataStatusB.configure(
                text = UI_support.LBL_SELECT_READY + "" + queryStrFilterB,
                background = Color_support.SELECT_LISTBOX_STATUS_READY_BG,
                foreground = Color_support.SELECT_LISTBOX_STATUS_READY_FG
            )
            self.setDatasetStripeReady(True, self.labelQuerySetDataStripesB)

        print ("LEN (After) IS " + str(len(self.datasetA['Data'])))
        print ("Dataset B COUNT IS " + str(self.datasetCountB))
        print ("")
        return "break"

    def querySetFeature(self, event):
        if self.buttonQueryFeature_state is not DISABLED:
            entryQuery = self.entryQueryFeature.get()

            # If the dataset is empty, do not continue finding the feature
            if (len(self.datasetA['Data']) <= 0 or len(self.datasetB['Data']) <= 0):
                tkMessageBox.showerror("Error: Empty dataset",
                                       "Dataset is empty. Please check if you uploaded your population dataset")
                self.setFilterStripeReady(False, self.labelFilterStripes)
                # CLEAR filter feature box
                self.queryResetFilterDetails(event)

            # If one of the sample groups is empty, do not continue finding the feature
            elif self.datasetCountA <= 0:
                tkMessageBox.showerror("Error: No samples selected for A",
                                       "You must have at least 1 sample in your selection.")
                self.setFilterStripeReady(False, self.labelFilterStripes)
                # CLEAR filter feature box
                self.queryResetFilterDetails(event)

            elif self.datasetCountB <= 0:
                tkMessageBox.showerror("Error: No samples selected for B",
                                       "You must have at least 1 sample in your selection.")
                self.setFilterStripeReady(False, self.labelFilterStripes)
                # CLEAR filter feature box
                self.queryResetFilterDetails(event)

            else:
                try:
                    self.querySetFeatureA(entryQuery)
                    self.querySetFeatureB(entryQuery)
                    self.setFilterStripeReady(True, self.labelFilterStripes)

                    # Get the feature description
                    featureDesc = self.datasetA['Focus Feature'][
                        'Description']  # Doesn't matter if you use datasetA or datasetB

                    # If the description is too long
                    if len(featureDesc) > 70:
                        featureDesc = featureDesc[:71] + '...'  # Shorten it

                    # Display the description
                    self.labelQueryDataFeatureName.config(text = UI_support.FILTER_STATUS_CONFIRMED_TEXT + featureDesc)

                except NameError:
                    tkMessageBox.showerror("Error: No features",
                                           "Features not found. Please upload your variable description file.")
                    self.setFilterStripeReady(False, self.labelFilterStripes)
                except:
                    print ("Exception in " + "def querySetFeature(self, event)")
        return "break"

    ''' Find the feature and display the dataset's frequencies and proportions for each of its values '''

    def querySetFeatureA(self, entryQuery):
        # findFeature(entryQuery, self.listQueryDataA, self.datasetA,"Focus_Feature")
        self.findFeature(entryQuery, self.listQueryDataA, self.datasetA, self.populationDatasetOriginalA, False,
                         "Focus_Feature")


    ''' Find the feature and display the dataset's frequencies and proportions for each of its values '''

    def querySetFeatureB(self, entryQuery):
        # findFeature(entryQuery, self.listQueryDataB, self.datasetB, "Focus_Feature")
        self.findFeature(entryQuery, self.listQueryDataB, self.datasetB, self.populationDatasetOriginalB, True,
                         "Focus_Feature")

    # endregion

    '''TEST HEADER'''

    # region

    def selectOptionChiSquare(self, event):

        # Change button appearance to selected
        self.buttonChooseChiSquare.configure(
            background = Color_support.PROCESS_CHI_SQUARE_TITLE_FG,
            foreground = Color_support.PROCESS_CHI_SQUARE_TITLE_BG
        )

        # Revert other buttons to deselected
        self.buttonChooseZTest.configure(
            background = Color_support.PROCESS_Z_TEST_TITLE_BG,
            foreground = Color_support.PROCESS_Z_TEST_TITLE_FG,
        )

        # Show Z-Test options
        self.hideWidget(self.labelFrameProcessZTest)
        # Hide Chi-square options
        self.showWidget(self.labelFrameProcessChiSquare)

    def selectOptionZTest(self, event):
        # Change button appearance to selected
        self.buttonChooseZTest.configure(
            background = Color_support.PROCESS_CHI_SQUARE_TITLE_FG,
            foreground = Color_support.PROCESS_CHI_SQUARE_TITLE_BG
        )
        # Revert other buttons to deselected
        self.buttonChooseChiSquare.configure(
            background = Color_support.PROCESS_Z_TEST_TITLE_BG,
            foreground = Color_support.PROCESS_Z_TEST_TITLE_FG,
        )

        # Show Z-Test options
        self.hideWidget(self.labelFrameProcessChiSquare)
        # Hide Chi-square options
        self.showWidget(self.labelFrameProcessZTest)

    '''CONSOLE HEADER'''

    # region

    def clearConsole(self):
        self.listConsoleScreen.delete(0, END)

    def addToConsole(self, consoleItem, consoleScreen):
        if self.dictConsoleScreens[consoleScreen] == const.SCREENS.Z_TEST:
            targetScreen = self.listConsoleZTestScreen

        elif self.dictConsoleScreens[consoleScreen] == const.SCREENS.CHI_SQUARE:
            targetScreen = self.listConsoleChiSquareScreen

        elif self.dictConsoleScreens[consoleScreen] == const.SCREENS.QUEUE:
            targetScreen = self.listConsoleQueueScreen

        else:
            targetScreen = self.listConsoleScreen

        targetScreen.configure(state = NORMAL)

        targetScreen.insert(END, consoleItem)
        targetScreen.tag_add(const.CONSOLE.DEFAULT, '1.0', END)

        targetScreen.configure(state = DISABLED)

    '''Select a single line in the console screen Text widget'''

    def selectConsoleEntry(self, event, consoleScreen):
        # Enable console
        consoleScreen.configure(state = NORMAL)

        # Clear previous highlights by deleting the old tag
        consoleScreen.tag_delete(const.CONSOLE.SELECT)

        # Reconfigure tag settings
        consoleScreen.tag_configure(const.CONSOLE.SELECT,
                                    background = Color_support.FUSCHIA,
                                    foreground = Color_support.WHITE
                                    )

        # Get current insert index
        insertIndex = float(consoleScreen.index(tk.INSERT))

        # Get the highlight index by taking the floor and ceiling of the insert index
        start = math.floor(insertIndex)
        indexStart = str(start)
        end = start + 1
        indexEnd = str(end)
        # print(str(insertIndex))
        # print("S " + str(indexStart))
        # print("E " + str(indexEnd))
        # self.listConsoleScreen.tag_raise("sel")
        # self.listConsoleScreen.tag_bind(CONSTANTS.CONSOLE.SELECT, show_hand_cursor)

        if consoleScreen.get(indexStart, indexEnd).strip() != '':
            # Highlight the range by specifying the tag
            consoleScreen.tag_add(const.CONSOLE.SELECT, indexStart, indexEnd)

        # Disable the entry to prevent editing
        consoleScreen.configure(state = DISABLED)

    def highlightEntry(self, consoleScreen):
        consoleScreen.text.tag_remove("current_line", 1.0, "end")
        consoleScreen.text.tag_add("current_line", "insert linestart", "insert lineend+1c")

    def showConsoleScreen(self, event, consoleScreen):

        # Hide all screens first
        self.hideWidget(self.listConsoleScreen)
        self.hideWidget(self.listConsoleQueueScreen)
        self.hideWidget(self.listConsoleZTestScreen)
        self.hideWidget(self.listConsoleChiSquareScreen)

        # Reset relief
        self.buttonConsoleAll['relief'] = FLAT
        self.buttonConsoleZTest['relief'] = FLAT
        self.buttonConsoleChiSquare['relief'] = FLAT
        self.buttonConsoleQueue['relief'] = FLAT

        # Reset background color
        self.buttonConsoleAll['background'] = Color_support.WHITE
        self.buttonConsoleZTest['background'] = Color_support.WHITE
        self.buttonConsoleChiSquare['background'] = Color_support.WHITE
        self.buttonConsoleQueue['background'] = Color_support.WHITE

        # Reset foreground color
        self.buttonConsoleAll['foreground'] = Color_support.FG_COLOR
        self.buttonConsoleZTest['foreground'] = Color_support.FG_COLOR
        self.buttonConsoleChiSquare['foreground'] = Color_support.FG_COLOR
        self.buttonConsoleQueue['foreground'] = Color_support.FG_COLOR

        if self.dictConsoleScreens[consoleScreen] == const.SCREENS.QUEUE:
            self.showWidget(self.listConsoleQueueScreen)
            self.labelConsoleScreenTaskBar['text'] = '''QUEUE'''
            self.buttonConsoleQueue['background'] = Color_support.FUSCHIA
            self.buttonConsoleQueue['foreground'] = Color_support.WHITE
            self.buttonConsoleQueue['relief'] = GROOVE

        elif self.dictConsoleScreens[consoleScreen] == const.SCREENS.Z_TEST:
            self.showWidget(self.listConsoleZTestScreen)
            self.labelConsoleScreenTaskBar['text'] = '''Z-TEST'''
            self.buttonConsoleZTest['background'] = Color_support.FUSCHIA
            self.buttonConsoleZTest['foreground'] = Color_support.WHITE
            self.buttonConsoleZTest['relief'] = GROOVE


        elif self.dictConsoleScreens[consoleScreen] == const.SCREENS.CHI_SQUARE:
            self.showWidget(self.listConsoleChiSquareScreen)
            self.labelConsoleScreenTaskBar['text'] = '''CHI-SQUARE'''
            self.buttonConsoleChiSquare['background'] = Color_support.FUSCHIA
            self.buttonConsoleChiSquare['foreground'] = Color_support.WHITE
            self.buttonConsoleChiSquare['relief'] = GROOVE


        else:
            self.showWidget(self.listConsoleScreen)
            self.labelConsoleScreenTaskBar['text'] = '''ALL'''
            self.buttonConsoleAll['background'] = Color_support.FUSCHIA
            self.buttonConsoleAll['foreground'] = Color_support.WHITE
            self.buttonConsoleAll['relief'] = GROOVE

    """ >>> HELPER FUNCTIONS CALLED BY BOUNDED ELEMENTS (e.g. enter, leave) <<< """

    # TODO Optimize (avoid resizing, keep a reference)
    # region
    def enterCheckIcon(self, event, iconSize = Icon_support.SELECT_ICO_SIZE):
        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK_ON).resize(iconSize, PIL.Image.ANTIALIAS)

        btn_check_icon = PIL.ImageTk.PhotoImage(im)
        item = event.widget
        item.configure(
            image = btn_check_icon)
        item.image = btn_check_icon  # < ! > Required to make images appear

    def leaveCheckIcon(self, event, iconSize = Icon_support.SELECT_ICO_SIZE):
        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(iconSize, PIL.Image.ANTIALIAS)
        btn_check_icon = PIL.ImageTk.PhotoImage(im)
        item = event.widget
        item.configure(
            image = btn_check_icon)
        item.image = btn_check_icon  # < ! > Required to make images appear

    def enterCrossIcon(self, event, iconSize = Icon_support.SELECT_ICO_SIZE):
        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS_ON).resize(iconSize, PIL.Image.ANTIALIAS)

        btn_cross_icon = PIL.ImageTk.PhotoImage(im)
        item = event.widget
        item.configure(
            image = btn_cross_icon)
        item.image = btn_cross_icon  # < ! > Required to make images appear

    def leaveCrossIcon(self, event, iconSize = Icon_support.SELECT_ICO_SIZE):
        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(iconSize, PIL.Image.ANTIALIAS)
        btn_cross_icon = PIL.ImageTk.PhotoImage(im)
        item = event.widget
        item.configure(
            image = btn_cross_icon)
        item.image = btn_cross_icon  # < ! > Required to make images appear

    def enterAddIcon(self, event, iconSize = Icon_support.SELECT_ICO_SIZE):
        im = PIL.Image.open(Icon_support.TAB_ICO_ADD_ON).resize(iconSize, PIL.Image.ANTIALIAS)

        btn_add_icon = PIL.ImageTk.PhotoImage(im)
        item = event.widget
        item.configure(
            image = btn_add_icon)
        item.image = btn_add_icon  # < ! > Required to make images appear

    def leaveAddIcon(self, event, iconSize = Icon_support.SELECT_ICO_SIZE):
        im = PIL.Image.open(Icon_support.TAB_ICO_ADD).resize(iconSize, PIL.Image.ANTIALIAS)
        btn_add_icon = PIL.ImageTk.PhotoImage(im)
        item = event.widget
        item.configure(
            image = btn_add_icon)
        item.image = btn_add_icon  # < ! > Required to make images appear

    def enterDownArrowIcon(self, event, iconSize = Icon_support.SELECT_ICO_SIZE):
        item = event.widget

        im = PIL.Image.open(Icon_support.TAB_ICO_DOWN_ARROW_ON).resize(iconSize, PIL.Image.ANTIALIAS)

        btn_down_arrow_icon = PIL.ImageTk.PhotoImage(im)
        item.configure(
            image = btn_down_arrow_icon)
        item.image = btn_down_arrow_icon  # < ! > Required to make images appear

    def leaveDownArrowIcon(self, event, iconSize = Icon_support.SELECT_ICO_SIZE):
        im = PIL.Image.open(Icon_support.TAB_ICO_DOWN_ARROW).resize(iconSize, PIL.Image.ANTIALIAS)
        btn_down_arrow_icon = PIL.ImageTk.PhotoImage(im)
        item = event.widget
        item.configure(
            image = btn_down_arrow_icon)
        item.image = btn_down_arrow_icon  # < ! > Required to make images appear

    def enterRightArrowIcon(self, event, iconSize = Icon_support.RUN_ICO_SIZE):
        item = event.widget

        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW_ON).resize(iconSize, PIL.Image.ANTIALIAS)

        btn_right_arrow_icon = PIL.ImageTk.PhotoImage(im)
        item.configure(
            image = btn_right_arrow_icon)
        item.image = btn_right_arrow_icon  # < ! > Required to make images appear

    def leaveRightArrowIcon(self, event, iconSize = Icon_support.RUN_ICO_SIZE):
        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW).resize(iconSize, PIL.Image.ANTIALIAS)
        btn_right_arrow_icon = PIL.ImageTk.PhotoImage(im)
        item = event.widget
        item.configure(
            image = btn_right_arrow_icon)
        item.image = btn_right_arrow_icon  # < ! > Required to make images appear

    def enterRightArrowPlainIcon(self, event, state = NORMAL, iconSize = Icon_support.SELECT_ICO_SIZE_BUTTONS):
        if state != DISABLED:
            item = event.widget
            im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW_PLAIN_ON).resize(iconSize, PIL.Image.ANTIALIAS)

            btn_right_arrow_icon = PIL.ImageTk.PhotoImage(im)
            item.configure(
                image = btn_right_arrow_icon)
            item.image = btn_right_arrow_icon  # < ! > Required to make images appear

    def leaveRightArrowPlainIcon(self, event, state = NORMAL, iconSize = Icon_support.SELECT_ICO_SIZE_BUTTONS):
        if state != DISABLED:
            item = event.widget
            if item['state'] != DISABLED:
                im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW_PLAIN).resize(iconSize, PIL.Image.ANTIALIAS)
                btn_right_arrow_icon = PIL.ImageTk.PhotoImage(im)
                item.configure(
                    image = btn_right_arrow_icon)
                item.image = btn_right_arrow_icon  # < ! > Required to make images appear

    def enterQueryZTest(self, event):
        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK_ON).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_z_test_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryZTest.configure(
            image = btn_query_z_test_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryZTest.image = btn_query_z_test_icon  # < ! > Required to make images appear

    def leaveQueryZTest(self, event):
        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_z_test_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryZTest.configure(
            image = btn_query_z_test_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryZTest.image = btn_query_z_test_icon  # < ! > Required to make images appear

    # endregion

    """ >>> GENERAL HELPER FUNCTIONS <<< """

    def checkIfDatasetReady(self):
        if not self.isReadyDatasetA:  # If Dataset A is not ready
            # Clear and disable filter features option
            self.disableFilter()
            self.setDatasetStatusReady(False, self.labelQuerySetDataStatusA, self.labelQuerySetDataStripesA)

        if not self.isReadyDatasetB:  # If Dataset B is not ready
            # Clear and disable filter features option
            self.disableFilter()
            self.setDatasetStatusReady(False, self.labelQuerySetDataStatusB, self.labelQuerySetDataStripesB)

        if self.isReadyDatasetA and self.isReadyDatasetB:  # If both are ready
            # Enable filter feature option
            self.enableFilter()

    def disableFilter(self):
        # Clear filter results
        event = None
        self.queryResetFilterDetails(event)

        # Disable entry
        self.entryQueryFeature.configure(
            state = DISABLED
        )
        # Disable button
        self.buttonQueryFeature_state = DISABLED

        # Disable feature name
        self.labelQueryDataFeatureName.configure(
            background = Color_support.FILTER_LISTBOX_FEATURE_STATUS_BG,
            foreground = Color_support.FILTER_LISTBOX_FEATURE_STATUS_FG,
            text = UI_support.FILTER_STATUS_NO_FEATURE_TEXT
        )

        # Show lock cover
        self.labelOverlayFilterListData.place(
            relx = UI_support.getRelX(self.labelFrameFilterListData),
            rely = UI_support.getRelY(self.labelFrameFilterListData),
            relwidth = UI_support.getRelW(self.labelFrameFilterListData),
            relheight = UI_support.getRelH(self.labelFrameFilterListData))

        # Change stripe color
        self.setFilterStripeReady(False, self.labelFilterStripes)

    def enableFilter(self):
        # Enable entry
        self.entryQueryFeature.configure(
            state = NORMAL
        )
        # Enable button
        self.buttonQueryFeature_state = NORMAL

        # Enable feature name
        self.labelQueryDataFeatureName.configure(
            background = Color_support.FILTER_LISTBOX_FEATURE_STATUS_ON_BG,
            foreground = Color_support.FILTER_LISTBOX_FEATURE_STATUS_ON_FG,
            text = UI_support.FILTER_STATUS_READY_TEXT
        )

        # Hide lock cover
        self.labelOverlayFilterListData.place(
            relx = FS.getRelX(self.labelFrameFilterListData), rely = FS.getRelY(self.labelFrameFilterListData),
            relwidth = 0, relheight = 0)

        # Change stripe color
        self.setFilterStripeReady(False, self.labelFilterStripes)

    def setDatasetStatusReady(self, isReady, statusWidget, stripeWidget):
        if isReady:
            statusWidget.configure(
                background = Color_support.SELECT_LISTBOX_STATUS_READY_BG,
                foreground = Color_support.SELECT_LISTBOX_STATUS_READY_FG,
                relief = GROOVE
            )
        else:
            statusWidget.configure(
                text = UI_support.SELECT_STATUS_NO_DATA_TEXT,
                background = Color_support.SELECT_LISTBOX_STATUS_BG,
                foreground = Color_support.SELECT_LISTBOX_STATUS_FG,
                relief = UI_support.SELECT_LISTBOX_RELIEF
            )

    def setDatasetStripeReady(self, isReady, stripeWidget):
        if isReady:
            im = PIL.Image.open(Icon_support.TEXTURE_STRIPE_LIME)
            texture_lime_stripes = PIL.ImageTk.PhotoImage(im)
            stripeWidget.configure(
                image = texture_lime_stripes
            )
            stripeWidget.image = texture_lime_stripes  # < ! > Required to make images appear
        else:
            im = PIL.Image.open(Icon_support.TEXTURE_STRIPE_PINK)
            texture_pink_stripes = PIL.ImageTk.PhotoImage(im)
            stripeWidget.configure(
                image = texture_pink_stripes
            )
            stripeWidget.image = texture_pink_stripes

    def setFilterStripeReady(self, isReady, stripeWidget):
        if isReady:
            im = PIL.Image.open(Icon_support.TEXTURE_STRIPE_LIME)
            texture_lime_stripes = PIL.ImageTk.PhotoImage(im)
            stripeWidget.configure(
                image = texture_lime_stripes
            )
            stripeWidget.image = texture_lime_stripes  # < ! > Required to make images appear
        else:
            im = PIL.Image.open(Icon_support.TEXTURE_STRIPE_ORANGE)
            texture_orange_stripes = PIL.ImageTk.PhotoImage(im)
            stripeWidget.configure(
                image = texture_orange_stripes
            )
            stripeWidget.image = texture_orange_stripes

    """
    Hides the widget by setting its relative width and height to 0.
    Use showWidget() to make the widget re-appear.
    Always set the widget's 'name' first.
    """

    def hideWidget(self, widget):
        widget.update()

        # Store widget width and height if it's not in the dictionary
        widgetName = self.getWidgetName(widget)
        if not (widgetName + '_W' in self.dictWidgetPlace):
            self.dictWidgetPlace[widgetName + '_W'] = UI_support.getRelW(widget)
            self.dictWidgetPlace[widgetName + '_H'] = UI_support.getRelH(widget)

        # Set widget width and height to 0
        widget.place(relwidth = 0, relheight = 0)

    def showWidget(self, widget):

        widgetName = self.getWidgetName(widget)

        # Retrieve widget width and height if it's in the dictionary
        if (widgetName + '_W' in self.dictWidgetPlace):
            widgetWidth = self.dictWidgetPlace[widgetName + '_W']
            widgetHeight = self.dictWidgetPlace[widgetName + '_H']

            # Set widget width and height
            widget.place(relwidth = widgetWidth, relheight = widgetHeight)

            # Remove keys from dictionary
            self.dictWidgetPlace.pop(widgetName + '_W', None)
            self.dictWidgetPlace.pop(widgetName + '_H', None)

        widget.update()

    def getWidgetName(self, widget):
        # print("widget name:", str(widget).split(".")[-1])
        return str(widget).split(".")[-1]

    '''
    Clears all of the filters of the dataset and resets the data back to that of
    the uploaded population file. 
    '''

    def resetDataset(self):

        new_dataset = {'Data': [], 'Filter Features': []}
        try:
            populationDataset = FS.readCSVDict(self.populationDir)
            for record in populationDataset:
                new_dataset['Data'].append(record)
            return new_dataset
        except:
            new_dataset = {'Data': [], 'Filter Features': []}
            return new_dataset

    def getDatasetCountA(self):
        return str(self.datasetCountA)

    def getDatasetCountB(self):
        return str(self.datasetCountB)

    # endregion
