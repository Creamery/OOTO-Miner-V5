#! /usr/bin/env python

"""
{Description}

"""

__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"

'''
    This script is the main module for the Automated Mining (AM) UI.
    It consolidates an AutomatedMining_View, AutomatedMining_View,
    and AutomatedMining_Controller. The _View script handles all UI
    elements, the _Model script handles the data shown by the _View,
    and the _Controller script handles UI functionality.
    
    This is the class instantiated by the driver in order to create the
    AM tab in the UI.
    [Candy]
'''

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
        self.view = VIEW.AutomatedMining_View(parentFrame, root)
        # self.controller = CONTROLLER.AutomatedMining_Controller(self.view, self.model, self.root)
        self.controller = CONTROLLER.AutomatedMining_Controller(self.view, self.model, self.root)


    def readFeatures(self, variableDescription):
        return self.controller.readFeatures(variableDescription, "^")

    def uploadDataset(self, dirPopulation):
        return self.controller.uploadDataset(dirPopulation)