
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"

'''
    This script contains various functions that help in
    UI widget placement.
    [Candy]
'''
import sys
import tkinter as tk
from tkinter.ttk import *
from ctypes import windll

import PIL.Image
import PIL.ImageTk

import _Color_support as CS
import _UI_support as US
import _Icon_support as IS
import Function_support as FS

from Keys_support import Dataset as KSD
from Keys_support import SSF as KSS
from CONSTANTS import SYSTEMATIC_FILTERING as CSF

import ChiTest as CHI

from collections import OrderedDict
import itertools
import pandas as pd
from itertools import combinations
from itertools import islice

GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

""" CREATORS """
# region creator functions

def createDefaultToplevelWindow(root, placeInfo = [800, 600],
                                isOverrideRedirect = True, isTaskbar = True):
    top = tk.Toplevel(root)

    # remove title bar
    top.overrideredirect(isOverrideRedirect)
    if isTaskbar:
        top.after(10, lambda: showInTaskBar(top))

    top.transient(root)
    top.grab_set()

    # top.protocol("WM_DELETE_WINDOW", onTopClose)  # TODO return this
    top.resizable(0, 0)

    top.style = Style()
    if sys.platform == "win32":
        top.style.theme_use('winnative')

    top.style.configure('.', font = "TkDefaultFont")

    # center window
    strDimensions = str(placeInfo[0]) + "x" + str(placeInfo[1])
    top.geometry(strDimensions)
    root.update()
    newX, newY = FS.centerWindow(top, root, 0, -FS.gripHeight)
    top.geometry(strDimensions + "+" + str(int(newX)) + "+" + str(int(newY)))

    return top


def createOverlayWindow(root, gripHeightOffset = 0, bgColor = CS.BLACK):
    wX = root.winfo_x()
    wY = root.winfo_y()
    wWidth = root.winfo_width()
    wHeight = root.winfo_height() + gripHeightOffset

    # print "x y is " + str(wX) + " and " + str(wY)
    top = createDefaultToplevelWindow(root, [wWidth, wHeight], True, False)
    top.wm_attributes('-alpha', 0.7)

    label = tk.Label(top)
    label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
    label.configure(background = bgColor)

    strDimensions = str(wWidth) + "x" + str(wHeight)
    root.update()
    top.geometry(strDimensions + "+" + str(wX) + "+" + str(wY))

    return top


def createDefaultFrame(parentFrame, placeInfo = [0, 0, 1, 1],
                       isRelative = [True, True], bgColor = CS.WHITE, fgColor = CS.D_BLUE):
    wX = placeInfo[0]
    wY = placeInfo[1]
    wWidth = placeInfo[2]
    wHeight = placeInfo[3]

    lfFrame = tk.LabelFrame(parentFrame, bd = 0)
    lfFrame.place(x = wX, y = wY,)

    # region relative conditions
    if isRelative[0]:  # width is relative
        lfFrame.place(relwidth = wWidth)
    else:
        lfFrame.place(width = wWidth)

    if isRelative[1]:  # height is relative
        lfFrame.place(relheight = wHeight)
    else:
        lfFrame.place(height = wHeight)
    # endregion relative conditions


    lfFrame.configure(
        background = bgColor, foreground = fgColor,
        relief = tk.FLAT)

    lfFrame.update()

    return lfFrame


def createDefaultHeader(parentFrame, wText = "", placeInfo = [0, 0, 1, 1],
                        isRelative = [True, True], bgColor = CS.D_BLUE, fgColor = CS.WHITE,
                        wFont = US.FONT_DEFAULT_BOLD):
    wX = placeInfo[0]
    wY = placeInfo[1]
    wWidth = placeInfo[2]
    wHeight = placeInfo[3]

    lblHeader = tk.Label(parentFrame)

    lblHeader.place(x = wX, y = wY,)
    # region relative conditions
    if isRelative[0]:  # width is relative
        lblHeader.place(relwidth = wWidth)
    else:
        lblHeader.place(width = wWidth)

    if isRelative[1]:  # height is relative
        lblHeader.place(relheight = wHeight)
    else:
        lblHeader.place(height = wHeight)
    # endregion relative conditions

    lblHeader.configure(
        background =bgColor, foreground = fgColor,
        bd = 0, relief = tk.FLAT,
        text = wText,
        font = wFont,
    )

    lblHeader.update()
    return lblHeader


