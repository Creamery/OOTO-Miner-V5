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


import Color_support as CS
import Icon_support
import UI_support
import PIL.Image
import PIL.ImageTk
import CONSTANTS as const
import KEYS_support as key

import Function_support as FS

class SystematicFiltering_View:

    def __init__(self, parentWindow):
        self.parentFrame = LabelFrame(parentWindow, bd = 0)
        self.parentFrame.configure(background = CS.WHITE)
        self.parentFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        self.initializeProperties()
        FS.redraw(self.parentFrame)




    def initializeProperties(self):
        print "initializeProperties"
        # self.btnConfirmConfirmedFeatures = [None]


    " GETTERS "
    def getFrame(self):
        return self.parentFrame