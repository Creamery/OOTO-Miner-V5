#! /usr/bin/env python

"""
{Description}
Systematic Filtering Model
"""

__author__ = ["Candy Espulgar"]

__copyright__ = "Copyright 2019, TE3D House"
__credits__ = ["Arnulfo Azcarraga"]
__version__ = "3.0"


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


import PIL.Image
import PIL.ImageTk
import CONSTANTS as const
from Keys_support import Dataset as KSD
from Keys_support import SSF as KSS

import Color_support as CS
import Function_support as FS
import Widget_support as WS
import Icon_support as IS
import UI_support as US
from _THREAD_CrossProcess import CrossProcessThread
from _THREAD_CrossProcessProgress import CrossProcessProgressThread

class SystematicFiltering_Model:

    def __init__(self):

        # initialize properties
        # self.__rawDataset = dataset
        # print "convertDatasetValuesToGroups : "

        # print "---- dataset : "
        # print str(dataset.keys())
        # print str(dataset['FeatureList'])
        # print str(dataset['Samples'])

        # # self.__dataset = FS.convertDatasetValuesToGroups(dataset, featureDescription)
        # self.__dataset = dataset
        # self.__featureDescription = featureDescription
        # self.__salientFeatures = salientFeatures
        # self.__SSF = WS.initializeSSF(salientFeatures)


        # thread that handles the actual processing
        # self.__threadCrossProcess = CrossProcessThread()  # TODO Remove
        # thread that handles the UI progress updates
        # self.__threadCrossProcessProgress = CrossProcessProgressThread(self.__dataset, self.__SSF)

        self.__isCrossProcessing = False

    " FUNCTIONS "
    def startSystematicFiltering(self, viewProgressible):
        print "startSystematicFiltering"

        # set progressible view
        self.getThreadCrossProcessProgress().setProgressible(viewProgressible)
        # self.getThreadCrossProcessProgress().setData(viewProgressible)
        # self.getThreadCrossProcess().setProgressible(viewProgressible)

        self.setCrossProcessing(True)
        # self.getThreadCrossProcess().start()
        self.getThreadCrossProcessProgress().start()

    def stopSystematicFiltering(self):
        pass

    " GETTERS "
    def getDataset(self):
        return self.__dataset

    def isCrossProcessing(self):
        return self.__isCrossProcessing

    # def getThreadCrossProcess(self):__threadCrossProcess

    def getThreadCrossProcessProgress(self):
        return self.__threadCrossProcessProgress

    def getSSF(self):
        return self.__SSF

    " SETTERS "
    def setCrossProcessing(self, value):
        self.__isCrossProcessing = value
