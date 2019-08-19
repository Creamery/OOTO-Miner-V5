#! /usr/bin/env python

"""
{Description}
Automated Mining User Interface
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


import Color_support
import Icon_support
import UI_support
import PIL.Image
import PIL.ImageTk
import CONSTANTS as const
import Function_support as FS


class AutomatedMining_View:

    def __init__(self, parentFrame):
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

        # self.configureTestTabElements(parentFrame)
        # self.configureZTestElements(parentFrame)
        # self.configureTestTabConsoleElements(parentFrame)

    def initTabFrame(self, parentFrame):
        tabFrame = LabelFrame(parentFrame, bd = 0)
        tabFrame.place(
            relx = UI_support.TAB_REL_X, rely = UI_support.TAB_REL_Y,
            relwidth = UI_support.TAB_REL_W, relheight = UI_support.TAB_REL_H
        )
        tabFrame.configure(
            background = Color_support.TAB_BG_COLOR, foreground = Color_support.FG_COLOR
        )
        return tabFrame

    def initTopPaddingUI(self, parentFrame):
        topPaddingFrame = LabelFrame(parentFrame, bd = 0)
        # region init topPaddingFrame
        topPaddingFrame.place(
            relx = UI_support.TAB_TEST_TYPE_REL_X, rely = UI_support.TAB_TEST_TYPE_REL_Y,
            relwidth = UI_support.TAB_TEST_TYPE_REL_W, relheight = UI_support.TAB_TEST_TYPE_REL_H
        )
        topPaddingFrame.configure(
            background = Color_support.TYPE_BG, foreground = Color_support.FG_COLOR
        )
        # endregion topPaddingFrame
        return topPaddingFrame

    def initInputUI(self, parentFrame, relativeFrame):

        # set the UI parent position below relativeFrame
        newRelY = FS.getRelY(relativeFrame) + FS.getRelH(relativeFrame)

        inputFrame = LabelFrame(parentFrame, bd = 0)
        # region init inputFrame
        inputFrame.place(
            relx = UI_support.TAB_TEST_SELECT_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_SELECT_REL_W, relheight = UI_support.TAB_TEST_SELECT_REL_H
        )
        inputFrame.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR
        )
        # endregion init lfInputElements

        self.initFeatureList(inputFrame)

        return inputFrame

    def createTitleBar(self, parentFrame, strNumber, strName, colorBG):
        titleFrame = LabelFrame(parentFrame, bd = 0)
        titleFrame.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR  # , text = '''FILTER'''
        )

        # COLORED SEPARATOR
        self.createLabelSeparator(
            titleFrame, 1,
            False, colorBG, UI_support.TITLE_SEPARATOR_H,
            0.5, W
        )

        titleNumber = Label(titleFrame)
        newRelY = UI_support.LABEL_TITLE_REL_Y
        titleNumber.place(
            relx = 0, rely = newRelY,
            relwidth = 0.04 + 0.05,
            relheight = 1 - (newRelY * 2), anchor = NW)

        titleNumber.configure(
            font = UI_support.FONT_MED_BOLD,
            background = Color_support.SELECT_NUMBER_BG, foreground = Color_support.SELECT_NUMBER_FG,
            text = str(strNumber) + '''  ''',
            bd = 1, relief = GROOVE,
            anchor = SE
        )
        newRelX = FS.getRelX(titleNumber) + FS.getRelW(titleNumber)

        titleText = Label(titleFrame)
        newRelY = FS.getRelY(titleNumber)
        newRelH = FS.getRelH(titleNumber)
        titleText.place(
            relx = newRelX - 0.001, rely = newRelY,
            relwidth = 0.15, relheight = newRelH, anchor = NW)
        titleText.configure(
            font = UI_support.FONT_MED_BOLD,
            background = colorBG, foreground = Color_support.SELECT_TITLE_FG,
            text = str(strName),
            bd = 0, relief = GROOVE,
            anchor = S
        )
        # Title border
        self.separatorlabelFrameSelectTitleText = self.createLabelSeparator(
            titleText, 1,
            True, Color_support.WHITE,
            coordinate = 0.99, specifiedAnchor = NW
        )

        return titleFrame

    def initFeatureList(self, parentFrame):

        titleFrame = self.createTitleBar(parentFrame, '1', 'INPUT', Color_support.SELECT_TITLE_BG)
        # region init titleFrame
        titleFrame.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.12)
        newRelY = FS.getRelY(titleFrame) + FS.getRelH(titleFrame)
        titleRelH = FS.getRelH(titleFrame)
        # endregion init titleFrame

        self.lfFeatureSelect = LabelFrame(parentFrame, bd = 0)
        # region init lfFeatureSelect
        self.lfFeatureSelect.place(
            relx = 0.05, rely = newRelY,
            relwidth = UI_support.TAB_TEST_SELECT_DATASET_REL_W, relheight = 1 - titleRelH
        )
        self.lfFeatureSelect.configure(
            background = Color_support.SELECT_BG
        )
        newRelH = FS.getRelH(self.lfFeatureSelect)
        # endregion init lfFeatureSelect

        self.lfConfirmedFeatures = LabelFrame(parentFrame, bd = 0)
        # region init lfConfirmedFeatures
        self.lfConfirmedFeatures.place(
            relx = UI_support.TAB_TEST_SELECT_DATASET_REL_W + 0.15,
            rely = newRelY, relwidth = 0.4, relheight = newRelH
        )
        self.lfConfirmedFeatures.configure(
            background = Color_support.SELECT_BG
        )
        # endregion init lfConfirmedFeatures

        verticalSeparator = ttk.Separator(parentFrame, orient = VERTICAL)
        # region init vertical separator
        verticalSeparator.place(relx = 0.5, rely = newRelY + 0.05, relheight = 1 - titleRelH - 0.1)
        # endregion init vertical separator

        self.lfStatusFeatureSelect = LabelFrame(self.lfFeatureSelect, bd = 0)
        # region init lfStatusFeatureSelect
        self.lfStatusFeatureSelect.place(
            relx = UI_support.TAB_TEST_SELECT_QUERY_REL_X, rely = UI_support.TAB_TEST_SELECT_QUERY_REL_Y,
            relwidth = UI_support.TAB_TEST_SELECT_QUERY_REL_W, relheight = UI_support.TAB_TEST_SELECT_QUERY_REL_H)

        self.lfStatusFeatureSelect.configure(
            background = Color_support.SELECT_ENTRY_BG, foreground = Color_support.SELECT_ENTRY_FG,
            relief = GROOVE
        )

        # endregion init lfStatusFeatureSelect

        self.lblStatusFeatureSelect = Label(self.lfStatusFeatureSelect)  # TODO getter
        # region init lblStatusFeatureSelect
        self.lblStatusFeatureSelect.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        self.lblStatusFeatureSelect.configure(
            background = Color_support.SELECT_LISTBOX_STATUS_BG, foreground = Color_support.SELECT_LISTBOX_STATUS_FG,
            bd = UI_support.SELECT_STATUS_LABEL_BORDER, relief = UI_support.SELECT_STATUS_LABEL_RELIEF,
            text = UI_support.LBL_SELECT_NO_DATA,
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )
        if UI_support.SELECT_STATUS_LABEL_TOP_SEPARATOR:
            self.labelFrameNoDataAHorizontalSeparator = ttk.Separator(self.lblStatusFeatureSelect,
                                                                      orient = HORIZONTAL)
            self.labelFrameNoDataAHorizontalSeparator.place(relx = 0, rely = 0, relwidth = 1, anchor = NW)

        newRelY = UI_support.TAB_TEST_LISTBOX_QUERY_REL_Y + FS.getRelY(self.lfStatusFeatureSelect) + FS.getRelH(
            self.lfStatusFeatureSelect)

        # endregion init lblStatusFeatureSelect

        self.lfListFeatureSelect = LabelFrame(self.lfFeatureSelect, bd = 0)
        # region lfListFeatureSelect
        self.lfListFeatureSelect.place(
            relx = UI_support.TAB_TEST_LISTBOX_QUERY_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_LISTBOX_QUERY_REL_W, relheight = UI_support.TAB_TEST_LISTBOX_QUERY_REL_H)
        # endregion lfListFeatureSelect

        self.lfQueryFeatureSelect = LabelFrame(self.lfListFeatureSelect, bd = 0)
        # region init lfQueryFeatureSelect
        specifiedListBoxHeight = (0.78 - 0.03)
        newRelH = 1 - specifiedListBoxHeight  # TODO Make constant (0.78 - 0.03) is the listbox's supposed height
        self.lfQueryFeatureSelect.place(relx = 0, rely = 0, relwidth = 1, relheight = newRelH)
        newRelH = FS.getRelH(self.lfQueryFeatureSelect) * UI_support.SELECT_LABEL_STRIPES_REL_H_MULTIPLIER  # 5 / 8 # TODO Make constant reference
        # endregion init lfQueryFeatureSelect

        self.lblStripesQueryFeatureSelect = Label(self.lfListFeatureSelect, bd = 0, relief = GROOVE)  # TODO getter
        # region init lblStripesQueryFeatureSelect
        self.lblStripesQueryFeatureSelect.place(
            relx = 0,
            rely = 0,
            # rely = newRelY,
            relwidth = 1,
            relheight = newRelH,
            anchor = NW
        )
        newRelY = FS.getRelY(self.lblStripesQueryFeatureSelect) + FS.getRelH(self.lblStripesQueryFeatureSelect)

        # region reposition lfQueryFeatureSelect
        self.lfQueryFeatureSelect.place(
            relx = FS.getRelX(self.lfQueryFeatureSelect),
            rely = newRelY,
            relwidth = FS.getRelW(self.lfQueryFeatureSelect),
            relheight = FS.getRelH(self.lfQueryFeatureSelect),
        )
        # endregion reposition lfQueryFeatureSelect

        im = PIL.Image.open(
            Icon_support.TEXTURE_STRIPE_PINK)
        texture_pink_stripes = PIL.ImageTk.PhotoImage(im)
        self.lblStripesQueryFeatureSelect.configure(
            image = texture_pink_stripes,
            anchor = SW
        )
        self.lblStripesQueryFeatureSelect.image = texture_pink_stripes  # < ! > Required to make images appear

        # endregion init lblStripesQueryFeatureSelect

        lfBorderQueryFeatureList = LabelFrame(self.lfQueryFeatureSelect, bd = 0)
        # region init lfBorderQueryFeatureList
        lfBorderQueryFeatureList.place(
            relx = 0, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_LBL_REL_W, relheight = 1
        )
        lfBorderQueryFeatureList.configure(
            background = Color_support.SELECT_BUTTONS_BG
        )
        # endregion init lfBorderQueryFeatureList

        lblQueryFeatureList = Label(lfBorderQueryFeatureList)
        # region init lblQueryFeatureList
        lblQueryFeatureList.place(
            relx = 0.01, rely = 0.025,
            relwidth = 0.98, relheight = 0.95)
        lblQueryFeatureList.configure(
            background = Color_support.SELECT_LABEL_BG, foreground = Color_support.SELECT_LABEL_FG,
            text = UI_support.SELECT_LABEL_DATASETA_TEXT,
            font = UI_support.SELECT_LABEL_FONT,
            bd = 0, relief = FLAT,
        )

        newRelX = FS.getRelX(lfBorderQueryFeatureList) + FS.getRelW(
            lfBorderQueryFeatureList)
        # endregion init lblQueryFeatureList

        self.entryQueryFeatureList = Entry(self.lfQueryFeatureSelect)  # TODO getter
        # region init entryQueryFeatureList
        self.entryQueryFeatureList.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_ENTRY_REL_W, relheight = 1)
        self.entryQueryFeatureList.configure(
            background = Color_support.SELECT_ENTRY_BG, foreground = Color_support.SELECT_ENTRY_FG,
            bd = 1,
            font = UI_support.ENTRY_FONT, insertwidth = UI_support.INSERT_WIDTH,
            selectbackground = Color_support.SELECT_ENTRY_SELECT_HIGHLIGHT_BG,
            insertbackground = Color_support.SELECT_ENTRY_SELECT_INSERT_BG,
            takefocus = UI_support.ENTRY_TAKE_FOCUS, justify = UI_support.SELECT_ENTRY_JUSTIFY
        )  # TODO Constant font definiton

        newRelX = FS.getRelX(self.entryQueryFeatureList) + FS.getRelW(
            self.entryQueryFeatureList)  # + UI_support.TAB_3CHILD_LBL_REL_X

        # endregion init entryQueryFeatureList

        self.btnQueryFeatureList = Button(self.lfQueryFeatureSelect)  # TODO getter
        # region init btnQueryFeatureList
        self.btnQueryFeatureList.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_BTN_REL_W, relheight = 1)

        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW).resize(Icon_support.SELECT_ICO_SIZE_BUTTONS,
                                                                     PIL.Image.ANTIALIAS)
        btn_query_set_icon = PIL.ImageTk.PhotoImage(im)
        self.btnQueryFeatureList.configure(
            image = btn_query_set_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.btnQueryFeatureList.image = btn_query_set_icon  # < ! > Required to make images appear

        self.btnQueryFeatureList.configure(
            background = Color_support.SELECT_BUTTONS_BG, foreground = Color_support.SELECT_BUTTONS_FG,
            activebackground = Color_support.SELECT_BG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE
        )
        # endregion init btnQueryFeatureList


        self.lbListFeatureSelect = Listbox(self.lfListFeatureSelect)  # TODO getter
        # region init lbListFeatureSelect
        self.lbListFeatureSelect.configure(
            background = Color_support.SELECT_LISTBOX_BG, foreground = Color_support.SELECT_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = Color_support.SELECT_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = Color_support.SELECT_LISTBOX_SELECTED_ITEM_FG,
            font = UI_support.SELECT_LABEL_FONT,
            bd = UI_support.SELECT_LISTBOX_BORDER, relief = UI_support.SELECT_LISTBOX_RELIEF,
            highlightthickness = 0
        )
        newRelY = FS.getRelY(self.lfQueryFeatureSelect) + FS.getRelH(self.lfQueryFeatureSelect)
        newRelH = 1 - (FS.getRelH(self.lfQueryFeatureSelect) + FS.getRelH(self.lblStripesQueryFeatureSelect))
        self.lbListFeatureSelect.place(relx = 0, rely = newRelY, relwidth = 1, relheight = newRelH)

        newRelY = UI_support.TAB_TEST_COMMANDS_QUERY_REL_Y + FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(
            self.lfListFeatureSelect)

        # endregion init lbListFeatureSelect


        lfCommandsFeatureSelect = LabelFrame(self.lfFeatureSelect, bd = 0)
        # region init lfCommandsFeatureSelect
        lfCommandsFeatureSelect.place(
            relx = UI_support.TAB_TEST_COMMANDS_QUERY_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_COMMANDS_QUERY_REL_W,
            relheight = UI_support.TAB_TEST_COMMANDS_QUERY_REL_H * 0.85)  # TODO Reduced size

        lfCommandsFeatureSelect.configure(
            background = Color_support.WHITE
        )
        # endregion init lfCommandsFeatureSelect

        self.btnResetFeatureSelect = Button(lfCommandsFeatureSelect)  # TODO getter
        # region init btnResetFeatureSelect
        self.btnResetFeatureSelect.place(
            relx = 0, rely = 0,
            relwidth = 0.25, relheight = 1)
        self.btnResetFeatureSelect.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)

        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_reset_icon = PIL.ImageTk.PhotoImage(im)
        self.btnResetFeatureSelect.configure(
            image = btn_query_reset_icon)
        self.btnResetFeatureSelect.image = btn_query_reset_icon  # < ! > Required to make images appear

        newRelX = FS.getRelX(self.btnResetFeatureSelect) + FS.getRelW(self.btnResetFeatureSelect)

        # endregion init btnResetFeatureSelect

        lfCountFeatureSelect = LabelFrame(lfCommandsFeatureSelect, bd = 1)
        # region init lfCountFeatureSelect
        lfCountFeatureSelect.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.50 - 0.005, relheight = 1
        )
        lfCountFeatureSelect.configure(
            background = Color_support.SELECT_BG
        )

        # Define count variables
        self.featureSelectCount = 0
        self.confirmedFeaturesCount = 0

        # endregion init lfCountFeatureSelect

        self.labelQueryDataACount = Label(lfCountFeatureSelect)
        self.labelQueryDataACount.place(relx = 0, rely = 0, relwidth = 1,
                                        relheight = UI_support.TAB_TEST_SELECT_COUNT_REL_H)
        self.labelQueryDataACount.configure(
            font = UI_support.FONT_LARGE_BOLD,
            background = Color_support.SELECT_BG,
            text = self.getDatasetCountA()
        )
        self.labelQueryDataACountText = Label(lfCountFeatureSelect)
        self.labelQueryDataACountText.place(
            relx = 0, rely = FS.getRelH(self.labelQueryDataACount),
            relwidth = 1, relheight = UI_support.TAB_TEST_SELECT_COUNT_TEXT_REL_H)
        self.labelQueryDataACountText.configure(
            font = UI_support.FONT_DEFAULT_BOLD,
            background = Color_support.FG_COLOR, foreground = Color_support.SELECT_BG,
            text = '''SAMPLES'''
        )
        # endregion

        # COMMAND BORDERS - DATASET A
        # region
        newRelY = FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(self.lfListFeatureSelect)

        self.separatorlabelFrameCommandsARight = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsARight.place(
            relx = FS.getRelX(self.lfStatusFeatureSelect),
            rely = newRelY,
            relheight = 1 - newRelY - 0.025,  # TODO To adjust border height, just adjust this
            width = 1)
        self.separatorlabelFrameCommandsARight.configure(background = Color_support.DISABLED_D_BLUE)

        self.separatorlabelFrameCommandsALeft = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsALeft.place(
            relx = 1 - FS.getRelX(self.lfStatusFeatureSelect),
            rely = FS.getRelY(self.separatorlabelFrameCommandsARight),
            relheight = FS.getRelH(self.separatorlabelFrameCommandsARight),
            width = 1
        )
        self.separatorlabelFrameCommandsALeft.configure(background = Color_support.DISABLED_D_BLUE)

        self.separatorlabelFrameCommandsABottom = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsABottom.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsARight),
            # rely = 0.997,
            rely = FS.getRelY(self.separatorlabelFrameCommandsALeft) +
                   FS.getRelH(self.separatorlabelFrameCommandsALeft) - 0.003,
            relwidth = FS.getRelX(self.separatorlabelFrameCommandsALeft) - FS.getRelX(
                self.separatorlabelFrameCommandsARight),
            height = 1)
        self.separatorlabelFrameCommandsABottom.configure(background = Color_support.DISABLED_D_BLUE)

        newRelY = FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(self.lfListFeatureSelect)

        self.separatorlabelFrameCommandsATop = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsATop.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsARight),
            rely = newRelY,
            relwidth = FS.getRelW(self.separatorlabelFrameCommandsABottom),
            height = 1)
        self.separatorlabelFrameCommandsATop.configure(background = Color_support.DISABLED_D_BLUE)

        # endregion

        # endregion

        #  QUERY PARENT (DATASET B)
        # region
        self.labelFrameQueryDataB = LabelFrame(self.lfConfirmedFeatures, bd = 0)
        self.labelFrameQueryDataB.place(
            relx = FS.getRelX(self.lfStatusFeatureSelect),
            rely = FS.getRelY(self.lfStatusFeatureSelect),
            relwidth = FS.getRelW(self.lfStatusFeatureSelect),
            relheight = FS.getRelH(self.lfStatusFeatureSelect))
        self.labelFrameQueryDataB.configure(
            background = Color_support.SELECT_ENTRY_BG, foreground = Color_support.SELECT_ENTRY_FG,
            relief = GROOVE  # , text = '''Dataset B'''
        )
        # endregion
        # LISTBOX PARENT (DATASET B)
        # region
        self.labelFrameListBoxB = LabelFrame(self.lfConfirmedFeatures, bd = 0)
        self.labelFrameListBoxB.place(
            relx = FS.getRelX(self.lfListFeatureSelect),
            rely = FS.getRelY(self.lfListFeatureSelect),
            relwidth = FS.getRelW(self.lfListFeatureSelect),
            relheight = FS.getRelH(self.lfListFeatureSelect)
        )

        # STATUS CHILDREN - DATASET B
        # region

        # QUERY TOP STRIPE PARENT - DATASET B
        # region
        self.labelQuerySetDataStripesB = Label(self.labelFrameListBoxB, bd = 0, relief = GROOVE)
        self.labelQuerySetDataStripesB.place(
            relx = FS.getRelX(self.lblStripesQueryFeatureSelect),
            rely = FS.getRelY(self.lblStripesQueryFeatureSelect),
            relwidth = FS.getRelW(self.lblStripesQueryFeatureSelect),
            relheight = FS.getRelH(self.lblStripesQueryFeatureSelect)
        )
        im = PIL.Image.open(
            Icon_support.TEXTURE_STRIPE_PINK)
        texture_pink_stripes = PIL.ImageTk.PhotoImage(im)
        self.labelQuerySetDataStripesB.configure(
            image = texture_pink_stripes,
            anchor = SW
        )
        self.labelQuerySetDataStripesB.image = texture_pink_stripes  # < ! > Required to make images appear
        # endregion

        self.labelQuerySetDataStatusB = Label(self.labelFrameQueryDataB)
        # self.labelQuerySetDataStatusB = Label(self.labelFrameListBoxB)
        self.labelQuerySetDataStatusB.place(
            relx = FS.getRelX(self.lblStatusFeatureSelect),
            rely = FS.getRelY(self.lblStatusFeatureSelect),
            relwidth = FS.getRelW(self.lblStatusFeatureSelect),
            relheight = FS.getRelH(self.lblStatusFeatureSelect)
        )
        # self.labelQuerySetDataStatusB.place(relx = 0, rely = newRelY, relwidth = 1, relheight = newRelH)
        self.labelQuerySetDataStatusB.configure(
            background = Color_support.SELECT_LISTBOX_STATUS_BG, foreground = Color_support.SELECT_LISTBOX_STATUS_FG,
            bd = UI_support.SELECT_STATUS_LABEL_BORDER, relief = UI_support.SELECT_STATUS_LABEL_RELIEF,
            text = UI_support.LBL_SELECT_NO_DATA,
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )
        # endregion

        # endregion

        self.listQuerySetDataB = Listbox(self.labelFrameListBoxB)
        self.listQuerySetDataB.configure(
            background = Color_support.SELECT_LISTBOX_BG, foreground = Color_support.SELECT_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = Color_support.SELECT_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = Color_support.SELECT_LISTBOX_SELECTED_ITEM_FG,
            font = UI_support.SELECT_LABEL_FONT,
            bd = UI_support.SELECT_LISTBOX_BORDER, relief = UI_support.SELECT_LISTBOX_RELIEF,
            highlightthickness = 0
        )

        self.listQuerySetDataB.place(
            relx = FS.getRelX(self.lbListFeatureSelect),
            rely = FS.getRelY(self.lbListFeatureSelect),
            relwidth = FS.getRelW(self.lbListFeatureSelect),
            relheight = FS.getRelH(self.lbListFeatureSelect)
        )

        # STATUS - DATASET B
        # region
        self.labelFrameQuerySetDataStatusB = LabelFrame(self.labelFrameListBoxB, bd = 0)
        self.labelFrameQuerySetDataStatusB.place(
            relx = FS.getRelX(self.lfQueryFeatureSelect),
            rely = FS.getRelY(self.lfQueryFeatureSelect),
            relwidth = FS.getRelW(self.lfQueryFeatureSelect),
            relheight = FS.getRelH(self.lfQueryFeatureSelect)
        )
        # endregion

        # QUERY CHILDREN - DATASET B
        # region
        self.labelFrameBorderQuerySetDataB = LabelFrame(self.labelFrameQuerySetDataStatusB, bd = 0)
        self.labelFrameBorderQuerySetDataB.place(
            relx = FS.getRelX(lfBorderQueryFeatureList),
            rely = FS.getRelY(lfBorderQueryFeatureList),
            relwidth = FS.getRelW(lfBorderQueryFeatureList),
            relheight = FS.getRelH(lfBorderQueryFeatureList))
        self.labelFrameBorderQuerySetDataB.configure(
            background = Color_support.SELECT_BUTTONS_BG
        )

        self.labelQuerySetDataB = Label(self.labelFrameBorderQuerySetDataB)

        self.labelQuerySetDataB.place(
            relx = FS.getRelX(lblQueryFeatureList),
            rely = FS.getRelY(lblQueryFeatureList),
            relwidth = FS.getRelW(lblQueryFeatureList),
            relheight = FS.getRelH(lblQueryFeatureList))
        self.labelQuerySetDataB.configure(
            background = Color_support.SELECT_LABEL_BG, foreground = Color_support.SELECT_LABEL_FG,
            text = UI_support.SELECT_LABEL_DATASETB_TEXT,
            font = UI_support.SELECT_LABEL_FONT,
            bd = 0, relief = FLAT,
        )

        # ENTER CODE DATASET B

        self.entryQuerySetDataB = Entry(self.labelFrameQuerySetDataStatusB)
        self.entryQuerySetDataB.place(
            relx = FS.getRelX(self.entryQueryFeatureList),
            rely = FS.getRelY(self.entryQueryFeatureList),
            relwidth = FS.getRelW(self.entryQueryFeatureList),
            relheight = FS.getRelH(self.entryQueryFeatureList))
        self.entryQuerySetDataB.configure(
            background = Color_support.SELECT_ENTRY_BG, foreground = Color_support.SELECT_ENTRY_FG,
            bd = 1,
            font = UI_support.ENTRY_FONT, insertwidth = UI_support.INSERT_WIDTH,
            selectbackground = Color_support.SELECT_ENTRY_SELECT_HIGHLIGHT_BG,
            insertbackground = Color_support.SELECT_ENTRY_SELECT_INSERT_BG,
            takefocus = UI_support.ENTRY_TAKE_FOCUS, justify = UI_support.SELECT_ENTRY_JUSTIFY
        )  # TODO Constant font definiton

        # DATASET B
        self.buttonQuerySetDataB = Button(self.labelFrameQuerySetDataStatusB)
        self.buttonQuerySetDataB.place(
            relx = FS.getRelX(self.btnQueryFeatureList),
            rely = FS.getRelY(self.btnQueryFeatureList),
            relwidth = FS.getRelW(self.btnQueryFeatureList),
            relheight = FS.getRelH(self.btnQueryFeatureList))

        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW).resize(Icon_support.SELECT_ICO_SIZE_BUTTONS,
                                                                     PIL.Image.ANTIALIAS)
        btn_query_set_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQuerySetDataB.configure(
            image = btn_query_set_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQuerySetDataB.image = btn_query_set_icon  # < ! > Required to make images appear

        self.buttonQuerySetDataB.configure(
            background = Color_support.SELECT_BUTTONS_BG, foreground = Color_support.SELECT_BUTTONS_FG,
            activebackground = Color_support.SELECT_BTN_BG_ACTIVE,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE,
            # text = '''Find Feature'''
        )
        # endregion

        # COMMANDS PARENT (DATASET B)
        # region
        self.labelFrameCommandsB = LabelFrame(self.lfConfirmedFeatures, bd = 0)
        self.labelFrameCommandsB.place(
            relx = FS.getRelX(lfCommandsFeatureSelect),
            rely = FS.getRelY(lfCommandsFeatureSelect),
            relwidth = FS.getRelW(lfCommandsFeatureSelect),
            relheight = FS.getRelH(lfCommandsFeatureSelect)
        )
        # self.labelFrameCommandsB.place(
        #     relx = UI_support.TAB_TEST_COMMANDS_QUERY_REL_X, rely = newRelY,
        #     relwidth = UI_support.TAB_TEST_COMMANDS_QUERY_REL_W, relheight = UI_support.TAB_TEST_COMMANDS_QUERY_REL_H)

        self.labelFrameCommandsB.configure(
            background = Color_support.WHITE
        )
        # endregion

        # RESET BUTTON (DATASET B)
        # region
        self.buttonQueryResetFilterB = Button(self.labelFrameCommandsB)
        self.buttonQueryResetFilterB.place(
            relx = 0, rely = 0,
            relwidth = 0.25, relheight = 1)
        self.buttonQueryResetFilterB.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        # text = '''Reset''')

        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_reset_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryResetFilterB.configure(
            image = btn_query_reset_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryResetFilterB.image = btn_query_reset_icon  # < ! > Required to make images appear

        # endregion

        # COMMAND BORDERS - DATASET B
        # region
        # newRelY = FS.getRelY(self.labelFrameListBoxB) + FS.getRelH(self.labelFrameListBoxB)

        self.separatorlabelFrameCommandsBRight = Label(self.lfConfirmedFeatures)
        self.separatorlabelFrameCommandsBRight.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsARight),
            rely = FS.getRelY(self.separatorlabelFrameCommandsARight),
            relheight = FS.getRelH(self.separatorlabelFrameCommandsARight),
            width = 1
        )
        self.separatorlabelFrameCommandsBRight.configure(background = Color_support.DISABLED_D_BLUE)

        self.separatorlabelFrameCommandsBLeft = Label(self.lfConfirmedFeatures)
        self.separatorlabelFrameCommandsBLeft.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsALeft),
            rely = FS.getRelY(self.separatorlabelFrameCommandsALeft),
            relheight = FS.getRelH(self.separatorlabelFrameCommandsALeft),
            width = 1
        )
        self.separatorlabelFrameCommandsBLeft.configure(background = Color_support.DISABLED_D_BLUE)

        self.separatorlabelFrameCommandsBBottom = Label(self.lfConfirmedFeatures)
        self.separatorlabelFrameCommandsBBottom.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsABottom),
            rely = FS.getRelY(self.separatorlabelFrameCommandsABottom),
            relwidth = FS.getRelW(self.separatorlabelFrameCommandsABottom),
            height = 1)
        self.separatorlabelFrameCommandsBBottom.configure(background = Color_support.DISABLED_D_BLUE)

        newRelY = FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(self.lfListFeatureSelect)

        self.separatorlabelFrameCommandsBTop = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsBTop.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsATop),
            rely = FS.getRelY(self.separatorlabelFrameCommandsATop),
            relwidth = FS.getRelW(self.separatorlabelFrameCommandsATop),
            height = 1)
        self.separatorlabelFrameCommandsATop.configure(background = Color_support.DISABLED_PALER_YELLOW)

        # endregion

        # QUERY COUNT (DATASET B)
        # region
        lfCountFeatureSelectB = LabelFrame(self.labelFrameCommandsB, bd = 1)
        lfCountFeatureSelectB.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.50 - 0.005, relheight = 1
        )
        lfCountFeatureSelectB.configure(
            background = Color_support.SELECT_BG
        )

        self.labelQueryDataBCount = Label(lfCountFeatureSelectB)
        self.labelQueryDataBCount.place(relx = 0, rely = 0, relwidth = 1,
                                        relheight = UI_support.TAB_TEST_SELECT_COUNT_REL_H)
        self.labelQueryDataBCount.configure(
            font = UI_support.FONT_LARGE_BOLD,
            background = Color_support.SELECT_BG,
            text = self.getDatasetCountB()
        )
        self.labelQueryDataBCountText = Label(lfCountFeatureSelectB)
        self.labelQueryDataBCountText.place(
            relx = 0, rely = FS.getRelH(self.labelQueryDataBCount),
            relwidth = 1, relheight = UI_support.TAB_TEST_SELECT_COUNT_TEXT_REL_H)
        self.labelQueryDataBCountText.configure(
            font = UI_support.FONT_DEFAULT_BOLD,
            background = Color_support.FG_COLOR, foreground = Color_support.SELECT_BG,
            text = '''SAMPLES'''
        )

        # Create the left separator
        # lfCountFeatureSelectLeftSeparatorB = ttk.Separator(lfCountFeatureSelectB, orient = VERTICAL)
        # lfCountFeatureSelectLeftSeparatorB.place(relx = 0, rely = 0, relheight = 1)

        # lfCountFeatureSelectRightSeparatorB = ttk.Separator(lfCountFeatureSelectB, orient = VERTICAL)
        # lfCountFeatureSelectRightSeparatorB.place(relx = 0.99, rely = 0, relheight = 1)
        # endregion

        # FILTER BUTTON (DATASET A)
        # region
        newRelX = FS.getRelX(lfCountFeatureSelect) + FS.getRelW(lfCountFeatureSelect)
        newRelX = FS.getRelX(lfCountFeatureSelect) + FS.getRelW(lfCountFeatureSelect)

        self.buttonQueryAddFilterA = Button(lfCommandsFeatureSelect, compound = CENTER)
        self.buttonQueryAddFilterA.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.25 - 0.005, relheight = 1
        )

        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_filter_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryAddFilterA.configure(
            image = btn_query_filter_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryAddFilterA.image = btn_query_filter_icon  # < ! > Required to make images appear

        self.buttonQueryAddFilterA.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        # text = '''Filter''')
        self.buttonQueryAddFilterA.pack(side = RIGHT)
        self.btnResetFeatureSelect.pack(side = LEFT)

        # endregion
        # FILTER BUTTON (DATASET B)
        # region
        newRelX = FS.getRelX(lfCountFeatureSelectB) + FS.getRelW(lfCountFeatureSelectB)

        self.buttonQueryAddFilterB = Button(self.labelFrameCommandsB, compound = CENTER)
        self.buttonQueryAddFilterB.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.25 - 0.005, relheight = 1
        )

        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_filter_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryAddFilterB.configure(
            image = btn_query_filter_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryAddFilterB.image = btn_query_filter_icon  # < ! > Required to make images appear

        self.buttonQueryAddFilterB.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        # text = '''Filter''')
        self.buttonQueryAddFilterB.pack(side = RIGHT)

        self.buttonQueryResetFilterB.pack(side = LEFT)
        # endregion

        # self.configureSelectElements(self.lfInputElements)  # Configures all sub elements under SELECT




    def initProcessUI(self, parentFrame, relativeFrame):

        newRelY = FS.getRelY(relativeFrame) + FS.getRelH(relativeFrame)  # TODO Make constant (space in between)

        # FILTER Parent Frame
        processFrame = LabelFrame(parentFrame, bd = 0)
        processFrame.place(
            relx = UI_support.TAB_TEST_FILTER_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_REL_W, relheight = UI_support.TAB_TEST_FILTER_REL_H
        )
        processFrame.configure(
            background = Color_support.FILTER_BG, foreground = Color_support.FG_COLOR  # , text = '''FILTER'''
        )

        self.configureFilterElements(processFrame)  # Configures all sub elements under FILTER
        return processFrame

    def initResultsUI(self, parentFrame, relativeFrame):

        newRelY = FS.getRelY(relativeFrame) + FS.getRelH(relativeFrame)

        # PROCESS Parent Frame
        resultsFrame = LabelFrame(parentFrame, bd = 0)
        resultsFrame.place(
            # relx = UI_support.TAB_TEST_PROCESS_REL_X,
            relx = FS.getRelX(relativeFrame),
            rely = newRelY,
            relwidth = UI_support.TAB_TEST_PROCESS_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_REL_H
        )
        resultsFrame.configure(
            background = Color_support.PROCESS_BG, foreground = Color_support.FG_COLOR  # , text = '''PROCESS'''
        )

        self.configureProcessElements(resultsFrame)  # Configures all sub elements under FILTER
        return resultsFrame


    def initConsoleUI(self, parentFrame, relativeFrame):
        prevFrameRelX = float(relativeFrame.place_info()['relx'])
        prevFrameRelW = float(relativeFrame.place_info()['relwidth'])
        newRelX = prevFrameRelX + prevFrameRelW

        # CONSOLE Parent Frame
        consoleFrame = LabelFrame(parentFrame, bd = 1, relief = GROOVE)
        # self.labelFrameConsoleElements.place(
        #     relx = newRelX, rely = UI_support.TAB_TEST_CONSOLE_REL_Y,
        #     relwidth = UI_support.TAB_TEST_CONSOLE_REL_W, relheight = UI_support.TAB_TEST_CONSOLE_REL_H
        # )
        consoleFrame.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_CONSOLE_REL_W, relheight = 1
        )
        consoleFrame.configure(
            background = Color_support.WHITE, foreground = Color_support.FG_COLOR  # , text = '''CONSOLE'''
        )

        self.configureConsoleElements(consoleFrame)  # Configures all sub elements under CONSOLE
        self.testTabLeftSeparator = ttk.Separator(parentFrame, orient = VERTICAL)
        self.testTabLeftSeparator.place(relx = 0, rely = 0, relheight = 1)
        return consoleFrame





    # def configureTestTabElements(self, parentFrame):
    #     self.lfTabParentFrame = LabelFrame(parentFrame, bd = 0)
    #     self.lfTabParentFrame.place(
    #         relx = UI_support.TAB_REL_X, rely = UI_support.TAB_REL_Y,
    #         relwidth = UI_support.TAB_REL_W, relheight = UI_support.TAB_REL_H
    #     )
    #     self.lfTabParentFrame.configure(
    #         background = Color_support.TAB_BG_COLOR, foreground = Color_support.FG_COLOR
    #     )
    #
    #     # TYPE Parent Frame
    #     self.labelFrameTypeElements = LabelFrame(self.lfTabParentFrame, bd = 0)
    #     self.labelFrameTypeElements.place(
    #         relx = UI_support.TAB_TEST_TYPE_REL_X, rely = UI_support.TAB_TEST_TYPE_REL_Y,
    #         relwidth = UI_support.TAB_TEST_TYPE_REL_W, relheight = UI_support.TAB_TEST_TYPE_REL_H
    #         # + 0.05 # TODO Type edit
    #     )
    #     self.labelFrameTypeElements.configure(
    #         background = Color_support.TYPE_BG, foreground = Color_support.FG_COLOR  # , text = '''TYPE'''
    #     )
    #
    #     newRelY = FS.getRelY(self.labelFrameTypeElements) + FS.getRelH(self.labelFrameTypeElements)
    #
    #     # SELECT Parent Frame (Datasets)
    #     self.labelFrameSelectElements = LabelFrame(self.lfTabParentFrame, bd = 0)
    #     self.labelFrameSelectElements.place(
    #         relx = UI_support.TAB_TEST_SELECT_REL_X, rely = newRelY,
    #         relwidth = UI_support.TAB_TEST_SELECT_REL_W, relheight = UI_support.TAB_TEST_SELECT_REL_H
    #     )
    #     self.labelFrameSelectElements.configure(
    #         background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR  # , text = '''SELECT'''
    #     )
    #
    #     self.configureSelectElements(self.labelFrameSelectElements)  # Configures all sub elements under SELECT
    #
    #     newRelY = FS.getRelY(self.labelFrameSelectElements) + FS.getRelH(
    #         self.labelFrameSelectElements)  # TODO Make constant (space in between)
    #
    #     # FILTER Parent Frame
    #     self.labelFrameFilterElements = LabelFrame(self.lfTabParentFrame, bd = 0)
    #     self.labelFrameFilterElements.place(
    #         relx = UI_support.TAB_TEST_FILTER_REL_X, rely = newRelY,
    #         relwidth = UI_support.TAB_TEST_FILTER_REL_W, relheight = UI_support.TAB_TEST_FILTER_REL_H
    #     )
    #     self.labelFrameFilterElements.configure(
    #         background = Color_support.FILTER_BG, foreground = Color_support.FG_COLOR  # , text = '''FILTER'''
    #     )
    #
    #     self.configureFilterElements(self.labelFrameFilterElements)  # Configures all sub elements under FILTER
    #
    #     newRelY = FS.getRelY(self.labelFrameFilterElements) + FS.getRelH(self.labelFrameFilterElements)
    #
    #     # PROCESS Parent Frame
    #     self.labelFrameProcessElements = LabelFrame(self.lfTabParentFrame, bd = 0)
    #     self.labelFrameProcessElements.place(
    #         # relx = UI_support.TAB_TEST_PROCESS_REL_X,
    #         relx = FS.getRelX(self.labelFrameSelectElements),
    #         rely = newRelY,
    #         relwidth = UI_support.TAB_TEST_PROCESS_REL_W,
    #         relheight = UI_support.TAB_TEST_PROCESS_REL_H
    #     )
    #     self.labelFrameProcessElements.configure(
    #         background = Color_support.PROCESS_BG, foreground = Color_support.FG_COLOR  # , text = '''PROCESS'''
    #     )
    #
    #     self.configureProcessElements(self.labelFrameProcessElements)  # Configures all sub elements under FILTER
    #
    #     prevFrameRelX = float(self.labelFrameFilterElements.place_info()['relx'])
    #     prevFrameRelW = float(self.labelFrameFilterElements.place_info()['relwidth'])
    #     newRelX = prevFrameRelX + prevFrameRelW
    #
    #     # CONSOLE Parent Frame
    #     self.labelFrameConsoleElements = LabelFrame(self.lfTabParentFrame, bd = 1, relief = GROOVE)
    #     # self.labelFrameConsoleElements.place(
    #     #     relx = newRelX, rely = UI_support.TAB_TEST_CONSOLE_REL_Y,
    #     #     relwidth = UI_support.TAB_TEST_CONSOLE_REL_W, relheight = UI_support.TAB_TEST_CONSOLE_REL_H
    #     # )
    #     self.labelFrameConsoleElements.place(
    #         relx = newRelX, rely = 0,
    #         relwidth = UI_support.TAB_TEST_CONSOLE_REL_W, relheight = 1
    #     )
    #     self.labelFrameConsoleElements.configure(
    #         background = Color_support.WHITE, foreground = Color_support.FG_COLOR  # , text = '''CONSOLE'''
    #     )
    #
    #     self.configureConsoleElements(self.labelFrameConsoleElements)  # Configures all sub elements under CONSOLE
    #     self.testTabLeftSeparator = ttk.Separator(self.lfTabParentFrame, orient = VERTICAL)
    #     self.testTabLeftSeparator.place(relx = 0, rely = 0, relheight = 1)


    ''' --> Configure TEST ("TEST") TAB (2.2) <-- '''

    def configureTestTabConsoleElements(self, parentFrame):
        self.testTabConsoleParentFrame = LabelFrame(parentFrame, bd = 0)
        newRelW = 0.2
        # self.testTabConsoleParentFrame.place(
        #     relx = 1 - newRelW,
        #     rely = FS.getRelY(self.testTabParentFrame),
        #     relwidth = newRelW,
        #     relheight = FS.getRelH(self.testTabParentFrame)
        # )
        self.testTabConsoleParentFrame.configure(
            background = Color_support.D_BLUE, foreground = Color_support.FG_COLOR
        )



    def configureZTestElements(self, parentFrame):

        global arrQueryCriticalValue
        global arrQueryCriticalValueMapping

        # > COMBO BOX
        global testTypes
        testTypes = ["Sample vs Sample", "Sample vs Population"]
        self.comboQueryTest = ttk.Combobox(parentFrame)
        # self.comboQueryTest.place(relx = 0.01, rely = 0.02, height = 50, width = 360) # 316) # TODO SVP
        self.comboQueryTest.configure(exportselection = "0")
        self.comboQueryTest.configure(takefocus = "")
        self.comboQueryTest.configure(values = testTypes)
        self.comboQueryTest.current(0)
        self.comboQueryTest.configure(state = "readonly")

        # > CHI-TEST FRAME

        self.labelFrameQueryChi = LabelFrame(parentFrame)
        # self.labelFrameQueryChi.place(relx = 0.5, rely = 0.78, relheight = 0,
        #                               relwidth = 0)# 0.48)
        self.labelFrameQueryChi.configure(relief = GROOVE)
        self.labelFrameQueryChi.configure(foreground = "black")
        self.labelFrameQueryChi.configure(text = '''Chi Test''')
        self.labelFrameQueryChi.configure(background = "#d9d9d9")

        # > Z-TEST FRAME POPULATION ##### TODO Add functionality
        # region
        self.labelFrameQuerySvP = LabelFrame(parentFrame)
        # self.labelFrameQuerySvP.place(relx = 0.01, rely = 0.88, relheight = 0.1,
        #                               relwidth = 0.3) # 0.48) # TODO SVP
        self.labelFrameQuerySvP.configure(relief = GROOVE)
        self.labelFrameQuerySvP.configure(foreground = "black")
        self.labelFrameQuerySvP.configure(text = '''Z-Test Sample Vs Population''')
        self.labelFrameQuerySvP.configure(background = "#d9d9d9")

        self.comboQueryCriticalValueSvP = ttk.Combobox(self.labelFrameQuerySvP)
        # self.comboQueryCriticalValueSvP.place(relx = 0.24, rely = 0.01, height = 0, width = 0)
        self.comboQueryCriticalValueSvP.configure(exportselection = "0")
        self.comboQueryCriticalValueSvP.configure(takefocus = "")
        self.comboQueryCriticalValueSvP.configure(values = arrQueryCriticalValue)
        self.comboQueryCriticalValueSvP.set(arrQueryCriticalValue[0])
        self.comboQueryCriticalValueSvP.configure(state = "disabled")

        self.labelQueryZTestSvP = Label(self.labelFrameQuerySvP)
        # self.labelQueryZTestSvP.place(relx = 0.47, rely = 0.01, height = 0, width = 0)
        # self.labelQueryZTest.configure(background = "#d9d9d9")
        self.labelQueryZTestSvP.configure(disabledforeground = "#a3a3a3")
        self.labelQueryZTestSvP.configure(foreground = "#000000")
        self.labelQueryZTestSvP.configure(text = '''NO DATA''')
        self.labelQueryZTestSvP.configure(state = "disabled")

        self.buttonQueryZTestSvP = Button(self.labelFrameQuerySvP)
        self.buttonQueryZTestSvP.place(relx = 0.01, rely = 0.01, height = 20, width = 300)
        self.buttonQueryZTestSvP.configure(activebackground = "#d9d9d9")
        self.buttonQueryZTestSvP.configure(activeforeground = "#000000")
        self.buttonQueryZTestSvP.configure(background = "#d9d9d9")
        self.buttonQueryZTestSvP.configure(disabledforeground = "#a3a3a3")
        self.buttonQueryZTestSvP.configure(foreground = "#000000")
        self.buttonQueryZTestSvP.configure(highlightbackground = "#d9d9d9")
        self.buttonQueryZTestSvP.configure(highlightcolor = "black")
        self.buttonQueryZTestSvP.configure(pady = "0")
        self.buttonQueryZTestSvP.configure(text = '''Test''')
        self.buttonQueryZTestSvP.configure(state = "disabled")

        # endregion


    """ >>> FUNCTIONS FOR THE CONFIGURATION OF UI ELEMENTS <<< """
    # region

    ''' --> Elements under TEST ("TEST") TAB (2) <-- '''
    # region
    ''' -> Elements under the SELECT ("GROUP") HEADER <- '''

    def configureSelectElements(self, parentFrame):

        global queryStrFilterB

        # SELECT TITLE
        self.labelFrameSelectTitle = LabelFrame(parentFrame, bd = 0)
        self.labelFrameSelectTitle.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.12)
        self.labelFrameSelectTitle.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR  # , text = '''FILTER'''
        )

        # Create the top separator
        # self.labelFrameSelectHorizontalSeparator = ttk.Separator(self.labelFrameSelectTitle, orient = HORIZONTAL)
        # self.labelFrameSelectHorizontalSeparator.place(relx = 0.05, rely = 0.5, relwidth = 0.9)

        # COLORED SEPARATOR
        self.separatorlabelFrameSelectTitleNumber = self.createLabelSeparator(
            self.labelFrameSelectTitle, 1,
            False, Color_support.SELECT_TITLE_BG, UI_support.TITLE_SEPARATOR_H,
            0.5, W
        )

        # SELECT NUMBER
        self.labelFrameSelectTitleNumber = Label(self.labelFrameSelectTitle)
        newRelY = UI_support.LABEL_TITLE_REL_Y
        self.labelFrameSelectTitleNumber.place(
            relx = 0, rely = newRelY,
            relwidth = 0.04 + 0.05,
            relheight = 1 - (newRelY * 2), anchor = NW)

        self.labelFrameSelectTitleNumber.configure(
            font = UI_support.FONT_MED_BOLD,
            # background = Color_support.BG_TITLE, foreground = Color_support.FG_TITLE,
            background = Color_support.SELECT_NUMBER_BG, foreground = Color_support.SELECT_NUMBER_FG,
            text = '''1  ''',
            bd = 1, relief = GROOVE,
            anchor = SE
        )
        newRelX = FS.getRelX(self.labelFrameSelectTitleNumber) + FS.getRelW(self.labelFrameSelectTitleNumber)

        # SELECT TITLE
        self.labelFrameSelectTitleText = Label(self.labelFrameSelectTitle)
        newRelY = FS.getRelY(self.labelFrameSelectTitleNumber)
        newRelH = FS.getRelH(self.labelFrameSelectTitleNumber)
        self.labelFrameSelectTitleText.place(
            relx = newRelX - 0.001, rely = newRelY,
            relwidth = 0.15, relheight = newRelH, anchor = NW)
        self.labelFrameSelectTitleText.configure(
            font = UI_support.FONT_MED_BOLD,
            # background = Color_support.BG_TITLE, foreground = Color_support.FG_TITLE,
            background = Color_support.SELECT_TITLE_BG, foreground = Color_support.SELECT_TITLE_FG,
            text = '''GROUP''',
            bd = 0, relief = GROOVE,
            anchor = S
        )
        # Title border
        self.separatorlabelFrameSelectTitleText = self.createLabelSeparator(
            self.labelFrameSelectTitleText, 1,
            True, Color_support.WHITE,
            coordinate = 0.99, specifiedAnchor = NW
        )

        newRelY = FS.getRelY(self.labelFrameSelectTitle) + FS.getRelH(
            self.labelFrameSelectTitle)  # + UI_support.TAB_TEST_FILTER_QUERY_REL_Y
        titleRelH = FS.getRelH(self.labelFrameSelectTitle)

        self.lfFeatureSelect = LabelFrame(parentFrame, bd = 0)
        self.lfFeatureSelect.place(
            relx = 0.05, rely = newRelY,
            relwidth = UI_support.TAB_TEST_SELECT_DATASET_REL_W, relheight = 1 - titleRelH
        )
        self.lfFeatureSelect.configure(
            background = Color_support.SELECT_BG
        )
        newRelH = FS.getRelH(self.lfFeatureSelect)
        self.lfConfirmedFeatures = LabelFrame(parentFrame, bd = 0)
        self.lfConfirmedFeatures.place(
            relx = UI_support.TAB_TEST_SELECT_DATASET_REL_W + 0.15,
            # (2 * FS.getRelX(self.labelFrameDatasetA)) + FS.getRelW(self.labelFrameDatasetA),
            rely = newRelY, relwidth = 0.4, relheight = newRelH
        )
        self.lfConfirmedFeatures.configure(
            background = Color_support.SELECT_BG
        )

        # DATASET SEPARATOR
        self.labelFrameDatasetCenterSeparator = ttk.Separator(parentFrame, orient = VERTICAL)
        self.labelFrameDatasetCenterSeparator.place(relx = 0.5, rely = newRelY + 0.05, relheight = 1 - titleRelH - 0.1)

        # QUERY PARENT (DATASET A)
        self.lfStatusFeatureSelect = LabelFrame(self.lfFeatureSelect, bd = 0)
        self.lfStatusFeatureSelect.place(
            relx = UI_support.TAB_TEST_SELECT_QUERY_REL_X, rely = UI_support.TAB_TEST_SELECT_QUERY_REL_Y,
            relwidth = UI_support.TAB_TEST_SELECT_QUERY_REL_W, relheight = UI_support.TAB_TEST_SELECT_QUERY_REL_H)
        self.lfStatusFeatureSelect.configure(
            background = Color_support.SELECT_ENTRY_BG, foreground = Color_support.SELECT_ENTRY_FG,
            relief = GROOVE  # , text = '''Dataset A'''
        )

        # QUERY STATUS CHILD - DATASET A
        # region
        self.lblStatusFeatureSelect = Label(self.lfStatusFeatureSelect)
        # self.labelQuerySetDataStatusA = Label(self.labelFrameQuerySetDataStatusA)
        # self.labelQuerySetDataStatusA = Label(self.labelFrameListBoxA)
        self.lblStatusFeatureSelect.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        # self.labelQuerySetDataStatusA.place(relx = 0, rely = newRelY, relwidth = 1, relheight = newRelH)
        self.lblStatusFeatureSelect.configure(
            background = Color_support.SELECT_LISTBOX_STATUS_BG, foreground = Color_support.SELECT_LISTBOX_STATUS_FG,
            bd = UI_support.SELECT_STATUS_LABEL_BORDER, relief = UI_support.SELECT_STATUS_LABEL_RELIEF,
            text = UI_support.LBL_SELECT_NO_DATA,
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )
        if UI_support.SELECT_STATUS_LABEL_TOP_SEPARATOR:
            self.labelFrameNoDataAHorizontalSeparator = ttk.Separator(self.lblStatusFeatureSelect,
                                                                      orient = HORIZONTAL)
            self.labelFrameNoDataAHorizontalSeparator.place(relx = 0, rely = 0, relwidth = 1, anchor = NW)
        # endregion

        # LISTBOX PARENT (DATASET A)
        # region
        newRelY = UI_support.TAB_TEST_LISTBOX_QUERY_REL_Y + FS.getRelY(self.lfStatusFeatureSelect) + FS.getRelH(
            self.lfStatusFeatureSelect)

        self.lfListFeatureSelect = LabelFrame(self.lfFeatureSelect, bd = 0)
        self.lfListFeatureSelect.place(
            relx = UI_support.TAB_TEST_LISTBOX_QUERY_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_LISTBOX_QUERY_REL_W, relheight = UI_support.TAB_TEST_LISTBOX_QUERY_REL_H)

        # QUERY STATUS PARENT - DATASET A
        # region
        # newRelY = FS.getRelY(self.listQuerySetDataA) + FS.getRelH(self.listQuerySetDataA)
        # newRelH = 1 - FS.getRelH(self.listQuerySetDataA)

        self.lfQueryFeatureSelect = LabelFrame(self.lfListFeatureSelect, bd = 0)
        # self.labelFrameQuerySetDataStatusA.place(relx = 0, rely = newRelY, relwidth = 1, relheight = newRelH)
        specifiedListBoxHeight = (0.78 - 0.03)
        newRelH = 1 - specifiedListBoxHeight  # TODO Make constant (0.78 - 0.03) is the listbox's supposed height
        self.lfQueryFeatureSelect.place(relx = 0, rely = 0, relwidth = 1, relheight = newRelH)

        # QUERY TOP STRIPE PARENT - DATASET A
        # region
        # newRelH = FS.getRelH(self.labelFrameQuerySetDataStatusA) * 7 / 11 # 5 / 8 # TODO Make constant reference
        newRelH = FS.getRelH(
            self.lfQueryFeatureSelect) * UI_support.SELECT_LABEL_STRIPES_REL_H_MULTIPLIER  # 5 / 8 # TODO Make constant reference
        self.lblStripesQueryFeatureSelect = Label(self.lfListFeatureSelect, bd = 0, relief = GROOVE)
        self.lblStripesQueryFeatureSelect.place(
            relx = 0,
            rely = 0,
            # rely = newRelY,
            relwidth = 1,
            relheight = newRelH,
            anchor = NW
        )
        newRelY = FS.getRelY(self.lblStripesQueryFeatureSelect) + FS.getRelH(self.lblStripesQueryFeatureSelect)
        self.lfQueryFeatureSelect.place(
            relx = FS.getRelX(self.lfQueryFeatureSelect),
            rely = newRelY,
            relwidth = FS.getRelW(self.lfQueryFeatureSelect),
            relheight = FS.getRelH(self.lfQueryFeatureSelect),
        )
        im = PIL.Image.open(
            Icon_support.TEXTURE_STRIPE_PINK)
        texture_pink_stripes = PIL.ImageTk.PhotoImage(im)
        self.lblStripesQueryFeatureSelect.configure(
            image = texture_pink_stripes,
            anchor = SW
        )
        self.lblStripesQueryFeatureSelect.image = texture_pink_stripes  # < ! > Required to make images appear
        # endregion

        # QUERY FRAME - DATASET A
        # region
        # lfBorderQueryFeatureList = LabelFrame(self.labelFrameQueryDataA, bd = 0)
        lfBorderQueryFeatureList = LabelFrame(self.lfQueryFeatureSelect, bd = 0)
        lfBorderQueryFeatureList.place(
            relx = 0, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_LBL_REL_W, relheight = 1
        )
        lfBorderQueryFeatureList.configure(
            background = Color_support.SELECT_BUTTONS_BG
        )

        lblQueryFeatureList = Label(lfBorderQueryFeatureList)

        lblQueryFeatureList.place(
            relx = 0.01, rely = 0.025,
            relwidth = 0.98, relheight = 0.95)
        lblQueryFeatureList.configure(
            background = Color_support.SELECT_LABEL_BG, foreground = Color_support.SELECT_LABEL_FG,
            text = UI_support.SELECT_LABEL_DATASETA_TEXT,
            font = UI_support.SELECT_LABEL_FONT,
            bd = 0, relief = FLAT,
        )

        newRelX = FS.getRelX(lfBorderQueryFeatureList) + FS.getRelW(
            lfBorderQueryFeatureList)  # + UI_support.TAB_3CHILD_LBL_REL_X

        # ENTRY - DATASET A
        # region
        # self.entryQuerySetDataA = Entry(self.labelFrameQueryDataA)
        self.entryQueryFeatureList = Entry(self.lfQueryFeatureSelect)
        self.entryQueryFeatureList.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_ENTRY_REL_W, relheight = 1)
        self.entryQueryFeatureList.configure(
            background = Color_support.SELECT_ENTRY_BG, foreground = Color_support.SELECT_ENTRY_FG,
            bd = 1,
            font = UI_support.ENTRY_FONT, insertwidth = UI_support.INSERT_WIDTH,
            selectbackground = Color_support.SELECT_ENTRY_SELECT_HIGHLIGHT_BG,
            insertbackground = Color_support.SELECT_ENTRY_SELECT_INSERT_BG,
            takefocus = UI_support.ENTRY_TAKE_FOCUS, justify = UI_support.SELECT_ENTRY_JUSTIFY
        )  # TODO Constant font definiton
        # endregion
        # QUERY BUTTON - DATASET A
        # region
        newRelX = FS.getRelX(self.entryQueryFeatureList) + FS.getRelW(
            self.entryQueryFeatureList)  # + UI_support.TAB_3CHILD_LBL_REL_X

        # self.buttonQuerySetDataA = Button(self.labelFrameQueryDataA)
        self.btnQueryFeatureList = Button(self.lfQueryFeatureSelect)
        self.btnQueryFeatureList.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_BTN_REL_W, relheight = 1)

        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW).resize(Icon_support.SELECT_ICO_SIZE_BUTTONS,
                                                                     PIL.Image.ANTIALIAS)
        btn_query_set_icon = PIL.ImageTk.PhotoImage(im)
        self.btnQueryFeatureList.configure(
            image = btn_query_set_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.btnQueryFeatureList.image = btn_query_set_icon  # < ! > Required to make images appear

        self.btnQueryFeatureList.configure(
            background = Color_support.SELECT_BUTTONS_BG, foreground = Color_support.SELECT_BUTTONS_FG,
            activebackground = Color_support.SELECT_BG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE,
            # text = '''Find Feature'''
        )
        # endregion

        # endregion

        # endregion

        # LISTBOX - DATASET A
        # region
        # self.scrollbarQuerySetDataA = Scrollbar(self.labelFrameListBox, orient = VERTICAL)
        # self.listQuerySetDataA = Listbox(self.labelFrameListBoxA, yscrollcommand = self.scrollbarQuerySetDataA.set)

        self.lbListFeatureSelect = Listbox(self.lfListFeatureSelect)
        self.lbListFeatureSelect.configure(
            background = Color_support.SELECT_LISTBOX_BG, foreground = Color_support.SELECT_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = Color_support.SELECT_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = Color_support.SELECT_LISTBOX_SELECTED_ITEM_FG,
            font = UI_support.SELECT_LABEL_FONT,
            bd = UI_support.SELECT_LISTBOX_BORDER, relief = UI_support.SELECT_LISTBOX_RELIEF,
            highlightthickness = 0
        )
        newRelY = FS.getRelY(self.lfQueryFeatureSelect) + FS.getRelH(self.lfQueryFeatureSelect)
        newRelH = 1 - (FS.getRelH(self.lfQueryFeatureSelect) + FS.getRelH(self.lblStripesQueryFeatureSelect))
        self.lbListFeatureSelect.place(relx = 0, rely = newRelY, relwidth = 1, relheight = newRelH)

        # self.listQuerySetDataA.place(
        #     relx = 0.01, rely = 0.025,
        #     relwidth = 0.98, relheight = 0.95)
        # # self.listQuerySetDataA.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.78 - 0.03)
        # endregion

        newRelY = UI_support.TAB_TEST_COMMANDS_QUERY_REL_Y + FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(
            self.lfListFeatureSelect)

        # COMMANDS PARENT (DATASET A)
        # region

        lfCommandsFeatureSelect = LabelFrame(self.lfFeatureSelect, bd = 0)
        lfCommandsFeatureSelect.place(
            relx = UI_support.TAB_TEST_COMMANDS_QUERY_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_COMMANDS_QUERY_REL_W,
            relheight = UI_support.TAB_TEST_COMMANDS_QUERY_REL_H * 0.85)  # TODO Reduced size

        lfCommandsFeatureSelect.configure(
            background = Color_support.WHITE
        )

        # RESET BUTTON (DATASET A)
        # region
        self.btnResetFeatureSelect = Button(lfCommandsFeatureSelect)
        self.btnResetFeatureSelect.place(
            relx = 0, rely = 0,
            relwidth = 0.25, relheight = 1)
        self.btnResetFeatureSelect.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        # text = '''Reset''')

        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_reset_icon = PIL.ImageTk.PhotoImage(im)
        self.btnResetFeatureSelect.configure(
            image = btn_query_reset_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.btnResetFeatureSelect.image = btn_query_reset_icon  # < ! > Required to make images appear
        # endregion

        # QUERY COUNT (DATASET A)
        # region
        newRelX = FS.getRelX(self.btnResetFeatureSelect) + FS.getRelW(self.btnResetFeatureSelect)

        lfCountFeatureSelect = LabelFrame(lfCommandsFeatureSelect, bd = 1)
        lfCountFeatureSelect.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.50 - 0.005, relheight = 1
        )
        lfCountFeatureSelect.configure(
            background = Color_support.SELECT_BG
        )

        # Define count variables
        self.featureSelectCount = 0
        self.confirmedFeaturesCount = 0

        self.labelQueryDataACount = Label(lfCountFeatureSelect)
        self.labelQueryDataACount.place(relx = 0, rely = 0, relwidth = 1,
                                        relheight = UI_support.TAB_TEST_SELECT_COUNT_REL_H)
        self.labelQueryDataACount.configure(
            font = UI_support.FONT_LARGE_BOLD,
            background = Color_support.SELECT_BG,
            text = self.getDatasetCountA()
        )
        self.labelQueryDataACountText = Label(lfCountFeatureSelect)
        self.labelQueryDataACountText.place(
            relx = 0, rely = FS.getRelH(self.labelQueryDataACount),
            relwidth = 1, relheight = UI_support.TAB_TEST_SELECT_COUNT_TEXT_REL_H)
        self.labelQueryDataACountText.configure(
            font = UI_support.FONT_DEFAULT_BOLD,
            background = Color_support.FG_COLOR, foreground = Color_support.SELECT_BG,
            text = '''SAMPLES'''
        )
        # endregion

        # COMMAND BORDERS - DATASET A
        # region
        newRelY = FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(self.lfListFeatureSelect)

        self.separatorlabelFrameCommandsARight = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsARight.place(
            relx = FS.getRelX(self.lfStatusFeatureSelect),
            rely = newRelY,
            relheight = 1 - newRelY - 0.025,  # TODO To adjust border height, just adjust this
            width = 1)
        self.separatorlabelFrameCommandsARight.configure(background = Color_support.DISABLED_D_BLUE)

        self.separatorlabelFrameCommandsALeft = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsALeft.place(
            relx = 1 - FS.getRelX(self.lfStatusFeatureSelect),
            rely = FS.getRelY(self.separatorlabelFrameCommandsARight),
            relheight = FS.getRelH(self.separatorlabelFrameCommandsARight),
            width = 1
        )
        self.separatorlabelFrameCommandsALeft.configure(background = Color_support.DISABLED_D_BLUE)

        self.separatorlabelFrameCommandsABottom = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsABottom.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsARight),
            # rely = 0.997,
            rely = FS.getRelY(self.separatorlabelFrameCommandsALeft) +
                   FS.getRelH(self.separatorlabelFrameCommandsALeft) - 0.003,
            relwidth = FS.getRelX(self.separatorlabelFrameCommandsALeft) - FS.getRelX(
                self.separatorlabelFrameCommandsARight),
            height = 1)
        self.separatorlabelFrameCommandsABottom.configure(background = Color_support.DISABLED_D_BLUE)

        newRelY = FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(self.lfListFeatureSelect)

        self.separatorlabelFrameCommandsATop = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsATop.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsARight),
            rely = newRelY,
            relwidth = FS.getRelW(self.separatorlabelFrameCommandsABottom),
            height = 1)
        self.separatorlabelFrameCommandsATop.configure(background = Color_support.DISABLED_D_BLUE)

        # endregion

        # endregion

        #  QUERY PARENT (DATASET B)
        # region
        self.labelFrameQueryDataB = LabelFrame(self.lfConfirmedFeatures, bd = 0)
        self.labelFrameQueryDataB.place(
            relx = FS.getRelX(self.lfStatusFeatureSelect),
            rely = FS.getRelY(self.lfStatusFeatureSelect),
            relwidth = FS.getRelW(self.lfStatusFeatureSelect),
            relheight = FS.getRelH(self.lfStatusFeatureSelect))
        self.labelFrameQueryDataB.configure(
            background = Color_support.SELECT_ENTRY_BG, foreground = Color_support.SELECT_ENTRY_FG,
            relief = GROOVE  # , text = '''Dataset B'''
        )
        # endregion
        # LISTBOX PARENT (DATASET B)
        # region
        self.labelFrameListBoxB = LabelFrame(self.lfConfirmedFeatures, bd = 0)
        self.labelFrameListBoxB.place(
            relx = FS.getRelX(self.lfListFeatureSelect),
            rely = FS.getRelY(self.lfListFeatureSelect),
            relwidth = FS.getRelW(self.lfListFeatureSelect),
            relheight = FS.getRelH(self.lfListFeatureSelect)
        )

        # STATUS CHILDREN - DATASET B
        # region

        # QUERY TOP STRIPE PARENT - DATASET B
        # region
        self.labelQuerySetDataStripesB = Label(self.labelFrameListBoxB, bd = 0, relief = GROOVE)
        self.labelQuerySetDataStripesB.place(
            relx = FS.getRelX(self.lblStripesQueryFeatureSelect),
            rely = FS.getRelY(self.lblStripesQueryFeatureSelect),
            relwidth = FS.getRelW(self.lblStripesQueryFeatureSelect),
            relheight = FS.getRelH(self.lblStripesQueryFeatureSelect)
        )
        im = PIL.Image.open(
            Icon_support.TEXTURE_STRIPE_PINK)
        texture_pink_stripes = PIL.ImageTk.PhotoImage(im)
        self.labelQuerySetDataStripesB.configure(
            image = texture_pink_stripes,
            anchor = SW
        )
        self.labelQuerySetDataStripesB.image = texture_pink_stripes  # < ! > Required to make images appear
        # endregion

        self.labelQuerySetDataStatusB = Label(self.labelFrameQueryDataB)
        # self.labelQuerySetDataStatusB = Label(self.labelFrameListBoxB)
        self.labelQuerySetDataStatusB.place(
            relx = FS.getRelX(self.lblStatusFeatureSelect),
            rely = FS.getRelY(self.lblStatusFeatureSelect),
            relwidth = FS.getRelW(self.lblStatusFeatureSelect),
            relheight = FS.getRelH(self.lblStatusFeatureSelect)
        )
        # self.labelQuerySetDataStatusB.place(relx = 0, rely = newRelY, relwidth = 1, relheight = newRelH)
        self.labelQuerySetDataStatusB.configure(
            background = Color_support.SELECT_LISTBOX_STATUS_BG, foreground = Color_support.SELECT_LISTBOX_STATUS_FG,
            bd = UI_support.SELECT_STATUS_LABEL_BORDER, relief = UI_support.SELECT_STATUS_LABEL_RELIEF,
            text = UI_support.LBL_SELECT_NO_DATA,
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )
        # endregion

        # endregion

        self.listQuerySetDataB = Listbox(self.labelFrameListBoxB)
        self.listQuerySetDataB.configure(
            background = Color_support.SELECT_LISTBOX_BG, foreground = Color_support.SELECT_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = Color_support.SELECT_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = Color_support.SELECT_LISTBOX_SELECTED_ITEM_FG,
            font = UI_support.SELECT_LABEL_FONT,
            bd = UI_support.SELECT_LISTBOX_BORDER, relief = UI_support.SELECT_LISTBOX_RELIEF,
            highlightthickness = 0
        )

        self.listQuerySetDataB.place(
            relx = FS.getRelX(self.lbListFeatureSelect),
            rely = FS.getRelY(self.lbListFeatureSelect),
            relwidth = FS.getRelW(self.lbListFeatureSelect),
            relheight = FS.getRelH(self.lbListFeatureSelect)
        )

        # STATUS - DATASET B
        # region
        self.labelFrameQuerySetDataStatusB = LabelFrame(self.labelFrameListBoxB, bd = 0)
        self.labelFrameQuerySetDataStatusB.place(
            relx = FS.getRelX(self.lfQueryFeatureSelect),
            rely = FS.getRelY(self.lfQueryFeatureSelect),
            relwidth = FS.getRelW(self.lfQueryFeatureSelect),
            relheight = FS.getRelH(self.lfQueryFeatureSelect)
        )
        # endregion

        # QUERY CHILDREN - DATASET B
        # region
        self.labelFrameBorderQuerySetDataB = LabelFrame(self.labelFrameQuerySetDataStatusB, bd = 0)
        self.labelFrameBorderQuerySetDataB.place(
            relx = FS.getRelX(lfBorderQueryFeatureList),
            rely = FS.getRelY(lfBorderQueryFeatureList),
            relwidth = FS.getRelW(lfBorderQueryFeatureList),
            relheight = FS.getRelH(lfBorderQueryFeatureList))
        self.labelFrameBorderQuerySetDataB.configure(
            background = Color_support.SELECT_BUTTONS_BG
        )

        self.labelQuerySetDataB = Label(self.labelFrameBorderQuerySetDataB)

        self.labelQuerySetDataB.place(
            relx = FS.getRelX(lblQueryFeatureList),
            rely = FS.getRelY(lblQueryFeatureList),
            relwidth = FS.getRelW(lblQueryFeatureList),
            relheight = FS.getRelH(lblQueryFeatureList))
        self.labelQuerySetDataB.configure(
            background = Color_support.SELECT_LABEL_BG, foreground = Color_support.SELECT_LABEL_FG,
            text = UI_support.SELECT_LABEL_DATASETB_TEXT,
            font = UI_support.SELECT_LABEL_FONT,
            bd = 0, relief = FLAT,
        )

        # ENTER CODE DATASET B

        self.entryQuerySetDataB = Entry(self.labelFrameQuerySetDataStatusB)
        self.entryQuerySetDataB.place(
            relx = FS.getRelX(self.entryQueryFeatureList),
            rely = FS.getRelY(self.entryQueryFeatureList),
            relwidth = FS.getRelW(self.entryQueryFeatureList),
            relheight = FS.getRelH(self.entryQueryFeatureList))
        self.entryQuerySetDataB.configure(
            background = Color_support.SELECT_ENTRY_BG, foreground = Color_support.SELECT_ENTRY_FG,
            bd = 1,
            font = UI_support.ENTRY_FONT, insertwidth = UI_support.INSERT_WIDTH,
            selectbackground = Color_support.SELECT_ENTRY_SELECT_HIGHLIGHT_BG,
            insertbackground = Color_support.SELECT_ENTRY_SELECT_INSERT_BG,
            takefocus = UI_support.ENTRY_TAKE_FOCUS, justify = UI_support.SELECT_ENTRY_JUSTIFY
        )  # TODO Constant font definiton

        # DATASET B
        self.buttonQuerySetDataB = Button(self.labelFrameQuerySetDataStatusB)
        self.buttonQuerySetDataB.place(
            relx = FS.getRelX(self.btnQueryFeatureList),
            rely = FS.getRelY(self.btnQueryFeatureList),
            relwidth = FS.getRelW(self.btnQueryFeatureList),
            relheight = FS.getRelH(self.btnQueryFeatureList))

        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW).resize(Icon_support.SELECT_ICO_SIZE_BUTTONS,
                                                                     PIL.Image.ANTIALIAS)
        btn_query_set_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQuerySetDataB.configure(
            image = btn_query_set_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQuerySetDataB.image = btn_query_set_icon  # < ! > Required to make images appear

        self.buttonQuerySetDataB.configure(
            background = Color_support.SELECT_BUTTONS_BG, foreground = Color_support.SELECT_BUTTONS_FG,
            activebackground = Color_support.SELECT_BTN_BG_ACTIVE,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE,
            # text = '''Find Feature'''
        )
        # endregion

        # COMMANDS PARENT (DATASET B)
        # region
        self.labelFrameCommandsB = LabelFrame(self.lfConfirmedFeatures, bd = 0)
        self.labelFrameCommandsB.place(
            relx = FS.getRelX(lfCommandsFeatureSelect),
            rely = FS.getRelY(lfCommandsFeatureSelect),
            relwidth = FS.getRelW(lfCommandsFeatureSelect),
            relheight = FS.getRelH(lfCommandsFeatureSelect)
        )
        # self.labelFrameCommandsB.place(
        #     relx = UI_support.TAB_TEST_COMMANDS_QUERY_REL_X, rely = newRelY,
        #     relwidth = UI_support.TAB_TEST_COMMANDS_QUERY_REL_W, relheight = UI_support.TAB_TEST_COMMANDS_QUERY_REL_H)

        self.labelFrameCommandsB.configure(
            background = Color_support.WHITE
        )
        # endregion

        # RESET BUTTON (DATASET B)
        # region
        self.buttonQueryResetFilterB = Button(self.labelFrameCommandsB)
        self.buttonQueryResetFilterB.place(
            relx = 0, rely = 0,
            relwidth = 0.25, relheight = 1)
        self.buttonQueryResetFilterB.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        # text = '''Reset''')

        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_reset_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryResetFilterB.configure(
            image = btn_query_reset_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryResetFilterB.image = btn_query_reset_icon  # < ! > Required to make images appear

        # endregion

        # COMMAND BORDERS - DATASET B
        # region
        # newRelY = FS.getRelY(self.labelFrameListBoxB) + FS.getRelH(self.labelFrameListBoxB)

        self.separatorlabelFrameCommandsBRight = Label(self.lfConfirmedFeatures)
        self.separatorlabelFrameCommandsBRight.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsARight),
            rely = FS.getRelY(self.separatorlabelFrameCommandsARight),
            relheight = FS.getRelH(self.separatorlabelFrameCommandsARight),
            width = 1
        )
        self.separatorlabelFrameCommandsBRight.configure(background = Color_support.DISABLED_D_BLUE)

        self.separatorlabelFrameCommandsBLeft = Label(self.lfConfirmedFeatures)
        self.separatorlabelFrameCommandsBLeft.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsALeft),
            rely = FS.getRelY(self.separatorlabelFrameCommandsALeft),
            relheight = FS.getRelH(self.separatorlabelFrameCommandsALeft),
            width = 1
        )
        self.separatorlabelFrameCommandsBLeft.configure(background = Color_support.DISABLED_D_BLUE)

        self.separatorlabelFrameCommandsBBottom = Label(self.lfConfirmedFeatures)
        self.separatorlabelFrameCommandsBBottom.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsABottom),
            rely = FS.getRelY(self.separatorlabelFrameCommandsABottom),
            relwidth = FS.getRelW(self.separatorlabelFrameCommandsABottom),
            height = 1)
        self.separatorlabelFrameCommandsBBottom.configure(background = Color_support.DISABLED_D_BLUE)

        newRelY = FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(self.lfListFeatureSelect)

        self.separatorlabelFrameCommandsBTop = Label(self.lfFeatureSelect)
        self.separatorlabelFrameCommandsBTop.place(
            relx = FS.getRelX(self.separatorlabelFrameCommandsATop),
            rely = FS.getRelY(self.separatorlabelFrameCommandsATop),
            relwidth = FS.getRelW(self.separatorlabelFrameCommandsATop),
            height = 1)
        self.separatorlabelFrameCommandsATop.configure(background = Color_support.DISABLED_PALER_YELLOW)

        # endregion

        # QUERY COUNT (DATASET B)
        # region
        lfCountFeatureSelectB = LabelFrame(self.labelFrameCommandsB, bd = 1)
        lfCountFeatureSelectB.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.50 - 0.005, relheight = 1
        )
        lfCountFeatureSelectB.configure(
            background = Color_support.SELECT_BG
        )

        self.labelQueryDataBCount = Label(lfCountFeatureSelectB)
        self.labelQueryDataBCount.place(relx = 0, rely = 0, relwidth = 1,
                                        relheight = UI_support.TAB_TEST_SELECT_COUNT_REL_H)
        self.labelQueryDataBCount.configure(
            font = UI_support.FONT_LARGE_BOLD,
            background = Color_support.SELECT_BG,
            text = self.getDatasetCountB()
        )
        self.labelQueryDataBCountText = Label(lfCountFeatureSelectB)
        self.labelQueryDataBCountText.place(
            relx = 0, rely = FS.getRelH(self.labelQueryDataBCount),
            relwidth = 1, relheight = UI_support.TAB_TEST_SELECT_COUNT_TEXT_REL_H)
        self.labelQueryDataBCountText.configure(
            font = UI_support.FONT_DEFAULT_BOLD,
            background = Color_support.FG_COLOR, foreground = Color_support.SELECT_BG,
            text = '''SAMPLES'''
        )

        # Create the left separator
        # lfCountFeatureSelectLeftSeparatorB = ttk.Separator(lfCountFeatureSelectB, orient = VERTICAL)
        # lfCountFeatureSelectLeftSeparatorB.place(relx = 0, rely = 0, relheight = 1)

        # lfCountFeatureSelectRightSeparatorB = ttk.Separator(lfCountFeatureSelectB, orient = VERTICAL)
        # lfCountFeatureSelectRightSeparatorB.place(relx = 0.99, rely = 0, relheight = 1)
        # endregion

        # FILTER BUTTON (DATASET A)
        # region
        newRelX = FS.getRelX(lfCountFeatureSelect) + FS.getRelW(lfCountFeatureSelect)
        newRelX = FS.getRelX(lfCountFeatureSelect) + FS.getRelW(lfCountFeatureSelect)

        self.buttonQueryAddFilterA = Button(lfCommandsFeatureSelect, compound = CENTER)
        self.buttonQueryAddFilterA.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.25 - 0.005, relheight = 1
        )

        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_filter_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryAddFilterA.configure(
            image = btn_query_filter_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryAddFilterA.image = btn_query_filter_icon  # < ! > Required to make images appear

        self.buttonQueryAddFilterA.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        # text = '''Filter''')
        self.buttonQueryAddFilterA.pack(side = RIGHT)
        self.btnResetFeatureSelect.pack(side = LEFT)

        # endregion
        # FILTER BUTTON (DATASET B)
        # region
        newRelX = FS.getRelX(lfCountFeatureSelectB) + FS.getRelW(lfCountFeatureSelectB)

        self.buttonQueryAddFilterB = Button(self.labelFrameCommandsB, compound = CENTER)
        self.buttonQueryAddFilterB.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.25 - 0.005, relheight = 1
        )

        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_filter_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryAddFilterB.configure(
            image = btn_query_filter_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryAddFilterB.image = btn_query_filter_icon  # < ! > Required to make images appear

        self.buttonQueryAddFilterB.configure(
            background = Color_support.SELECT_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        # text = '''Filter''')
        self.buttonQueryAddFilterB.pack(side = RIGHT)

        self.buttonQueryResetFilterB.pack(side = LEFT)
        # endregion

    ''' -> Elements under the FILTER ("FILTER") HEADER <- '''

    def configureFilterElements(self, parentFrame):
        titleFrame = self.createTitleBar(parentFrame, '2', 'PROCESS', Color_support.FILTER_TITLE_BG)
        titleFrame.place(relx = 0, rely = 0.08, relwidth = 1,
                         relheight = UI_support.TAB_TEST_FILTER_TITLE_REL_H)

        newRelY = FS.getRelY(titleFrame) + FS.getRelH(titleFrame) + UI_support.TAB_TEST_FILTER_QUERY_REL_Y

        # TOP LABEL FEATURE NAME
        # self.labelQueryDataFeatureName = Label(self.labelFrameFilterListData)
        self.labelQueryDataFeatureName = Label(parentFrame)
        # self.labelQueryDataFeatureName.place(
        #     relx = 0, rely = 0,
        #     relheight = UI_support.TAB_TEST_FILTER_QUERY_FEATURE_NAME_REL_H, relwidth = 1)

        self.labelQueryDataFeatureName.place(
            # relx = UI_support.TAB_TEST_FILTER_QUERY_REL_X, rely = 0,
            relx = UI_support.TAB_TEST_FILTER_QUERY_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_QUERY_REL_W, relheight = UI_support.TAB_TEST_FILTER_QUERY_REL_H
        )
        self.labelQueryDataFeatureName.configure(
            background = Color_support.FILTER_LISTBOX_FEATURE_STATUS_BG,
            foreground = Color_support.FILTER_LISTBOX_FEATURE_STATUS_FG,
            bd = UI_support.FILTER_STATUS_LABEL_BORDER, relief = UI_support.FILTER_STATUS_LABEL_RELIEF,
            text = UI_support.FILTER_STATUS_NO_FEATURE_TEXT,
            font = UI_support.FILTER_STATUS_LABEL_FONT,
        )

        newRelY = FS.getRelY(self.labelQueryDataFeatureName) + FS.getRelH(self.labelQueryDataFeatureName)

        # FILTER LIST PARENT
        self.labelFrameFilterListData = LabelFrame(parentFrame, bd = 0)

        self.labelFrameFilterListData.place(
            relx = UI_support.TAB_TEST_FILTER_LIST_DATA_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_LIST_DATA_REL_W,
            relheight = UI_support.TAB_TEST_FILTER_LIST_DATA_REL_H
        )
        self.labelFrameFilterListData.configure(
            background = Color_support.FILTER_BG
        )

        # FILTER QUERY PARENT
        # self.labelFrameFilterQueryData = LabelFrame(parentFrame, bd = 0)
        self.labelFrameFilterQueryData = LabelFrame(self.labelFrameFilterListData, bd = 0)
        self.labelFrameFilterQueryData.place(
            relx = 0, rely = 0,
            relheight = UI_support.TAB_TEST_FILTER_QUERY_FEATURE_NAME_REL_H, relwidth = 1
        )
        #     .place(
        #     relx = UI_support.TAB_TEST_FILTER_QUERY_REL_X, rely = 0,
        #     # relx = UI_support.TAB_TEST_FILTER_QUERY_REL_X, rely = newRelY,
        #     relwidth = UI_support.TAB_TEST_FILTER_QUERY_REL_W, relheight = UI_support.TAB_TEST_FILTER_QUERY_REL_H
        # )
        self.labelFrameFilterQueryData.configure(
            background = Color_support.FILTER_BG
        )

        # FILTER QUERY LABEL
        # region
        self.labelFrameBorderQueryFeature = LabelFrame(self.labelFrameFilterQueryData, bd = 0)
        self.labelFrameBorderQueryFeature.place(
            relx = 0, rely = 0,
            relwidth = UI_support.TAB_TEST_FILTER_QUERY_LBL_REL_W, relheight = 1)
        self.labelFrameBorderQueryFeature.configure(
            background = Color_support.FILTER_BUTTONS_BG
        )

        self.labelQueryFeature = Label(self.labelFrameBorderQueryFeature)
        self.labelQueryFeature.place(
            relx = 0.01, rely = 0.025,
            relwidth = 0.98, relheight = 0.95)
        self.labelQueryFeature.configure(
            background = Color_support.FILTER_LABEL_BG, foreground = Color_support.FILTER_LABEL_FG,
            text = UI_support.FILTER_LABEL_QUERY_FEATURE_TEXT,
            font = UI_support.FILTER_LABEL_FONT,
            bd = 0, relief = FLAT,
        )
        # endregion

        newRelX = FS.getRelX(self.labelFrameBorderQueryFeature) + FS.getRelW(self.labelFrameBorderQueryFeature)

        # FILTER QUERY ENTRY
        # region
        self.entryQueryFeature = Entry(self.labelFrameFilterQueryData)
        self.entryQueryFeature.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_FILTER_QUERY_ENTRY_REL_W - 0.001, relheight = 1)
        self.entryQueryFeature.configure(
            background = Color_support.FILTER_ENTRY_BG, foreground = Color_support.FILTER_ENTRY_FG,
            bd = 1,
            font = UI_support.ENTRY_FONT, insertwidth = UI_support.INSERT_WIDTH,
            selectbackground = Color_support.FILTER_ENTRY_SELECT_HIGHLIGHT_BG,
            insertbackground = Color_support.FILTER_ENTRY_SELECT_INSERT_BG,
            takefocus = UI_support.ENTRY_TAKE_FOCUS, justify = UI_support.FILTER_ENTRY_JUSTIFY
        )
        # endregion
        newRelX = FS.getRelX(self.entryQueryFeature) + FS.getRelW(self.entryQueryFeature)

        # FILTER QUERY BUTTON
        # region
        self.buttonQueryFeature = Button(self.labelFrameFilterQueryData)
        self.buttonQueryFeature.place(
            relx = newRelX, rely = 0,
            relwidth = 0.041, relheight = 1)
        # relwidth = UI_support.TAB_TEST_SELECT_BTN_REL_W, relheight = 1)

        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW).resize(Icon_support.FILTER_ICO_SIZE_BUTTONS,
                                                                     PIL.Image.ANTIALIAS)
        btn_query_feature_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryFeature.configure(
            image = btn_query_feature_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryFeature.image = btn_query_feature_icon  # < ! > Required to make images appear

        self.buttonQueryFeature.configure(
            background = Color_support.FILTER_BUTTONS_BG, foreground = Color_support.FILTER_BUTTONS_FG,
            activebackground = Color_support.SELECT_BTN_BG_ACTIVE,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = FLAT
        )
        # endregion

        # newRelY = FS.getRelY(self.labelFrameFilterQueryData) + FS.getRelH(self.labelFrameFilterQueryData)
        ### INSERT CODE HERE

        # newRelY = FS.getRelY(self.labelQueryDataFeatureName) + FS.getRelH(self.labelQueryDataFeatureName)
        # newRelH = 1 - (FS.getRelY(self.labelQueryDataFeatureName) + FS.getRelH(self.labelQueryDataFeatureName)) - 0.2
        newRelY = FS.getRelY(self.labelFrameFilterQueryData) + FS.getRelH(self.labelFrameFilterQueryData)
        newRelH = 1 - (
                    FS.getRelY(self.labelFrameFilterQueryData) + FS.getRelH(self.labelFrameFilterQueryData)) - 0.2

        # FILTER LIST DATA A PARENT
        self.labelFrameFilterListDataA = LabelFrame(self.labelFrameFilterListData, bd = 0)
        self.labelFrameFilterListDataA.place(
            relx = UI_support.TAB_TEST_FILTER_LISTBOX_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_LISTBOX_REL_W, relheight = newRelH
            # UI_support.TAB_TEST_FILTER_LISTBOX_REL_H
        )
        self.labelFrameFilterListDataA.configure(
            background = Color_support.FILTER_BG
        )

        # FILTER LIST BOX - DATASET A
        # newRelY = UI_support.FILTER_LABEL_STRIPES_REL_H + 0.03725 # TODO Make constant, + is the percent of stripes
        newRelY = UI_support.FILTER_LABEL_STRIPES_REL_H * UI_support.FILTER_LABEL_BOTTOM_STRIPES_REL_H_MULTIPLIER,
        self.listQueryDataA = Listbox(self.labelFrameFilterListDataA, bd = 0)
        self.listQueryDataA.place(
            relx = UI_support.TAB_TEST_FILTER_LISTBOX_LIST_REL_X,
            rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_LISTBOX_LIST_REL_W,
            relheight = UI_support.TAB_TEST_FILTER_LISTBOX_LIST_REL_H -
                        (
                                    UI_support.FILTER_LABEL_STRIPES_REL_H * UI_support.FILTER_LABEL_BOTTOM_STRIPES_REL_H_MULTIPLIER))

        self.listQueryDataA.configure(
            background = Color_support.FILTER_LISTBOX_BG, foreground = Color_support.FILTER_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = Color_support.FILTER_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = Color_support.FILTER_LISTBOX_SELECTED_ITEM_FG,
            font = UI_support.FILTER_LABEL_FONT,
            bd = UI_support.FILTER_LISTBOX_BORDER, relief = UI_support.FILTER_LISTBOX_RELIEF,
            highlightthickness = 0
        )

        newRelY = FS.getRelY(self.listQueryDataA) + FS.getRelH(self.listQueryDataA)
        newRelH = 1 - (FS.getRelY(self.listQueryDataA) + FS.getRelH(self.listQueryDataA))

        # BOTTOM STATUS LABEL - DATASET A
        self.labelQueryDataA = Label(self.labelFrameFilterListDataA)
        self.labelQueryDataA.place(
            relx = UI_support.TAB_TEST_FILTER_LISTBOX_STATUS_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_LISTBOX_STATUS_REL_W, relheight = newRelH)

        self.labelQueryDataA.configure(
            background = Color_support.FILTER_LISTBOX_STATUS_BG, foreground = Color_support.FILTER_LISTBOX_STATUS_FG,
            bd = UI_support.FILTER_STATUS_LABEL_BORDER, relief = UI_support.FILTER_STATUS_LABEL_RELIEF,
            text = UI_support.FILTER_STATUS_NO_DATA_TEXT,
            font = UI_support.FILTER_STATUS_LABEL_FONT,
        )

        newRelX = FS.getRelX(self.labelFrameFilterListDataA) + FS.getRelW(self.labelFrameFilterListDataA)
        newRelY = FS.getRelY(self.labelFrameFilterListDataA)
        # FILTER LIST DATA B PARENT
        self.labelFrameFilterListDataB = LabelFrame(self.labelFrameFilterListData, bd = 0)

        newRelH = FS.getRelH(self.labelFrameFilterListDataA)
        self.labelFrameFilterListDataB.place(
            relx = newRelX, rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_LISTBOX_REL_W, relheight = newRelH
            # UI_support.TAB_TEST_FILTER_LISTBOX_REL_H
        )
        self.labelFrameFilterListDataB.configure(
            background = Color_support.FILTER_BG
        )

        # FILTER LIST BOX - DATASET B

        self.listQueryDataB = Listbox(self.labelFrameFilterListDataB, bd = 0)
        self.listQueryDataB.place(
            relx = UI_support.TAB_TEST_FILTER_LISTBOX_LIST_REL_X, rely = FS.getRelY(self.listQueryDataA),
            relwidth = UI_support.TAB_TEST_FILTER_LISTBOX_LIST_REL_W,
            relheight = FS.getRelH(self.listQueryDataA))

        self.listQueryDataB.configure(
            background = Color_support.FILTER_LISTBOX_BG, foreground = Color_support.FILTER_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = Color_support.FILTER_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = Color_support.FILTER_LISTBOX_SELECTED_ITEM_FG,
            font = UI_support.FILTER_LABEL_FONT,
            bd = UI_support.FILTER_LISTBOX_BORDER, relief = UI_support.FILTER_LISTBOX_RELIEF,
            highlightthickness = 0
        )

        newRelY = FS.getRelY(self.listQueryDataB) + FS.getRelH(self.listQueryDataB)
        newRelH = 1 - (FS.getRelY(self.listQueryDataA) + FS.getRelH(self.listQueryDataA))
        # BOTTOM STATUS LABEL - DATASET B
        self.labelQueryDataB = Label(self.labelFrameFilterListDataB)
        self.labelQueryDataB.place(
            relx = UI_support.TAB_TEST_FILTER_LISTBOX_STATUS_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_LISTBOX_STATUS_REL_W,
            relheight = newRelH)

        self.labelQueryDataB.configure(
            background = Color_support.FILTER_LISTBOX_STATUS_BG, foreground = Color_support.FILTER_LISTBOX_STATUS_FG,
            bd = UI_support.FILTER_STATUS_LABEL_BORDER, relief = UI_support.FILTER_STATUS_LABEL_RELIEF,
            text = UI_support.FILTER_STATUS_NO_DATA_TEXT,
            font = UI_support.FILTER_STATUS_LABEL_FONT,
        )

        # QUERY BOTTOM STRIPES
        self.labelFilterStripes = Label(self.labelFrameFilterListData, bd = 1, relief = GROOVE)
        self.labelFilterStripes.place(
            relx = FS.getRelX(self.labelFrameFilterListDataA),
            rely = FS.getRelY(self.labelFrameFilterListDataA),
            relwidth = 1,
            # relheight = UI_support.FILTER_LABEL_STRIPES_REL_H # * UI_support.FILTER_LABEL_STRIPES_REL_H_MULTIPLIER,
            relheight = UI_support.FILTER_LABEL_STRIPES_REL_H * UI_support.FILTER_LABEL_BOTTOM_STRIPES_REL_H_MULTIPLIER,
            # relheight = FS.getRelH(self.labelFrameFilterQueryData) * UI_support.FILTER_LABEL_STRIPES_REL_H_MULTIPLIER,
            anchor = NW
        )
        im = PIL.Image.open(
            Icon_support.TEXTURE_STRIPE_ORANGE)  # .resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        texture_orange_stripes = PIL.ImageTk.PhotoImage(im)
        self.labelFilterStripes.configure(
            image = texture_orange_stripes,
            anchor = SW
        )  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.labelFilterStripes.image = texture_orange_stripes  # < ! > Required to make images appear

        # FILTER BORDERS
        self.separatorFilterListDataA = Label(self.labelFrameFilterListDataA)
        self.separatorFilterListDataA.place(relx = 0, rely = 0, relheight = 1, width = 1)
        self.separatorFilterListDataA.configure(background = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)

        self.separatorFilterListDataCenter = Label(self.labelFrameFilterListDataB)
        self.separatorFilterListDataCenter.place(relx = 0, rely = 0, relheight = 1, width = 1)
        self.separatorFilterListDataCenter.configure(background = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)

        self.separatorFilterListDataB = Label(self.labelFrameFilterListDataB)
        self.separatorFilterListDataB.place(relx = 0.997, rely = 0, relheight = 1, width = 1)
        self.separatorFilterListDataB.configure(background = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)

        # FILTER LOCK OVERLAY
        # FILTER LOCK QUERY ENTRY COVER
        # FILTER LOCK MOCK PARENT COVER
        self.labelOverlayFilterListData = LabelFrame(parentFrame, bd = 0)

        self.labelOverlayFilterListData.place(
            relx = FS.getRelX(self.labelFrameFilterListData),
            rely = FS.getRelY(self.labelFrameFilterListData),
            # relwidth = 0, relheight = 0)
            relwidth = FS.getRelW(self.labelFrameFilterListData),
            relheight = FS.getRelH(self.labelFrameFilterListData))

        self.labelOverlayFilterListData.configure(
            background = self.labelFrameFilterListData['background'],
            bd = self.labelFrameFilterListData['bd'],
            relief = self.labelFrameFilterListData['relief']
        )

        # MOCK QUERY PARENT FRAME
        self.labelOverlayFilterQueryData = Label(self.labelOverlayFilterListData)
        self.labelOverlayFilterQueryData.place(
            relx = FS.getRelX(self.labelFrameFilterQueryData),
            rely = FS.getRelY(self.labelFrameFilterQueryData),
            relwidth = FS.getRelW(self.labelFrameFilterQueryData),
            relheight = FS.getRelH(self.labelFrameFilterQueryData) * UI_support.FILTER_LABEL_STRIPES_REL_H_MULTIPLIER
        )
        self.labelOverlayFilterQueryData.configure(
            background = self.labelFrameFilterQueryData['background'],
            foreground = Color_support.FILTER_LABEL_OVERLAY_BG,
            text = '''Please confirm the dataset groupings before filtering''',
            font = UI_support.FILTER_LABEL_FONT,
            bd = 0, relief = GROOVE,
            # bd = self.labelFrameFilterQueryData['bd'], relief = self.labelFrameFilterQueryData['relief'],
        )

        # MOCK STRIPED COVER
        self.labelOverlayFilterStripes = Label(self.labelOverlayFilterQueryData)
        self.labelOverlayFilterStripes.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 1,
            anchor = NW
        )
        im = PIL.Image.open(
            Icon_support.TEXTURE_STRIPE_ORANGE)  # .resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        texture_orange_stripes = PIL.ImageTk.PhotoImage(im)
        self.labelOverlayFilterStripes.configure(
            image = texture_orange_stripes,
            anchor = SW,
            bd = 0
        )
        self.labelOverlayFilterStripes.image = texture_orange_stripes  # < ! > Required to make images appear


        # FILTER LOCK LISTBOX COVER

        # LEFT COVER
        # self.labelOverlayFilterListDataA = Label(self.labelFrameFilterListDataA)
        self.labelOverlayFilterListDataA = Label(self.labelOverlayFilterListData)
        newRelY = FS.getRelY(self.labelOverlayFilterQueryData) + FS.getRelH(self.labelOverlayFilterQueryData)
        self.labelOverlayFilterListDataA.place(
            relx = FS.getRelX(self.labelFrameFilterListDataA),
            # rely = FS.getRelY(self.labelFrameFilterListDataA) - UI_support.FILTER_LABEL_STRIPES_REL_H_REDUCTION,
            rely = newRelY,
            relwidth = FS.getRelW(self.labelFrameFilterListDataA),
            # relheight = FS.getRelH(self.labelFrameFilterListDataA) + UI_support.FILTER_LABEL_STRIPES_REL_H_REDUCTION)
            # relheight = FS.getRelH(self.labelFrameFilterListDataA) + FS.getRelH(self.labelOverlayFilterQueryData))
            relheight = FS.getRelH(self.labelFrameFilterListDataA) +
                        FS.getRelH(self.labelOverlayFilterQueryData) +
                        FS.getRelH(self.labelFilterStripes) - 0.018)

        self.labelOverlayFilterListDataA.configure(
            background = Color_support.FILTER_LISTBOX_OVERLAY_BG,
            foreground = Color_support.FILTER_LABEL_OVERLAY_FG,
            font = UI_support.FILTER_LABEL_FONT,
            # bd = 0, relief = RIDGE,
            bd = self.labelFrameFilterListDataA['bd'], relief = self.labelFrameFilterListDataA['relief'],
            # bd = self.labelFrameFilterListDataA['bd'], relief = self.labelFrameFilterListDataA['relief'],
        )
        # FILTER LOCK BOTTOM MOCK NO DATA LABEL
        self.labelOverlayQueryDataA = Label(self.labelOverlayFilterListDataA)
        newRelYReduction = 0.01
        self.labelOverlayQueryDataA.place(
            relx = FS.getRelX(self.labelQueryDataA),
            rely = FS.getRelY(self.labelQueryDataA) + (UI_support.FILTER_LABEL_STRIPES_REL_H_REDUCTION / 2),
            # TODO Make constant
            relwidth = FS.getRelW(self.labelQueryDataA),
            relheight = FS.getRelH(self.labelQueryDataA) - newRelYReduction)

        self.labelOverlayQueryDataA.configure(
            background = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG,
            foreground = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_FG,
            bd = self.labelQueryDataA['bd'], relief = UI_support.FILTER_STATUS_LABEL_RELIEF,
            text = UI_support.FILTER_STATUS_NO_DATA_TEXT,
            font = UI_support.FILTER_STATUS_LABEL_FONT,
        )

        self.separatorOverlayFilterListDataA = Label(self.labelOverlayFilterListDataA)
        self.separatorOverlayFilterListDataA.place(relx = 0, rely = 0, relheight = 1, width = 1)
        self.separatorOverlayFilterListDataA.configure(
            background = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)


        # RIGHT COVER
        self.labelOverlayFilterListDataB = Label(self.labelOverlayFilterListData)
        self.labelOverlayFilterListDataB.place(
            relx = FS.getRelX(self.labelFrameFilterListDataB), rely = FS.getRelY(self.labelOverlayFilterListDataA),
            relwidth = FS.getRelW(self.labelFrameFilterListDataB),
            relheight = FS.getRelH(self.labelOverlayFilterListDataA))
        self.labelOverlayFilterListDataB.configure(
            background = Color_support.FILTER_LISTBOX_OVERLAY_BG,
            foreground = Color_support.FILTER_LABEL_OVERLAY_FG,
            font = UI_support.FILTER_LABEL_FONT,
            bd = self.labelOverlayFilterListDataA['border'], relief = self.labelOverlayFilterListDataA['relief'],
            # bd = 1, relief = RIDGE,
            # bd = self.labelFrameFilterListDataB['bd'], relief = self.labelFrameFilterListDataB['relief'],
        )
        # FILTER LOCK BOTTOM MOCK NO DATA LABEL
        self.labelOverlayQueryDataB = Label(self.labelOverlayFilterListDataB)
        self.labelOverlayQueryDataB.place(
            relx = FS.getRelX(self.labelOverlayQueryDataA),
            rely = FS.getRelY(self.labelOverlayQueryDataA),
            relwidth = FS.getRelW(self.labelOverlayQueryDataA),
            relheight = FS.getRelH(self.labelOverlayQueryDataA))

        self.labelOverlayQueryDataB.configure(
            background = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG,
            foreground = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_FG,
            bd = self.labelQueryDataA['bd'], relief = UI_support.FILTER_STATUS_LABEL_RELIEF,
            text = UI_support.FILTER_STATUS_NO_DATA_TEXT,
            font = UI_support.FILTER_STATUS_LABEL_FONT,
        )
        # self.separatorOverlayFilterListDataB1 = ttk.Separator(self.labelOverlayFilterListDataB, orient = VERTICAL)
        # self.separatorOverlayFilterListDataB1.place(relx = 0, rely = 0, relheight = 1)
        self.separatorOverlayFilterListDataCenter = Label(self.labelOverlayFilterListDataB)
        self.separatorOverlayFilterListDataCenter.place(relx = 0, rely = 0, relheight = 1, width = 1)
        self.separatorOverlayFilterListDataCenter.configure(
            background = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)

        self.separatorOverlayFilterListDataB = Label(self.labelOverlayFilterListDataB)
        self.separatorOverlayFilterListDataB.place(relx = 0.997, rely = 0, relheight = 1, width = 1)
        self.separatorOverlayFilterListDataB.configure(
            background = Color_support.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)


    ''' -> Elements under the PROCESS ("TEST") HEADER <- '''

    def configureProcessElements(self, parentFrame):

        titleFrame = self.createTitleBar(parentFrame, '3', 'RESULTS', Color_support.PROCESS_TITLE_BG)
        titleFrame.place(relx = 0, rely = 0,
                         relwidth = 1, relheight = UI_support.TAB_TEST_PROCESS_TITLE_REL_H)


        newRelY = FS.getRelH(titleFrame) + UI_support.TAB_TEST_PROCESS_COMMANDS_REL_Y

        # PROCESS COMMANDS PARENT
        self.labelFrameProcessCommands = LabelFrame(parentFrame, bd = 0)
        self.labelFrameProcessCommands.place(
            relx = UI_support.TAB_TEST_PROCESS_COMMANDS_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_PROCESS_COMMANDS_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_COMMANDS_REL_H
        )
        self.labelFrameProcessCommands.configure(
            background = Color_support.PROCESS_BG
        )

        # PROCESS STATISTICAL TEST OPTIONS
        self.labelFrameProcessStatTests = LabelFrame(self.labelFrameProcessCommands, bd = 0)
        self.labelFrameProcessStatTests.place(
            relx = 0, rely = 0,
            relwidth = UI_support.TEST_PROCESS_Z_TEST_PARENT, relheight = 1
        )

        self.labelFrameProcessStatTests.configure(
            background = Color_support.PROCESS_BG
        )

        # TITLE
        self.labelFrameProcessStatTestsTitle = Label(self.labelFrameProcessStatTests)
        self.labelFrameProcessStatTestsTitle.place(
            relx = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_X,
            rely = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y,
            relwidth = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H)
        self.labelFrameProcessStatTestsTitle.configure(
            font = UI_support.FONT_MED_BOLD,
            background = Color_support.PROCESS_Z_TEST_TITLE_BG, foreground = Color_support.PROCESS_Z_TEST_TITLE_FG,
            text = '''TYPE''',
            anchor = CENTER,
            bd = 0, relief = GROOVE
        )

        newRelY = FS.getRelY(self.labelFrameProcessStatTestsTitle) + FS.getRelH(
            self.labelFrameProcessStatTestsTitle)
        self.labelFrameProcessStatTestsButtonElements = LabelFrame(self.labelFrameProcessStatTests, bd = 0)
        self.labelFrameProcessStatTestsButtonElements.place(
            relx = FS.getRelX(self.labelFrameProcessStatTestsTitle),
            rely = newRelY,
            relwidth = FS.getRelW(self.labelFrameProcessStatTestsTitle),
            relheight = 1 - FS.getRelH(self.labelFrameProcessStatTestsTitle)  # 0.35
        )
        self.labelFrameProcessStatTestsButtonElements.configure(
            background = Color_support.PROCESS_BG
        )

        # CHOOSE Z-TEST BUTTON
        self.buttonChooseZTest = Button(self.labelFrameProcessStatTestsButtonElements, compound = CENTER)

        # im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        # btn_query_z_test_icon = PIL.ImageTk.PhotoImage(im)
        # self.buttonChooseZTest.configure(
        #     image = btn_query_z_test_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        # self.buttonChooseZTest.image = btn_query_z_test_icon  # < ! > Required to make images appear
        self.buttonChooseZTest.place(
            relx = 0, rely = 0.1,
            relwidth = 1, relheight = 0.28
        )
        self.buttonChooseZTest.configure(
            background = Color_support.D_BLUE, foreground = Color_support.WHITE,
            activebackground = Color_support.PROCESS_Z_TEST_TITLE_BG,
            bd = 1, relief = GROOVE, overrelief = SUNKEN,
            font = UI_support.FONT_DEFAULT_BOLD,
            text = '''Z - TEST''')

        # self.buttonChooseZTest.pack(fill = X, expand = True)
        self.buttonChooseZTest.update()

        # CHOOSE CHI-SQUARE BUTTON
        self.buttonChooseChiSquare = Button(self.labelFrameProcessStatTestsButtonElements, compound = CENTER)

        # im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        # btn_query_chi_square_icon = PIL.ImageTk.PhotoImage(im)
        # self.buttonChooseChiSquare.configure(
        #     image = btn_query_z_test_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        # self.buttonChooseChiSquare.image = btn_query_z_test_icon  # < ! > Required to make images appear

        newRelY = 0.05 + FS.getRelY(self.buttonChooseZTest) + FS.getRelH(self.buttonChooseZTest)
        self.buttonChooseChiSquare.place(
            relx = 0, rely = newRelY,
            relwidth = FS.getRelW(self.buttonChooseZTest), relheight = FS.getRelH(self.buttonChooseZTest)
        )
        self.buttonChooseChiSquare.configure(
            background = Color_support.WHITE, foreground = Color_support.D_BLUE,
            activebackground = Color_support.PROCESS_Z_TEST_TITLE_BG,
            bd = 1, relief = GROOVE, overrelief = SUNKEN,
            font = UI_support.FONT_DEFAULT_BOLD,
            text = '''CHI - SQUARE''')

        # self.buttonChooseChiSquare.pack(fill = X, expand = True)
        # self.buttonChooseChiSquare.update()


        # TEST OPTIONS PARENT
        # PROCESS Z-TEST PARENT
        newRelX = FS.getRelX(self.labelFrameProcessStatTests) + FS.getRelW(self.labelFrameProcessStatTests)
        self.labelFrameProcessTestOptions = LabelFrame(self.labelFrameProcessCommands, bd = 0)
        self.labelFrameProcessTestOptions.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TEST_PROCESS_Z_TEST_PARENT, relheight = 1
        )
        self.labelFrameProcessTestOptions.configure(
            background = Color_support.PROCESS_BG
        )

        self.labelFrameProcessTestOptionsTitle = Label(self.labelFrameProcessTestOptions)
        self.labelFrameProcessTestOptionsTitle.place(
            relx = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_X,
            rely = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y,
            relwidth = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H)
        self.labelFrameProcessTestOptionsTitle.configure(
            font = UI_support.FONT_MED_BOLD,
            background = Color_support.PROCESS_Z_TEST_TITLE_BG, foreground = Color_support.PROCESS_Z_TEST_TITLE_FG,
            # text = '''OPTIONS''',
            anchor = CENTER,
            bd = 1, relief = GROOVE
        )



        # PROCESS Z-TEST PARENT
        # newRelX = FS.getRelX(self.labelFrameProcessStatTests) + FS.getRelW(self.labelFrameProcessStatTests)
        self.labelFrameProcessZTest = LabelFrame(self.labelFrameProcessTestOptions, bd = 0,
                                                 name = 'labelFrameProcessZTest')
        self.labelFrameProcessZTest.place(
            # relx = newRelX, rely = 0,
            relx = 0, rely = 0,
            relwidth = 1, relheight = 1
            # relwidth = UI_support.TEST_PROCESS_Z_TEST_PARENT, relheight = 1
        )
        self.labelFrameProcessZTest.configure(
            background = Color_support.PROCESS_BG
        )

        self.labelFrameProcessZTestTitle = Label(self.labelFrameProcessZTest)
        self.labelFrameProcessZTestTitle.place(
            relx = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_X,
            rely = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y,
            relwidth = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H)
        self.labelFrameProcessZTestTitle.configure(
            font = UI_support.FONT_MED_BOLD,
            background = Color_support.PROCESS_Z_TEST_TITLE_BG, foreground = Color_support.PROCESS_Z_TEST_TITLE_FG,
            text = '''Z - TEST''',
            # text = '''OPTIONS''',
            anchor = CENTER,
            bd = 0, relief = GROOVE
        )

        global arrQueryCriticalValue
        arrQueryCriticalValue = ["0.80", "0.90", "0.95", "0.98", "0.99"]

        global arrQueryCriticalValueMapping
        arrQueryCriticalValueMapping = {"0.80": 1.28, "0.90": 1.645, "0.95": 1.96, "0.98": 2.33, "0.99": 2.58}

        newRelY = FS.getRelY(self.labelFrameProcessZTestTitle) + FS.getRelH(
            self.labelFrameProcessZTestTitle) + UI_support.TAB_TEST_PROCESS_Z_TEST_SPINNER_ELEMENTS_REL_Y

        # SPINBOX ELEMENTS
        # self.labelFrameProcessZTestConfidence = LabelFrame(self.labelFrameProcessZTest, bd = 0)
        self.labelFrameProcessZTestConfidence = LabelFrame(self.labelFrameProcessTestOptions, bd = 0)
        self.labelFrameProcessZTestConfidence.place(
            relx = 0.11, rely = newRelY,
            relwidth = 0.525, relheight = UI_support.TAB_TEST_PROCESS_Z_TEST_SPINNER_ELEMENTS_REL_H
        )
        self.labelFrameProcessZTestConfidence.configure(
            background = Color_support.PROCESS_BG
        )

        newRelX = FS.getRelX(self.labelFrameProcessZTestConfidence) + FS.getRelW(
            self.labelFrameProcessZTestConfidence)
        newRelY = FS.getRelY(self.labelFrameProcessZTestConfidence)

        # BUTTON ELEMENTS
        self.labelFrameProcessZTestButtonElements = LabelFrame(self.labelFrameProcessZTest, bd = 0)
        self.labelFrameProcessZTestButtonElements.place(
            relx = newRelX + 0.05, rely = newRelY,
            relwidth = 1 - (newRelX + FS.getRelX(self.labelFrameProcessZTestConfidence)),
            # relwidth = 0.5 - 2 * FS.getRelX(self.labelFrameProcessZTestConfidence),
            relheight = 0.35
        )
        self.labelFrameProcessZTestButtonElements.configure(
            background = Color_support.PROCESS_BG
        )

        # CONFIDENCE SPINBOX LABEL
        self.labelQueryZConfidenceText = Label(self.labelFrameProcessZTestConfidence)
        self.labelQueryZConfidenceText.place(
            relx = 0, rely = 0,
            relwidth = 1, relheight = UI_support.TAB_TEST_PROCESS_CONFIDENCE_TEXT_REL_H)
        self.labelQueryZConfidenceText.configure(
            font = UI_support.FONT_DEFAULT_BOLD,
            background = Color_support.FG_COLOR, foreground = Color_support.SELECT_BG,
            text = '''CONFIDENCE'''
        )

        newRelY = FS.getRelY(self.labelQueryZConfidenceText) + FS.getRelH(self.labelQueryZConfidenceText)
        newRelH = 1 - FS.getRelH(self.labelQueryZConfidenceText)

        # CONFIDENCE SPINBOX
        self.spinBoxQueryZConfidence = Spinbox(self.labelFrameProcessZTestConfidence,
                                               values = arrQueryCriticalValue)

        self.spinBoxQueryZConfidence.place(
            relx = 0, rely = newRelY,
            relwidth = 1, relheight = newRelH
        )

        # Used to validate spinbox value
        stringVar = StringVar()
        stringVar.trace('w', lambda nm, idx, mode, var = stringVar: self.validateZConfidenceSpinbox(var,
                                                                                                    self.spinBoxQueryZConfidence))

        self.spinBoxQueryZConfidence.configure(
            textvariable = stringVar,
            font = UI_support.FONT_LARGE_BOLD,
            background = Color_support.WHITE, foreground = Color_support.FG_COLOR,
            exportselection = 0,
            buttonbackground = Color_support.WHITE,
            buttonuprelief = FLAT, buttondownrelief = GROOVE,
            justify = CENTER

        )
        self.refreshSpinBoxValue(self.spinBoxQueryZConfidence)


        # Z-TEST BUTTON
        self.buttonQueryZTest = Button(self.labelFrameProcessZTestButtonElements, compound = CENTER)

        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_z_test_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueryZTest.configure(
            image = btn_query_z_test_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueryZTest.image = btn_query_z_test_icon  # < ! > Required to make images appear

        self.buttonQueryZTest.configure(
            background = Color_support.PROCESS_BG, foreground = Color_support.PROCESS_BUTTONS_FG,
            activebackground = Color_support.PROCESS_TITLE_BG,
            highlightbackground = Color_support.PROCESS_TITLE_BG,
            bd = 1, relief = FLAT, overrelief = FLAT)
        # text = '''Test''')

        self.buttonQueryZTest.pack(anchor = CENTER)
        self.buttonQueryZTest.update()


        # endregion

        # PROCESS CHI-SQUARE OPTIONS
        # region
        self.labelFrameProcessChiSquare = LabelFrame(self.labelFrameProcessTestOptions, bd = 0,
                                                     name = "labelFrameProcessChiSquare")
        self.labelFrameProcessChiSquare.place(
            # relx = newRelX, rely = 0,
            relx = 0, rely = 0,
            # relwidth = UI_support.TEST_PROCESS_CHI_SQUARE_PARENT, relheight = 1
            relwidth = 1, relheight = 1
        )
        self.labelFrameProcessChiSquare.configure(
            background = Color_support.PROCESS_BG
        )

        # newRelX = FS.getRelX(self.labelFrameProcessChiSquare) + FS.getRelW(self.labelFrameProcessChiSquare)

        # PROCESS CHI-SQUARE TITLE
        self.labelFrameProcessChiSquareTitle = Label(self.labelFrameProcessChiSquare)
        # self.labelFrameProcessChiSquareTitle = Label(self.labelFrameProcessChiSquare)
        self.labelFrameProcessChiSquareTitle.place(
            relx = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_X,
            rely = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y,
            relwidth = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H)
        self.labelFrameProcessChiSquareTitle.configure(
            font = UI_support.FONT_MED_BOLD,
            background = Color_support.PROCESS_CHI_SQUARE_TITLE_BG,
            foreground = Color_support.PROCESS_CHI_SQUARE_TITLE_FG,

            text = '''CHI - SQUARE''',
            anchor = CENTER,
            bd = 0, relief = GROOVE
        )

        # Top horizontal separator # TODO
        self.chiSquareTitleSeparator = ttk.Separator(self.labelFrameProcessChiSquareTitle, orient = HORIZONTAL)
        self.chiSquareTitleSeparator.place(relx = 0, rely = 1, relwidth = 1)

        # self.chiSquareRightSeparator = ttk.Separator(self.labelFrameProcessChiSquare, orient = VERTICAL)
        # self.chiSquareRightSeparator.place(relx = 0.99, rely = 0, relheight = 1)

        newRelY = FS.getRelY(self.labelFrameProcessZTestTitle) + FS.getRelH(
            self.labelFrameProcessZTestTitle) + UI_support.TAB_TEST_PROCESS_Z_TEST_SPINNER_ELEMENTS_REL_Y

        # BUTTON ELEMENTS
        self.labelFrameProcessChiSquareElements = LabelFrame(self.labelFrameProcessChiSquare, bd = 0)
        self.labelFrameProcessChiSquareElements.place(
            relx = 0, rely = newRelY,
            relwidth = 1, relheight = 0.35
        )
        self.labelFrameProcessChiSquareElements.configure(
            background = Color_support.PROCESS_BG
        )

        # QUEUE ELEMENTS
        self.labelFrameProcessChiSquareQueue = LabelFrame(self.labelFrameProcessChiSquareElements, bd = 1)
        self.labelFrameProcessChiSquareQueue.place(
            relx = 0.275, rely = 0,
            relwidth = 0.45, relheight = 1
        )
        self.labelFrameProcessChiSquareQueue.configure(
            background = Color_support.PROCESS_BG
        )

        newRelX = FS.getRelX(self.labelFrameProcessChiSquare) + FS.getRelW(
            self.labelFrameProcessChiSquare)

        # > QUEUE COUNT
        self.labelQueueText = Label(self.labelFrameProcessChiSquareQueue)
        self.labelQueueText.place(
            relx = 0, rely = 0,
            relwidth = 1, relheight = UI_support.TAB_TEST_PROCESS_QUEUE_TEXT_REL_H
        )
        self.labelQueueText.configure(
            font = UI_support.FONT_DEFAULT_BOLD,
            background = Color_support.FG_COLOR, foreground = Color_support.SELECT_BG,
            text = '''QUEUE SIZE'''
        )

        newRelY = FS.getRelY(self.labelQueueText) + FS.getRelH(self.labelQueueText)
        newRelH = 1 - FS.getRelH(self.labelQueueText)

        self.labelQueueCount = Label(self.labelFrameProcessChiSquareQueue)
        self.labelQueueCount.place(
            relx = 0, rely = newRelY,
            relwidth = 1, relheight = newRelH)
        self.labelQueueCount.configure(
            font = UI_support.FONT_LARGE_BOLD,
            background = Color_support.SELECT_BG,
            text = '''0'''
        )

        # ENQUEUE BUTTON
        # Enqueue button parent (to handle centering after pack)

        newRelX = FS.getRelX(self.labelFrameProcessChiSquareQueue) + FS.getRelW(
            self.labelFrameProcessChiSquareQueue)

        self.labelFrameProcessQueue = LabelFrame(self.labelFrameProcessChiSquareElements, bd = 0)
        self.labelFrameProcessQueue.place(
            relx = newRelX + 0.025, rely = 0,
            relwidth = 0.25, relheight = 1
        )
        self.labelFrameProcessQueue.configure(
            background = Color_support.PROCESS_BG
        )

        # Enqueue button
        self.buttonQueue = Button(self.labelFrameProcessQueue, compound = CENTER)

        im = PIL.Image.open(Icon_support.TAB_ICO_ADD).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_queue_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueue.configure(
            image = btn_queue_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueue.image = btn_queue_icon  # < ! > Required to make images appear

        self.buttonQueue.configure(
            background = Color_support.PROCESS_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)

        self.buttonQueue.pack(side = LEFT)
        self.buttonQueue.update()

        # CLEAR QUEUE BUTTON

        # Clear queue button parent (to handle centering after pack)
        self.labelFrameProcessClearQueue = LabelFrame(self.labelFrameProcessChiSquareElements, bd = 0)
        self.labelFrameProcessClearQueue.place(
            relx = 0, rely = 0,
            relwidth = 0.25, relheight = 1
        )
        self.labelFrameProcessClearQueue.configure(
            background = Color_support.PROCESS_BG
        )

        self.buttonClearQueue = Button(self.labelFrameProcessClearQueue, compound = CENTER)

        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_clear_queue_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonClearQueue.configure(
            image = btn_clear_queue_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonClearQueue.image = btn_clear_queue_icon  # < ! > Required to make images appear

        self.buttonClearQueue.configure(
            background = Color_support.PROCESS_BG, foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT
        )

        self.buttonClearQueue.pack(side = RIGHT)
        self.buttonClearQueue.update()

        # endregion

        newRelX = FS.getRelX(self.labelFrameProcessTestOptions) + FS.getRelW(self.labelFrameProcessTestOptions)

        # PROCESS RUN PARENT
        self.labelFrameProcessRun = LabelFrame(self.labelFrameProcessCommands, bd = 0)
        self.labelFrameProcessRun.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TEST_PROCESS_RUN_PARENT, relheight = 1
        )
        self.labelFrameProcessRun.configure(
            background = Color_support.PROCESS_BG
        )

        # PROCESS RUN MINER TITLE
        self.labelFrameProcessRunMinerTitle = Label(self.labelFrameProcessRun)
        self.labelFrameProcessRunMinerTitle.place(
            relx = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_X,
            rely = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y,
            relwidth = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H)
        self.labelFrameProcessRunMinerTitle.configure(
            font = UI_support.FONT_MED_BOLD,
            background = Color_support.D_BLUE, foreground = Color_support.WHITE,
            # background = Color_support.PROCESS_RUN_MINER_TITLE_BG, foreground = Color_support.PROCESS_RUN_MINER_TITLE_FG,
            text = '''RUN MINER''',
            anchor = CENTER,
            bd = 1, relief = GROOVE
        )

        # Top horizontal separator # TODO
        self.runMinerTitleSeparator = ttk.Separator(self.labelFrameProcessRunMinerTitle, orient = HORIZONTAL)
        self.runMinerTitleSeparator.place(relx = 0, rely = 1, relwidth = 1)

        newRelY = FS.getRelH(self.labelFrameProcessRunMinerTitle) + FS.getRelY(self.labelFrameProcessRunMinerTitle)
        newRelH = 1 - (FS.getRelH(self.labelFrameProcessRunMinerTitle) + FS.getRelY(
            self.labelFrameProcessRunMinerTitle))
        self.labelFrameRunMiner = LabelFrame(self.labelFrameProcessRun, bd = 0)
        self.labelFrameRunMiner.place(
            relx = 0, rely = newRelY,
            relwidth = 1, relheight = newRelH
        )
        self.labelFrameRunMiner.configure(
            background = Color_support.PROCESS_BG
        )
        self.labelFrameRunMinerElements = LabelFrame(self.labelFrameRunMiner, bd = 0)
        self.labelFrameRunMinerElements.place(
            relx = 0, rely = 0,
            relwidth = 1, relheight = 1
        )
        self.labelFrameRunMinerElements.configure(
            background = Color_support.PROCESS_BG
        )

        # region RUN MINER BUTTON
        self.buttonTestQueue = Button(self.labelFrameRunMinerElements, compound = CENTER)

        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW).resize(Icon_support.RUN_ICO_SIZE, PIL.Image.ANTIALIAS)
        # im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)/
        btn_queue_icon = PIL.ImageTk.PhotoImage(im)

        self.buttonTestQueue.configure(
            image = btn_queue_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonTestQueue.image = btn_queue_icon  # < ! > Required to make images appear

        self.buttonTestQueue.configure(
            background = Color_support.PROCESS_BUTTONS_BG, foreground = Color_support.PROCESS_BUTTONS_FG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = FLAT)

        self.buttonTestQueue.place(
            relx = 0, rely = 0,
            relwidth = 1, relheight = 1
        )
        self.buttonTestQueue.pack(side = RIGHT)
        # self.buttonTestQueue.update()
        self.labelFrameRunMinerElements.pack(fill = Y, expand = True)

        self.runLeftSeparator = ttk.Separator(self.labelFrameProcessRun, orient = VERTICAL)
        self.runLeftSeparator.place(relx = 0, rely = 0, relheight = 1)

        # endregion RUN MINER BUTTON

        # SEPARATOR  ELEMENTS
        newRelX = FS.getRelX(self.labelFrameProcessTestOptions)  # + FS.getRelW(self.labelFrameProcessZTest)
        self.zTestRightSeparator = ttk.Separator(self.labelFrameProcessCommands, orient = VERTICAL)
        self.zTestRightSeparator.place(relx = 0.335, rely = 0, relheight = 1, anchor = NE)

        newRelX = FS.getRelX(self.labelFrameProcessRun)  # + FS.getRelW(self.labelFrameProcessChiSquare)
        self.runLeftSeparator = ttk.Separator(self.labelFrameProcessCommands, orient = VERTICAL)
        self.runLeftSeparator.place(relx = 0.6666, rely = 0, relheight = 1)


    """ Performs spinbox value validation """
    def validateZConfidenceSpinbox(self, spinBoxValue, spinBox):
        global arrQueryCriticalValue, arrQueryCriticalValueMapping

        newValue = spinBoxValue.get()
        try:
            floatValue = float(newValue)
            if not arrQueryCriticalValueMapping[
                floatValue]:  # If the new value is not defined in the value mapping, don't accept it
                self.refreshSpinBoxValue(spinBox)
        except:
            self.refreshSpinBoxValue(spinBox)

        spinBox.update()

    """ Reconfigures spinbox value by pressing the up then down buttons """
    def refreshSpinBoxValue(self, spinBox):
        spinBox.invoke("buttonup")
        spinBox.invoke("buttondown")

    """ Elements under the CONSOLE ("") HEADER """
    def configureConsoleElements(self, parentFrame):

        # PROCESS COMMANDS PARENT
        self.labelFrameConsoleScreen = LabelFrame(parentFrame, bd = 0)
        newRelW = 0.72
        newRelH = 0.8
        newRelY = 0.09  # 0.092

        self.labelFrameConsoleScreen.place(
            relx = (1 - newRelW) / 2,
            rely = newRelY,
            relwidth = newRelW,
            relheight = newRelH
        )

        self.labelFrameConsoleScreen.configure(
            background = Color_support.CONSOLE_BG,
            bd = 0, relief = GROOVE
        )

        # TASKBAR

        self.labelConsoleScreenTaskBar = Label(self.labelFrameConsoleScreen)
        self.labelConsoleScreenTaskBar.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 0.0425  # 0.042
        )

        self.labelConsoleScreenTaskBar.configure(
            background = Color_support.SELECT_LISTBOX_STATUS_BG, foreground = Color_support.SELECT_LISTBOX_STATUS_FG,
            bd = UI_support.SELECT_STATUS_LABEL_BORDER, relief = UI_support.SELECT_STATUS_LABEL_RELIEF,
            text = UI_support.LBL_SELECT_NO_DATA,
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )

        # self.createCornerImage(self.labelConsoleScreenTaskBar) # TODO Create borders

        # STRIPES
        self.labelConsoleStripes = Label(self.labelFrameConsoleScreen, bd = 0, relief = GROOVE)
        newRelY = FS.getRelY(self.labelConsoleScreenTaskBar) + FS.getRelH(self.labelConsoleScreenTaskBar)
        newRelH = 0.014  # 0.008
        self.labelConsoleStripes.place(
            relx = 0,
            rely = newRelY,
            relwidth = 1,
            relheight = newRelH
        )

        im = PIL.Image.open(Icon_support.TEXTURE_STRIPE_PINK)
        texture_pink_stripes = PIL.ImageTk.PhotoImage(im)
        self.labelConsoleStripes.configure(
            image = texture_pink_stripes,
            anchor = SW
        )
        self.labelConsoleStripes.image = texture_pink_stripes  # < ! > Required to make images appear

        # CONSOLE SCREEN
        self.configureConsoleScreenElements()

        # CONSOLE CONTROLS

        self.labelFrameConsoleControls = LabelFrame(self.labelFrameConsoleScreen)

        sizeReference = self.labelConsoleScreenTaskBar
        newRelY = FS.getRelY(self.listConsoleScreen) + FS.getRelH(self.listConsoleScreen)
        self.labelFrameConsoleControls.place(
            relx = FS.getRelX(sizeReference) + 0.025,
            rely = newRelY + 0.01,
            relwidth = 0.95,
            relheight = FS.getRelH(sizeReference) * 2 * 2 / 3
        )

        self.labelFrameConsoleControls.configure(
            background = Color_support.WHITE,
            bd = 0, relief = GROOVE
        )

        # SHOW ALL CONSOLE
        self.buttonConsoleAll = Button(self.labelFrameConsoleControls)
        self.buttonConsoleAll.place(
            relx = 0.008,
            rely = 0.01,
            relwidth = 0.24,
            relheight = 0.98)

        self.buttonConsoleAll.configure(
            text = '''ALL''',
            background = Color_support.WHITE,
            foreground = Color_support.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = Color_support.L_GRAY,
            activeforeground = Color_support.DATASET_BTN_FG_ACTIVE,
            disabledforeground = Color_support.FG_DISABLED_COLOR
        )

        # SHOW Z-TEST CONSOLE
        self.buttonConsoleZTest = Button(self.labelFrameConsoleControls)
        buttonReference = self.buttonConsoleAll
        newRelX = FS.getRelX(buttonReference) + FS.getRelW(buttonReference) + FS.getRelX(self.buttonConsoleAll)

        self.buttonConsoleZTest.place(
            relx = newRelX,
            rely = FS.getRelY(buttonReference),
            relwidth = FS.getRelW(buttonReference),
            relheight = FS.getRelH(buttonReference)
        )

        self.buttonConsoleZTest.configure(
            text = '''Z''',
            background = buttonReference['background'],
            foreground = buttonReference['foreground'],
            bd = buttonReference['bd'], relief = buttonReference['relief'], overrelief = buttonReference['overrelief'],
            activebackground = buttonReference['activebackground'],
            activeforeground = buttonReference['activeforeground'],
            disabledforeground = buttonReference['disabledforeground'],
        )

        # SHOW CHI-SQUARE CONSOLE
        self.buttonConsoleChiSquare = Button(self.labelFrameConsoleControls)
        buttonReference = self.buttonConsoleZTest
        newRelX = FS.getRelX(buttonReference) + FS.getRelW(buttonReference) + FS.getRelX(self.buttonConsoleAll)

        self.buttonConsoleChiSquare.place(
            relx = newRelX,
            rely = FS.getRelY(buttonReference),
            relwidth = FS.getRelW(buttonReference),
            relheight = FS.getRelH(buttonReference)
        )

        self.buttonConsoleChiSquare.configure(
            text = '''CHI''',
            background = buttonReference['background'],
            foreground = buttonReference['foreground'],
            bd = buttonReference['bd'], relief = buttonReference['relief'], overrelief = buttonReference['overrelief'],
            activebackground = buttonReference['activebackground'],
            activeforeground = buttonReference['activeforeground'],
            disabledforeground = buttonReference['disabledforeground'],
        )

        # SHOW QUEUE CONSOLE
        self.buttonConsoleQueue = Button(self.labelFrameConsoleControls)
        buttonReference = self.buttonConsoleChiSquare
        newRelX = FS.getRelX(buttonReference) + FS.getRelW(buttonReference) + FS.getRelX(self.buttonConsoleAll)

        self.buttonConsoleQueue.place(
            relx = newRelX,
            rely = FS.getRelY(buttonReference),
            relwidth = FS.getRelW(buttonReference),
            relheight = FS.getRelH(buttonReference)
        )

        self.buttonConsoleQueue.configure(
            text = '''Q''',
            background = buttonReference['background'],
            foreground = buttonReference['foreground'],
            bd = buttonReference['bd'], relief = buttonReference['relief'], overrelief = buttonReference['overrelief'],
            activebackground = buttonReference['activebackground'],
            activeforeground = buttonReference['activeforeground'],
            disabledforeground = buttonReference['disabledforeground'],
        )

        # Add console borders
        self.createLabelBorders(self.labelFrameConsoleScreen)
    def configureConsoleScreenElements(self):
        self.scrollConsoleScreen = Scrollbar(self.labelFrameConsoleScreen, orient = VERTICAL,
                                             name = 'scrollConsoleScreen')
        newRelH = 0.8
        newRelY = FS.getRelY(self.labelConsoleStripes) + FS.getRelH(self.labelConsoleStripes)

        # region BASIC CONSOLE SCREEN
        # self.listConsoleScreen = Listbox(self.scrollConsoleScreen, name = 'listConsoleScreen')
        self.listConsoleScreen = Text(self.labelFrameConsoleScreen, name = 'listConsoleScreen')
        # self.listConsoleScreen.insert(END, "A really \n long \n text \n to \n test \n this")
        self.listConsoleScreen.place(
            relx = 0,
            rely = newRelY,
            relwidth = 1,
            relheight = newRelH
        )
        self.listConsoleScreen.configure(
            yscrollcommand = self.scrollConsoleScreen.set,
            background = Color_support.SELECT_LISTBOX_BG, foreground = Color_support.SELECT_LISTBOX_FG,
            selectbackground = Color_support.SELECT_LISTBOX_BG, selectforeground = Color_support.SELECT_LISTBOX_FG,
            font = UI_support.FONT_SMALL,
            bd = UI_support.SELECT_LISTBOX_BORDER, relief = UI_support.SELECT_LISTBOX_RELIEF,

            cursor = "arrow",
            state = DISABLED,
            padx = 0
        )

        self.listConsoleScreen.tag_configure(const.CONSOLE.DEFAULT,
                                             lmargin1 = 5,
                                             lmargin2 = 5,
                                             rmargin = 5,

                                             spacing1 = 0,
                                             spacing2 = 0,
                                             spacing3 = 0,
                                             justify = LEFT)


        # endregion BASIC CONSOLE SCREEN

        # region QUEUE SCREEN listConsoleQueueScreen
        self.listConsoleQueueScreen = Text(self.labelFrameConsoleScreen, name = 'listConsoleQueueScreen')
        screenWidget = self.listConsoleQueueScreen
        screenReference = self.listConsoleScreen

        screenWidget.place(
            relx = FS.getRelX(screenReference),
            rely = FS.getRelY(screenReference),
            relwidth = FS.getRelW(screenReference),
            relheight = FS.getRelH(screenReference)
        )
        screenWidget.configure(
            background = screenReference['background'],
            foreground = screenReference['foreground'],
            selectbackground = screenReference['selectbackground'],
            selectforeground = screenReference['selectforeground'],

            font = screenReference['font'],
            bd = screenReference['bd'],
            relief = screenReference['relief'],

            cursor = screenReference['cursor'],
            state = screenReference['state'],
            padx = screenReference['padx']
        )
        screenWidget.tag_configure(const.CONSOLE.DEFAULT,
                                   lmargin1 = 5,
                                   lmargin2 = 5,
                                   rmargin = 5,

                                   spacing1 = 0,
                                   spacing2 = 0,
                                   spacing3 = 0,
                                   justify = LEFT)
        # endregion QUEUE SCREEN listConsoleQueueScreen

        # region Z-TEST CONSOLE SCREEN listConsoleZTestScreen
        self.listConsoleZTestScreen = Text(self.labelFrameConsoleScreen, name = 'listConsoleZTestScreen')
        screenWidget = self.listConsoleZTestScreen
        screenReference = self.listConsoleScreen

        screenWidget.place(
            relx = FS.getRelX(screenReference),
            rely = FS.getRelY(screenReference),
            relwidth = FS.getRelW(screenReference),
            relheight = FS.getRelH(screenReference)
        )
        screenWidget.configure(
            background = screenReference['background'],
            foreground = screenReference['foreground'],
            selectbackground = screenReference['selectbackground'],
            selectforeground = screenReference['selectforeground'],

            font = screenReference['font'],
            bd = screenReference['bd'],
            relief = screenReference['relief'],

            cursor = screenReference['cursor'],
            state = screenReference['state'],
            padx = screenReference['padx']
        )
        screenWidget.tag_configure(const.CONSOLE.DEFAULT,
                                   lmargin1 = 5,
                                   lmargin2 = 5,
                                   rmargin = 5,

                                   spacing1 = 0,
                                   spacing2 = 0,
                                   spacing3 = 0,
                                   justify = LEFT)

        # endregion Z-TEST CONSOLE SCREEN listConsoleZTestScreen

        # region CHI-SQUARE CONSOLE SCREEN listConsoleChiSquareScreen
        self.listConsoleChiSquareScreen = Text(self.labelFrameConsoleScreen, name = 'listConsoleChiSquareScreen')
        screenWidget = self.listConsoleChiSquareScreen
        screenReference = self.listConsoleScreen

        screenWidget.place(
            relx = FS.getRelX(screenReference),
            rely = FS.getRelY(screenReference),
            relwidth = FS.getRelW(screenReference),
            relheight = FS.getRelH(screenReference)
        )
        screenWidget.configure(
            background = screenReference['background'],
            foreground = screenReference['foreground'],

            # selectmode = screenReference['selectmode'],
            # exportselection = screenReference['exportselection'],
            # activestyle = screenReference['activestyle'],
            selectbackground = screenReference['selectbackground'],
            selectforeground = screenReference['selectforeground'],

            font = screenReference['font'],
            bd = screenReference['bd'],
            relief = screenReference['relief'],

            cursor = screenReference['cursor'],
            state = screenReference['state'],
            padx = screenReference['padx']
        )
        screenWidget.tag_configure(const.CONSOLE.DEFAULT,
                                   lmargin1 = 5,
                                   lmargin2 = 5,
                                   rmargin = 5,

                                   spacing1 = 0,
                                   spacing2 = 0,
                                   spacing3 = 0,
                                   justify = LEFT)


        self.scrollConsoleScreen.place(
            relx = 0,
            rely = 0,
            relwidth = 0,
            relheight = 0
            # rely = newRelY,
            # relwidth = 1,
            # relheight = newRelH
        )
        self.scrollConsoleScreen.configure(
            background = Color_support.D_BLUE,
            bd = 0,
        )

        # endregion CHI-SQUARE CONSOLE SCREEN listConsoleChiSquareScreen

        # Configure screen dictionary
        self.dictConsoleScreens = {
            self.listConsoleScreen: const.SCREENS.ALL,
            self.listConsoleQueueScreen: const.SCREENS.QUEUE,
            self.listConsoleZTestScreen: const.SCREENS.Z_TEST,
            self.listConsoleChiSquareScreen: const.SCREENS.CHI_SQUARE,
        }



    """ UI HELPER FUNCTIONS """
    # region UI HELPER FUNCTIONS
    def createCornerImage(self, cornerParent):

        labelNE = Label(cornerParent)
        im = PIL.Image.open(
            Icon_support.CORNER_ROUND_NE)  # .resize(Icon_support.CORNER_ICO_SIZE_SMALL, PIL.Image.ANTIALIAS)
        corner_round_ne = PIL.ImageTk.PhotoImage(im)
        labelNE.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 1
        )
        labelNE.configure(
            image = corner_round_ne)
        labelNE.image = corner_round_ne  # < ! > Required to make images appear
        labelNE.configure(background = Color_support.PALE_ORANGE)  # cornerParent['background'])
        labelNE.pack()
        # labelNE.pack(side = RIGHT, fill = Y, expand = True, anchor = CENTER)

    def createLabelSeparator(self, separatorParent, span, isVertical, color, thickness = 1, coordinate = 0,
                             specifiedAnchor = NW):

        separatorHolder = Label(separatorParent)
        if isVertical:
            newRelY = (1 - (1 - span)) / 2
            separatorHolder.place(
                relx = coordinate,
                rely = newRelY,
                relheight = span,  # TODO To adjust border height, just adjust this
                width = thickness,
                anchor = specifiedAnchor
            )
        else:
            newRelX = (1 - (1 - span)) / 2
            separatorHolder.place(
                relx = newRelX,
                rely = coordinate,
                relwidth = span,  # TODO To adjust border height, just adjust this
                height = thickness,
                anchor = specifiedAnchor
            )
        separatorHolder.configure(background = color)
        return separatorHolder

    def createLabelBorders(self, borderParent, color = Color_support.DISABLED_D_BLUE):

        # COLORED SEPARATOR
        topBorder = self.createLabelSeparator(
            borderParent, 1,
            False, color
        )

        bottomBorder = self.createLabelSeparator(
            borderParent, 1,
            False, color,
            coordinate = 0.9985
        )

        leftBorder = self.createLabelSeparator(
            borderParent, 1,
            True, color
        )

        rightBorder = self.createLabelSeparator(
            borderParent, 1,
            True, color,
            coordinate = 0.995
        )

    # endregion UI HELPER FUNCTIONS


    """ SETTERS """
    # region SETTERS
    def setArrQueryCriticalValue(self, arrayValue):
        self.arrQueryCriticalValue = arrayValue

    def setArrQueryCriticalValueMapping(self, arrayValue):
        self.arrQueryCriticalValueMapping = arrayValue

    def getMainFrame(self):
        return self.lfTabParentFrame
    # endregion SETTERS

    """ GETTERS """
    # region GETTERS
    def getDatasetCountA(self):
        return str(self.featureSelectCount)

    def getDatasetCountB(self):
        return str(self.confirmedFeaturesCount)


    def getButtonQuerySetDataA(self):
        return self.btnQueryFeatureList
    def getButtonQuerySetDataB(self):
        return self.buttonQuerySetDataB

    def getButtonQueryAddFilterA(self):
        return self.buttonQueryAddFilterA
    def getButtonQueryAddFilterB(self):
        return self.buttonQueryAddFilterB

    def getButtonQueryFeature(self):
        return self.buttonQueryFeature

    def getButtonQueryZTest(self):
        return self.buttonQueryZTest

    def getButtonQueue(self):
        return self.buttonQueue
    def getButtonClearQueue(self):
        return self.buttonClearQueue
    def getButtonTestQueue(self):
        return self.buttonTestQueue

    def getButtonQueryResetFilterA(self):
        return self.btnResetFeatureSelect
    def getButtonQueryResetFilterB(self):
        return self.buttonQueryResetFilterB

    def getButtonChooseChiSquare(self):
        return self.buttonChooseChiSquare
    def getButtonChooseZTest(self):
        return self.buttonChooseZTest

    def getButtonConsoleAll(self):
        return self.buttonConsoleAll
    def getButtonConsoleZTest(self):
        return self.buttonConsoleZTest
    def getButtonConsoleChiSquare(self):
        return self.buttonConsoleChiSquare
    def getButtonConsoleQueue(self):
        return self.buttonConsoleQueue

    def getListConsoleScreen(self):
        return self.listConsoleScreen
    def getListConsoleZTestScreen(self):
        return self.listConsoleZTestScreen
    def getListConsoleChiSquareScreen(self):
        return self.listConsoleChiSquareScreen
    def getListConsoleQueueScreen(self):
        return self.listConsoleQueueScreen


    def getLabelQueryDataA(self):
        return self.labelQueryDataA
    def getLabelQueryDataB(self):
        return self.labelQueryDataB

    def getLabelQueryDataFeatureName(self):
        return self.labelQueryDataFeatureName

    def getListQueryDataA(self):
        return self.listQueryDataA
    def getListQueryDataB(self):
        return self.listQueryDataB

    def getEntryQueryFeature(self):
        return self.entryQueryFeature

    def getLabelOverlayFilterListData(self):
        return self.labelOverlayFilterListData
    def getLabelFrameFilterListData(self):
        return self.labelFrameFilterListData
    def getLabelFilterStripes(self):
        return self.labelFilterStripes

    def getLabelQuerySetDataStatusA(self):
        return self.lblStatusFeatureSelect
    def getLabelQuerySetDataStatusB(self):
        return self.labelQuerySetDataStatusB

    def getLabelQuerySetDataStripesA(self):
        return self.lblStripesQueryFeatureSelect
    def getLabelQuerySetDataStripesB(self):
        return self.labelQuerySetDataStripesB

    def getLabelQueryDataACount(self):
        return self.labelQueryDataACount
    def getLabelQueryDataBCount(self):
        return self.labelQueryDataBCount

    def getEntryQuerySetDataA(self):
        return self.entryQueryFeatureList
    def getEntryQuerySetDataB(self):
        return self.entryQuerySetDataB

    def getListQuerySetDataA(self):
        return self.lbListFeatureSelect
    def getListQuerySetDataB(self):
        return self.listQuerySetDataB

    def getLabelFrameProcessChiSquare(self):
        return self.labelFrameProcessChiSquare
    def getLabelFrameProcessZTest(self):
        return self.labelFrameProcessZTest

    def getSpinBoxQueryZConfidence(self):
        return self.spinBoxQueryZConfidence

    def getDictConsoleScreens(self):
        return self.dictConsoleScreens

    def getLabelConsoleScreenTaskBar(self):
        return self.labelConsoleScreenTaskBar

    def getLabelQueueCount(self):
        return self.labelQueueCount

    def getButtonQueryZTestSvP(self):
        return self.buttonQueryZTestSvP

    def getComboQueryTest(self):
        return self.comboQueryTest

    # endregion GETTERS
