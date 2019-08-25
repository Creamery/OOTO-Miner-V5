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
import KEYS_support as key

import Color_support as CS
import Function_support as FS
import Widget_support as WS
import Icon_support as IS
import UI_support as US
from CrossProcessThread import CrossProcessThread

class SystematicFiltering_Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.winSystematicFiltering = None
        self.threadCrossProcess = None
        self.configureViewBindings()

    def configureViewBindings(self):
        button = self.view.getBtnStartCrossProcess()
        button.bind('<Button-1>', self.startCrossProcessThread)


    " FUNCTIONS "
    def startCrossProcessThread(self, event):
        if not self.model.isCrossProcessing():

            self.model.startSystematicFiltering(self.view)
            # self.view.getFrame().protocol("WM_DELETE_WINDOW", self.stopCrossProcess)

            # crossProcess = CrossProcessThread(self)
            # crossProcess.start()
        else:
            print ("isProcessing")

    def stopCrossProcess(self):
        print "crossProcess stopped"


    " GETTERS "
