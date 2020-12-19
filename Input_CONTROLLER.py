
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    The Controller class of the Input tab. It
    handles the main functionality of its View.
    [Candy]
'''
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import tkinter as tk

import _UI_support
import _UIConstants_support as UICS

class Input_Controller:

    def __init__(self, view):
        self.view = view
        self.initializeVariables()
        self.configureDataTabBindings()


    def initializeVariables(self):
        self.hasUploadedVariableDescription = False
        self.hasUploadedPopulation = False
        self.hasFeatureNames = False



    ''' --> Binding elements under the DATA ("DATA") TAB (1) <-- '''

    def configureDataTabBindings(self):
        # TODO Add integrity check - if ENTRY is edited, change the file input
        self.buttonInitialVarDesc = self.view.getButtonInitialVarDesc()
        self.buttonInitialVarDesc.bind('<Button-1>', self.selectInitVarDesc)
        self.buttonQueryPopulation = self.view.getButtonQueryPopulation()
        self.buttonQueryPopulation.bind('<Button-1>', self.selectSetPopulation)

        self.btnInitialFeatureNames = self.view.getButtonVariableFile()
        self.btnInitialFeatureNames.bind('<Button-1>', self.selectFeatureNamesFile)


        # self.buttonVariableFile = self.view.getButtonVariableFile()
        # self.buttonVariableFile.bind('<Button-1>', self.getVariableFile)
        # self.buttonValuesFile = self.view.getButtonValuesFile()
        # self.buttonValuesFile.bind('<Button-1>', self.getValuesFile)

        # self.buttonStartVariableDescriptor.bind('<Button-1>', self.makeInitialVarDesc) ### TODO
        self.buttonStartDatasetUpload = self.view.getButtonStartDatasetUpload()
        # self.buttonStartDatasetUpload.bind('<Button-1>', self.uploadDataset)

        self.entryInitialVarDesc = self.view.getEntryInitialVarDesc()
        self.entryQueryPopulation = self.view.getEntryQueryPopulation()
        self.entryVariableFile = self.view.getEntryVariableFile()
        # self.entryValuesFile = self.view.getEntryValuesFile()


    ''' Selects the variable description file '''

    def selectInitVarDesc(self, evt):
        self.hasUploadedVariableDescription = False

        self.initVarDisc = tkFileDialog.askopenfilename(title = "Select file",
                                                        filetypes = (("csv files", "*.csv"), ("all files", "*.*")))

        if len(self.initVarDisc) == 0:
            tkMessageBox.showerror("Error: Upload Variable description",
                                   "Please select a valid [variable description] file.")
        else:
            self.hasUploadedVariableDescription = True
            self.entryInitialVarDesc.delete(0, tk.END)
            self.entryInitialVarDesc.insert(0, self.initVarDisc)

        return "break"  # this "unsinks" the button after opening the file explorer

    ''' Selects the population module file '''

    def selectSetPopulation(self, evt):
        self.hasUploadedPopulation = False

        global dirPopulation
        dirPopulation = tkFileDialog.askopenfilename(title = "Select file",
                                                     filetypes = (("csv files", "*.csv"), ("all files", "*.*")))

        if len(dirPopulation) == 0:
            tkMessageBox.showerror("Error: Upload error", "Please select a valid [population dataset].")
        else:
            self.hasUploadedPopulation = True
            self.entryQueryPopulation.delete(0, tk.END)
            self.entryQueryPopulation.insert(0, dirPopulation)
        return "break"

    ''' Selects the Feature Names file for AM '''

    def selectFeatureNamesFile(self, evt):
        self.hasFeatureNames = False

        global dirFeatureNames
        dirFeatureNames = tkFileDialog.askopenfilename(title = "Select file",
                                                       filetypes = (("csv files", "*.csv"), ("all files", "*.*")))

        if len(dirFeatureNames) == 0:
            tkMessageBox.showerror("Error: Upload error", "Please select a valid [feature names] file.")
        else:
            self.hasFeatureNames = True
            self.entryVariableFile.delete(0, tk.END)
            self.entryVariableFile.insert(0, dirFeatureNames)
            UICS.PATH_FTRNAMES = dirFeatureNames
        return "break"
    # endregion


    ''' (?) Generates the initial variable description '''
    def makeInitialVarDesc(self, evt):
        varFileDir = self.entryVariableFile.get()
        # valFileDir = self.entryValuesFile.get()

        # tkMessageBox.showinfo("Work in progress",'Make the Initial Variable Descriptor! (WIP)') # TODO!!
        # print self.entryQueryPopulation.get()[-4:]

        if self.entryInitialVarDesc.get()[-4:] != ".csv":  # TODO Properly check for valid files
            tkMessageBox.showinfo("System Message", "Please enter a valid Variable Description CSV file")  # TODO!!

        elif self.entryQueryPopulation.get()[-4:] != ".csv":
            tkMessageBox.showinfo("System Message", "Please enter a valid Population Dataset CSV file")  # TODO!!

        else:
            tkMessageBox.showinfo("System Message", "Dataset successfully uploaded!")  # TODO!!
            self.Tabs.select(_UI_support.TAB_TEST_INDEX)
        return "break"





    ''' --> Elements under the DATA ("DATA") TAB (1) <-- '''
    # region


    def getHasUploadedVariableDescription(self):
        return self.hasUploadedVariableDescription

    def getHasUploadedPopulation(self):
        return self.hasUploadedPopulation

    def getHasFeatureNames(self):
        return self.hasFeatureNames

    def getInitVarDisc(self):
        return self.initVarDisc

    def getButtonStartDatasetUpload(self):
        return self.buttonStartDatasetUpload

    def getPopulationDir(self):
        global dirPopulation
        return dirPopulation