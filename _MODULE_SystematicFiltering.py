
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
import Grip_support as GS
import Widget_support as WS
import SystematicFiltering_VIEW as VIEW


class SystematicFiltering:
    def __init__(self, root = None):
        self.root = root
        self.type = 0
        self.maxType = 2

        self.threadCrossProcess = None
        self.lfProgressView = None

        self.winTop = self.initializeWindow(root)
        self.view = VIEW.SystematicFiltering_View(self.winTop)

        self.grip = self.configureGrip(self.winTop)
        FS.placeBelow(self.view.getFrame(), self.grip)

        self.configureBorders(self.winTop)

    def initializeWindow(self, root):
        top = Toplevel(root)
        # remove title bar
        top.overrideredirect(True)
        top.after(10, lambda: FS.showInTaskBar(top))

        # top.transient(root)
        top.grab_set()
        # top.protocol("WM_DELETE_WINDOW", onTopClose)  # TODO return this
        top.resizable(0, 0)

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.style.configure('.', font = "TkDefaultFont")

        # center window
        strDimensions = str(FS.sfWidth) + "x" + str(FS.sfHeight)
        top.geometry(strDimensions)
        root.update()
        newX, newY = FS.centerWindow(top, root, 0, -FS.gripHeight)
        top.geometry(strDimensions + "+" + str(newX) + "+" + str(newY))

        top.title("Systematic Filtering")


        return top

    def configureGrip(self, parentWindow):
        grip = GS.GripLabel(parentWindow).getGrip()
        return grip

    def configureBorders(self, parentFrame):
        borderWidth = parentFrame.winfo_width()
        borderHeight = parentFrame.winfo_height()
        borderColor = CS.D_GRAY
        WS.emborder(parentFrame,
                    [0, 0, borderWidth, borderHeight],
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor])
