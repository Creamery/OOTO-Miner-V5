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
import KEYS_support as key


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

        FS.redraw(self.lfTabParentFrame)
        self.lfProcessFrame.place(width = 0, height = 0)
        self.lfResultsFrame.place(width = 0, height = 0)
        # self.lfConsoleFrame.place(width = 0, height = 0)

        self.configureSeparators(parentFrame)
        self.updateFS()


        # print "After HEIGHT: " + str(self.lfCommandsFeatureSelect.place_info())
        # print "After HEIGHT: " + str(self.lfCommandsFeatureSelect.winfo_height())

        # self.configureTestTabElements(parentFrame)
        # self.configureZTestElements(parentFrame)
        # self.configureTestTabConsoleElements(parentFrame)

    def updateFS(self):
        FS.headerWidth = self.lblHeaderFeatureSelect.winfo_width()
        FS.headerHeight = self.lblHeaderFeatureSelect.winfo_height()

        FS.stripeWidth = self.lblStripesQueryFeatureSelect.winfo_width()
        FS.stripeHeight = self.lblStripesQueryFeatureSelect.winfo_height()

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


    def configureSeparators(self, parentFrame):
        parentFrame.update()

        borderX = self.lfConsoleFrame.winfo_x()
        borderHeight = self.lfConsoleFrame.winfo_height()

        FS.emborder(parentFrame,
                    borderX, 0, 1, borderHeight,
                    [False, False, False, True])


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
        self.lfConfirmedFeatures = FS.copyWidget(self.lfFeatureSelect, inputFrame)
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

        self.lblHeaderConfirmedFeatures['text'] = 'SELECTED FEATURES'
        self.lblCountConfirmedFeaturesText.place(
            relx = 0, rely = 0,
            x = - 1, y = - 1)
        FS.placeBelow(self.lblCountConfirmedFeaturesTitle, self.lblCountConfirmedFeaturesText)
        FS.alignStart(self.lblCountConfirmedFeaturesTitle, self.lblCountConfirmedFeaturesText, -1)

    """
    Track FeatureSelect widgets to be assigned to ConfirmedFeatures widgets.
    You must call applyTracked<...>Widgets afterwards.
    """
    def getTrackedConfirmedFeaturesWidgets(self):
        trackedWidgets = {
            repr(self.btnConfirmFeatureSelect): 0,
            repr(self.btnResetFeatureSelect): 1,
            repr(self.btnQueryFeatureList): 2,
            repr(self.lbListFeatureSelect): 3,
            repr(self.lbListFeatureDetails): 4,
            repr(self.lblCountFeatureSelectText): 5,
            repr(self.entryQueryFeatureList): 6,
            repr(self.lblHeaderFeatureSelect): 7,
            repr(self.lblCountFeatureSelectTitle): 8
        }
        trackedVariableList = [
            self.btnConfirmConfirmedFeatures,
            self.btnResetConfirmedFeatures,
            self.btnQueryConfirmedFeatures,
            self.lbListConfirmedFeatures,
            self.lbListConfirmedDetails,
            self.lblCountConfirmedFeaturesText,
            self.entryQueryConfirmedFeatures,
            self.lblHeaderConfirmedFeatures,
            self.lblCountConfirmedFeaturesTitle
        ]
        return trackedWidgets, trackedVariableList

    """
    Sets the variable values to the widget assignment
    (Since the widgets are placed in a list in order to be updated).
    """
    def applyTrackedConfirmedFeaturesWidgets(self):
        self.btnConfirmConfirmedFeatures = self.btnConfirmConfirmedFeatures[0]
        self.btnResetConfirmedFeatures = self.btnResetConfirmedFeatures[0]
        self.btnQueryConfirmedFeatures = self.btnQueryConfirmedFeatures[0]
        self.lbListConfirmedFeatures = self.lbListConfirmedFeatures[0]
        self.lbListConfirmedDetails = self.lbListConfirmedDetails[0]
        self.lblCountConfirmedFeaturesText = self.lblCountConfirmedFeaturesText[0]
        self.entryQueryConfirmedFeatures = self.entryQueryConfirmedFeatures[0]
        self.lblHeaderConfirmedFeatures = self.lblHeaderConfirmedFeatures[0]
        self.lblCountConfirmedFeaturesTitle = self.lblCountConfirmedFeaturesTitle[0]


    def createConfirmedFeatures(self, parentFrame, reference, trackedWidgets, trackedVariableList):
        reference.update()
        for item in reference.winfo_children():
            itemClone = FS.copyWidget(item, parentFrame)

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
        FS.redraw(parentFrame)

        # region extend lfFeatureList
        height = 165 # self.lfCommandsFeatureSelect.winfo_height() * 5
        partialTopHeight = 80
        partialBottomHeight = height - partialTopHeight

        parentFrame.place(height = parentFrame.winfo_height() + height)

        self.lfFeatureSelect.place(height = self.lfFeatureSelect.winfo_height() + height)

        self.lfListFeatureSelect.place(
            height = self.lfListFeatureSelect.winfo_height() + partialTopHeight)

        self.lbListFeatureSelect.place(y = self.lbListFeatureSelect.winfo_y(),
                                       height = self.lbListFeatureSelect.winfo_height() + partialTopHeight)

        self.lfCommandsFeatureSelect.place(y = self.lfCommandsFeatureSelect.winfo_y() + height)


        # endregion extend lfFeatureList

        # region create lfListFeatureDetails
        FS.redraw(parentFrame)
        self.lfListFeatureDetails, self.lbListFeatureDetails, self.lblHeaderFeatureDetails = self.createFeatureDetails(self.lfFeatureSelect,
                                                                                         self.lfListFeatureSelect,
                                                                                         partialBottomHeight)
        FS.redraw(parentFrame)
        self.lfListFeatureSelect.place(
            y = self.lfListFeatureSelect.winfo_y(),
            height = self.lfListFeatureSelect.winfo_height()
        )
        # endregion create lfListFeatureDetails

        # region emborder lfListFeatureDetails
        FS.redraw(parentFrame)
        borderX = self.lfListFeatureDetails.winfo_x()
        borderY = self.lfListFeatureSelect.winfo_y() + self.lfListFeatureSelect.winfo_height()
        borderW = self.lfListFeatureDetails.winfo_width()
        borderH = self.lfListFeatureDetails.winfo_height()
        FS.emborder(self.lfFeatureSelect,
                      borderX, borderY, borderW, borderH,
                      [True, True, False, True],
                      [None, CS.DEFAULT_LIGHT_BORDER, None, CS.DEFAULT_BORDER])
        # endregion emborder lfListFeatureDetails


        # region emborder lfCommandsFeatureSelect
        FS.redraw(parentFrame)
        borderX = self.lfListFeatureDetails.winfo_x()
        borderY = self.lfListFeatureDetails.winfo_y() + self.lfListFeatureDetails.winfo_height()
        borderW = self.lfListFeatureSelect.winfo_width()
        borderH = self.lfFeatureSelect.winfo_height() - borderY
        FS.emborder(self.lfFeatureSelect, borderX, borderY, borderW, borderH)
        # endregion emborder

        # region adjust counter
        FS.redraw(parentFrame)
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

        FS.redraw(parentFrame)

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
        lblHeaderFeatureDetails.place(
            x = 0, y = 1,
            width = referenceFrame.winfo_width(), height = self.lblHeaderFeatureSelect.winfo_height())
        lblHeaderFeatureDetails.configure(
            background = CS.SELECT_LISTBOX_STATUS_BG, foreground = CS.SELECT_LISTBOX_STATUS_FG,
            bd = UI_support.SELECT_STATUS_LABEL_BORDER, relief = UI_support.SELECT_STATUS_LABEL_RELIEF,
            text = 'OPTIONS',
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )
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

        self.lblHeaderFeatureSelect = Label(self.lfHeaderFeatureSelect)  # TODO getter
        # region init lblHeaderFeatureSelect
        self.lblHeaderFeatureSelect.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

        self.lblHeaderFeatureSelect.configure(
            background = CS.SELECT_LISTBOX_STATUS_BG, foreground = CS.SELECT_LISTBOX_STATUS_FG,
            bd = UI_support.SELECT_STATUS_LABEL_BORDER, relief = UI_support.SELECT_STATUS_LABEL_RELIEF,
            text = 'FEATURE LIST',
            font = UI_support.SELECT_STATUS_LABEL_FONT,
        )
        if UI_support.SELECT_STATUS_LABEL_TOP_SEPARATOR:
            sepStatusHorizontal = ttk.Separator(self.lblHeaderFeatureSelect,
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

        self.entryQueryFeatureList = Entry(self.lfQueryFeatureSelect)  # TODO getter
        # region init entryQueryFeatureList
        self.entryQueryFeatureList.place(
            relx = newRelX, rely = 0,
            relwidth = UI_support.TAB_TEST_SELECT_ENTRY_REL_W, relheight = 1)
        self.entryQueryFeatureList.configure(
            background = CS.SELECT_ENTRY_BG, foreground = CS.SELECT_ENTRY_FG,
            bd = 1,
            font = UI_support.ENTRY_FONT, insertwidth = UI_support.INSERT_WIDTH,
            selectbackground = CS.SELECT_ENTRY_SELECT_HIGHLIGHT_BG,
            insertbackground = CS.SELECT_ENTRY_SELECT_INSERT_BG,
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
            background = CS.SELECT_BUTTONS_BG, foreground = CS.SELECT_BUTTONS_FG,
            activebackground = CS.SELECT_BG,
            highlightthickness = 0, padx = 0, pady = 0,
            bd = 0, relief = FLAT, overrelief = GROOVE
        )
        # endregion init btnQueryFeatureList

        self.lbListFeatureSelect = Listbox(self.lfListFeatureSelect)  # TODO getter
        # region init lbListFeatureSelect
        self.lbListFeatureSelect.configure(
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
        self.lbListFeatureSelect.place(relx = 0, rely = newRelY, relwidth = 1, relheight = newRelH)

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

        self.btnResetFeatureSelect = Button(self.lfCommandsFeatureSelect)  # TODO getter
        # region init btnResetFeatureSelect
        self.btnResetFeatureSelect.place(
            relx = 0, rely = 0,
            relwidth = 0.25, relheight = 1)
        self.btnResetFeatureSelect.configure(
            background = CS.SELECT_BG, foreground = CS.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)

        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_reset_icon = PIL.ImageTk.PhotoImage(im)
        self.btnResetFeatureSelect.configure(
            image = btn_query_reset_icon)
        self.btnResetFeatureSelect.image = btn_query_reset_icon  # < ! > Required to make images appear

        newRelX = FS.getRelX(self.btnResetFeatureSelect) + FS.getRelW(self.btnResetFeatureSelect)

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


        self.btnConfirmFeatureSelect = Button(self.lfCommandsFeatureSelect, compound = CENTER)  # TODO getter
        # region init btnConfirmFeatureSelect
        self.btnConfirmFeatureSelect.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.25 - 0.005, relheight = 1
        )

        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_filter_icon = PIL.ImageTk.PhotoImage(im)
        self.btnConfirmFeatureSelect.configure(
            image = btn_query_filter_icon)
        self.btnConfirmFeatureSelect.image = btn_query_filter_icon  # < ! > Required to make images appear

        self.btnConfirmFeatureSelect.configure(
            background = CS.SELECT_BG, foreground = CS.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        self.btnConfirmFeatureSelect.pack(side = RIGHT)
        self.btnResetFeatureSelect.pack(side = LEFT)

        """
        newRelX = FS.getRelX(self.lfCountConfirmedFeatures) + FS.getRelW(self.lfCountConfirmedFeatures)
        # endregion init btnConfirmFeatureSelect

        self.btnConfirmConfirmedFeatures = Button(self.lfCommandsConfirmedFeatures, compound = CENTER)  # TODO getter
        # region init btnConfirmConfirmedFeatures
        self.btnConfirmConfirmedFeatures.place(
            relx = newRelX + 0.005, rely = 0,
            relwidth = 0.25 - 0.005, relheight = 1
        )

        im = PIL.Image.open(Icon_support.TAB_ICO_CHECK).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_query_filter_icon = PIL.ImageTk.PhotoImage(im)
        self.btnConfirmConfirmedFeatures.configure(
            image = btn_query_filter_icon)
        self.btnConfirmConfirmedFeatures.image = btn_query_filter_icon  # < ! > Required to make images appear

        self.btnConfirmConfirmedFeatures.configure(
            background = CS.SELECT_BG, foreground = CS.FG_COLOR,
            bd = 1, relief = FLAT, overrelief = FLAT)
        self.btnConfirmConfirmedFeatures.pack(side = RIGHT)
        self.btnResetConfirmedFeatures.pack(side = LEFT)
        # endregion init btnConfirmConfirmedFeatures
        """


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
            background = CS.PROCESS_BG, foreground = CS.FG_COLOR  # , text = '''PROCESS'''
        )

        self.configureProcessElements(resultsFrame)  # Configures all sub elements under FILTER
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
        self.testTabLeftSeparator = ttk.Separator(parentFrame, orient = VERTICAL)
        self.testTabLeftSeparator.place(relx = 0, rely = 0, relheight = 1)
        return consoleFrame


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
            background = CS.D_BLUE, foreground = CS.FG_COLOR
        )


    ''' -> Elements under the FILTER ("FILTER") HEADER <- '''

    def configureFilterElements(self, parentFrame):
        titleFrame = self.createTitleBar(parentFrame, '2', 'PROCESS', CS.FILTER_TITLE_BG)
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
            background = CS.FILTER_LISTBOX_FEATURE_STATUS_BG,
            foreground = CS.FILTER_LISTBOX_FEATURE_STATUS_FG,
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
            background = CS.FILTER_BG
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
            background = CS.FILTER_BG
        )

        # FILTER QUERY LABEL
        # region
        self.labelFrameBorderQueryFeature = LabelFrame(self.labelFrameFilterQueryData, bd = 0)
        self.labelFrameBorderQueryFeature.place(
            relx = 0, rely = 0,
            relwidth = UI_support.TAB_TEST_FILTER_QUERY_LBL_REL_W, relheight = 1)
        self.labelFrameBorderQueryFeature.configure(
            background = CS.FILTER_BUTTONS_BG
        )

        self.labelQueryFeature = Label(self.labelFrameBorderQueryFeature)
        self.labelQueryFeature.place(
            relx = 0.01, rely = 0.025,
            relwidth = 0.98, relheight = 0.95)
        self.labelQueryFeature.configure(
            background = CS.FILTER_LABEL_BG, foreground = CS.FILTER_LABEL_FG,
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
            background = CS.FILTER_ENTRY_BG, foreground = CS.FILTER_ENTRY_FG,
            bd = 1,
            font = UI_support.ENTRY_FONT, insertwidth = UI_support.INSERT_WIDTH,
            selectbackground = CS.FILTER_ENTRY_SELECT_HIGHLIGHT_BG,
            insertbackground = CS.FILTER_ENTRY_SELECT_INSERT_BG,
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
            background = CS.FILTER_BUTTONS_BG, foreground = CS.FILTER_BUTTONS_FG,
            activebackground = CS.SELECT_BTN_BG_ACTIVE,
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
            background = CS.FILTER_BG
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
            background = CS.FILTER_LISTBOX_BG, foreground = CS.FILTER_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = CS.FILTER_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = CS.FILTER_LISTBOX_SELECTED_ITEM_FG,
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
            background = CS.FILTER_LISTBOX_STATUS_BG, foreground = CS.FILTER_LISTBOX_STATUS_FG,
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
            background = CS.FILTER_BG
        )

        # FILTER LIST BOX - DATASET B

        self.listQueryDataB = Listbox(self.labelFrameFilterListDataB, bd = 0)
        self.listQueryDataB.place(
            relx = UI_support.TAB_TEST_FILTER_LISTBOX_LIST_REL_X, rely = FS.getRelY(self.listQueryDataA),
            relwidth = UI_support.TAB_TEST_FILTER_LISTBOX_LIST_REL_W,
            relheight = FS.getRelH(self.listQueryDataA))

        self.listQueryDataB.configure(
            background = CS.FILTER_LISTBOX_BG, foreground = CS.FILTER_LISTBOX_FG,
            selectmode = MULTIPLE, exportselection = "0",
            activestyle = "none",
            selectbackground = CS.FILTER_LISTBOX_SELECTED_ITEM_BG,
            selectforeground = CS.FILTER_LISTBOX_SELECTED_ITEM_FG,
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
            background = CS.FILTER_LISTBOX_STATUS_BG, foreground = CS.FILTER_LISTBOX_STATUS_FG,
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
        self.separatorFilterListDataA.configure(background = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)

        self.separatorFilterListDataCenter = Label(self.labelFrameFilterListDataB)
        self.separatorFilterListDataCenter.place(relx = 0, rely = 0, relheight = 1, width = 1)
        self.separatorFilterListDataCenter.configure(background = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)

        self.separatorFilterListDataB = Label(self.labelFrameFilterListDataB)
        self.separatorFilterListDataB.place(relx = 0.997, rely = 0, relheight = 1, width = 1)
        self.separatorFilterListDataB.configure(background = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)

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
            foreground = CS.FILTER_LABEL_OVERLAY_BG,
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
            background = CS.FILTER_LISTBOX_OVERLAY_BG,
            foreground = CS.FILTER_LABEL_OVERLAY_FG,
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
            background = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG,
            foreground = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_FG,
            bd = self.labelQueryDataA['bd'], relief = UI_support.FILTER_STATUS_LABEL_RELIEF,
            text = UI_support.FILTER_STATUS_NO_DATA_TEXT,
            font = UI_support.FILTER_STATUS_LABEL_FONT,
        )

        self.separatorOverlayFilterListDataA = Label(self.labelOverlayFilterListDataA)
        self.separatorOverlayFilterListDataA.place(relx = 0, rely = 0, relheight = 1, width = 1)
        self.separatorOverlayFilterListDataA.configure(
            background = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)


        # RIGHT COVER
        self.labelOverlayFilterListDataB = Label(self.labelOverlayFilterListData)
        self.labelOverlayFilterListDataB.place(
            relx = FS.getRelX(self.labelFrameFilterListDataB), rely = FS.getRelY(self.labelOverlayFilterListDataA),
            relwidth = FS.getRelW(self.labelFrameFilterListDataB),
            relheight = FS.getRelH(self.labelOverlayFilterListDataA))
        self.labelOverlayFilterListDataB.configure(
            background = CS.FILTER_LISTBOX_OVERLAY_BG,
            foreground = CS.FILTER_LABEL_OVERLAY_FG,
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
            background = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG,
            foreground = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_FG,
            bd = self.labelQueryDataA['bd'], relief = UI_support.FILTER_STATUS_LABEL_RELIEF,
            text = UI_support.FILTER_STATUS_NO_DATA_TEXT,
            font = UI_support.FILTER_STATUS_LABEL_FONT,
        )
        # self.separatorOverlayFilterListDataB1 = ttk.Separator(self.labelOverlayFilterListDataB, orient = VERTICAL)
        # self.separatorOverlayFilterListDataB1.place(relx = 0, rely = 0, relheight = 1)
        self.separatorOverlayFilterListDataCenter = Label(self.labelOverlayFilterListDataB)
        self.separatorOverlayFilterListDataCenter.place(relx = 0, rely = 0, relheight = 1, width = 1)
        self.separatorOverlayFilterListDataCenter.configure(
            background = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)

        self.separatorOverlayFilterListDataB = Label(self.labelOverlayFilterListDataB)
        self.separatorOverlayFilterListDataB.place(relx = 0.997, rely = 0, relheight = 1, width = 1)
        self.separatorOverlayFilterListDataB.configure(
            background = CS.FILTER_LISTBOX_STATUS_READY_OVERLAY_BG)


    ''' -> Elements under the PROCESS ("TEST") HEADER <- '''

    def configureProcessElements(self, parentFrame):

        titleFrame = self.createTitleBar(parentFrame, '3', 'RESULTS', CS.PROCESS_TITLE_BG)
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
            background = CS.PROCESS_BG
        )

        # PROCESS STATISTICAL TEST OPTIONS
        self.labelFrameProcessStatTests = LabelFrame(self.labelFrameProcessCommands, bd = 0)
        self.labelFrameProcessStatTests.place(
            relx = 0, rely = 0,
            relwidth = UI_support.TEST_PROCESS_Z_TEST_PARENT, relheight = 1
        )

        self.labelFrameProcessStatTests.configure(
            background = CS.PROCESS_BG
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
            background = CS.PROCESS_Z_TEST_TITLE_BG, foreground = CS.PROCESS_Z_TEST_TITLE_FG,
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
            background = CS.PROCESS_BG
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
            background = CS.D_BLUE, foreground = CS.WHITE,
            activebackground = CS.PROCESS_Z_TEST_TITLE_BG,
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
            background = CS.WHITE, foreground = CS.D_BLUE,
            activebackground = CS.PROCESS_Z_TEST_TITLE_BG,
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
            background = CS.PROCESS_BG
        )

        self.labelFrameProcessTestOptionsTitle = Label(self.labelFrameProcessTestOptions)
        self.labelFrameProcessTestOptionsTitle.place(
            relx = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_X,
            rely = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y,
            relwidth = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H)
        self.labelFrameProcessTestOptionsTitle.configure(
            font = UI_support.FONT_MED_BOLD,
            background = CS.PROCESS_Z_TEST_TITLE_BG, foreground = CS.PROCESS_Z_TEST_TITLE_FG,
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
            background = CS.PROCESS_BG
        )

        self.labelFrameProcessZTestTitle = Label(self.labelFrameProcessZTest)
        self.labelFrameProcessZTestTitle.place(
            relx = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_X,
            rely = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y,
            relwidth = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_W,
            relheight = UI_support.TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H)
        self.labelFrameProcessZTestTitle.configure(
            font = UI_support.FONT_MED_BOLD,
            background = CS.PROCESS_Z_TEST_TITLE_BG, foreground = CS.PROCESS_Z_TEST_TITLE_FG,
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
            background = CS.PROCESS_BG
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
            background = CS.PROCESS_BG
        )

        # CONFIDENCE SPINBOX LABEL
        self.labelQueryZConfidenceText = Label(self.labelFrameProcessZTestConfidence)
        self.labelQueryZConfidenceText.place(
            relx = 0, rely = 0,
            relwidth = 1, relheight = UI_support.TAB_TEST_PROCESS_CONFIDENCE_TEXT_REL_H)
        self.labelQueryZConfidenceText.configure(
            font = UI_support.FONT_DEFAULT_BOLD,
            background = CS.FG_COLOR, foreground = CS.SELECT_BG,
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
            background = CS.WHITE, foreground = CS.FG_COLOR,
            exportselection = 0,
            buttonbackground = CS.WHITE,
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
            background = CS.PROCESS_BG, foreground = CS.PROCESS_BUTTONS_FG,
            activebackground = CS.PROCESS_TITLE_BG,
            highlightbackground = CS.PROCESS_TITLE_BG,
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
            background = CS.PROCESS_BG
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
            background = CS.PROCESS_CHI_SQUARE_TITLE_BG,
            foreground = CS.PROCESS_CHI_SQUARE_TITLE_FG,

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
            background = CS.PROCESS_BG
        )

        # QUEUE ELEMENTS
        self.labelFrameProcessChiSquareQueue = LabelFrame(self.labelFrameProcessChiSquareElements, bd = 1)
        self.labelFrameProcessChiSquareQueue.place(
            relx = 0.275, rely = 0,
            relwidth = 0.45, relheight = 1
        )
        self.labelFrameProcessChiSquareQueue.configure(
            background = CS.PROCESS_BG
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
            background = CS.FG_COLOR, foreground = CS.SELECT_BG,
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
            background = CS.SELECT_BG,
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
            background = CS.PROCESS_BG
        )

        # Enqueue button
        self.buttonQueue = Button(self.labelFrameProcessQueue, compound = CENTER)

        im = PIL.Image.open(Icon_support.TAB_ICO_ADD).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_queue_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonQueue.configure(
            image = btn_queue_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonQueue.image = btn_queue_icon  # < ! > Required to make images appear

        self.buttonQueue.configure(
            background = CS.PROCESS_BG, foreground = CS.FG_COLOR,
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
            background = CS.PROCESS_BG
        )

        self.buttonClearQueue = Button(self.labelFrameProcessClearQueue, compound = CENTER)

        im = PIL.Image.open(Icon_support.TAB_ICO_CROSS).resize(Icon_support.SELECT_ICO_SIZE, PIL.Image.ANTIALIAS)
        btn_clear_queue_icon = PIL.ImageTk.PhotoImage(im)
        self.buttonClearQueue.configure(
            image = btn_clear_queue_icon)  # , width = self.buttonQueryAddFilterA.winfo_reqheight())
        self.buttonClearQueue.image = btn_clear_queue_icon  # < ! > Required to make images appear

        self.buttonClearQueue.configure(
            background = CS.PROCESS_BG, foreground = CS.FG_COLOR,
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
            background = CS.PROCESS_BG
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
            background = CS.D_BLUE, foreground = CS.WHITE,
            # background = CS.PROCESS_RUN_MINER_TITLE_BG, foreground = CS.PROCESS_RUN_MINER_TITLE_FG,
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
            background = CS.PROCESS_BG
        )
        self.labelFrameRunMinerElements = LabelFrame(self.labelFrameRunMiner, bd = 0)
        self.labelFrameRunMinerElements.place(
            relx = 0, rely = 0,
            relwidth = 1, relheight = 1
        )
        self.labelFrameRunMinerElements.configure(
            background = CS.PROCESS_BG
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
            background = CS.PROCESS_BUTTONS_BG, foreground = CS.PROCESS_BUTTONS_FG,
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
        return self.btnQueryConfirmedFeatures

    def getButtonQueryAddFilterA(self): # TODO remove getter
        return self.btnConfirmFeatureSelect
    def getButtonQueryAddFilterB(self):
        return self.btnConfirmConfirmedFeatures

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

    def getButtonQueryResetFilterA(self): # TODO remove getter
        return self.btnResetFeatureSelect
    def getButtonQueryResetFilterB(self):
        return self.btnResetConfirmedFeatures

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
        return self.lblHeaderFeatureSelect
    def getLabelQuerySetDataStatusB(self):
        return self.lblStatusConfirmedFeatures

    def getLabelQuerySetDataStripesA(self):
        return self.lblStripesQueryFeatureSelect
    def getLabelQuerySetDataStripesB(self):
        return self.lblStripesConfirmedFeatures

    def getLabelQueryDataACount(self):
        return self.lblCountFeatureSelectText
    def getLabelQueryDataBCount(self):
        return self.lblCountConfirmedFeaturesText

    def getEntryQuerySetDataA(self):
        return self.entryQueryFeatureList
    def getEntryQuerySetDataB(self):
        return self.entryQueryConfirmedFeatures

    def getListQuerySetDataA(self):
        return self.lbListFeatureSelect
    def getListQuerySetDataB(self):
        return self.lbListConfirmedFeatures

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


    # NEW GETTERS
    def getBtnConfirmFeatureSelect(self):
        return self.btnConfirmFeatureSelect

    def getBtnResetFeatureSelect(self):
        return self.btnResetFeatureSelect

    def getBtnQueryFeatureList(self):
        return self.btnQueryFeatureList

    def getLbListFeatureSelect(self):
        return self.lbListFeatureSelect

    def getLbListFeatureDetails(self):
        return self.lbListFeatureDetails

    def getEntryQueryFeatureList(self):
        return self.entryQueryFeatureList


    def getBtnConfirmConfirmedFeatures(self):
        return self.btnConfirmConfirmedFeatures
    # endregion GETTERS


    """UPDATERS"""
    def updateLbListFeatureSelect(self, dictContents):
        self.getLbListFeatureSelect().delete(0, END)

        featureIDs = dictContents.keys()
        for featureID in featureIDs:
            entry = "  " + str(featureID) + "  -  " + str(dictContents[featureID][key.DESCRIPTION])
            self.getLbListFeatureSelect().insert(END, str(entry))

    def updateLbListFeatureDetails(self, dictResponses):
        self.getLbListFeatureDetails().delete(0, END)

        responseIDs = dictResponses.keys()
        for responseID in responseIDs:
            entry = "  " + str(responseID) + "  -  " + str(dictResponses[responseID][key.DESCRIPTION])
            self.getLbListFeatureDetails().insert(END, str(entry))
