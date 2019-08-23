
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


import SystematicFiltering_VIEW as VIEW

class SystematicFiltering:
    def __init__(self, root):
        self.root = root
        self.type = 0
        self.maxType = 2
        self.threadCrossProcess = None

        self.winTop, self.parentFrame = self.initializeWindow(root)

        self.view = VIEW.SystematicFiltering_View(self.parentFrame)


    def initializeWindow(self, root):
        top = Toplevel(root)
        top.protocol("WM_DELETE_WINDOW", onTopClose)
        top.resizable(0, 0)

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.style.configure('.', font = "TkDefaultFont")

        # top.geometry("1000x700+222+39")
        top.geometry("700x300")
        top.title("Systematic Filtering")


        parentFrame = LabelFrame(top)
        parentFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)


        return top, parentFrame


def onTopClose():
    print "onTopClose"