


__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"

'''
    This script handles the Input in the Manual Mining (MM)
    modules.
    [Candy]
'''

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

import Input_VIEW as VIEW
import Input_CONTROLLER as CONTROLLER

class InputModule:

    def __init__(self, parentFrame):
        self.view = VIEW.Input_View(parentFrame)
        self.controller = CONTROLLER.Input_Controller(self.view)


    def hasUploadedVariableDescription(self):
        return self.controller.getHasUploadedVariableDescription()


    def getInitVarDisc(self):
        return self.controller.getInitVarDisc()

    def getHasUploadedPopulation(self):
        return self.controller.getHasUploadedPopulation()

    def getButtonStartDatasetUpload(self):
        return self.controller.getButtonStartDatasetUpload()

    def getPopulationDir(self):
        return self.controller.getPopulationDir()