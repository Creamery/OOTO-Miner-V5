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
import Grip_support as GS

from _Progressible import _Progressible
import UIConstants_support as UICS
import tkMessageBox

class SystematicFiltering_View(_Progressible):

    def __init__(self, parentWindow):
        # super(SystematicFiltering_View, self).__init__()
        # call _Progressible constructor
        _Progressible.__init__(self)
        self.hasOverlay = False
        self.root = parentWindow
        self.declareBindingVariables()  # Initializes the button binding variables as None
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


    def declareBindingVariables(self):
        self.ico_width_check = None
        self.ico_height_check = None

        self.ico_width_cross = None
        self.ico_height_cross = None


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

        # BUTTONS
        btn_width = 40
        btn_height = btn_width
        icon_size = (btn_width, btn_height)

        self.ico_width_check = btn_width
        self.ico_height_check = btn_height

        self.ico_width_cross = btn_width
        self.ico_height_cross = btn_height


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

    def createDialog(self):

        self.createOverlay()

        overlay_width = self.__winDialogueOverlay.winfo_width()
        overlay_height = self.__winDialogueOverlay.winfo_height()
        dialogue_frame_width = int(overlay_width * 0.45)
        dialogue_frame_height = int(overlay_height * 0.37)  # + FS.gripHeight
        self.__lfDialogueFrame = self.__initializeWindow(self.root, dialogue_frame_width, dialogue_frame_height)
        # self.__lfDialogueFrame.geometry(str(dialogue_frame_width) + "x" + str(dialogue_frame_height))
        self.__winDialogueOverlay.lower(self.__lfDialogueFrame)


        bg_color = CS.D_GRAY
        self.lblBodyBorder = WS.createDefaultHeader(self.__lfDialogueFrame, "",
                                                    [0, 0, 1, 1], [True, True],
                                                    bg_color)
        bg_color = CS.WHITE
        self.lblBody = WS.createDefaultHeader(self.lblBodyBorder, "",
                                              [1, 0, 0.99, 0.99], [True, True],
                                              bg_color)
        # borderColor = CS.L_GRAY
        # WS.emborder(self.lblBody,
        #             [0, 0, 1, 1],
        #             [True, True, True, True],
        #             [borderColor, borderColor, borderColor, borderColor]
        #             )

        self.grip = GS.GripLabel(self.__lfDialogueFrame, False, False)



        message_y = 0
        message_rel_height = 0.68
        bg_color = CS.WHITE
        self.lblMessage = WS.createDefaultHeader(self.lblBody, "",
                                                 [0, message_y, 1, message_rel_height], [True, True],
                                                 bg_color)
        # Button Parent
        button_rel_height = 1 - message_rel_height
        bg_color = CS.WHITE
        self.lblButtons = WS.createDefaultHeader(self.lblBody, "",
                                                 [0, 0, 1, button_rel_height], [True, True],
                                                 bg_color)
        FS.placeBelow(self.lblButtons, self.lblMessage)

        # Button Variables
        btn_width = 40
        btn_height = btn_width
        icon_size = (btn_width, btn_height)
        rel_x = 0.2
        rel_y = 0.1

        parent_width = self.lblButtons.winfo_width()
        rel_width = float(btn_width) / float(parent_width)
        print(rel_width)
        # "NO" DIALOG Button
        self.btnDialog_NO = Button(self.lblButtons)
        self.btnDialog_NO.place(
            relx = rel_x, rely = rel_y,
            width = btn_width, height = btn_height)

        im = PIL.Image.open(IS.TAB_ICO_CROSS).resize(icon_size, PIL.Image.ANTIALIAS)
        btn_cross = PIL.ImageTk.PhotoImage(im)
        self.btnDialog_NO.configure(
            image = btn_cross)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.btnDialog_NO.image = btn_cross  # < ! > Required to make images appear

        self.btnDialog_NO.configure(
            background = CS.WHITE, foreground = CS.D_BLUE,
            activebackground = CS.FILTER_BG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE
        )

        # "YES" DIALOG BUTTON
        self.btnDialog_YES = Button(self.lblButtons)
        self.btnDialog_YES.place(
            relx = 1 - rel_x - rel_width, rely = rel_y,
            width = btn_width, height = btn_height)

        im = PIL.Image.open(IS.TAB_ICO_CHECK).resize(icon_size, PIL.Image.ANTIALIAS)
        btn_check = PIL.ImageTk.PhotoImage(im)
        self.btnDialog_YES.configure(
            image = btn_check)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.btnDialog_YES.image = btn_check  # < ! > Required to make images appear

        self.btnDialog_YES.configure(
            background = CS.WHITE, foreground = CS.D_BLUE,
            activebackground = CS.FILTER_BG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE
        )






        # self.__configureBorders(self.__lfDialogueFrame)


        # self.__winDialogueOverlay = WS.createOverlayWindow(parentWindow, FS.gripHeight)


        # self.lblOverlay = WS.createDefaultHeader(self.__lfDialogueOverlay, "",
        #                                          [0, 0, 1, 1], [True, True])
        # im = PIL.Image.open(IS.TEXTURE_BLACK).resize((50, 50), PIL.Image.ANTIALIAS)
        # img_overlay = PIL.ImageTk.PhotoImage(im)
        # self.lblOverlay.configure(image = img_overlay)
        # self.lblOverlay.image = img_overlay


        '''
        self.__lfDialogue = WS.createDefaultFrame(self.__lfDialogueOverlay,
                                                  [0, 0, 0.6, 0.6],
                                                  [True, True], CS.WHITE)
        # region create the progress header widgets
        bg_color = CS.PALER_YELLOW
        lblGrip = WS.createDefaultHeader(self.__lfDialogue, "Dialogue",
                                         [0, 0, 1, FS.headerHeight], [True, False],
                                         bg_color)

        borderColor = CS.L_GRAY
        WS.emborder(self.__lfDialogue,
                    [0, 0, None, None],
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor]
                    )
        '''

    '''
        Create an overlay and bind accordingly
    '''
    def openDialog(self):
        self.createDialog()
    '''
        Destroy the overlay and deiconify the root (main window)
    '''
    def closeDialog(self):
        # self.__winDialogueOverlay
        # self.__lfDialogueFrame.config(width = 0, height = 0)

        strDimensions = str(0) + "x" + str(0)
        self.__lfDialogueFrame.geometry(strDimensions)

        self.__lfDialogueFrame.destroy()
        self.__winDialogueOverlay.geometry(str(0) + "x" + str(0))

        self.__configureUnbind()
        self.__winDialogueOverlay.destroy()
        self.__winDialogueOverlay = None
        self.root.deiconify()

    def __initializeWindow(self, root, win_width = FS.sfWidth, win_height = FS.sfHeight):
        top = Toplevel(root)

        # remove title bar
        top.overrideredirect(True)
        top.after(10, lambda: WS.showInTaskBar(top))

        # top.transient(root)
        top.grab_set()
        # top.protocol("WM_DELETE_WINDOW", onTopClose)  # TODO return this
        top.resizable(0, 0)

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.style.configure('.', font = "TkDefaultFont")

        # center window
        strDimensions = str(win_width) + "x" + str(win_height)
        top.geometry(strDimensions)
        root.update()
        newX, newY = FS.centerWindow(top, root, 0, -FS.gripHeight)
        top.geometry(strDimensions + "+" + str(newX) + "+" + str(newY))

        top.title("Systematic Filtering")
        return top


    def createOverlay(self):
        height_offset = FS.gripHeight
        self.__winDialogueOverlay = WS.createOverlayWindow(self.root)
        self.hasOverlay = True
        # self.__winDialogueOverlay.lower(self.__lfDialogueFrame)
        # self.__configureBorders(self.__lfDialogueFrame)
        self.__configureBind()

    def __configureBorders(self, parentFrame):
        borderWidth = parentFrame.winfo_width()
        borderHeight = parentFrame.winfo_height()
        borderColor = CS.D_GRAY
        WS.emborder(parentFrame,
                    [0, 0, borderWidth, borderHeight],
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor])

    def __handleConfigure(self, event):
        # print self.root.tk.eval('wm stackorder '+str(self.winOverlay)+' isabove '+ str(self.root))
        # print "Stackorder: " + self.root.tk.eval('wm stackorder '+str(self.root))
        overlayBelowRoot = self.root.tk.eval('wm stackorder ' + str(self.__winDialogueOverlay)+ ' isabove ' + str(self.root))
        if overlayBelowRoot:
            self.__winDialogueOverlay.lift(self.root)
            self.root.lower(self.__winDialogueOverlay)

        self.__configureUnbind()
        # set a short delay before re-binding to avoid infinite loops
        self.root.after(1, lambda: self.__configureBind())

    def destroyOverlay(self):
        if self.hasOverlay:
            self.__configureUnbind()
            self.winOverlay.destroy()
            self.winOverlay = None

    def __configureBind(self):
        self.root.bind("<Configure>", self.__handleConfigure)

    def __configureUnbind(self):
        self.root.unbind("<Configure>")



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

    def getBtnDialog_NO(self):
        return self.btnDialog_NO

    def getBtnDialog_YES(self):
        return self.btnDialog_YES

    def getLbProgressConsole(self):
        return self.lbProgressConsole
    # endregion getters

    def getIcoWidthCheck(self):
        return self.ico_width_check

    def getIcoHeightCheck(self):
        return self.ico_height_check

    def getIcoWidthCross(self):
        return self.ico_width_cross

    def getIcoHeightCross(self):
        return self.ico_height_cross


