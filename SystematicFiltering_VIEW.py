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
import math
from math import modf
import collections

import Color_support as CS
import Function_support as FS
import Widget_support as WS
import Icon_support as IS
import UI_support as US

from _Progressible import _Progressible
import UIConstants_support as UICS


class SystematicFiltering_View(_Progressible):

    def __init__(self, parentWindow):
        # super(SystematicFiltering_View, self).__init__()
        # call _Progressible constructor
        _Progressible.__init__(self)
        self.dictWidgetPlace = collections.OrderedDict()  # For hiding and showing elements
        self.__parentFrame = WS.createDefaultFrame(parentWindow,
                                                   [0, 0, 1, 1],
                                                   [True, True])
        self.__parentFrame.place(relx = 0.02, relwidth = 0.96)
        self.initializeWidgets(self.__parentFrame)
        WS.redraw(self.__parentFrame)


        maxProgressBarWidth = self.lblStripe.winfo_width()
        _Progressible.setMaxProgress(self, maxProgressBarWidth)

        self.showStartMining()

    " INHERITED "

    '''
         A thread should call this function
    '''
    def updateProgress(self, percent, description = ""):
        if percent is not 0:
            # call super class
            _Progressible.updateProgress(self, percent)
            self.getLblCurrentProgress().place(width = self.getCurrentProgress())
            # self.getLblCurrentProgress().update()
        clean_description = ""
        if len(description) == 0:
            self.getLblCurrentDetails().configure(text = str(int(self.getCurrentPercent())) + "%")
        else:
            # Remove the symbols when showing in the progress bar label
            clean_description = description.replace(UICS.MODULE_INDICATOR, "")
            clean_description = clean_description.replace(UICS.SUB_MODULE_INDICATOR, "")
            self.getLblCurrentDetails().configure(text = str(clean_description.strip()))

        # Check if the string is a module title and add the necessary underscores before
        # and after it (cosmetic)
        if UICS.SINGLE_MODULE_SYMBOL in description:
            len_description = float(len(clean_description))
            symbol_count = float((UICS.LEN_MODULE_MAX - len_description) / 2)

            # Check if the half count is a decimal. If so, add another symbol according
            # to its value (i.e. if its greater than or less than 0.05)
            symbol_count_decimal = math.modf(symbol_count)
            addSymbol = ""
            if symbol_count_decimal >= 0.5:
                addSymbol = UICS.SINGLE_MODULE_SYMBOL
                symbol_count = int(symbol_count + 1)
            else:
                symbol_count = int(symbol_count)

            symbols = ''.join([char * symbol_count for char in UICS.SINGLE_MODULE_SYMBOL])

            description = UICS.PRE_STRING_SPACE + addSymbol + symbols + clean_description + symbols

        strProgressInfo = str(description)
        self.getLbProgressConsole().insert(END, strProgressInfo)
        self.getLbProgressConsole().yview(END)  # Automatically sets the scrollbar to the newly added item



    '''
        Default frames are as follows:
            > __lfProgressBar
            > __lfCurrentProgress
            > __lfProgressConsole
            > __lfConsoleCommands
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
        # endregion create the progress header widgets

        # region create the current progress widgets
        self.__lfCurrentProgress = WS.createDefaultFrame(parentFrame,
                                                         [0, 0, 1, FS.headerHeight],
                                                         [True, False])

        self.__lblCurrentDetails = WS.createDefaultHeader(
            self.__lfCurrentProgress,
            "Current Progress...",
            # lblTitle.winfo_width(), 0, self.lfCurrentProgress.winfo_width() - lblTitle.winfo_width(), 1,
            [0, 0, 1, 1], [True, True],
            CS.WHITE, CS.D_GRAY, US.FONT_DEFAULT)
        FS.placeBelow(self.__lfCurrentProgress, self.lblStripe)

        # endregion create the current progress widgets
        # region create console listbox widgets
        self.__lfCurrentProgress.update()
        wHeight = parentFrame.winfo_height() - (self.__lfCurrentProgress.winfo_y() + self.__lfCurrentProgress.winfo_height())
        wHeight = wHeight - (FS.commandsHeight + 10)

        self.__lfProgressConsole = WS.createDefaultFrame(parentFrame,
                                                         [0, y, 1, wHeight],
                                                         [True, False])
        self.lbProgressConsole = WS.createDefaultListbox(self.__lfProgressConsole, SINGLE)
        FS.placeBelow(self.__lfProgressConsole, self.__lfCurrentProgress)

        borderColor = CS.D_YELLOW
        WS.emborder(self.lbProgressConsole,
                    [0, 0, None, None],
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor]
                    )

        # endregion create console listbox widgets
        # region create command widgets
        bgColor = CS.WHITE  # CS.PALER_YELLOW
        self.__lfConsoleCommands = WS.createDefaultFrame(parentFrame,
                                                         [0, 0, 1, 0.15], [True, True],
                                                         bgColor)
        # WS.emborder(self.__lfConsoleCommands, [0, 0, None, None], [True, False, False, False])
        y_offset = 6
        FS.placeBelow(self.__lfConsoleCommands, self.__lfProgressConsole, y_offset)



        # TODO
        btn_width = 40
        btn_height = btn_width
        icon_size = (btn_width, btn_height)

        frame_parent_width = self.__lfConsoleCommands.winfo_width()
        frame_parent_height = self.__lfConsoleCommands.winfo_height()
        rel_width = float(btn_width) / float(frame_parent_width)
        rel_height = float(btn_height) / float(frame_parent_height)

        rel_x = 0.5 - (rel_width / 2)
        rel_y = 0.5 - (rel_height / 2)

        # START MINING Button
        self.__btnStartCrossProcess = Button(self.__lfConsoleCommands)
        self.__btnStartCrossProcess.place(
            relx = rel_x, rely = rel_y,
            width = btn_width, height = btn_height)

        im = PIL.Image.open(IS.AM_ICO_START).resize(icon_size, PIL.Image.ANTIALIAS)
        btn_start_AM = PIL.ImageTk.PhotoImage(im)
        self.__btnStartCrossProcess.configure(
            image = btn_start_AM)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.__btnStartCrossProcess.image = btn_start_AM  # < ! > Required to make images appear

        self.__btnStartCrossProcess.configure(
            background = CS.WHITE, foreground = CS.D_BLUE,
            activebackground = CS.FILTER_BG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE
        )

        # STOP MINING Button
        self.__btnStopCrossProcess = Button(self.__lfConsoleCommands)
        self.__btnStopCrossProcess.place(
            relx = rel_x, rely = rel_y,
            width = btn_width, height = btn_height)

        im = PIL.Image.open(IS.AM_ICO_CANCEL).resize(icon_size, PIL.Image.ANTIALIAS)
        btn_stop_AM = PIL.ImageTk.PhotoImage(im)
        self.__btnStopCrossProcess.configure(
            image = btn_stop_AM)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.__btnStopCrossProcess.image = btn_stop_AM  # < ! > Required to make images appear

        self.__btnStopCrossProcess.configure(
            background = CS.WHITE, foreground = CS.D_BLUE,
            activebackground = CS.FILTER_BG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE
        )
        # endregion create command widgets
    # endregion initialization functions


    '''
        WIDGET FUNCTIONS
    '''

    '''
        The function called when the close button is clicked in AM window.
    '''
    def showStopMining(self):
        self.showWidget(self.getBtnStopCrossProcess())
        self.hideWidget(self.getBtnStartCrossProcess())

    '''
        The function called when the start button is clicked in AM window.
    '''
    def showStartMining(self):
        self.showWidget(self.getBtnStartCrossProcess())
        self.hideWidget(self.getBtnStopCrossProcess())

    def hideWidget(self, widget):
        widget.update()

        # Store widget width and height if it's not in the dictionary
        widgetName = WS.getWidgetName(widget)
        if not (widgetName + '_W' in self.dictWidgetPlace):
            # For relative width and height
            self.dictWidgetPlace[widgetName + '_RelW'] = US.getRelW(widget)
            self.dictWidgetPlace[widgetName + '_RelH'] = US.getRelH(widget)

            # For width and height
            self.dictWidgetPlace[widgetName + '_W'] = US.getW(widget)
            self.dictWidgetPlace[widgetName + '_H'] = US.getH(widget)

        # Set widget width and height to 0
        widget.place(relwidth = 0, relheight = 0, width = 0, height = 0)


    def showWidget(self, widget):
        widgetName = WS.getWidgetName(widget)

        # Retrieve widget width and height if it's in the dictionary
        if widgetName + '_W' in self.dictWidgetPlace:
            widgetRelWidth = self.dictWidgetPlace[widgetName + '_RelW']
            widgetRelHeight = self.dictWidgetPlace[widgetName + '_RelH']

            widgetWidth = self.dictWidgetPlace[widgetName + '_W']
            widgetHeight = self.dictWidgetPlace[widgetName + '_H']

            # Set widget width and height
            widget.place(relwidth = widgetRelWidth, relheight = widgetRelHeight,
                         width = widgetWidth, height = widgetHeight)

            # Remove keys from dictionary
            self.dictWidgetPlace.pop(widgetName + '_RelW', None)
            self.dictWidgetPlace.pop(widgetName + '_RelH', None)

            self.dictWidgetPlace.pop(widgetName + '_W', None)
            self.dictWidgetPlace.pop(widgetName + '_H', None)

        widget.update()


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

    def getBtnStopCrossProcess(self):
        return self.__btnStopCrossProcess

    def getLbProgressConsole(self):
        return self.lbProgressConsole
    # endregion getters
