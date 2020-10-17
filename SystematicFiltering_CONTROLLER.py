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

class SystematicFiltering_Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.configureViewBindings()

    def configureViewBindings(self):
        button = self.view.getBtnStartCrossProcess()
        button.bind('<Button-1>', self.startCrossProcessThread)


    " FUNCTIONS "

    def updateProgress(self, progress, args = [""]):

        self.view.updateProgress(progress, args)




    def startCrossProcessThread(self, event):

        lblCurrentDetails = self.view.getLblCurrentDetails()
        print("Cross Process Start")
        startCrossProcessThread(lblCurrentDetails)

        # if not self.model.isCrossProcessing():
        #     self.model.startSystematicFiltering(self.view)
        #     # self.view.getFrame().protocol("WM_DELETE_WINDOW", self.stopCrossProcess)
        #
        #     # crossProcess = CrossProcessThread(self)
        #     # crossProcess.start()
        # else:
        #     print ("isProcessing")


    def stopCrossProcess(self):
        print "crossProcess stopped"



    # def threaded_function(arg):
    #     while True:
    #         print("in")
    #     # for i in range(arg):
    #     #     print("running")
    #     #     sleep(1)




'''
    THREADING FUNCTIONS
'''

lblDetails = None

def startCrossProcessThread(lblCurrentDetails):
    lblDetails = lblCurrentDetails
    thread = Thread(target = runCrossProcessThread)
    thread.start()
    # thread.join()
    print("thread finished...exiting")


def runCrossProcessThread():
    print("Running Cross Process Thread")
    # changeText(lblDetails, "HEY")
    AM_R.runAutomatedMining()
    # tkMessageBox.showinfo("Automated Mining Complete", "You can now review the results by searching below.")



def changeText(label, text):
    # current_text = label.get()
    # label.set(current_text + "Text updated")
    label.set(text + "Text updated")



    " GETTERS "






