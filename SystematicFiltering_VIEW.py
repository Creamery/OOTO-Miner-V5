#! /usr/bin/env python

"""
{Description}
Systematic Filtering User Interface
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


import Icon_support
import UI_support
import PIL.Image
import PIL.ImageTk
import CONSTANTS as const
import KEYS_support as key

import Color_support as CS
import Function_support as FS
import Widget_support as WS

class SystematicFiltering_View:

    def __init__(self, parentWindow):
        self.parentFrame = LabelFrame(parentWindow, bd = 0)
        self.parentFrame.configure(background = CS.WHITE)
        self.parentFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        self.initializeWidgets(self.parentFrame)
        FS.redraw(self.parentFrame)


    def initializeWidgets(self, parentFrame):
        self.lfProgressBar = WS.createDefaultFrame(parentFrame,
                                                   0, 0, 1, FS.headerHeight,
                                                   [True, False])

        WS.createDefaultHeader(self.lfProgressBar, 0, 0, 1, 1, "PROGRESS", [True, True])

    def initializeProperties(self):
        print "initializeProperties"
        # self.btnConfirmConfirmedFeatures = [None]


    " GETTERS "
    def getFrame(self):
        return self.parentFrame