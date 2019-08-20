
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
import tkMessageBox

class AutomatedMining_Model:
    def __init__(self):
        self.isProcessing = False
        self.winProgressBar = None
        self.pbProgressBar = None

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
            if not (self.winProgressBar is None):
                self.onProgressBarClose()

            self.winProgressBar = Tk()
            self.winProgressBar.protocol("WM_DELETE_WINDOW", self.onProgressBarClose)
            self.varProgressBar = 0
            [self.pbProgressBar, self.lblProgressBar] = self.initProgressBar(self.winProgressBar)

            ThreadedTask(self.winProgressBar, self.pbProgressBar, self.lblProgressBar, self.varProgressBar).start()
        else:
            print ("isProcessing")

    def initProgressBar(self, parentFrame):
        progBar = ttk.Progressbar(
            parentFrame, orient = "horizontal",
            length = 300, variable = self.varProgressBar)

        progBar.pack(side = TOP)
        progText = Label(progBar)
        progText.place(relx = 0, rely = 0, relh = 1)
        return progBar, progText

    def onProgressBarClose(self):
        # if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        #     self.winProgressBar.destroy()
        #     self.winProgressBar = None
        #     self.isProcessing = False
        self.winProgressBar.destroy()
        self.winProgressBar = None
        self.isProcessing = False


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
            # self.prog_bar.start()
            while self.count < 100:
                self.count += 1
                # self.prog_bar.after(1, self.process_queue)
                self.process_queue()
                time.sleep(0.01)


        finally:
            self.prog_text["text"] = "COMPLETE"

    def process_queue(self):
        self.prog_val = float(self.count)
        self.prog_bar["value"] = self.prog_val
        self.prog_text["text"] = self.prog_val
        # self.prog_bar.start()
        # print str(self.prog_val)
