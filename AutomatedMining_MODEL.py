
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

import threading
import time


class AutomatedMining_Model:
    def __init__(self):
        self.isProcessing = False
        self.winProgress = None

    def confirmFeatureSelect(self, evt):
        print "confirmFeatureSelect"
        self.startThread(evt)
        return "break"

    def resetFeatureSelect(self, evt):
        print "resetFeatureSelect"
        return "break"


    # THREADING TEST FUNCTIONS
    def startThread(self, evt):
        if not self.isProcessing:
            self.isProcessing = True
            if not (self.winProgress is None):
                self.winProgress.destroy()
                self.winProgress = None

            self.winProgress = Tk()
            self.progress_var = 0
            [self.prog_bar, self.prog_text] = self.initProgress(self.winProgress)

            ThreadedTask(self.winProgress, self.prog_bar, self.prog_text, self.progress_var).start()


    def initProgress(self, parentFrame):
        progBar = ttk.Progressbar(
            parentFrame, orient = "horizontal",
            length = 300, variable = self.progress_var
            )

        progBar.pack(side = TOP)
        progText = Label(progBar)
        progText.place(relx = 0, rely = 0, relh = 1)
        return progBar, progText


class ThreadedTask(threading.Thread):
    def __init__(self, winProgress, prog_bar, prog_text, prog_val):
        threading.Thread.__init__(self)
        self.winProgress = winProgress
        self.prog_bar = prog_bar
        self.prog_text = prog_text
        self.prog_val = prog_val
        self.count = 0

    def run(self):
        try:
            while self.count < 100:
                self.count += 10
                self.process_queue()
                time.sleep(1)


        finally:
            # self.prog_bar.stop()
            print('TASK FINISHED')
            self.isProcessing = False

    def process_queue(self):
        self.prog_val = float(self.count)
        self.prog_bar["value"] = self.prog_val
        self.prog_text["text"] = self.prog_val
        # self.prog_bar.start()
        # print str(self.prog_val)
