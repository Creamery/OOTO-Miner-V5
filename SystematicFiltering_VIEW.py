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


import PIL.Image
import PIL.ImageTk
import CONSTANTS as const
import KEYS_support as key

import Color_support as CS
import Function_support as FS
import Widget_support as WS
import Icon_support as IS
import UI_support as US

class SystematicFiltering_View:

    def __init__(self, parentWindow):
        self.parentFrame = WS.createDefaultFrame(parentWindow,
                                                 [0, 0, 1, 1],
                                                 [True, True])

        self.initializeWidgets(self.parentFrame)
        WS.redraw(self.parentFrame)


    def initializeWidgets(self, parentFrame):
        self.lfProgressBar = WS.createDefaultFrame(parentFrame,
                                                   [0, 0, 1, 1],
                                                   [True, True])
        # region create the progress header widgets
        lblHeader = WS.createDefaultHeader(self.lfProgressBar, "PROGRESS",
                                           [0, 0, 1, FS.headerHeight], [True, False])
        lblStripe = WS.createDefaultStripe(self.lfProgressBar,
                                           [0, 0, 1, FS.stripeHeight], [True, False])
        FS.placeBelow(lblStripe, lblHeader)

        self.lblGreenStripe = WS.createDefaultStripe(lblStripe, [0, 0, 1, 1],
                                                     [True, True], IS.TEXTURE_STRIPE_LIME)
        self.lblGreenStripe.place(relwidth = 0)
        # endregion create the progress header widgets

        # region create the current progress widgets
        self.lfCurrentProgress = WS.createDefaultFrame(parentFrame,
                                                       [0, 0, 1, FS.headerHeight],
                                                       [True, False])

        # lblTitle = WS.createDefaultHeader(self.lfCurrentProgress, 0, 0, 0.2, 1,
        #                                   "Details", [True, True],
        #                                   CS.WHITE, CS.FUSCHIA,
        #                                   US.FONT_DEFAULT)
        # borderColor = CS.FUSCHIA
        # WS.emborder(lblTitle, 0, 0, None, None,
        #             conditions = [True, True, True, True],
        #             colors = [borderColor, borderColor, borderColor, borderColor]
        #             )

        self.lblCurrentDetails = WS.createDefaultHeader(
            self.lfCurrentProgress,
            "Current Progress...",
            # lblTitle.winfo_width(), 0, self.lfCurrentProgress.winfo_width() - lblTitle.winfo_width(), 1,
            [0, 0, 1, 1], [True, True],
            CS.WHITE, CS.D_GRAY, US.FONT_DEFAULT)
        borderColor = CS.L_GRAY
        WS.emborder(self.lblCurrentDetails,
                    [0, 0, None, None],
                    conditions = [True, True, True, True],
                    colors = [borderColor, borderColor, borderColor, borderColor]
                    )
        FS.placeBelow(self.lfCurrentProgress, lblStripe)
        # endregion create the current progress widgets

        # region create console listbox widgets
        self.lfCurrentProgress.update()
        wHeight = parentFrame.winfo_height() - (self.lfCurrentProgress.winfo_y() + self.lfCurrentProgress.winfo_height())
        wHeight -= FS.commandsHeight
        self.lfProgressConsole = WS.createDefaultFrame(parentFrame,
                                                       [0, 0, 1, wHeight],
                                                       [True, False])
        self.lbProgressConsole = WS.createDefaultListbox(self.lfProgressConsole, SINGLE)
        FS.placeBelow(self.lfProgressConsole, self.lfCurrentProgress)
        # endregion create console listbox widgets

        # region create command widgets
        self.lfConsoleCommands = WS.createDefaultFrame(self.lfProgressBar,
                                                       [0, 0, 1, FS.commandsHeight], [True, False])
        WS.emborder(self.lfConsoleCommands, [0, 0, None, None], [True, False, False, False])
        FS.placeBelow(self.lfConsoleCommands, self.lfProgressConsole)
        # endregion create command widgets


    def initializeProperties(self):
        print "initializeProperties"
        # self.btnConfirmConfirmedFeatures = [None]


    " GETTERS "
    def getFrame(self):
        return self.parentFrame

    def getLblCurrentDetails(self):
        return self.lblCurrentDetails
