
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

# import tkMessageBox
import Color_support as CS
import Function_support as FS
import SystematicFiltering_VIEW as VIEW

class SystematicFiltering:
    def __init__(self, root = None):
        self.root = root
        self.type = 0
        self.maxType = 2

        self.threadCrossProcess = None
        self.lfProgressView = None

        self.winTop, self.parentFrame = self.initializeWindow(root)

        self.view = VIEW.SystematicFiltering_View(self.parentFrame)


    def initializeWindow(self, root):
        top = Toplevel(root)
        # top.transient(root)
        top.grab_set()
        # top.protocol("WM_DELETE_WINDOW", onTopClose)  # TODO return this
        top.resizable(0, 0)

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.style.configure('.', font = "TkDefaultFont")

        top.geometry("700x500")
        newX, newY = FS.centerWindow(top)
        top.geometry("700x500" + "+" + str(newX) + "+" + str(newY))

        top.title("Systematic Filtering")


        parentFrame = LabelFrame(top, bd = 0)
        parentFrame.configure(background = CS.WHITE)
        parentFrame.place(x = 0, y = 0, relwidth = 1, relheight = 1)


        return top, parentFrame


# def onTopClose():
#     print "onTopClose"
#     if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
#         global winTop
#         winTop.destroy()
#         winTop = None