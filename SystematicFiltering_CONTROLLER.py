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

from threading import Thread
import AutomatedMining_RUN as AM_R
import tkMessageBox
import time

import UIConstants_support as UICS

class SystematicFiltering_Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.configureViewBindings()

    def configureViewBindings(self):
        button = self.view.getBtnStartCrossProcess()
        button.bind('<Button-1>', self.startCrossProcessThread)


    " FUNCTIONS "
    '''
        For this function, the passed parameter 'args' gives the
        message to show on below the progress bar.
    '''
    def updateProgress(self, progress, args = ""):
        self.view.updateProgress(progress, args)


    def startCrossProcessThread(self):
        print("Cross Process Start")
        startCrossProcessThread([self])

        # if not self.model.isCrossProcessing():
        #     self.model.startSystematicFiltering(self.view)
        #     # self.view.getFrame().protocol("WM_DELETE_WINDOW", self.stopCrossProcess)
        #
        #     # crossProcess = CrossProcessThread(self)
        #     # crossProcess.start()
        # else:
        #     print ("isProcessing")


    '''
        FUNCTIONS - For updating the progress bar
    '''
    def updateModuleProgress(self, key, current_iteration, description):
        UICS.iterateProcessKey(key)  # Increment the given key's progress by 1

        key_values = UICS.getProcessKeyValues(key)  # Get the current key's value and max value

        # Compute the progress for the current section of the program indicated
        # by the key by dividing the key's current progress from its max progress
        max_process_count = key_values[0]
        current_process_iterator = key_values[1]
        current_section_progress = float(current_process_iterator) / float(max_process_count)


        # The current progress will be the current section progress multiplied by
        # the current section number over the total number of sections (done in the
        # section_percent variable)
        section_percent = UICS.getSectionPercent(key)
        progress = current_section_progress * section_percent

        self.updateProgress(progress, "    " + description)






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



    " GETTERS "






