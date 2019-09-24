import threading
import tkMessageBox
import os
import time

from ChiTest import ChiTest
import Function_support as FS
import Widget_support as WS
from Keys_support import SSF as KSS

from collections import OrderedDict

class CrossProcessProgressThread(threading.Thread):

    # pass the widgets that the thread will update
    def __init__(self, SSF):
        threading.Thread.__init__(self)
        self.progressible = None
        self.progress = 0
        self.__SSF = SSF

        # self.__LVL0 = [OrderedDict()] * len(SSF)

        self.CROSS = []  # array of cross processes

    def setProgressible(self, progressible):
        self.progressible = progressible

    def run(self):
        print str(self.__SSF)
        # WS.createFilters(self.__LVL0, self.__SSF)

        # create filters, where FILTERS[level] is an array of dict filters for that level
        FILTERS = WS.createFilters(self.__SSF)

        # create FILTER_PAIRS within each level, which is a comparison of 2 elements from FILTERS[level]
        FILTER_PAIRS = WS.createFilterPairs(FILTERS)
        print ""
        print "FILTER_PAIRS[1]: "
        print str(FILTER_PAIRS[1])
        print ""
        print "FILTER_PAIRS[3]: "
        print str(FILTER_PAIRS[3][0])
    
        # print "FILTERS[3] type : "
        # print str(type(FILTERS[3][0]))
        # print str(FILTERS[3][0].keys())

        # for each FILTERS level, and each FILTER per level, create a CSV
        """
        try:
            # self.prog_bar.start()
            self.progressible.resetProgress(50)
            self.progress = 0

            while not self.progressible.isComplete():
            # TODO
            # self.prepareData(tests)
            # self.performCrossProcess(dataset, features)


                self.progress += 1
                self.updateProgressible(self.progress)
                print "progress " + str(self.progressible.getCurrentPercent())
                # time.sleep(0.01)


        finally:
            print "ThreadCrossProcessProgress DONE"
            # self.lblProgressText["text"] = "COMPLETE"
        """
    def updateProgressible(self, progress):
        strProgress = str(progress) + "% completed."
        arrInfo = [strProgress]
        self.progressible.updateProgress(progress, arrInfo)

    def prepareData(self, tests):

        if len(tests) == 0:
            tkMessageBox.showerror("Error: Empty queue", "Queue is empty. Please queue a test.")
            return "break"
            # return -1
            # self.listQueryDataB.delete(0, END)
        i = 0

        chiTest = ChiTest.getInstance()  # Initialize singleton

        for test in tests:
            fileNames = []
            if (test['Type'] == 'Sample vs Sample'):
                i += 1
                # [1] pre-process : make file names
                for dataset in test['Datasets']:  # For each sample pairs in queue
                    FS.convertDatasetValuesToGroups(dataset, features)
                    fileName = FS.makeFileName(
                        dataset)  # TODO This makes the intermediate tables based on the selected features
                    # print ("GENERATED FILENAME: " + str(fileName))
                    FS.writeCSVDict(fileName, dataset['Data'])
                    fileNames.append(fileName)
                # [2] make updated-variables file
                if not (os.path.isfile("Updated-Variables.csv")):
                    FS.makeUpdatedVariables(features, "Updated-Variables.csv")

                # [3] perform chi-square test
                # saveFile = ct.chiTest(fileNames)
                saveFile = chiTest.chiTest(fileNames)

                print ("saveFile is " + str(saveFile))

                # tempString = "Chi-test complete. " + str(i) + "/" + str(len(tests)) + "complete."
                # self.listQueryDataB.insert(END, tempString) #### TODO Put this somewhere else (CONSOLE)
                # removeFiles(fileNames) # TODO This removes the intermediate tables
        tkMessageBox.showinfo("Test Queue Complete", "All of the tests in the queue have been completed.")
        return "break"

    def performCrossProcess(self, dataset, features):
        pass

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


