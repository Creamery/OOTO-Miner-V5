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
    from tkinter import *

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

import AutomatedMining_MODEL as MODEL
import AutomatedMining_VIEW as VIEW
import AutomatedMining_CONTROLLER as CONTROLLER


class AutomatedMining:
    def __init__(self, parentFrame, root = None):
        self.root = root

        arrQueryCriticalValue = ["0.80", "0.90", "0.95", "0.98", "0.99"]
        arrQueryCriticalValueMapping = {"0.80": 1.28, "0.90": 1.645, "0.95": 1.96, "0.98": 2.33, "0.99": 2.58}

        self.model = MODEL.AutomatedMining_Model()
        self.view = VIEW.AutomatedMining_View(parentFrame)
        self.controller = CONTROLLER.AutomatedMining_Controller(self.view, self.model, self.root)

        self.view.setArrQueryCriticalValue(arrQueryCriticalValue)
        self.view.setArrQueryCriticalValueMapping(arrQueryCriticalValueMapping)

        self.controller.setArrQueryCriticalValue(arrQueryCriticalValue)
        self.controller.setArrQueryCriticalValueMapping(arrQueryCriticalValueMapping)

    def readFeatures(self, variableDescription):
        return self.controller.readFeatures(variableDescription, "^")

    def uploadDataset(self, populationDataset):
        return self.controller.uploadDataset(populationDataset) # TODO return functionality
        # return True