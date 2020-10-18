#! /usr/bin/env python

"""
{Description}
Systematic Filtering Controller
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
from _THREAD_CrossProcess import CrossProcessThread
import Grip_support as GS

from threading import Thread
import AutomatedMining_RUN as AM_R
import tkMessageBox
import collections

import UIConstants_support as UICS

class SystematicFiltering_Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.grip = None
        # self.dialogue_grip = None

        self.setDictResults(None)
        self.declareBindingVariables()
        self.configureViewBindings()


        # self.winDialogueOverlay = WS.createOverlayWindow(self.view.getFrame())
        # self.winDialogueTop = self.__initializeWindow(self.view.getFrame())  # WS.createDefaultToplevelWindow(root, [FS.sfWidth, FS.sfHeight], True, True)
        # self.winDialogueTop.configure(bg = CS.WHITE)
        # self.gripDialogue = self.__configureDialogueGrip(self.winDialogueTop, self.winDialogueOverlay, root)
        # self.__configureBorders(self.winDialogueTop)
        # self.winDialogueOverlay.lower(self.winDialogueTop)
        # self.controller.setDialogueGrip(self.gripDialogue)
        # self.controller.resizeDialogueOverlay()

    # def __configureDialogueGrip(self, parentWindow, winDialogueOverlay, root):
    #     dialogue_grip = DGS.DialogueGripLabel(parentWindow, True, True)
    #     dialogue_grip.assignOverlay(winDialogueOverlay, root)
    #     return dialogue_grip

    '''
        Connect buttons from view with their functionality
    '''
    def configureViewBindings(self):
        button = self.view.getBtnStartCrossProcess()
        button.bind('<Button-1>', self.startAutomatedMining)
        button.bind("<Enter>", self.enterCheckIcon)
        button.bind("<Leave>", self.leaveCheckIcon)


        button = self.view.getBtnStopCrossProcess()
        button.bind('<Button-1>', self.stopAutomatedMining)
        button.bind("<Enter>", self.enterCrossIcon)
        button.bind("<Leave>", self.leaveCrossIcon)




    def showDialogPrompt(self, event):
        self.view.openDialog()
        self.bindDialogButtons()

    def closeDialog(self, event):
        self.view.closeDialog()

    def declareBindingVariables(self):
        self.icon_check_on = None
        self.icon_check_off = None

        self.icon_cross_on = None
        self.icon_cross_off = None


    def bindDialogButtons(self):
        button = self.view.getBtnCloseDialog()
        button.bind('<Button-1>', self.closeDialog)

    def bindParentGripButtons(self):
        # button.bind("<Button-1>", lambda event: self.onTopClose())
        button = self.getParentGrip().getCloseButton()
        button.bind('<Button-1>', self.showDialogPrompt)

    '''
        FUNCTIONS
    '''
    '''
        This function calls the update progress in its view.
    '''
    def updateProgress(self, progress, description = ""):
        self.view.updateProgress(progress, description)


    def startAutomatedMining(self, event):
        self.view.showStopMining()
        print("Start Systematic Filtering (From SFModule")
        startCrossProcessThread([self])

        return "break"

    def stopAutomatedMining(self, event):
        self.view.showStartMining()
        # TODO Perform necessary warnings in view before stopping

        # tkMessageBox.showinfo("Automated Mining Complete", "You can now review the results by searching below.")
        # self.closeWindow()

        return "break"


    def closeWindow(self):  # TODO
        self.getGrip().onTopClose()

    '''
        FUNCTIONS - For updating the progress bar
    '''
    def updateModuleProgress(self, key, description):
        if key is 0:  # Key = 0 is used for the first message
            progress = 0
            self.updateProgress(progress, description)

        else:
            UICS.iterateProcessKey(key)  # Increment the given key's progress by 1

            key_values = UICS.getProcessKeyValues(key)  # Get the current key's value and max value

            # Compute the progress for the current section of the program indicated
            # by the key by dividing the key's current progress from its max progress
            max_process_count = key_values[0]
            current_process_iterator = key_values[1]

            # The amount to add for a single successful process under the given section
            single_section_progress = float(1) / float(max_process_count)

            # The current section progress is a single process times the current iteration of that section
            current_section_progress = float(current_process_iterator) * single_section_progress

            # The progress of this section as part of the whole process
            section_progress_from_whole = current_section_progress * UICS.SINGLE_SECTION_PERCENT
            UICS.setKeyDecimalProgress(key, section_progress_from_whole)

            # if current_section_progress > 0.1:  # If progress is too small to record, set the value to the smallest allowed
            #     current_section_progress = 0.1

            # Get the percent of the previous section
            prev_running_percent = UICS.getPrevKeyRunningProgress(key)

            progress = section_progress_from_whole
            progress = (progress + prev_running_percent)  # Previous section progress(es) + current section's progress
            progress = progress * 100  # Multiply by 100 to express as percent

            self.updateProgress(progress, "    " + description)

    '''
        FUNCTIONS - For Sections 2 and 3 functionality
    '''
    def searchResults(self, feat_code):
        if self.dict_results is not None:  # Check if dict_results was ever initialized
            dict_output = collections.OrderedDict()
            for key, value in self.dict_results.items():
                if feat_code in str(key):
                    dict_output[key] = value

            return dict_output



    '''
        FUNCTIONS - For button effects
    '''
    def enterCheckIcon(self, event):
        if self.icon_check_on is None:
            iconSize = self.getIcoSizeCheck()
            im = PIL.Image.open(IS.TAB_ICO_CHECK_ON).resize(iconSize, PIL.Image.ANTIALIAS)
            self.icon_check_on = PIL.ImageTk.PhotoImage(im)

        item = event.widget
        item.configure(
            image = self.icon_check_on)
        item.image = self.icon_check_on  # < ! > Required to make images appear


    def leaveCheckIcon(self, event):
        if self.icon_check_off is None:
            iconSize = self.getIcoSizeCheck()
            im = PIL.Image.open(IS.TAB_ICO_CHECK).resize(iconSize, PIL.Image.ANTIALIAS)
            self.icon_check_off = PIL.ImageTk.PhotoImage(im)

        item = event.widget
        item.configure(
            image = self.icon_check_off)
        item.image = self.icon_check_off  # < ! > Required to make images appear


    def enterCrossIcon(self, event):
        if self.icon_cross_on is None:
            iconSize = self.getIcoSizeCross()
            im = PIL.Image.open(IS.TAB_ICO_CROSS_ON).resize(iconSize, PIL.Image.ANTIALIAS)
            self.icon_cross_on = PIL.ImageTk.PhotoImage(im)

        item = event.widget
        item.configure(
            image = self.icon_cross_on)
        item.image = self.icon_cross_on  # < ! > Required to make images appear

    def leaveCrossIcon(self, event):
        if self.icon_cross_off is None:
            iconSize = self.getIcoSizeCross()
            im = PIL.Image.open(IS.TAB_ICO_CROSS).resize(iconSize, PIL.Image.ANTIALIAS)
            self.icon_cross_off = PIL.ImageTk.PhotoImage(im)

        item = event.widget
        item.configure(
            image = self.icon_cross_off)
        item.image = self.icon_cross_off  # < ! > Required to make images appear

    # def resizeDialogueOverlay(self):
    #     # x = self.view.getFrame().winfo_x()
    #     # y = self.view.getFrame().winfo_y()
    #
    #     width = self.view.getFrame().winfo_width()
    #     height = self.view.getFrame().winfo_height()
    #     x = float(width) / float(2)
    #     y = float(height) / float(2)  # self.view.getFrame().winfo_y()
    #     self.dialogue_grip.resizeOverlay(int(x), int(y), width, height)

    '''
        GETTERS / SETTERS
    '''
    def getDictResults(self):
        return self.dict_results

    def setDictResults(self, dict_results):
        self.dict_results = dict_results

    def getGrip(self):
        return self.grip

    def setGrip(self, module_grip):
        self.grip = module_grip

    def setParentGrip(self, grip):
        self.parent_grip = grip

    def getParentGrip(self):
        return self.parent_grip


    # def getDialogueGrip(self):
    #     return self.dialogue_grip

    # def setDialogueGrip(self, grip):
    #     self.dialogue_grip = grip

    def getIcoSizeCheck(self):
        width = self.view.getIcoWidthCheck()
        height = self.view.getIcoHeightCheck()
        return width, height

    def getIcoSizeCross(self):
        width = self.view.getIcoWidthCross()
        height = self.view.getIcoHeightCross()
        return width, height



'''
    THREADING FUNCTIONS
'''

lblDetails = None

def startCrossProcessThread(controller):
    thread = Thread(target = runCrossProcessThread, args = controller)
    thread.start()
    # thread.join()
    print("thread finished...exiting")


def runCrossProcessThread(controller):
    print("Running Cross Process Thread")

    # changeText(lblDetails, "HEY")
    progress = 0
    while progress < 100:
        if progress == 0:
            thread = Thread(target = runAutomatedMining, args = [controller])
            thread.start()

        progress = progress + 1
        # controller.updateProgress(progress)
    # tkMessageBox.showinfo("Automated Mining Complete", "You can now review the results by searching below.")


def runAutomatedMining(controller):
    AM_R.runAutomatedMining(controller)

def changeText(label, text):
    # current_text = label.get()
    # label.set(current_text + "Text updated")
    label.set(text + "Text updated")





