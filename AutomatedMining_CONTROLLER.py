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

        # self.configureTestTabBindings()
        # self.initializeVariables()

    def configureViewBindings(self):
        button = self.view.getBtnConfirmFeatureSelect()
        button.bind('<Button-1>', self.confirmFeatureSelect)

        button = self.view.getBtnConfirmConfirmedFeatures()
        button.bind('<Button-1>', self.confirmConfirmedFeatures)

        button = self.view.getBtnResetFeatureSelect()
        button.bind('<Button-1>', self.model.resetFeatureSelect)

        button = self.view.getBtnQueryFeatureList()
        button.bind('<Button-1>', self.queryFeatureID)

        listbox = self.view.getLbListFeatureSelect()
        listbox.bind('<<ListboxSelect>>', self.selectFeature)

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

    def selectFeature(self, event):
        listbox = event.widget
        selectedIndices = listbox.curselection()

        lastSelectedIndex = self.model.viewModel.updateSelectedFeatures(listbox, selectedIndices)
        # lastSelectedIndex = listbox.get(lastSelectedIndex)

        response = self.model.updateSelectedFeatureResponse(lastSelectedIndex)
        self.view.updateLbListFeatureDetails(response)


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

        print "UPLOADED"
        return True

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