def createDefaultListbox(parentFrame,
                         selectMode = tk.SINGLE,
                         placeInfo = [0,0,1,1],
                         isRelative = [True, True],
                         bg = CS.PALER_YELLOW,
                         bgSelect = CS.PALE_PLUM,
                         fg = CS.D_BLUE,
                         fgSelect = CS.D_BLUE):
    wX = placeInfo[0]
    wY = placeInfo[1]
    wWidth = placeInfo[2]
    wHeight = placeInfo[3]

    listbox = tk.Listbox(parentFrame)
    listbox.place(x = wX, y = wY)
    # region relative conditions
    if isRelative[0]: # width is relative
        listbox.place(relwidth = wWidth)
    else:
        listbox.place(width = wWidth)

    if isRelative[1]: # height is relative
        listbox.place(relheight = wHeight)
    else:
        listbox.place(height = wHeight)
    # endregion relative conditions

    listbox.configure(
        background = bg, foreground = fg,
        selectmode = selectMode, exportselection = "0",
        activestyle = "none",
        selectbackground = bgSelect,
        selectforeground = fgSelect,
        font = US.SELECT_LABEL_FONT,
        bd = 0,
        relief = tk.GROOVE,
        highlightthickness = 0
    )

    listbox.update()
    return listbox


def createDefaultStripe(parentFrame, placeInfo = [0,0,1,1],
                        isRelative = [True, True],
                        texture = IS.TEXTURE_STRIPE_GREY):
    wX = placeInfo[0]
    wY = placeInfo[1]
    wWidth = placeInfo[2]
    wHeight = placeInfo[3]

    lblStripes = tk.Label(parentFrame, bd = 0, relief = tk.GROOVE)

    lblStripes.place(x = wX, y = wY,)
    # region relative conditions
    if isRelative[0]:  # width is relative
        lblStripes.place(relwidth = wWidth)
    else:
        lblStripes.place(width = wWidth)

    if isRelative[1]:  # height is relative
        lblStripes.place(relheight = wHeight)
    else:
        lblStripes.place(height = wHeight)
    # endregion relative conditions

    im = PIL.Image.open(texture)
    icoStripes = PIL.ImageTk.PhotoImage(im)
    lblStripes.configure(
        image = icoStripes,
        anchor = tk.SW
    )
    lblStripes.image = icoStripes  # < ! > Required to make images appear

    lblStripes.update()
    return lblStripes


# endregion creator functions

""" UTILITIES """
# region utility functions
""" Returns the widget name """
def getWidgetName(widget):
    return str(widget).split(".")[-1]



""" A recursive call that updates all tk.Widgets and their tk.Widget children """
def redraw(parentFrame):
    parentFrame.update()

    for item in parentFrame.winfo_children():
        # print 'item type is ' + str(type(item))
        item.place(
            relx = 0, rely = 0, relwidth = 0, relheight = 0,
            x = item.winfo_x(), y = item.winfo_y(), width = item.winfo_width(), height = item.winfo_height())
        if isinstance(item, tk.Widget):
            redraw(item)
        else:
            return "break"

    parentFrame.update()


def copyWidget(widget, parent):
    # parent = widget.nametowidget(widget.winfo_parent())

    widgetClass = widget.__class__
    clone = widgetClass(parent)


    # set configuration according to class
    copyWidgetConfiguration(clone, widget)
    return clone

def copyWidgetConfiguration(widget, reference):
    reference.update()
    widget.place(
        x = reference.winfo_x(),
        y = reference.winfo_y(),
        width = reference.winfo_width(),
        height = reference.winfo_height(),
    )

    if isinstance(widget, LabelFrame):
        widget.configure(
            bd = reference['bd'],
            background = reference['background']
        )

    elif isinstance(widget, Label):
        widget.configure(
            font = reference['font'],
            background = reference['background'], foreground = reference['foreground'],
            text = reference['text'],
            bd = reference['bd'], relief = reference['relief'],
            anchor = reference['anchor'],
            image = reference['image'],
        )
        widget.image = reference['image']  # < ! > Required to make images appear

    elif isinstance(widget, Button):
        widget.configure(
            background = reference['background'], foreground = reference['foreground'],
            activebackground = reference['activebackground'],
            highlightthickness = reference['highlightthickness'], padx = reference['padx'], pady = reference['pady'],
            bd = reference['bd'], relief = reference['relief'], overrelief = reference['overrelief'],
            anchor = reference['anchor'],
            image = reference['image']
        )
        widget.image = reference['image']  # < ! > Required to make images appear

    elif isinstance(widget, Entry):
        widget.configure(
            background = reference['background'], foreground = reference['foreground'],
            bd = reference['bd'],
            font = reference['font'], insertwidth = reference['insertwidth'],
            selectbackground = reference['selectbackground'],
            insertbackground = reference['insertbackground'],
            takefocus = reference['takefocus'], justify = reference['justify']
        )

    elif isinstance(widget, tk.Listbox):
        widget.configure(
            background = reference['background'], foreground = reference['foreground'],
            selectmode = reference['selectmode'], exportselection = reference['exportselection'],
            activestyle = reference['activestyle'],
            selectbackground = reference['selectbackground'],
            selectforeground = reference['selectforeground'],
            font =reference['font'],
            bd = reference['bd'],
            relief = reference['relief'],
            highlightthickness = reference['highlightthickness']
        )


