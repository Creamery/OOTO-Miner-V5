#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Feb 26, 2018 12:01:25 PM

"""
{Description}
The runnable script for OOTO Miner
"""

__author__ = ["Arren Antioquia", "Arces Talavera", "Jet Virtusio",
              "Edmund Gerald Cruz", "Rgee Gallega",
              "Candy Espulgar"]

__copyright__ = "Copyright 2019, TE3D House"
__credits__ = ["Arnulfo Azcarraga"]
__version__ = "3.0"


import sys
import csv
import tkMessageBox
from tkFileDialog import askopenfilename
import copy
import SampleVsPopulation as svp
import SampleVsSample as svs
import ChiTest as ct
import os
import numpy as np
from collections import Counter

import Tkinter as tk

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

import math
import Mother_support
import Color_support as CS
import Icon_support as IS
import UI_support as US
import PIL.Image
import PIL.ImageTk

import Grip_support as GS
import Function_support as FS
import Widget_support as WS
import _MODULE_Input as INPUT
import _MODULE_ManualMining as MM
import _MODULE_AutomatedMining as AM

w = None


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root

    root = Tk()
    # root.protocol("WM_DELETE_WINDOW", onRootClose)
    root.resizable(0, 0)
    # Mother_support.set_Tk_var()
    # top = OOTO_Miner(root)
    OOTO_Miner(root)
    # root.update()
    # Mother_support.init(root, top)
    root.mainloop()

# def onRootClose():
#     if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
#         global root
#         root.destroy()
#         root = None



# def create_OOTO_Miner(root, *args, **kwargs):
#     '''Starting point when module is imported by another program.'''
#     global w, w_win, rt
#     rt = root
#     w = Toplevel(root)
#     Mother_support.set_Tk_var()
#     top = OOTO_Miner(w)
#     Mother_support.init(w, top, *args, **kwargs)
#     return (w, top)


# def destroy_OOTO_Miner():
#     global w
#     w.destroy()
#     w = None

