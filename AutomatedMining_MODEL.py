
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
import Queue
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

            self.progress(self.winProgress)
            self.prog_bar.start()
            self.queue = Queue.Queue()
            ThreadedTask(self.queue).start()
            self.winProgress.after(100, self.process_queue)


    def progress(self, parentFrame):
        self.prog_bar = ttk.Progressbar(
            parentFrame, orient = "horizontal",
            length = 200, mode = "indeterminate"
            )
        self.prog_bar.pack(side=  TOP)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            print str(msg)
            # Show result of the task if needed

            self.prog_bar.stop()
            self.isProcessing = False
        except Queue.Empty:
            self.winProgress.after(100, self.process_queue)

class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        time.sleep(5)  # Simulate long running process
        self.queue.put("Task finished")