def emborder(parentFrame, placeInfo = [0, 0, None, None],
             conditions = [True, True, True, True], colors = [None, None, None, None]):
    # region handle defaults
    borderX = placeInfo[0]
    borderY = placeInfo[1]
    borderW = placeInfo[2]
    borderH = placeInfo[3]
    # use default color if not specified by the user
    colors = [CS.L_GRAY if color is None else color for color in colors]
    # use parentFrame width and height if not specified by the user
    if borderW is None:
        borderW = parentFrame.winfo_width()
    if borderH is None:
        borderH = parentFrame.winfo_height()
    # endregion handle defaults

    borderW = borderW - 1  # done so that the end borders won't get cut off
    borderH = borderH - 1  # done so that the end borders won't get cut off

    index = 0
    if conditions[index]:
        sepCommandTop = tk.Label(parentFrame)
        sepCommandTop.place(
            x = borderX,
            y = borderY,
            width = borderW,
            height = 1)
        sepCommandTop.configure(background = colors[index])

    index = 2
    if conditions[index]:
        sepCommandBottom = tk.Label(parentFrame)
        sepCommandBottom.place(
            x = borderX,
            y = borderY + borderH,
            width = borderW,
            height = 1)
        sepCommandBottom.configure(background = colors[index])

    index = 3
    if conditions[index]:
        sepCommandLeft = tk.Label(parentFrame)
        sepCommandLeft.place(
            x = borderX,
            y = borderY,
            width = 1,
            height = borderH)
        sepCommandLeft.configure(background = colors[index])

    index = 1
    if conditions[index]:
        sepCommandRight = tk.Label(parentFrame)
        sepCommandRight.place(
            x = borderX + borderW,
            y = borderY,
            width = 1,
            height = borderH)
        sepCommandRight.configure(background = colors[index])

""" Make the root window wait until the modal window is closed """
def makeModal(modalWindow, root):
    root.wait_window(modalWindow)  # make the window modal by setting root's wait_window


