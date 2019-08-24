
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

import ManualMining_VIEW as VIEW
import ManualMining_CONTROLLER as CONTROLLER


class ManualMining:
    def __init__(self, parentFrame):


        arrQueryCriticalValue = ["0.80", "0.90", "0.95", "0.98", "0.99"]
        arrQueryCriticalValueMapping = {"0.80": 1.28, "0.90": 1.645, "0.95": 1.96, "0.98": 2.33, "0.99": 2.58}


        self.view = VIEW.ManualMining_View(parentFrame)
        self.controller = CONTROLLER.ManualMining_Controller(self.view)

        self.view.setArrQueryCriticalValue(arrQueryCriticalValue)
        self.view.setArrQueryCriticalValueMapping(arrQueryCriticalValueMapping)

        self.controller.setArrQueryCriticalValue(arrQueryCriticalValue)
        self.controller.setArrQueryCriticalValueMapping(arrQueryCriticalValueMapping)

    def readFeatures(self, variableDescription):
        return self.controller.readFeatures(variableDescription, "^")

    def uploadDataset(self, directory, populationDataset):
        return self.controller.uploadDataset(directory, populationDataset)