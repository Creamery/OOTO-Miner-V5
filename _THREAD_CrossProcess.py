import threading
import time

class CrossProcessThread(threading.Thread):

    # pass the widgets that the thread will update
    def __init__(self):
        threading.Thread.__init__(self)
        self.progressible = None

    def setProgressible(self, progressible):
        self.progressible = progressible


    def run(self):
        try:
            # self.prog_bar.start()
            self.progressible.resetProgress()

            while not self.progressible.isComplete():
                # self.prog_bar.after(1, self.process_queue)
                # self.process_queue()
                print "progress " + str(self.progressible.getCurrentPercent())
                time.sleep(0.01)


        finally:
            pass
            # self.lblProgressText["text"] = "COMPLETE"

    # def process_queue(self):
    #     self.lblProgressValue = float(self.count)
    #     self.pbProgressBar["value"] = self.lblProgressValue
    #     self.lblProgressText["text"] = self.lblProgressValue




    # THREADING TEST FUNCTIONS
    # def startThread(self, event):
    #     if not self.isProcessing:
    #         self.isProcessing = True
    #         if not (self.winProgressBar is None):
    #             self.onProgressBarClose()
    #
    #         self.winProgressBar = Toplevel()  # Tk() TODO add parent
    #         self.winProgressBar.protocol("WM_DELETE_WINDOW", self.onProgressBarClose)
    #         self.varProgressBar = 0
    #         [self.pbProgressBar, self.lblProgressBar] = self.initProgressBar(self.winProgressBar)
    #
    #         crossProcess = CrossProcessThread(self.winProgressBar, self.pbProgressBar,
    #                                           self.lblProgressBar, self.varProgressBar)
    #         crossProcess.start()
    #     else:
    #         print ("isProcessing")
    #
    #
    # def initProgressBar(self, parentFrame):
    #     progBar = ttk.Progressbar(
    #         parentFrame, orient = "horizontal",
    #         length = 300, variable = self.varProgressBar)
    #
    #     progBar.pack(side = TOP)
    #     progText = Label(progBar)
    #     progText.place(relx = 0, rely = 0, relh = 1)
    #     return progBar, progText
    #
    #
    # def onProgressBarClose(self):
    #     # if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
    #     #     self.winProgressBar.destroy()
    #     #     self.winProgressBar = None
    #     #     self.isProcessing = False
    #     self.winProgressBar.destroy()
    #     self.winProgressBar = None
    #     self.isProcessing = False