""" Allows windows to appear in taskbar when overideredirect is set to True """
def showInTaskBar(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

def enterSplashscreen(root):
    root.wm_attributes('-alpha', '0.0')
    # TODO show the window with splash image

def exitSplashscreen(root):
    root.wm_attributes('-alpha', '1.0')
    # TODO hide the window with splash image

# endregion utility functions

""" DICTIONARY FUNCTIONS """
# region dictionary functions
# return an alphabetically sorted ordered dictionary
def AlphabeticalDict(dictionary):
    if isinstance(dictionary, list):
        dictionary = dict(dictionary)

    return OrderedDict(sorted(dictionary.items()))

# returns a merged then alphabetically sorted dictionary
def MergedDict(dictionary1, dictionary2):
    mergedDictionary = dictionary1.copy()
    mergedDictionary.update(dictionary2)

    return AlphabeticalDict(mergedDictionary)

# subtracts dictionary2 from dictionary1 and returns the alphabetically sorted difference
def SubtractedDict(dictionary1, dictionary2):
    subtractedDictionary = {k: v for k, v in dictionary1.items() if k not in dictionary2}
    return AlphabeticalDict(subtractedDictionary)


# return the first n dictionary items

def PrintDictItems(n, dictionary):
    iterable = dictionary.iteritems()
    return list(islice(iterable, n))

# endregion dictionary functions


""" LIST FUNCTIONS """
# region list functions
# keep unique values in a list while preserving order
def unique(inputList):
    seen = set()
    seen_add = seen.add
    return [x for x in inputList if not (x in seen or seen_add(x))]
# endregion list functions

""" SYSTEMATIC FILTERING FUNCTIONS """
# region systematic filtering functions
# returns a dictionary of dictionaries, where each dictionary is an altered key-value pair
# of featureIDs ('s17'), groups ('a'), and codes ([1, 3])
def initializeSSF(salientFeatures):
    SSF = {}
    ssfItems = salientFeatures.items()  # [0] - key, [1] - value

    SSF[KSS.FEATURES] = []
    SSF[KSS.FEAT_GROUP_CODE] = OrderedDict()  # key : featureID, value : group-code dictionary
    SSF[KSS.FEAT_CODE] = OrderedDict()  # key : featureID, value : array of code arrays (by group)
    SSF[KSS.FEAT_GROUP] = OrderedDict()  # key : featureID, value : array of code arrays (by group)
    # SSF[KSS.GROUP_CODE] = OrderedDict()

    FEAT_LIST = SSF[KSS.FEATURES]
    FEAT_GROUP_CODE = SSF[KSS.FEAT_GROUP_CODE]
    FEAT_CODE = SSF[KSS.FEAT_CODE]
    FEAT_GROUP = SSF[KSS.FEAT_GROUP]
    # GROUP_CODE = SSF[KSS.GROUP_CODE]

    for item in ssfItems:
        featureID = item[0]
        featureDetails = item[1]  # Description, Responses
        responseDetails = featureDetails[KSD.RESPONSES].items()  # returns a tuple of response (code)
        responseGroups = [response[0] for response in responseDetails]  # list of possible responses ('a', 'b', 'c')

        FEAT_LIST.append(featureID)
        FEAT_GROUP[featureID] = responseGroups

        # print ('responseGroups : ')
        # print str(responseGroups)

        # prepare FEAT_CODE dictionary
        FEAT_CODE[featureID] = []
        # assign FEAT_CODE dictionary
        for response in responseDetails:
            code = response[1][KSD.CODE]
            FEAT_CODE[featureID].append(code)


        # assign FEAT_GROUP_CODE dictionary where GROUP is a dictionary of group-code pairs
        FEAT_GROUP_CODE[featureID] = dict((group, []) for group in responseGroups)

        # for group in responseGroups:
        for response, group in itertools.izip(responseDetails, responseGroups):
            code = response[1][KSD.CODE]
            FEAT_GROUP_CODE[featureID][group] = code

        FEAT_GROUP_CODE[featureID] = AlphabeticalDict(FEAT_GROUP_CODE[featureID])

    # print "SSF contents:"
    # print str(SSF)

    return SSF


def createFilterPairs(FILTERS, maxLevel = CSF.MAX_LVL):
    FILTER_PAIRS = [[]] * (maxLevel + 1)

    for level in range(1, (maxLevel + 1)):
        FILTER = FILTERS[level]
        FILTER_PAIRS[level] = list(combinations(FILTER, 2))
    return FILTER_PAIRS

""" 1. Initialize SSF - prepares a dictionary with various featID, CODE, and GROUP pairs
    2. Create featureSet (LVLS) for levels 1, 2, and 3 - where a featureSet is the grouping of features acc. to level
    3. Map each feature in LVLS[level] with its corresponding GROUP (e.g. ['a', 'b', 'c'])
    4. Create filterSet for levels 1, 2, and 3 from featureSet
    5. Return FILTERS
"""
def createFilters(SSF, maxLevel = CSF.MAX_LVL):
    level = 1
    LVLS = OrderedDict()

    LVLS[0] = [[]] * len(SSF)  # an empty level

    # print "LVL[0] = "
    # print str(LVLS[0])
    # print "SSF[KSS.FEATURES] = "
    # print str(SSF[KSS.FEATURES])
    # print "SSF[KSS.FEAT_GROUP] = "
    # print str(SSF[KSS.FEAT_GROUP])
    # print "SSF[KSS.FEAT_GROUP_CODE] = "
    # print str(SSF[KSS.FEAT_GROUP_CODE])
    # print "SSF[KSS.FEAT_CODE] = "
    # print str(SSF[KSS.FEAT_CODE])

    # create feature set
    BagOfFeatures = SSF[KSS.FEATURES]
    while level <= maxLevel:
        LVLprev = LVLS[level-1]
        LVLS[level] = createFeatureSet(level, LVLprev, BagOfFeatures)
        level += 1

    # create filter set
    FILTERS = [[]] * (maxLevel + 1)

    for level in range(1, maxLevel + 1):
        # print "level " + str(level)
        LVL = LVLS[level]
        FILTERS[level] = createFilterSet(LVL, SSF[KSS.FEAT_GROUP])  # dict of array of dict, ex: {'level': }

        # print "FILTERS : "
        # print str(FILTERS[level])
    return FILTERS


""" Create the current Feature Set for the given level based on the BagOfFeatures.
    A level = 2 with BagOfFeatures = [a1, a2, a3] will return :
        LVL = [[a1, a2], [a1, a3], [a2, a3]]
"""
def createFeatureSet(level, LVLprev, BagOfFeatures):
    # print "level = " + str(level)
    # print "BagOfFeatures = " + str(BagOfFeatures)

    LVL = []
    lenBOF = len(BagOfFeatures)
    lenLVLprev = len(LVLprev)
    prevLevel = level - 1
    # firstIndex = prevLevel
    # lastIndex = lenBOF - (prevLevel)

    # range is (inclusive, exclusive)
    # for i in range(firstIndex, lastIndex):
    # for each item in the previous LVL
    for i in range(lenLVLprev):
        prevItem = list(LVLprev[i])
        # print "prevItem " + str(prevItem)

        firstIndex = i + prevLevel
        # go over each BOF item
        for j in range(firstIndex, lenBOF):
            item = list(prevItem)
            item.append(BagOfFeatures[j])
            LVL.append(tuple(item))

    # LVL = unique(LVL)  # only maintain unique values (pandas should preserve order)
    tupleLVL = tuple(LVL)  # convert list to tuples to be compatible with pd.unique
    # print "type " + str(type(tupleLVL))
    LVL = pd.unique(tupleLVL)  # only maintain unique values (pandas should preserve order)
    LVL = [list(x) for x in LVL]  # convert LVL to list

    return LVL


""" Creates the filterSet from a given LVL.
    A 'LVL' is one item from the LVLS list (e.g. LVLS[2]).
    A sample LVL is:
        [[a1, a2], [a1, a3], [a2, a3]]
    which is a sample content of LVLS[2].
"""
def createFilterSet(LVL, featureGroupMap):
    filterSet = []  # an array of filters (dict)
    for featureSet in LVL:
        filterSet.extend(createFilter(featureSet, featureGroupMap))

    return filterSet

""" Returns the list of filters from the given featureSet and featureGroupMap.
    Ex: [a1, a2] or [a1, a3]
"""
def createFilter(featureSet, featureGroupMap):

    filters = []
    groupSet = []

    # initialize groupSet array
    for feature in featureSet:
        groupSet.append(featureGroupMap[feature])  # an array of groups, ex: [ [a, b, c], [a, b] ]

    groupSet = list(itertools.product(*groupSet))  # store all the combinations of a list of lists via itertools

    keys = featureSet
    for group in groupSet:
        filter = OrderedDict(zip(keys, group))
        filters.append(filter)

    return filters



# endregion systematic filtering functions


# region chi-test functions
def runChiTest(FILTER_PAIRS, DATASET):
    chiTest = CHI.ChiTest.getInstance()  # Initialize singleton


    # i = 0
    # for FILTER_PAIR in FILTER_PAIRS:
    #     fileNames = []
    #     i += 1
    #     for dataset in test['Datasets']:  # For each sample pairs in queue
    #         FS.convertDatasetValuesToGroups(dataset, features)
    #
    #         print "convertDatasetValuesToGroups : "
    #         print "---- dataset : "
    #         print str(dataset)
    #         print "---- features : "
    #         print str(features)
    #
    #         fileName = FS.makeFileName(
    #             dataset)  # TODO This makes the intermediate tables based on the selected features
    #         # print ("GENERATED FILENAME: " + str(fileName))
    #         FS.writeCSVDict(fileName, dataset['Data'])
    #         fileNames.append(fileName)
    #     if not (os.path.isfile("Updated-Variables.csv")):
    #         FS.makeUpdatedVariables(features, "Updated-Variables.csv")
    #
    #     # saveFile = ct.chiTest(fileNames)
    #     saveFile = chiTest.chiTest(fileNames)
    #     print ("saveFile is " + str(saveFile))
    #
    #     # tempString = "Chi-test complete. " + str(i) + "/" + str(len(tests)) + "complete."
    #     # self.listQueryDataB.insert(END, tempString) #### TODO Put this somewhere else (CONSOLE)
    #     # removeFiles(fileNames) # TODO This removes the intermediate tables

# endregion chi-test functions
