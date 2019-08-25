
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

        # create overlay window
        self.winOverlay = WS.createOverlayWindow(root)
        self.winTop = self.initializeWindow(root)  # WS.createDefaultToplevelWindow(
            # root, [FS.sfWidth, FS.sfHeight], True, True)

        self.view = VIEW.SystematicFiltering_View(self.winTop)

        self.grip = self.configureGrip(self.winTop, self.winOverlay, self.root)
        FS.placeBelow(self.view.getFrame(), self.grip)

        self.configureBorders(self.winTop)
        self.winOverlay.lower(self.winTop)


        self.configureBind()
        WS.makeModal(self.winTop, self.root)  # make the window modal by setting root's wait_window

    # region overlay functions
    def handleConfigure(self, event):
        # print self.root.tk.eval('wm stackorder '+str(self.winOverlay)+' isabove '+ str(self.root))
        # print "Stackorder: " + self.root.tk.eval('wm stackorder '+str(self.root))
        overlayBelowRoot = self.root.tk.eval('wm stackorder ' + str(self.winOverlay)+ ' isabove ' + str(self.root))
        if overlayBelowRoot:
            self.winOverlay.lift(self.root)
            self.root.lower(self.winOverlay)


        self.configureUnbind()
        # set a short delay before re-binding to avoid infinite loops
        self.root.after(1, lambda: self.configureBind())

    def configureBind(self):
        self.root.bind("<Configure>", self.handleConfigure)

    def configureUnbind(self):
        self.root.unbind("<Configure>")
    # endregion overlay functions

    def initializeWindow(self, root):
        top = Toplevel(root)
        
        # remove title bar
        top.overrideredirect(True)
        top.after(10, lambda: WS.showInTaskBar(top))

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

    def configureGrip(self, parentWindow, winOverlay, root):
        grip = GS.GripLabel(parentWindow, False)
        grip.assignOverlay(winOverlay, root)

        return grip.getGrip()

    def configureBorders(self, parentFrame):
        borderWidth = parentFrame.winfo_width()
        borderHeight = parentFrame.winfo_height()
        borderColor = CS.D_GRAY
        WS.emborder(parentFrame,
                    [0, 0, borderWidth, borderHeight],
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor])
