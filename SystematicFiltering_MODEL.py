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
import KEYS_support as key

import Color_support as CS
import Function_support as FS
import Widget_support as WS
import Icon_support as IS
import UI_support as US
from CrossProcessThread import CrossProcessThread
from _Progressible import _Progressible

class SystematicFiltering_Model(_Progressible):

    def __init__(self):
        # call _Progressible constructor
        # super(SystematicFiltering_Model, self).__init__()
        _Progressible.__init__(self)

        # initialize properties
        self.type = 0
        self.maxType = 2

        self.__threadCrossProcess = CrossProcessThread(self)
        self.__isCrossProcessing = False

    " FUNCTIONS "
    def startSystematicFiltering(self, view):
        print "startSystematicFiltering"
        self.setCrossProcessing(True)
        self.getThreadCrossProcess().start()

    " GETTERS "
    def isCrossProcessing(self):
        return self.__isCrossProcessing

    def getThreadCrossProcess(self):
        return self.__threadCrossProcess

    " SETTERS "
    def setCrossProcessing(self, value):
        self.__isCrossProcessing = value