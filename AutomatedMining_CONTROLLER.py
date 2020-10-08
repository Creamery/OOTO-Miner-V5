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


        self.configureViewBindings()
        self.configureConsoleViewBindings()
        self.initializeVariables()

    def initializeVariables(self):
        self.showConsoleScreen(None, self.listConsoleScreen)

    def configureViewBindings(self):
        button = self.view.getBtnConfirmFeatureSelect()
        button.bind('<Button-1>', self.confirmFeatureSelect)

        button = self.view.getBtnConfirmConfirmedFeatures()
        button.bind('<Button-1>', self.confirmConfirmedFeatures)

        button = self.view.getBtnResetFeatureSelect()
        button.bind('<Button-1>', self.resetListboxEvent)

        button = self.view.getBtnResetConfirmedFeatures()
        button.bind('<Button-1>', self.resetListboxEvent)

        button = self.view.getBtnQueryFeatureList()
        button.bind('<Button-1>', self.queryFeatureID)

        listbox = self.view.getLbListFeatureSelect()
        listbox.bind('<<ListboxSelect>>', self.selectFeatureEvent)

        listbox = self.view.getLbListConfirmedFeatures()
        listbox.bind('<<ListboxSelect>>', self.selectConfirmedFeatureEvent)

        # TODO Entry Change

    def confirmFeatureSelect(self, event):
        # set model's confirmed features
        confirmedFeatures = self.model.confirmFeatureSelect()
        # update view's confirmed features listbox
        self.view.updateLbListConfirmedFeatures(confirmedFeatures)
        return "break"

    def confirmConfirmedFeatures(self, event):
        self.model.confirmConfirmedFeatures(self.root)
        return "break"

    def queryFeatureID(self, event):
        print "queryFeatureID"
        # get featureID from entry widget
        featureID = self.view.getEntryQueryFeatureList().get()

        queryFeatureList = self.model.queryFeature(featureID)

        self.view.updateLbListFeatureSelect(queryFeatureList)

        # update model with listbox contents
        listbox = self.view.getLbListFeatureSelect()
        responseListbox = self.view.getLbListFeatureResponses()
        self.selectFeature(listbox)

        # update model's confirmed features
        self.confirmFeatureSelect(event)

    def selectFeatureEvent(self, event):
        listbox = event.widget
        self.selectFeature(listbox)

    def selectConfirmedFeatureEvent(self, event):
        listbox = event.widget
        self.selectFeature(listbox)

    def selectFeature(self, listbox):
        selectedIndices = listbox.curselection()
        print "selected indices"
        print str(selectedIndices)

        if listbox is self.view.getLbListFeatureSelect():
            lastSelectedIndex = self.model.viewModel.updateSelectedFeatures(listbox, selectedIndices)
            # update the model for the given response listbox
            response = self.model.updateSelectedFeatureResponse(lastSelectedIndex)
            self.view.updateLbListFeatureResponses(response)
        else:
            lastSelectedIndex = self.model.viewModel.updateConfirmedSelectedFeatures(listbox, selectedIndices)
            # update the model for the given response listbox
            response = self.model.updateConfirmedFeatureResponse(lastSelectedIndex)
            self.view.updateLbListConfirmedFeatureResponses(response)

        return "break"

    def resetListboxEvent(self, event):
        button = event.widget

        # reset feature select
        if button is self.view.getBtnResetFeatureSelect():
            self.model.resetFeatureSelect()
            # self.view.updateLbListFeatureSelect()

        # reset confirmed features
        elif button is self.view.getBtnResetConfirmedFeatures():
            confirmedFeatures = self.model.resetConfirmedFeatures()
            self.view.updateLbListConfirmedFeatures(confirmedFeatures)

        return "break"

    def readFeatures(self, variableDescription, itemMarker):
        features = FS.readFeatures(variableDescription, itemMarker)
        if (len(features)) <= 0:
            return False
        else:
            self.model.readFeatures(features)
            self.model.readFeatureNames(features)
            # print "FEATURES " + str(type(features[0]))
            return True

    def uploadDataset(self, dirPopulation):

        self.model.readDataset(dirPopulation)

        print "UPLOADED"
        return True


    def configureConsoleViewBindings(self):

        # GENERAL
        self.dictConsoleScreens = self.view.getDictConsoleScreens()

        # LABELS
        self.labelConsoleScreenTaskBar = self.view.getLabelConsoleScreenTaskBar()


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
        # self.buttonQuerySetDataA.bind("<Enter>", self.enterRightArrowPlainIcon)
        # self.buttonQuerySetDataA.bind("<Leave>", self.leaveRightArrowPlainIcon)

        # self.buttonQuerySetDataB.bind("<Enter>", self.enterRightArrowPlainIcon)
        # self.buttonQuerySetDataB.bind("<Leave>", self.leaveRightArrowPlainIcon)
        # self.buttonQuerySetDataB.bind("<Enter>", lambda event, iconSize =  Icon_support.SELECT_ICO_SIZE_BUTTONS: self.enterRightArrowIcon(event, Icon_support.SELECT_ICO_SIZE_BUTTONS))
        # self.buttonQuerySetDataB.bind("<Leave>", self.leaveRightArrowIcon(Icon_support.SELECT_ICO_SIZE_BUTTONS))

        # self.buttonQueryAddFilterA.bind("<Enter>", self.enterCheckIcon)
        # self.buttonQueryAddFilterA.bind("<Leave>", self.leaveCheckIcon)

        # self.buttonQueryAddFilterB.bind("<Enter>", self.enterCheckIcon)
        # self.buttonQueryAddFilterB.bind("<Leave>", self.leaveCheckIcon)

        # self.buttonQueryFeature.bind("<Enter>", self.enterRightArrowPlainIcon)
        # self.buttonQueryFeature.bind("<Leave>", self.leaveRightArrowPlainIcon)
        # self.buttonQueryFeature.bind("<Enter>",
        #                              lambda event: self.enterRightArrowPlainIcon(event, self.buttonQueryFeature_state))
        # self.buttonQueryFeature.bind("<Leave>",
        #                              lambda event: self.leaveRightArrowPlainIcon(event, self.buttonQueryFeature_state))

        # self.buttonQueryZTest.bind("<Enter>", self.enterCheckIcon)
        # self.buttonQueryZTest.bind("<Leave>", self.leaveCheckIcon)

        # self.buttonQueue.bind("<Enter>", self.enterAddIcon)
        # self.buttonQueue.bind("<Leave>", self.leaveAddIcon)
        # self.buttonQueue.bind("<Enter>", self.enterDownArrowIcon)
        # self.buttonQueue.bind("<Leave>", self.leaveDownArrowIcon)

        # self.buttonClearQueue.bind("<Enter>", self.enterCrossIcon)
        # self.buttonClearQueue.bind("<Leave>", self.leaveCrossIcon)

        # self.buttonTestQueue.bind("<Enter>", self.enterRightArrowIcon)
        # self.buttonTestQueue.bind("<Leave>", self.leaveRightArrowIcon)

        # self.buttonQueryResetFilterA.bind("<Enter>", self.enterCrossIcon)
        # self.buttonQueryResetFilterA.bind("<Leave>", self.leaveCrossIcon)

        # self.buttonQueryResetFilterB.bind("<Enter>", self.enterCrossIcon)
        # self.buttonQueryResetFilterB.bind("<Leave>", self.leaveCrossIcon)

        # LISTBOX
        # self.listQuerySetDataA = self.view.getListQuerySetDataA()
        # self.listQuerySetDataA.bind('<<ListboxSelect>>', self.querySelectDataValuesA)
        # self.listQuerySetDataB = self.view.getListQuerySetDataB()
        # self.listQuerySetDataB.bind('<<ListboxSelect>>', self.querySelectDataValuesB)

        # self.listQueryDataA = self.view.getListQueryDataA()
        # self.listQueryDataA.bind('<<ListboxSelect>>', self.setFocusFeatureValues)
        # self.listQueryDataB = self.view.getListQueryDataB()
        # self.listQueryDataB.bind('<<ListboxSelect>>', self.setFocusFeatureValues)


        # MOUSEWHEEL
        # self.listQueryDataA.bind("<MouseWheel>", self.scrollFilterListBox)
        # self.listQueryDataB.bind("<MouseWheel>", self.scrollFilterListBox)

        # COMBOBOX
        # self.comboQueryTest = self.view.getComboQueryTest()
        # self.comboQueryTest.bind('<<ComboboxSelected>>', self.querySetType)


    '''CONSOLE HEADER'''
    # region console functions
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
    # endregion console functions