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
import Function_support as FS
import KEYS_support as key


class SystematicFiltering_View:

    def __init__(self, parentFrame):
        self.initializeProperties()

        # parent frame for all elements in the Automated Mining tab
        self.lfTabParentFrame = self.initTabFrame(parentFrame)

        # empty frame for top padding
        self.lfTopPadding = self.initTopPaddingUI(self.lfTabParentFrame)

        # frame containing the first row of UI elements
        self.lfInputFrame = self.initInputUI(self.lfTabParentFrame, self.lfTopPadding)

        # frame containing the second row of UI elements
        self.lfProcessFrame = self.initProcessUI(self.lfTabParentFrame, self.lfInputFrame)

        # frame containing the third row of UI elements
        self.lfResultsFrame = self.initResultsUI(self.lfTabParentFrame, self.lfProcessFrame)

        # frame containing the console UI elements
        self.lfConsoleFrame = self.initConsoleUI(self.lfTabParentFrame, self.lfProcessFrame)

        self.redraw(self.lfTabParentFrame)
        self.lfProcessFrame.place(width = 0, height = 0)
        self.lfResultsFrame.place(width = 0, height = 0)
        # self.lfConsoleFrame.place(width = 0, height = 0)


    def initializeProperties(self):
        self.btnConfirmConfirmedFeatures = [None]
        self.btnResetConfirmedFeatures = [None]
        self.btnQueryConfirmedFeatures = [None]
        self.lbListConfirmedFeatures = [None]
        self.lbListConfirmedDetails = [None]
        self.lblCountConfirmedFeaturesText = [None]
        self.entryQueryConfirmedFeatures = [None]
        self.lblHeaderConfirmedFeatures = [None]
        self.lblCountConfirmedFeaturesTitle = [None]


