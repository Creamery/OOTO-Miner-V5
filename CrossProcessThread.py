import threading
import time


class CrossProcessThread(threading.Thread):
    def __init__(self, parentFrame, progressBar, lblText, lblValue):
        threading.Thread.__init__(self)
        self.winProgressBar = parentFrame
        self.pbProgressBar = progressBar
        self.lblProgressText = lblText
        self.lblProgressValue = lblValue
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
            self.lblProgressText["text"] = "COMPLETE"

    def process_queue(self):
        self.lblProgressValue = float(self.count)
        self.pbProgressBar["value"] = self.lblProgressValue
        self.lblProgressText["text"] = self.lblProgressValue