class OOTO_Miner:

    def __init__(self, top = None):
        self.top = top
        # Configure style maps / themes
        self.configureStyle(top)



        ''' TAB 1 - DATA (Tabs_t2) '''
        self.INPUT = self.configureDataTabElements(self.Tabs_t2)
        self.INPUT.getButtonStartDatasetUpload().bind('<Button-1>', self.uploadInputFiles)

        ''' TAB 2 - AM (Tabs_t3) '''
        self.MM = self.configureManualMiningTab(self.Tabs_t3)

        # ''' TAB 2.2 TEST CONSOLE - (Tabs_t3)'''
        # self.configureTestTabConsoleElements()

        ''' TAB 3 - AM (Tabs_t5) '''
        self.AM = self.configureAutomatedMiningTab(self.Tabs_t5)

        ''' TAB 4 - INFO (Tabs_t4) '''
        self.configureInfoTabElements()

        # create a draggable label
        self.configureGrip(top)
        # create frame borders
        self.configureBorders(top)



        # Bind functionality to all UI elements
        # self.configureBindings()

        # self.initializeVariables()

        # self.enableFilter() # TODO REMOVE!
        # self.labelQueryDataACount.configure(text = "n: " + str(len(self.datasetA['Data'])))
        # self.labelQueryDataBCount.configure(text = "n: " + str(len(self.datasetB['Data'])))


    def configureGrip(self, parentFrame):
        self.grip = GS.GripLabel(parentFrame, True).getGrip()
        self.grip.update()
        self.Tabs.place(y = self.Tabs.winfo_y() + self.grip.winfo_height())

    def configureBorders(self, parentFrame):
        borderWidth = parentFrame.winfo_width()
        borderHeight = parentFrame.winfo_height()
        borderColor = CS.D_GRAY
        WS.emborder(parentFrame,
                    [0, 0, borderWidth, borderHeight],
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor])

    """ Functions for draggable window """
    # def startWinMove(self, event):
    #     self.gripX = event.x
    #     self.gripY = event.y
    #
    # def stopWinMove(self, event):
    #     self.top.x = None
    #     self.top.y = None
    #
    # def onWinMove(self, event):
    #     deltaX = event.x - self.gripX
    #     deltaY = event.y - self.gripY
    #     x = self.top.winfo_x() + deltaX
    #     y = self.top.winfo_y() + deltaY
    #     self.top.geometry("+%s+%s" % (x, y))


    """ >>> CONFIGURE STYLE MAPS / THEMES <<< """

    # region
    def configureStyle(self, top):

        # remove title bar
        top.overrideredirect(True)
        # show window in taskbar after titlebar is removed
        top.after(10, lambda: FS.showInTaskBar(root))

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        # else:
        #     self.style.theme_use('clam')

        self.style.configure('.', font = "TkDefaultFont")
        # self.style.map('.',background =
        #     [('selected', _compcolor), ('active',_ana2color)])

        strRootWidth = str(FS.rootWidth)
        strRootHeight = str(FS.rootHeight)
        top.geometry(strRootWidth + "x" + strRootHeight)
        newX, newY = FS.centerWindow(top)
        top.geometry(strRootWidth + "x" + strRootHeight + "+" + str(newX) + "+" + str(newY))
        top.title("OOTO Miner")

        # root.wm_attributes('-transparentcolor', root['bg'])
        # root.wm_attributes('-transparentcolor', 'black')

        # top.configure(background = _top_bgcolor)
        # top.configure(highlightbackground = _top_bgcolor) #"#d9d9d9"
        # top.configure(highlightcolor = _top_bgcolor) # = "black")

        # Transparency
        # root.wm_attributes('-transparentcolor', root['bg'])

        # Removes the dashed line in tabs
        self.style.layout('Tab',
                          [('Notebook.tab', {'sticky': 'nswe', 'children':
                              [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                              # [('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                                  [('Notebook.label', {'side': 'top', 'sticky': ''})],
                                                     # })],
                                                     })],
                                             })]
                          )

        self.Tabs = ttk.Notebook(root, style = 'Tab')  # top)
        self.Tabs.place(relx = 0.0, rely = 0.0, relheight = 1.0, relwidth = 1)
        # self.Tabs.place(relx = 0.0, rely = 0.0, relheight = 1.0, relwidth = 1)
        # self.Tabs.configure(takefocus = "")

        # Top horizontal separator # TODO
        self.rootTopSeparator = ttk.Separator(root, orient = HORIZONTAL)
        self.rootTopSeparator.place(relx = 0, rely = 0, relwidth = 1)

        # > START TAB (0)
        self.Tabs_t2 = ttk.Frame(self.Tabs)
        ''' Tab icon '''
        im = PIL.Image.open(IS.TAB_ICO_START).resize(IS.TAB_ICO_SIZE, PIL.Image.ANTIALIAS)
        tab_start_icon = PIL.ImageTk.PhotoImage(im)
        self.Tabs_t2.image = tab_start_icon  # < ! > Required to make images appear
        self.Tabs.add(self.Tabs_t2, text = "Data", image = tab_start_icon,
                      compound = CENTER)  # self.Tabs.add(self.Tabs_t2, text = _txtpadding+"Data"+_txtpadding, image = photo, compound = TOP)
        # self.Tabs.tab(0, text = _txtpadding+"Data"+_txtpadding, underline = "-1")

        # > TEST TAB (1)

        self.Tabs_t3 = ttk.Frame(self.Tabs)
        ''' Tab icon '''
        im = PIL.Image.open(IS.TAB_ICO_TEST).resize(IS.TAB_ICO_SIZE, PIL.Image.ANTIALIAS)
        tab_test_icon = PIL.ImageTk.PhotoImage(im)
        self.Tabs_t3.image = tab_test_icon  # < ! > Required to make images appear
        self.Tabs.add(self.Tabs_t3, text = "MM", image = tab_test_icon,
                      compound = CENTER)  # self.Tabs.add(self.Tabs_t2, text = _txtpadding+"Data"+_txtpadding, image = photo, compound = TOP)


        # > ABOUT TAB (2)
        self.Tabs_t5 = ttk.Frame(self.Tabs)
        ''' Tab icon '''
        im = PIL.Image.open(IS.TAB_ICO_INFO).resize(IS.TAB_ICO_SIZE, PIL.Image.ANTIALIAS)
        tab_info_icon = PIL.ImageTk.PhotoImage(im)
        self.Tabs_t5.image = tab_info_icon  # < ! > Required to make images appear
        self.Tabs.add(self.Tabs_t5, text = "AM", image = tab_info_icon,
                      compound = CENTER)


        # > ABOUT TAB (4)
        self.Tabs_t4 = ttk.Frame(self.Tabs)
        ''' Tab icon '''
        im = PIL.Image.open(IS.TAB_ICO_INFO).resize(IS.TAB_ICO_SIZE, PIL.Image.ANTIALIAS)
        tab_info_icon = PIL.ImageTk.PhotoImage(im)
        self.Tabs_t4.image = tab_info_icon  # < ! > Required to make images appear
        self.Tabs.add(self.Tabs_t4, text = "Info", image = tab_info_icon,
                      compound = CENTER)  # self.Tabs.add(self.Tabs_t2, text = _txtpadding+"Data"+_txtpadding, image = photo, compound = TOP)




        self.style.configure("Tab",
                             background = CS.TAB_BG_COLOR,
                             foreground = CS.FG_COLOR,
                             borderwidth = 0,
                             tabposition = 'wn',
                             height = FS.rootTabWidth)

        self.style.map("Tab",
                       background = [('selected', CS.ACTIVE_COLOR), ('active', CS.L_GRAY)])

    # endregion

    """ >>> CONFIGURE MAIN TABS <<< """
    # region

    ''' --> Configure DATA ("DATA") TAB (1) <-- '''

    def configureDataTabElements(self, parentFrame):
        self.INPUT = INPUT.InputModule(parentFrame)
        return self.INPUT
    ''' --> Configure TEST ("TEST") TAB (2.1) <-- '''

    def configureManualMiningTab(self, parentFrame):
        manualMining = MM.ManualMining(parentFrame)
        # self.testTabParentFrame = manualMining.getMainFrame() # LabelFrame(self.Tabs_t3, bd = 0)
        return manualMining
    ''' --> Configure TEST ("TEST") TAB (2.2) <-- '''

    def configureTestTabConsoleElements(self):
        self.testTabConsoleParentFrame = LabelFrame(self.Tabs_t3, bd = 0)
        # newRelW = 0.2
        # self.testTabConsoleParentFrame.place(
        #     relx = 1 - newRelW,
        #     rely = self.getRelY(self.testTabParentFrame),
        #     relwidth = newRelW,
        #     relheight = self.getRelH(self.testTabParentFrame)
        # )
        self.testTabConsoleParentFrame.configure(
            background = CS.D_BLUE, foreground = CS.FG_COLOR
        )

    ''' --> Configure INFO ("INFO") TAB (3) <-- '''
    def configureAutomatedMiningTab(self, parentFrame):
        global root
        self.Tabs.select(2)  # show the current tab to be able to retrieve height and
        automatedMining = AM.AutomatedMining(parentFrame, root)
        self.Tabs.select(0)  # return to first tab
        return automatedMining

        # self.chiTabParentFrame = chiFrame.getMainFrame()
        # self.chiTabParentFrame.place(
        #     relx = US.TAB_REL_X, rely = US.TAB_REL_Y,
        #     relwidth = US.TAB_REL_W, relheight = US.TAB_REL_H
        # )
        # self.chiTabParentFrame.configure(
        #     background = CS.TAB_BG_COLOR, foreground = CS.FG_COLOR
        # )

    def configureInfoTabElements(self):
        # Creates the parent frame (infoTabParentFrame) that will hold all the elements in INFO TAB 3 (Tabs_t4)
        self.infoTabParentFrame = LabelFrame(self.Tabs_t4, bd = 0)
        self.infoTabParentFrame.place(
            relx = US.TAB_REL_X, rely = US.TAB_REL_Y,
            relwidth = US.TAB_REL_W, relheight = US.TAB_REL_H)
        self.infoTabParentFrame.configure(background = CS.TAB_BG_COLOR, foreground = CS.FG_COLOR)
        # Create the left separator
        self.infoTabLeftSeparator = ttk.Separator(self.infoTabParentFrame, orient = VERTICAL)
        self.infoTabLeftSeparator.place(relx = 0, rely = 0, relheight = 1)

        self.configureAboutElements()

        '''
        BINDING FOR INFO TAB
        '''
        # self.buttonQueryPopulation.bind('<Button-1>', self.querySetPopulation)
        # self.buttonQuerySetDataA.bind('<Button-1>', self.querySetDataA)

    # endregion

    """ >>> FUNCTIONS FOR THE CONFIGURATION OF UI ELEMENTS <<< """
    # region

    ''' --> Elements under DATA ("DATA") TAB (1) <-- '''
    # region


    ''' --> Elements under TEST ("TEST") TAB (2) <-- '''
    # MOVED

    ''' --> Elements under INFO ("INFO") TAB (2) <-- '''
    # MOVED

    # region
    def configureAboutElements(self):
        # Create the About parent frame
        self.labelFrameAbout = LabelFrame(self.infoTabParentFrame, bd = 0)
        self.labelFrameAbout.configure(
            background = CS.ABOUT_BG, foreground = CS.FG_COLOR, text = US.TITLE_ABOUT)
        self.labelFrameAbout.place(
            relx = US.TAB_ABOUT_REL_X, rely = US.TAB_ABOUT_REL_Y + US.TAB_CHILD_PADDING_TOP,
            relwidth = US.TAB_ABOUT_REL_W, relheight = US.TAB_ABOUT_REL_H)

        # Create the About element parent frame
        self.labelFrameAboutElements = LabelFrame(self.labelFrameAbout, bd = 0)
        self.labelFrameAboutElements.configure(
            background = CS.ABOUT_BG, foreground = CS.FG_COLOR)
        self.labelFrameAboutElements.place(
            relx = US.TAB_ELEMENT_REL_X, rely = 0.1,
            relwidth = US.TAB_ELEMENT_REL_W, relheight = 0.80)

        # > ABOUT ELEMENTS
        # Version label
        self.labelVersion = Label(self.labelFrameAboutElements)
        self.labelVersion.place(
            relx = US.TAB_CHILD_LBL_REL_X, rely = US.TAB_CHILD_LBL_REL_Y,
            relwidth = US.TAB_CHILD_LBL_REL_W, relheight = US.TAB_CHILD_LBL_REL_H)
        self.labelVersion.configure(
            background = CS.ABOUT_LBL_BG, foreground = CS.ABOUT_LBL_FG,
            text = US.LBL_ABOUT_VER,
            disabledforeground = CS.FG_DISABLED_COLOR,
            bd = 1)

        # Previous values (1.1)
        prevLblRelX = float(self.labelVersion.place_info()['relx'])
        prevLblRelY = float(self.labelVersion.place_info()['rely'])
        prevLblRelW = float(self.labelVersion.place_info()['relwidth'])
        prevLblRelH = float(self.labelVersion.place_info()['relheight'])

        newRelX = US.TAB_CHILD_LBL_REL_X + prevLblRelX + prevLblRelW

        # Version text
        self.labelVersionText = Label(self.labelFrameAboutElements)
        self.labelVersionText.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = US.TAB_CHILD_STR_REL_W, relheight = prevLblRelH)
        self.labelVersionText.configure(
            background = CS.ABOUT_STR_BG, foreground = CS.ABOUT_STR_FG,
            text = US.STR_ABOUT_VER,
            bd = 1,
            disabledforeground = CS.FG_DISABLED_COLOR)

        # Previous values (1.2)
        prevStrRelX = float(self.labelVersionText.place_info()['relx'])
        prevStrRelY = float(self.labelVersionText.place_info()['rely'])
        prevStrRelW = float(self.labelVersionText.place_info()['relwidth'])
        prevStrRelH = float(self.labelVersionText.place_info()['relheight'])

        newRelY = US.TAB_CHILD_LBL_REL_Y + prevLblRelY + prevLblRelH

        # Author label
        self.labelAuthor = Label(self.labelFrameAboutElements)
        self.labelAuthor.place(
            relx = prevLblRelX, rely = newRelY,
            relwidth = prevLblRelW, relheight = prevLblRelH)
        self.labelAuthor.configure(
            background = CS.ABOUT_LBL_BG, foreground = CS.ABOUT_LBL_FG,
            text = US.LBL_ABOUT_AUTHOR,
            disabledforeground = CS.FG_DISABLED_COLOR)

        # Author text
        self.labelAuthorText = Label(self.labelFrameAboutElements)
        self.labelAuthorText.place(
            relx = prevStrRelX, rely = newRelY,
            relwidth = prevStrRelW, relheight = prevStrRelH)
        self.labelAuthorText.configure(
            background = CS.ABOUT_STR_BG, foreground = CS.ABOUT_STR_FG,
            text = US.STR_ABOUT_AUTHOR,
            disabledforeground = CS.FG_DISABLED_COLOR)

        # Previous Y values
        prevLblRelY = float(self.labelAuthor.place_info()['rely'])
        prevStrRelY = float(self.labelAuthorText.place_info()['rely'])

        newRelY = US.TAB_CHILD_LBL_REL_Y + prevLblRelY + prevLblRelH

        # Affiliation label
        self.labelAffiliation = Label(self.labelFrameAboutElements)
        self.labelAffiliation.place(
            relx = prevLblRelX, rely = newRelY,
            relwidth = prevLblRelW, relheight = prevLblRelH)
        self.labelAffiliation.configure(
            background = CS.ABOUT_LBL_BG, foreground = CS.ABOUT_LBL_FG,
            text = US.LBL_ABOUT_AFFILIATION,
            disabledforeground = CS.FG_DISABLED_COLOR)

        # Affiliation text
        self.labelAffiliationText = Label(self.labelFrameAboutElements)
        self.labelAffiliationText.place(
            relx = prevStrRelX, rely = newRelY,
            relwidth = prevStrRelW, relheight = prevStrRelH)
        self.labelAffiliationText.configure(
            background = CS.ABOUT_STR_BG, foreground = CS.ABOUT_STR_FG,
            text = US.STR_ABOUT_AFFILIATION,
            disabledforeground = CS.FG_DISABLED_COLOR)

    # endregion

    """ >>> HELPER FUNCTIONS UI ELEMENTS <<< """

    # region
    def createCornerImage(self, cornerParent):

        labelNE = Label(cornerParent)
        im = PIL.Image.open(
            IS.CORNER_ROUND_NE)  # .resize(IS.CORNER_ICO_SIZE_SMALL, PIL.Image.ANTIALIAS)
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

    # endregion

    """ >>> FUNCTIONS CALLED FOR BINDING ELEMENTS <<< """
    # region
    ''' --> General call to all binding sub-functions <-- '''

    # def configureBindings(self):
        # self.configureDataTabBindings()
        # self.configureTestTabBindings()


    ''' --> Binding elements under the TEST ("TEST") TAB (2) <-- '''
    # MOVED

    """ >>> FUNCTIONS CALLED BY BOUNDED ELEMENTS (e.g. buttons, listboxes) <<< """


    ''' Upload the dataset and variable description files '''

    def uploadInputFiles(self, event):
        # Upload initVarDesc (Variable Description)

        if not self.INPUT.hasUploadedVariableDescription():  # Check if variable description was uploaded
            tkMessageBox.showerror("Error 1: Upload Variable description",
                                   "Please select a valid variable description file.")
            return "break"
        else:
            # Upload Variable Descriptions to modules
            isSuccessfulMM = self.MM.readFeatures(self.INPUT.getInitVarDisc())
            isSuccessfulAM = self.AM.readFeatures(self.INPUT.getInitVarDisc())

            if not (isSuccessfulMM and isSuccessfulAM):
                tkMessageBox.showerror("Error 1: Upload Variable description",
                                       "Please select a valid variable description file.")
                return "break"
            # else:
            # tkMessageBox.showinfo("Variable description set", "Variable description uploaded")
            # # getCommonGroups(features)

        # Upload populationDir (Population Dataset)
        if not self.INPUT.getHasUploadedPopulation():  # Check if population dataset was uploaded
            tkMessageBox.showerror("Error 1: Upload Population Dataset",
                                   "Please select a population dataset file.")
            return "break"

        else:
            populationDir = self.INPUT.getPopulationDir()

            populationDataset = FS.readCSVDict(populationDir)
            isSuccessfulAM = self.AM.uploadDataset(populationDataset)


            populationDataset = FS.readCSVDict(populationDir)
            isSuccessfulMM = self.MM.uploadDataset(populationDir, populationDataset)

            if (isSuccessfulMM and isSuccessfulAM):
                tkMessageBox.showinfo("Success: Upload Dataset",
                                       "Dataset successfully uploaded!")
                self.Tabs.select(US.TAB_TEST_INDEX)

            elif not (isSuccessfulMM and isSuccessfulAM):
                tkMessageBox.showerror("Error 1: Upload Dataset",
                                       "Dataset upload failed, please check input files.")

            elif not isSuccessfulMM:
                tkMessageBox.showerror("Error 2: Upload Dataset",
                                       "Manual Mining dataset upload failed, please check input files.")

            elif not isSuccessfulAM:
                tkMessageBox.showerror("Error 3: Upload Dataset",
                                       "Automated Mining dataset upload failed, please check input files.")

        return "break"




if __name__ == '__main__':
    vp_start_gui()
