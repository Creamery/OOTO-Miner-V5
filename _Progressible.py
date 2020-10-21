

__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    This class serves as the super class for the progress bar.
    It is the bare minimum functionality needed for the
    progress bar to work.
    [Candy]
'''

class _Progressible:
    def __init__(self):
        self.__currentProgress = 0
        self.__currentPercent = 0
        self.__maxProgress = 1
        self.__maxPercent = 100
        self.__isComplete = False

    def resetProgress(self, maxProgress):
        self.__currentProgress = float(0)
        self.__currentPercent = float(0)
        self.__isComplete = False
        self.setMaxProgress(maxProgress)

    def updateProgress(self, percent, args = [""]):
        # self.setCurrentProgress(self.getCurrentProgress() + progress)
        self.setCurrentPercent(percent)
        progress = self.getMaxProgress() * (percent / self.getMaxPercent())

        # self.setCurrentPercent(progress)
        self.setCurrentProgress(progress)
        if self.getCurrentPercent() == self.getMaxPercent():
            self.completeProgress()

    def completeProgress(self):
        self.__isComplete = True

    " GETTERS "
    def getMaxProgress(self):
        return float(self.__maxProgress)

    def getMaxPercent(self):
        return float(self.__maxPercent)

    def getCurrentProgress(self):
        return float(self.__currentProgress)

    def getCurrentPercent(self):
        return float(self.__currentPercent)

    def getCurrentDecimal(self):
        return float(self.getCurrentPercent() * float(0.01))

    def isComplete(self):
        return self.__isComplete


    " SETTERS "
    ''' 
        The maximum width of the label that serves as
        the progress bar.
    '''
    def setMaxProgress(self, value):
        self.__maxProgress = float(value)

    def setCurrentProgress(self, value):
        if value > self.getMaxProgress():
            value - self.getMaxProgress()
        self.__currentProgress = float(value)

    def setCurrentPercent(self, value):
        self.__currentPercent = float(value)


