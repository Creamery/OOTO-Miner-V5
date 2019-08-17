
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

import tkMessageBox
import UI_support
import Function_support as FS
from tkFileDialog import askopenfilename
import CONSTANTS as const

import SampleVsSample as svs
import os
import numpy as np
from collections import Counter

import csv
import copy

class Input_Controller:

    def __init__(self, view):
        self.view = view
        self.configureDataTabBindings()

    ''' --> Binding elements under the DATA ("DATA") TAB (1) <-- '''

    def configureDataTabBindings(self):
        # TODO Add integrity check - if ENTRY is edited, change the file input
        self.buttonInitialVarDesc = self.view.getButtonInitialVarDesc()
        self.buttonInitialVarDesc.bind('<Button-1>', self.selectInitVarDesc)
        self.buttonQueryPopulation = self.view.getButtonQueryPopulation()
        self.buttonQueryPopulation.bind('<Button-1>', self.selectSetPopulation)

        self.buttonVariableFile = self.view.getButtonVariableFile()
        self.buttonVariableFile.bind('<Button-1>', self.getVariableFile)
        self.buttonValuesFile = self.view.getButtonValuesFile()
        self.buttonValuesFile.bind('<Button-1>', self.getValuesFile)

        # self.buttonStartVariableDescriptor.bind('<Button-1>', self.makeInitialVarDesc) ### TODO
        self.buttonStartDatasetUpload = self.view.getButtonStartDatasetUpload()
        # self.buttonStartDatasetUpload.bind('<Button-1>', self.uploadDataset)

        self.entryInitialVarDesc = self.view.getEntryInitialVarDesc()
        self.entryQueryPopulation = self.view.getEntryQueryPopulation()
        self.entryVariableFile = self.view.getEntryVariableFile()
        self.entryValuesFile = self.view.getEntryValuesFile()


    ''' Selects the variable description file '''

    def selectInitVarDesc(self, evt):
        self.hasUploadedVariableDescription = False

        self.initVarDisc = askopenfilename(title = "Select file",
                                           filetypes = (("csv files", "*.csv"), ("all files", "*.*")))

        if len(self.initVarDisc) == 0:
            tkMessageBox.showerror("Error: Upload Variable description",
                                   "Please select a valid variable description file.")
        else:
            self.hasUploadedVariableDescription = True
            self.entryInitialVarDesc.delete(0, END)
            self.entryInitialVarDesc.insert(0, self.initVarDisc)

        return "break"  # this "unsinks" the button after opening the file explorer

    ''' Selects the population module file '''

    def selectSetPopulation(self, evt):
        self.hasUploadedPopulation = False

        global populationDir
        populationDir = askopenfilename(title = "Select file",
                                        filetypes = (("csv files", "*.csv"), ("all files", "*.*")))

        if len(populationDir) == 0:
            tkMessageBox.showerror("Error: Upload error", "Please select a valid population dataset.")
        else:
            self.hasUploadedPopulation = True
            self.entryQueryPopulation.delete(0, END)
            self.entryQueryPopulation.insert(0, populationDir)
        return "break"

    # endregion


    ''' (?) Generates the initial variable description '''
    def makeInitialVarDesc(self, evt):
        varFileDir = self.entryVariableFile.get()
        valFileDir = self.entryValuesFile.get()

        # tkMessageBox.showinfo("Work in progress",'Make the Initial Variable Descriptor! (WIP)') # TODO!!
        print self.entryQueryPopulation.get()[-4:]

        if self.entryInitialVarDesc.get()[-4:] != ".csv":  # TODO Properly check for valid files
            tkMessageBox.showinfo("System Message", "Please enter a valid Variable Description CSV file")  # TODO!!

        elif self.entryQueryPopulation.get()[-4:] != ".csv":
            tkMessageBox.showinfo("System Message", "Please enter a valid Population Dataset CSV file")  # TODO!!

        else:
            tkMessageBox.showinfo("System Message", "Dataset successfully uploaded!")  # TODO!!
            self.Tabs.select(UI_support.TAB_TEST_INDEX)
        return "break"





    ''' --> Elements under the DATA ("DATA") TAB (1) <-- '''
    # region

    ''' (?) Uploads the variable file '''

    def getVariableFile(self, evt):
        varFileDir = askopenfilename(title = "Select variable file",
                                     filetypes = (("txt files", "*.txt"), ("all files", "*.*")))
        self.entryVariableFile.delete(0, END)
        self.entryVariableFile.insert(0, varFileDir)
        return "break"

    ''' (?) Uploads the values file '''

    def getValuesFile(self, evt):
        valFileDir = askopenfilename(title = "Select values file",
                                     filetypes = (("txt files", "*.txt"), ("all files", "*.*")))
        self.entryValuesFile.delete(0, END)
        self.entryValuesFile.insert(0, valFileDir)
        return "break"


    def getHasUploadedVariableDescription(self):
        return self.hasUploadedVariableDescription

    def getHasUploadedPopulation(self):
        return self.hasUploadedPopulation

    def getInitVarDisc(self):
        return self.initVarDisc

    def getButtonStartDatasetUpload(self):
        return self.buttonStartDatasetUpload

    def getPopulationDir(self):
        global populationDir
        return populationDir