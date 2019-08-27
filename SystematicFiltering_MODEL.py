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
import Keys_support as key

import Color_support as CS
import Function_support as FS
import Widget_support as WS
import Icon_support as IS
import UI_support as US
from _THREAD_CrossProcess import CrossProcessThread
from _THREAD_CrossProcessProgress import CrossProcessProgressThread

class SystematicFiltering_Model:

    def __init__(self, dataset, features):

        # initialize properties
        self.__type = 0
        self.__maxType = 2
        self.__dataset = dataset
        self.__features = features

        # thread that handles the actual processing
        self.__threadCrossProcess = CrossProcessThread()
        # thread that handles the UI progress updates
        self.__threadCrossProcessProgress = CrossProcessProgressThread()

        self.__isCrossProcessing = False

    " FUNCTIONS "
    def startSystematicFiltering(self, viewProgressible):
        print "startSystematicFiltering"

        # set progressible view
        self.getThreadCrossProcessProgress().setProgressible(viewProgressible)
        # self.getThreadCrossProcessProgress().setData(viewProgressible)
        self.getThreadCrossProcess().setProgressible(viewProgressible)

        self.setCrossProcessing(True)
        # self.getThreadCrossProcess().start()
        self.getThreadCrossProcessProgress().start()

    def stopSystematicFiltering(self):
        pass

    " GETTERS "
    def isCrossProcessing(self):
        return self.__isCrossProcessing

    def getThreadCrossProcess(self):
        return self.__threadCrossProcess

    def getThreadCrossProcessProgress(self):
        return self.__threadCrossProcessProgress

    " SETTERS "

    def setCrossProcessing(self, value):
        self.__isCrossProcessing = value
