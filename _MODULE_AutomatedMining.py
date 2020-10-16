#! /usr/bin/env python

"""
{Description}

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

import AutomatedMining_MODEL as MODEL
import AutomatedMining_VIEW as VIEW
import AutomatedMining_CONTROLLER as CONTROLLER
import Function_support as FS


class AutomatedMining:
    def __init__(self, parentFrame, root = None):
        self.root = root

        self.model = MODEL.AutomatedMining_Model()
        self.view = VIEW.AutomatedMining_View(parentFrame)
        # self.controller = CONTROLLER.AutomatedMining_Controller(self.view, self.model, self.root)
        self.controller = CONTROLLER.AutomatedMining_Controller(self.view, self.model, self.root)


    def readFeatures(self, variableDescription):
        return self.controller.readFeatures(variableDescription, "^")

    def uploadDataset(self, dirPopulation):
        return self.controller.uploadDataset(dirPopulation)