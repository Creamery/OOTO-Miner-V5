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
from Keys_support import Dataset as KSD

import Color_support as CS
import Function_support as FS
import Widget_support as WS
import Icon_support as IS
import UI_support as US

from _Progressible import _Progressible

class SystematicFiltering_View(_Progressible):

    def __init__(self, parentWindow):
        # super(SystematicFiltering_View, self).__init__()
        # call _Progressible constructor
        _Progressible.__init__(self)

        self.__parentFrame = WS.createDefaultFrame(parentWindow,
                                                   [0, 0, 1, 1],
                                                   [True, True])
        self.__parentFrame.place(relx = 0.02, relwidth = 0.96)
        self.initializeWidgets(self.__parentFrame)
        WS.redraw(self.__parentFrame)


        maxProgressBarWidth = self.lblStripe.winfo_width()
        _Progressible.setMaxProgress(self, maxProgressBarWidth)
        self.updateProgress(50)



    " INHERITED "
    def updateProgress(self, percent, args = [""]):
        # call super class
        _Progressible.updateProgress(self, percent)
        print "MAX BAR WIDTH " + str(self.getMaxProgress())
        print "CURRENT BAR WIDTH " + str(self.getCurrentProgress())

        self.getLblCurrentProgress().place(width = self.getCurrentProgress())
        # self.getLblCurrentProgress().update()
        self.getLblCurrentDetails().configure(text = str(int(self.getCurrentPercent())) + "%")

        strProgressInfo = str(args[0])
        self.getLbProgressConsole().insert(0, strProgressInfo)



    '''
        Default frames are as follows:
            > __lfProgressBar
            > 
    '''
    # region initialization functions
    def initializeWidgets(self, parentFrame):
        y = 10
        self.__lfProgressBar = WS.createDefaultFrame(parentFrame,
                                                     [0, y, 1, 0.7],
                                                     [True, True])
        # region create the progress header widgets
        lblHeader = WS.createDefaultHeader(self.__lfProgressBar, "PROGRESS",
                                           [0, 0, 1, FS.headerHeight], [True, False])

        self.lblStripe = WS.createDefaultStripe(self.__lfProgressBar,
                                           [0, 0, 1, FS.stripeHeight], [True, False], IS.TEXTURE_STRIPE_GREY)
        FS.placeBelow(self.lblStripe, lblHeader)

        # self.__lblGreyStripe = WS.createDefaultStripe(lblStripe, [0, 0, 1, 1],
        #                                               [True, True], IS.TEXTURE_STRIPE_GREY)
        # self.__lblGreyStripe.place(relwidth = 0)

        self.__lblGreenStripe = WS.createDefaultStripe(self.lblStripe, [0, 0, 0.999, 1],
                                                       [True, True], IS.TEXTURE_STRIPE_LIME)
        self.__lblGreenStripe.place(relwidth = 0)
        borderColor = CS.L_GRAY
        print(self.__lfProgressBar.place_info())
        # WS.emborder(self.__lfProgressBar,
        #             [0, 0, None, None],
        #             [True, True, True, True],
        #             [borderColor, borderColor, borderColor, borderColor]
        #             )



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
        FS.placeBelow(self.__lfCurrentProgress, self.lblStripe)

        # borderColor = CS.L_GRAY
        # WS.emborder(self.__lblCurrentDetails,
        #             [0, 0, None, None],
        #             [True, True, True, True],
        #             [borderColor, borderColor, borderColor, borderColor]
        #             )
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

        borderColor = CS.L_GRAY
        # WS.emborder(self.lbProgressConsole,
        #             [0, 0, None, None],
        #             [True, True, True, True],
        #             [borderColor, borderColor, borderColor, borderColor]
        #             )
        # endregion create console listbox widgets

        # region create command widgets
        self.__lfConsoleCommands = WS.createDefaultFrame(self.__lfProgressBar,
                                                         [0, 0, 1, FS.commandsHeight], [True, False])
        # WS.emborder(self.__lfConsoleCommands, [0, 0, None, None], [True, False, False, False])
        FS.placeBelow(self.__lfConsoleCommands, self.__lfProgressConsole)


        # TODO
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

    def getLbProgressConsole(self):
        return self.lbProgressConsole
    # endregion getters
