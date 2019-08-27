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
import Keys_support as key

import Color_support as CS
import Function_support as FS
import Widget_support as WS
import Icon_support as IS
import UI_support as US

from _Progressible import _Progressible

class SystematicFiltering_View(_Progressible):

    def __init__(self, parentWindow):
        # call _Progressible constructor
        _Progressible.__init__(self)
        # super(SystematicFiltering_View, self).__init__()

        self.__parentFrame = WS.createDefaultFrame(parentWindow,
                                                   [0, 0, 1, 1],
                                                   [True, True])

        self.initializeWidgets(self.__parentFrame)
        WS.redraw(self.__parentFrame)

    " INHERITED "
    def updateProgress(self, progress):
        # call super class
        _Progressible.updateProgress(self, progress)
        print "dec is " + str(self.getCurrentDecimal())
        self.getLblCurrentProgress().place(relwidth = self.getCurrentDecimal())
        # self.getLblCurrentProgress().update()
        self.getLblCurrentDetails().configure(text = str(self.getCurrentPercent()) + "%")



    # region initialization functions
    def initializeWidgets(self, parentFrame):
        self.__lfProgressBar = WS.createDefaultFrame(parentFrame,
                                                     [0, 0, 1, 1],
                                                     [True, True])
        # region create the progress header widgets
        lblHeader = WS.createDefaultHeader(self.__lfProgressBar, "PROGRESS",
                                           [0, 0, 1, FS.headerHeight], [True, False])
        lblStripe = WS.createDefaultStripe(self.__lfProgressBar,
                                           [0, 0, 1, FS.stripeHeight], [True, False])
        FS.placeBelow(lblStripe, lblHeader)

        self.__lblGreenStripe = WS.createDefaultStripe(lblStripe, [0, 0, 1, 1],
                                                       [True, True], IS.TEXTURE_STRIPE_LIME)
        self.__lblGreenStripe.place(relwidth = 0)
        # endregion create the progress header widgets

        # region create the current progress widgets
        self.__lfCurrentProgress = WS.createDefaultFrame(parentFrame,
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

        self.__lblCurrentDetails = WS.createDefaultHeader(
            self.__lfCurrentProgress,
            "Current Progress...",
            # lblTitle.winfo_width(), 0, self.lfCurrentProgress.winfo_width() - lblTitle.winfo_width(), 1,
            [0, 0, 1, 1], [True, True],
            CS.WHITE, CS.D_GRAY, US.FONT_DEFAULT)
        borderColor = CS.L_GRAY
        WS.emborder(self.__lblCurrentDetails,
                    [0, 0, None, None],
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor]
                    )
        FS.placeBelow(self.__lfCurrentProgress, lblStripe)
        # endregion create the current progress widgets

        # region create console listbox widgets
        self.__lfCurrentProgress.update()
        wHeight = parentFrame.winfo_height() - (self.__lfCurrentProgress.winfo_y() + self.__lfCurrentProgress.winfo_height())
        wHeight -= FS.commandsHeight
        self.__lfProgressConsole = WS.createDefaultFrame(parentFrame,
                                                         [0, 0, 1, wHeight],
                                                         [True, False])
        self.lbProgressConsole = WS.createDefaultListbox(self.__lfProgressConsole, SINGLE)
        FS.placeBelow(self.__lfProgressConsole, self.__lfCurrentProgress)
        # endregion create console listbox widgets

        # region create command widgets
        self.__lfConsoleCommands = WS.createDefaultFrame(self.__lfProgressBar,
                                                         [0, 0, 1, FS.commandsHeight], [True, False])
        WS.emborder(self.__lfConsoleCommands, [0, 0, None, None], [True, False, False, False])
        FS.placeBelow(self.__lfConsoleCommands, self.__lfProgressConsole)

        self.__btnStartCrossProcess = Button(self.__lfConsoleCommands)
        self.__btnStartCrossProcess.place(x = 0, y = 0, width = 30, height = 30)
        # endregion create command widgets


    def initializeProperties(self):
        print "initializeProperties"
        # self.btnConfirmConfirmedFeatures = [None]


    # endregion initialization functions

    " GETTERS "
    # region getters
    def getFrame(self):
        return self.__parentFrame

    def getLblCurrentDetails(self):
        return self.__lblCurrentDetails

    def getLblCurrentProgress(self):
        return self.__lblGreenStripe

    def getBtnStartCrossProcess(self):
        return self.__btnStartCrossProcess
    # endregion getters
