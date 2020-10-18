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
        button.bind('<Button-1>', self.startAutomatedMining)


    " FUNCTIONS "
    '''
        This function calls the update progress in its view.
    '''
    def updateProgress(self, progress, description = ""):
        self.view.updateProgress(progress, description)



    def startAutomatedMining(self, event):
        print("Start Systematic Filtering (From SFModule")
        startCrossProcessThread([self])

        return "break"


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

            # print("")
            # print(key)
            # print("SINGLE SECTION " + str(single_section_progress))
            # print("ITERATOR " + str(current_process_iterator))
            # print("MAX PROGRESS " + str(max_process_count))
            # print("CURRENT SECTION PROGRESS IS " + str(current_section_progress))
            # print("PREV RUNNING PERCENT IS " + str(prev_running_percent))


            progress = section_progress_from_whole
            progress = (progress + prev_running_percent)  # Previous section progress(es) + current section's progress
            progress = progress * 100  # Multiply by 100 to express as percent

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






