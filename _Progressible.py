


class _Progressible:
    def __init__(self):
        self.__currentProgress = 0
        self.__currentPercent = 0
        self.setMaxProgress(100)
        self.__isComplete = False

    def resetProgress(self):
        self.__currentProgress = float(0)
        self.__currentPercent = float(0)
        self.__isComplete = False

    def updateProgress(self, progress):
        self.setCurrentProgress(self.getCurrentProgress() + progress)
        self.setCurrentPercent(self.getCurrentProgress() / self.getMaxProgress())
        if self.getCurrentPercent() == 100:
            self.completeProgress()

    def completeProgress(self):
        self.__isComplete = True

    " GETTERS "
    def getMaxProgress(self):
        return float(self.__maxProgress)

    def getCurrentProgress(self):
        return float(self.__currentProgress)

    def getCurrentPercent(self):
        return float(self.__currentPercent)

    def isComplete(self):
        return self.__isComplete

    " SETTERS "
    def setMaxProgress(self, value):
        self.__maxProgress = float(value)

    def setCurrentProgress(self, value):
        self.__currentProgress = float(value)

    def setCurrentPercent(self, value):
        self.__currentPercent = float(value)
