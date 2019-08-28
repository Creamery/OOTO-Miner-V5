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


import Color_support as CS
import Icon_support
import UI_support
import PIL.Image
import PIL.ImageTk
import CONSTANTS as const
import Function_support as FS
import Widget_support as WS
import Keys_support as key


class AutomatedMining_View:

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

        WS.redraw(self.lfTabParentFrame)
        self.lfProcessFrame.place(width = 0, height = 0)
        self.lfResultsFrame.place(width = 0, height = 0)
        # self.lfConsoleFrame.place(width = 0, height = 0)

        self.configureSeparators(parentFrame)
        self.updateFS()


    def updateFS(self):
        FS.headerWidth = self.__lblHeaderFeatureSelect.winfo_width()
        FS.headerHeight = self.__lblHeaderFeatureSelect.winfo_height()

        FS.stripeWidth = self.lblStripesQueryFeatureSelect.winfo_width()
        FS.stripeHeight = self.lblStripesQueryFeatureSelect.winfo_height()


    def initializeProperties(self):
        self.__btnConfirmConfirmedFeatures = [None]
        self.__btnResetConfirmedFeatures = [None]
        self.__btnQueryConfirmedFeatures = [None]
        self.__lbListConfirmedFeatures = [None]
        self.__lbListConfirmedResponses = [None]
        self.__lblCountConfirmedFeaturesText = [None]
        self.__entryQueryConfirmedFeatures = [None]
        self.__lblHeaderConfirmedFeatures = [None]
        self.__lblCountConfirmedFeaturesTitle = [None]


    def configureSeparators(self, parentFrame):
        parentFrame.update()
        # region emborder console
        borderX = self.lfConsoleFrame.winfo_x()
        WS.emborder(parentFrame,
                    [borderX, 0, 1, None],
                    [False, False, False, True])
        # endregion emborder console

        # region emborder for tab
        WS.emborder(parentFrame,
                    [0, 0, 1, None],
                    [False, False, False, True])
        # endregion emborder for tab

    def initTabFrame(self, parentFrame):
        tabFrame = LabelFrame(parentFrame, bd = 0)
        tabFrame.place(
            relx = UI_support.TAB_REL_X, rely = UI_support.TAB_REL_Y,
            relwidth = UI_support.TAB_REL_W, relheight = UI_support.TAB_REL_H
        )
        tabFrame.configure(
            background = CS.TAB_BG_COLOR, foreground = CS.FG_COLOR
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
            background = CS.TYPE_BG, foreground = CS.FG_COLOR
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
            background = CS.SELECT_BG, foreground = CS.FG_COLOR
        )
        # endregion init lfInputElements

        # configure elements
        self.initFeatureList(inputFrame)

        # adjust elements
        self.adjustFeatureList(inputFrame)

        # create the ConfirmedFeatures frame, which is a copy of the FeatureSelect frame
        self.lfFeatureSelect.update()
        self.lfConfirmedFeatures = WS.copyWidget(self.lfFeatureSelect, inputFrame)
        # region init lfConfirmedFeatures
        reference = self.lfFeatureSelect
        newX = inputFrame.winfo_width() - reference.winfo_x() - reference.winfo_width()
        self.lfConfirmedFeatures.place(
            x = newX, y = reference.winfo_y(),
            width = reference.winfo_width(),
            height = reference.winfo_height())
        # endregion lfConfirmedFeatures

        # assign widgets to track from FeatureSelect to ConfirmedFeatures
        trackedWidgets, trackedVariableList = self.getTrackedConfirmedFeaturesWidgets()

        # create a copy of FeatureSelect and assign 'tracked' widgets (e.g. buttons, entries, labels)
        # to corresponding ConfirmedFeatures (self) variables
        self.createConfirmedFeatures(self.lfConfirmedFeatures, self.lfFeatureSelect, trackedWidgets, trackedVariableList)

        # 'apply' tracked widget variables to ConfirmedFeatures (self) variables by 'de-listing' them
        self.applyTrackedConfirmedFeaturesWidgets()

        # adjust elements
        self.adjustConfirmedFeatures(inputFrame)

        # region create vertical separator
        inputFrame.update()
        offset = 5
        newY = self.lfFeatureSelect.winfo_y() + self.lfHeaderFeatureSelect.winfo_y() + offset
        newHeight = self.lfFeatureSelect.winfo_height() - (offset * 6)
        verticalSeparator = ttk.Separator(inputFrame, orient = VERTICAL)
        verticalSeparator.place(relx = 0.5, y = newY,
                                height = newHeight)
        # endregion create vertical separator

        return inputFrame

    """Adjust values of ConfirmedFeatures (since it is a direct clone of FeatureSelect)"""
    def adjustConfirmedFeatures(self, parentFrame):
        parentFrame.update()

        self.__lblHeaderConfirmedFeatures['text'] = 'SELECTED FEATURES'
        self.__lblCountConfirmedFeaturesText.place(
            relx = 0, rely = 0,
            x = - 1, y = - 1)
        FS.placeBelow(self.__lblCountConfirmedFeaturesTitle, self.__lblCountConfirmedFeaturesText)
        FS.alignStart(self.__lblCountConfirmedFeaturesTitle, self.__lblCountConfirmedFeaturesText, -1)

    """
    Track FeatureSelect widgets to be assigned to ConfirmedFeatures widgets.
    You must call applyTracked<...>Widgets afterwards.
    """
    def getTrackedConfirmedFeaturesWidgets(self):
        trackedWidgets = {
            repr(self.__btnConfirmFeatureSelect): 0,
            repr(self.__btnResetFeatureSelect): 1,
            repr(self.__btnQueryFeatureList): 2,
            repr(self.__lbListFeatureSelect): 3,
            repr(self.__lbListFeatureResponses): 4,
            repr(self.lblCountFeatureSelectText): 5,
            repr(self.__entryQueryFeatureList): 6,
            repr(self.__lblHeaderFeatureSelect): 7,
            repr(self.lblCountFeatureSelectTitle): 8
        }
        trackedVariableList = [
            self.__btnConfirmConfirmedFeatures,
            self.__btnResetConfirmedFeatures,
            self.__btnQueryConfirmedFeatures,
            self.__lbListConfirmedFeatures,
            self.__lbListConfirmedResponses,
            self.__lblCountConfirmedFeaturesText,
            self.__entryQueryConfirmedFeatures,
            self.__lblHeaderConfirmedFeatures,
            self.__lblCountConfirmedFeaturesTitle
        ]
        return trackedWidgets, trackedVariableList

    """
    Sets the variable values to the widget assignment
    (Since the widgets are placed in a list in order to be updated).
    """
    def applyTrackedConfirmedFeaturesWidgets(self):
        self.__btnConfirmConfirmedFeatures = self.__btnConfirmConfirmedFeatures[0]
        self.__btnResetConfirmedFeatures = self.__btnResetConfirmedFeatures[0]
        self.__btnQueryConfirmedFeatures = self.__btnQueryConfirmedFeatures[0]
        self.__lbListConfirmedFeatures = self.__lbListConfirmedFeatures[0]
        self.__lbListConfirmedResponses = self.__lbListConfirmedResponses[0]
        self.__lblCountConfirmedFeaturesText = self.__lblCountConfirmedFeaturesText[0]
        self.__entryQueryConfirmedFeatures = self.__entryQueryConfirmedFeatures[0]
        self.__lblHeaderConfirmedFeatures = self.__lblHeaderConfirmedFeatures[0]
        self.__lblCountConfirmedFeaturesTitle = self.__lblCountConfirmedFeaturesTitle[0]


    def createConfirmedFeatures(self, parentFrame, reference, trackedWidgets, trackedVariableList):
        reference.update()
        for item in reference.winfo_children():
            itemClone = WS.copyWidget(item, parentFrame)

            [isTracking, variableIndex] = self.checkTracking(item, trackedWidgets)
            if isTracking:
                # print "isTracking index " + str(variableIndex)
                trackedVariableList[variableIndex][0] = itemClone


            if isinstance(itemClone, Widget):
                self.createConfirmedFeatures(itemClone, item, trackedWidgets, trackedVariableList)
            else:
                return "break"



    def checkTracking(self, item, trackedWidgets):
        itemKey = repr(item)
        # print("itemKey is " + str(itemKey) + " in " + str(trackedWidgets.keys()))
        if FS.checkKey(trackedWidgets, itemKey):
            return True, trackedWidgets[itemKey]
        else:
            return False, -1

    def adjustFeatureList(self, parentFrame):
        WS.redraw(parentFrame)

        # region extend lfFeatureList
        height = 165 # self.lfCommandsFeatureSelect.winfo_height() * 5
        partialTopHeight = 80
        partialBottomHeight = height - partialTopHeight

        parentFrame.place(height = parentFrame.winfo_height() + height)

        self.lfFeatureSelect.place(height = self.lfFeatureSelect.winfo_height() + height)

        self.lfListFeatureSelect.place(
            height = self.lfListFeatureSelect.winfo_height() + partialTopHeight)

        self.__lbListFeatureSelect.place(y = self.__lbListFeatureSelect.winfo_y(),
                                         height = self.__lbListFeatureSelect.winfo_height() + partialTopHeight)

        self.lfCommandsFeatureSelect.place(y = self.lfCommandsFeatureSelect.winfo_y() + height)


        # endregion extend lfFeatureList

        # region create lfListFeatureDetails
        WS.redraw(parentFrame)
        self.lfListFeatureDetails, self.__lbListFeatureResponses, self.lblHeaderFeatureDetails = self.createFeatureDetails(self.lfFeatureSelect,
                                                                                                                           self.lfListFeatureSelect,
                                                                                                                           partialBottomHeight)
        WS.redraw(parentFrame)
        self.lfListFeatureSelect.place(
            y = self.lfListFeatureSelect.winfo_y(),
            height = self.lfListFeatureSelect.winfo_height()
        )
        # endregion create lfListFeatureDetails

        # region emborder lfListFeatureDetails
        WS.redraw(parentFrame)
        borderX = self.lfListFeatureDetails.winfo_x()
        borderY = self.lfListFeatureSelect.winfo_y() + self.lfListFeatureSelect.winfo_height()
        borderW = self.lfListFeatureDetails.winfo_width()
        borderH = self.lfListFeatureDetails.winfo_height()
        WS.emborder(self.lfFeatureSelect,
                      [borderX, borderY, borderW, borderH],
                      [True, True, False, True],
                      [None, CS.L_GRAY, None, CS.D_GRAY])  # TODO option border
        # endregion emborder lfListFeatureDetails


        # region emborder lfCommandsFeatureSelect
        WS.redraw(parentFrame)
        borderX = self.lfListFeatureDetails.winfo_x()
        borderY = self.lfListFeatureDetails.winfo_y() + self.lfListFeatureDetails.winfo_height()
        borderW = self.lfListFeatureSelect.winfo_width()
        borderH = self.lfFeatureSelect.winfo_height() - borderY
        WS.emborder(self.lfFeatureSelect,
                    [borderX, borderY, borderW, borderH])
        # endregion emborder

        # region adjust counter
        WS.redraw(parentFrame)
        self.lfCountFeatureSelect.place(
            relwidth = 0, relheight = 0,
            width = self.lfCountFeatureSelect.winfo_width(),
            height = self.lfCountFeatureSelect.winfo_height() + 6
        )

        self.lblCountFeatureSelectText.place(
            relx = 0,
            rely = 0,
            x = self.lblCountFeatureSelectText.winfo_x() - 9,
            y = - 2)
        FS.placeBelow(self.lblCountFeatureSelectTitle, self.lblCountFeatureSelectText)
        FS.alignStart(self.lblCountFeatureSelectTitle, self.lblCountFeatureSelectText, - 1)

        WS.redraw(parentFrame)

        # endregion

    def createFeatureDetails(self, parentFrame, referenceFrame, listHeight):
        lfListFeatureDetails = LabelFrame(parentFrame, bd = 0)
        # region init lfListFeatureDetails
        referenceFrame.update()
        lfListFeatureDetails.place(width = referenceFrame.winfo_width(), height = listHeight)
        FS.placeBelow(lfListFeatureDetails, referenceFrame, -1)
        FS.alignStart(lfListFeatureDetails, referenceFrame)
        # endregion lfListFeatureDetails

        lblHeaderFeatureDetails = Label(lfListFeatureDetails)
        # region init lblHeaderFeatureDetails
        self.__lblHeaderFeatureSelect.update()
        lblHeaderFeatureDetails.place(
            x = 0, y = 1,
            width = referenceFrame.winfo_width(), height = self.__lblHeaderFeatureSelect.winfo_height() + 2)
        lblHeaderFeatureDetails.configure(
            background = CS.SELECT_LISTBOX_STATUS_BG, foreground = CS.SELECT_LISTBOX_STATUS_FG,
            bd = 0, relief = FLAT,
            text = 'OPTIONS',
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )
        # region emborder lblHeaderFeatureDetails
        # borderColor = CS.D_BLUE
        # lblHeaderFeatureDetails.update()
        # WS.emborder(lblHeaderFeatureDetails,
        #             [0, 0, None, None],
        #             [True, True, True, True],
        #             [borderColor, borderColor, borderColor, borderColor])
        # endregion emborder lblHeaderFeatureDetails
        # endregion lblHeaderFeatureDetails

        lbListFeatureDetails = Listbox(lfListFeatureDetails)  # TODO getter
        # region init lbListFeatureDetails
        lbListFeatureDetails.configure(
            background = CS.WHITE, foreground = CS.D_BLUE,
            selectmode = SINGLE, exportselection = "0",
            activestyle = "none",
            selectbackground = CS.DISABLED_ORANGE,
            selectforeground = CS.SELECT_LISTBOX_SELECTED_ITEM_FG,
            font = UI_support.SELECT_LABEL_FONT,
            bd = 0,
            relief = UI_support.SELECT_LISTBOX_RELIEF,
            highlightthickness = 0
        )
        lbListFeatureDetails.place(relwidth = 1, relheight = 1)
        FS.placeBelow(lbListFeatureDetails, lblHeaderFeatureDetails, -1)
        FS.alignStart(lbListFeatureDetails, lblHeaderFeatureDetails)
        # endregion lbListFeatureDetails

        return lfListFeatureDetails, lbListFeatureDetails, lblHeaderFeatureDetails
    def createTitleBar(self, parentFrame, strNumber, strName, colorBG):
        titleFrame = LabelFrame(parentFrame, bd = 0)
        titleFrame.configure(
            background = CS.SELECT_BG, foreground = CS.FG_COLOR  # , text = '''FILTER'''
        )

        # COLORED SEPARATOR
        self.createLabelSeparator(
            titleFrame, 1,
            False, colorBG, UI_support.TITLE_SEPARATOR_H,
            0.5
        )

        titleNumber = Label(titleFrame)
        newRelY = UI_support.LABEL_TITLE_REL_Y
        titleNumber.place(
            relx = 0, rely = newRelY,
            relwidth = 0.04 + 0.05,
            relheight = 1 - (newRelY * 2), anchor = NW)

        titleNumber.configure(
            font = UI_support.FONT_MED_BOLD,
            background = CS.SELECT_NUMBER_BG, foreground = CS.SELECT_NUMBER_FG,
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
            background = colorBG, foreground = CS.SELECT_TITLE_FG,
            text = str(strName),
            bd = 0, relief = GROOVE,
            anchor = S
        )
        # Title border
        self.separatorlabelFrameSelectTitleText = self.createLabelSeparator(
            titleText, 1,
            True, CS.WHITE,
            coordinate = 0.99, specifiedAnchor = NW
        )

        return titleFrame

    def initFeatureList(self, parentFrame):

        titleFrame = self.createTitleBar(parentFrame, '1', 'INPUT', CS.SELECT_TITLE_BG)
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
            background = CS.SELECT_BG
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
            background = CS.SELECT_BG
        )
        # endregion init lfConfirmedFeatures


        self.lfHeaderFeatureSelect = LabelFrame(self.lfFeatureSelect, bd = 0)
        # region init lfHeaderFeatureSelect
        self.lfHeaderFeatureSelect.place(
            relx = UI_support.TAB_TEST_SELECT_QUERY_REL_X, rely = UI_support.TAB_TEST_SELECT_QUERY_REL_Y,
            relwidth = UI_support.TAB_TEST_SELECT_QUERY_REL_W, relheight = UI_support.TAB_TEST_SELECT_QUERY_REL_H)

        self.lfHeaderFeatureSelect.configure(
            background = CS.SELECT_ENTRY_BG, foreground = CS.SELECT_ENTRY_FG,
            relief = GROOVE
        )

        # endregion init lfHeaderFeatureSelect

        self.__lblHeaderFeatureSelect = Label(self.lfHeaderFeatureSelect)  # TODO getter
        # region init lblHeaderFeatureSelect
        self.__lblHeaderFeatureSelect.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        self.__lblHeaderFeatureSelect.configure(
            background = CS.SELECT_LISTBOX_STATUS_BG, foreground = CS.SELECT_LISTBOX_STATUS_FG,
            bd = UI_support.SELECT_STATUS_LABEL_BORDER, relief = UI_support.SELECT_STATUS_LABEL_RELIEF,
            text = 'FEATURE LIST',
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )
        if UI_support.SELECT_STATUS_LABEL_TOP_SEPARATOR:
            sepStatusHorizontal = ttk.Separator(self.__lblHeaderFeatureSelect,
                                                orient = HORIZONTAL)
            sepStatusHorizontal.place(relx = 0, rely = 0, relwidth = 1, anchor = NW)

        newRelY = UI_support.TAB_TEST_LISTBOX_QUERY_REL_Y + FS.getRelY(self.lfHeaderFeatureSelect) + FS.getRelH(
            self.lfHeaderFeatureSelect)

        # endregion init lblHeaderFeatureSelect

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
            background = CS.SELECT_BUTTONS_BG
        )
        # endregion init lfBorderQueryFeatureList

        lblQueryFeatureList = Label(lfBorderQueryFeatureList)
        # region init lblQueryFeatureList
        lblQueryFeatureList.place(
            relx = 0.01, rely = 0.025,
            relwidth = 0.98, relheight = 0.95)
        lblQueryFeatureList.configure(
            background = CS.SELECT_LABEL_BG, foreground = CS.SELECT_LABEL_FG,
            text = 'Search',
            font = UI_support.SELECT_LABEL_FONT,
            bd = 0, relief = FLAT,
        )

        newRelX = FS.getRelX(lfBorderQueryFeatureList) + FS.getRelW(
            lfBorderQueryFeatureList)
        # endregion init lblQueryFeatureList

        self.__entryQueryFeatureList = Entry(self.lfQueryFeatureSelect)  # TODO getter
        # region init entryQueryFeatureList
        self.__entryQueryFeatureList.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_ENTRY_REL_W, relheight = 1)
        self.__entryQueryFeatureList.configure(
            background = CS.SELECT_ENTRY_BG, foreground = CS.SELECT_ENTRY_FG,
            bd = 1,
            font = UI_support.ENTRY_FONT, insertwidth = UI_support.INSERT_WIDTH,
            selectbackground = CS.SELECT_ENTRY_SELECT_HIGHLIGHT_BG,
            insertbackground = CS.SELECT_ENTRY_SELECT_INSERT_BG,
            takefocus = UI_support.ENTRY_TAKE_FOCUS, justify = UI_support.SELECT_ENTRY_JUSTIFY
        )  # TODO Constant font definiton

        newRelX = FS.getRelX(self.__entryQueryFeatureList) + FS.getRelW(
            self.__entryQueryFeatureList)  # + UI_support.TAB_3CHILD_LBL_REL_X

        # endregion init entryQueryFeatureList

        self.__btnQueryFeatureList = Button(self.lfQueryFeatureSelect)  # TODO getter
        # region init btnQueryFeatureList
        self.__btnQueryFeatureList.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_BTN_REL_W, relheight = 1)

        im = PIL.Image.open(Icon_support.TAB_ICO_RIGHT_ARROW).resize(Icon_support.SELECT_ICO_SIZE_BUTTONS,
                                                                     PIL.Image.ANTIALIAS)
        btn_query_set_icon = PIL.ImageTk.PhotoImage(im)
        self.__btnQueryFeatureList.configure(
            image = btn_query_set_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.__btnQueryFeatureList.image = btn_query_set_icon  # < ! > Required to make images appear

        self.__btnQueryFeatureList.configure(
            background = CS.SELECT_BUTTONS_BG, foreground = CS.SELECT_BUTTONS_FG,
            activebackground = CS.SELECT_BG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE
        )
        # endregion init btnQueryFeatureList

        self.__lbListFeatureSelect = Listbox(self.lfListFeatureSelect)  # TODO getter
        # region init lbListFeatureSelect
        self.__lbListFeatureSelect.configure(
            background = CS.SELECT_LISTBOX_BG, foreground = CS.SELECT_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = CS.SELECT_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = CS.SELECT_LISTBOX_SELECTED_ITEM_FG,
            font = UI_support.SELECT_LABEL_FONT,
            bd = UI_support.SELECT_LISTBOX_BORDER, relief = UI_support.SELECT_LISTBOX_RELIEF,
            highlightthickness = 0
        )
        newRelY = FS.getRelY(self.lfQueryFeatureSelect) + FS.getRelH(self.lfQueryFeatureSelect)
        newRelH = 1 - (FS.getRelH(self.lfQueryFeatureSelect) + FS.getRelH(self.lblStripesQueryFeatureSelect))
        self.__lbListFeatureSelect.place(relx = 0, rely = newRelY, relwidth = 1, relheight = newRelH)

        newRelY = UI_support.TAB_TEST_COMMANDS_QUERY_REL_Y + FS.getRelY(self.lfListFeatureSelect) + FS.getRelH(
            self.lfListFeatureSelect)

        # endregion init lbListFeatureSelect


        self.lfCommandsFeatureSelect = LabelFrame(self.lfFeatureSelect, bd = 0)
        # region init lfCommandsFeatureSelect
        self.lfCommandsFeatureSelect.place(
            relx = UI_support.TAB_TEST_COMMANDS_QUERY_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_COMMANDS_QUERY_REL_W,
            relheight = UI_support.TAB_TEST_COMMANDS_QUERY_REL_H * 0.85)  # TODO Reduced size

        self.lfCommandsFeatureSelect.configure(
            background = CS.WHITE
        )
        # endregion init lfCommandsFeatureSelect

        self.__btnResetFeatureSelect = Button(self.lfCommandsFeatureSelect)  # TODO getter
        # region init btnResetFeatureSelect
        self.__btnResetFeatureSelect.place(
            relx = 0, rely = 0,
            relwidth = 0.25, relheight = 1)
        self.__btnResetFeatureSelect.configure(
            background = CS.SELECT_BG, foreground = CS.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)

        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_reset_icon = PIL.ImageTk.PhotoImage(im)
        self.__btnResetFeatureSelect.configure(
            image = btn_query_reset_icon)
        self.__btnResetFeatureSelect.image = btn_query_reset_icon  # < ! > Required to make images appear

        newRelX = FS.getRelX(self.__btnResetFeatureSelect) + FS.getRelW(self.__btnResetFeatureSelect)

        # endregion init btnResetFeatureSelect

        self.lfCountFeatureSelect = LabelFrame(self.lfCommandsFeatureSelect, bd = 1)
        # region init self.lfCountFeatureSelect
        self.lfCountFeatureSelect.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.50 - 0.005, relheight = 1
        )
        self.lfCountFeatureSelect.configure(
            background = CS.SELECT_BG
        )

        # Define count variables
        self.featureSelectCount = 0
        self.confirmedFeaturesCount = 0

        # endregion init self.lfCountFeatureSelect

        self.lblCountFeatureSelectText = Label(self.lfCountFeatureSelect)  # TODO getter
        # region init lblCountFeatureSelectText
        self.lblCountFeatureSelectText.place(relx = 0, rely = 0, relwidth = 1,
                                             relheight = UI_support.TAB_TEST_SELECT_COUNT_REL_H)
        self.lblCountFeatureSelectText.configure(
            font = UI_support.FONT_LARGE_BOLD,
            background = CS.SELECT_BG,
            text = self.getDatasetCountA()
        )
        # endregion init lblCountFeatureSelectText

        self.lblCountFeatureSelectTitle = Label(self.lfCountFeatureSelect)
        # region init self.lblCountFeatureSelectTitle
        self.lblCountFeatureSelectTitle.place(
            relx = 0, rely = FS.getRelH(self.lblCountFeatureSelectText),
            relwidth = 1, relheight = UI_support.TAB_TEST_SELECT_COUNT_TEXT_REL_H)
        self.lblCountFeatureSelectTitle.configure(
            font = UI_support.FONT_DEFAULT_BOLD,
            background = CS.FG_COLOR, foreground = CS.SELECT_BG,
            text = 'SELECTED'
        )
        # endregion init self.lblCountFeatureSelectTitle


        self.__btnConfirmFeatureSelect = Button(self.lfCommandsFeatureSelect, compound = CENTER)  # TODO getter
        # region init btnConfirmFeatureSelect
        self.__btnConfirmFeatureSelect.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.25 - 0.005, relheight = 1
        )

        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_filter_icon = PIL.ImageTk.PhotoImage(im)
        self.__btnConfirmFeatureSelect.configure(
            image = btn_query_filter_icon)
        self.__btnConfirmFeatureSelect.image = btn_query_filter_icon  # < ! > Required to make images appear

        self.__btnConfirmFeatureSelect.configure(
            background = CS.SELECT_BG, foreground = CS.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        self.__btnConfirmFeatureSelect.pack(side = RIGHT)
        self.__btnResetFeatureSelect.pack(side = LEFT)



    def initProcessUI(self, parentFrame, relativeFrame):

        newRelY = FS.getRelY(relativeFrame) + FS.getRelH(relativeFrame)  # TODO Make constant (space in between)

        # FILTER Parent Frame
        processFrame = LabelFrame(parentFrame, bd = 0)
        processFrame.place(
            relx = UI_support.TAB_TEST_FILTER_REL_X, rely = newRelY,
            relwidth = UI_support.TAB_TEST_FILTER_REL_W, relheight = UI_support.TAB_TEST_FILTER_REL_H
        )
        processFrame.configure(
            background = CS.FILTER_BG, foreground = CS.FG_COLOR  # , text = '''FILTER'''
        )

        # self.configureFilterElements(processFrame)  # Configures all sub elements under FILTER
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
            background = CS.PROCESS_BG, foreground = CS.FG_COLOR  # , text = '''PROCESS'''
        )

        # self.configureProcessElements(resultsFrame)  # Configures all sub elements under FILTER
        return resultsFrame


    def initConsoleUI(self, parentFrame, relativeFrame):
        prevFrameRelX = float(relativeFrame.place_info()['relx'])
        prevFrameRelW = float(relativeFrame.place_info()['relwidth'])
        newRelX = prevFrameRelX + prevFrameRelW

        # CONSOLE Parent Frame
        consoleFrame = LabelFrame(parentFrame, bd = 0, relief = GROOVE)
        # self.labelFrameConsoleElements.place(
        #     relx = newRelX, rely = UI_support.TAB_TEST_CONSOLE_REL_Y,
        #     relwidth = UI_support.TAB_TEST_CONSOLE_REL_W, relheight = UI_support.TAB_TEST_CONSOLE_REL_H
        # )
        consoleFrame.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_CONSOLE_REL_W, relheight = 1
        )
        consoleFrame.configure(
            background = CS.WHITE, foreground = CS.FG_COLOR  # , text = '''CONSOLE'''
        )

        self.configureConsoleElements(consoleFrame)  # Configures all sub elements under CONSOLE

        return consoleFrame

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
            background = CS.CONSOLE_BG,
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
            background = CS.SELECT_LISTBOX_STATUS_BG, foreground = CS.SELECT_LISTBOX_STATUS_FG,
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
            background = CS.WHITE,
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
            background = CS.WHITE,
            foreground = CS.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = CS.L_GRAY,
            activeforeground = CS.DATASET_BTN_FG_ACTIVE,
            disabledforeground = CS.FG_DISABLED_COLOR
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
            background = CS.SELECT_LISTBOX_BG, foreground = CS.SELECT_LISTBOX_FG,
            selectbackground = CS.SELECT_LISTBOX_BG, selectforeground = CS.SELECT_LISTBOX_FG,
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
            background = CS.D_BLUE,
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
        labelNE.configure(background = CS.PALE_ORANGE)  # cornerParent['background'])
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

    def createLabelBorders(self, borderParent, color = CS.DISABLED_D_BLUE):

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
    def getMainFrame(self):
        return self.lfTabParentFrame
    # endregion SETTERS

    """ GETTERS """
    # region GETTERS
    def getDatasetCountA(self):
        return str(self.featureSelectCount)

    def getDatasetCountB(self):
        return str(self.confirmedFeaturesCount)

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

    def getLabelQueryDataACount(self):
        return self.lblCountFeatureSelectText

    def getDictConsoleScreens(self):
        return self.dictConsoleScreens

    def getLabelConsoleScreenTaskBar(self):
        return self.labelConsoleScreenTaskBar

    # NEW GETTERS
    # region feature select
    def getEntryQueryFeatureList(self):
        return self.__entryQueryFeatureList

    def getBtnQueryFeatureList(self):
        return self.__btnQueryFeatureList

    def getLbListFeatureSelect(self):
        return self.__lbListFeatureSelect

    def getLbListFeatureResponses(self):
        return self.__lbListFeatureResponses

    def getBtnConfirmFeatureSelect(self):
        return self.__btnConfirmFeatureSelect

    def getBtnResetFeatureSelect(self):
        return self.__btnResetFeatureSelect
    # endregion feature select

    # region confirmed features
    def getLbListConfirmedFeatures(self):
        return self.__lbListConfirmedFeatures

    def getLbListConfirmedResponses(self):
        return self.__lbListConfirmedResponses

    def getBtnConfirmConfirmedFeatures(self):
        return self.__btnConfirmConfirmedFeatures

    def getBtnResetConfirmedFeatures(self):
        return self.__btnResetConfirmedFeatures
    # endregion confirmed features

    # endregion GETTERS


    """UPDATERS"""
    # region feature select updaters
    def clearLbListFeatureSelect(self):
        self.getLbListFeatureSelect().delete(0, END)

    def clearLbListFeatureResponses(self):
        self.getLbListFeatureResponses().delete(0, END)

    def updateLbListFeatureSelect(self, dictContents):
        self.clearLbListFeatureSelect()

        featureIDs = dictContents.keys()
        for featureID in featureIDs:
            entry = "  " + str(featureID) + "  -  " + str(dictContents[featureID][key.DESCRIPTION])
            self.getLbListFeatureSelect().insert(END, str(entry))

    def updateLbListFeatureResponses(self, dictResponses):
        self.clearLbListFeatureResponses()

        responseIDs = dictResponses.keys()
        for responseID in responseIDs:
            entry = "  " + str(responseID) + "  -  " + str(dictResponses[responseID][key.DESCRIPTION])
            self.getLbListFeatureResponses().insert(END, str(entry))
    # endregion feature select updaters

    # region confirmed features updaters
    def clearLbListConfirmedFeatures(self):
        self.getLbListConfirmedFeatures().delete(0, END)

    def clearLbListConfirmedFeatureResponses(self):
        self.getLbListConfirmedResponses().delete(0, END)

    def updateLbListConfirmedFeatures(self, dictContents):
        self.clearLbListConfirmedFeatures()
        if len(dictContents) > 0:
            featureIDs = dictContents.keys()
            for featureID in featureIDs:
                entry = "  " + str(featureID) + "  -  " + str(dictContents[featureID][key.DESCRIPTION])
                self.getLbListConfirmedFeatures().insert(END, str(entry))

    def updateLbListConfirmedFeatureResponses(self, dictResponses):
        self.clearLbListConfirmedFeatureResponses()

        responseIDs = dictResponses.keys()
        for responseID in responseIDs:
            entry = "  " + str(responseID) + "  -  " + str(dictResponses[responseID][key.DESCRIPTION])
            self.getLbListConfirmedResponses().insert(END, str(entry))

    # endregion confirmed features updaters