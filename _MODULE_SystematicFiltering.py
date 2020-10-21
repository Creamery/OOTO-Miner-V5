
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"

'''
    This is the main class that handles the SystematicFiltering_View
    and SystematicFiltering_Controller. It is the class instantiated by the driver.
    
    This module is responsible for the pop-up window when running
    the Automated Mining process. 
    [Candy]
'''


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


import Function_support as FS
import _Grip_support as GS

import _Widget_support as WS
import SystematicFiltering_VIEW as VIEW
import SystematicFiltering_CONTROLLER as CONTROLLER

import _Color_support as CS


class SystematicFiltering:
    def __init__(self, root, AMController):
        self.root = root

        # create overlay window
        self.winOverlay = WS.createOverlayWindow(root)
        self.winTop = self.__initializeWindow(root)  # WS.createDefaultToplevelWindow(root, [FS.sfWidth, FS.sfHeight], True, True)
        self.winTop.configure(bg = CS.WHITE)
        self.view = VIEW.SystematicFiltering_View(self.winTop)
        self.controller = CONTROLLER.SystematicFiltering_Controller(self.view, AMController)

        self.grip = self.__configureGrip(self.winTop, self.winOverlay, self.root)
        FS.placeBelow(self.view.getFrame(), self.grip.getGrip())
        self.controller.setParentGrip(self.grip)
        self.controller.bindParentGripButtons()

        self.__configureBorders(self.winTop)
        self.winOverlay.lower(self.winTop)

        self.__configureBind()


    # region initialization functions
    # region overlay functions
    def __handleConfigure(self, event):
        overlayBelowRoot = self.root.tk.eval('wm stackorder ' + str(self.winOverlay)+ ' isabove ' + str(self.root))
        if overlayBelowRoot:
            self.winOverlay.lift(self.root)
            self.root.lower(self.winOverlay)


        self.__configureUnbind()
        # set a short delay before re-binding to avoid infinite loops
        self.root.after(1, lambda: self.__configureBind())

    def __configureBind(self):
        self.root.bind("<Configure>", self.__handleConfigure)

    def __configureUnbind(self):
        self.root.unbind("<Configure>")
    # endregion overlay functions

    def __initializeWindow(self, root):
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


    '''
        Configure the draggable top bar.
    '''
    def __configureGrip(self, parentWindow, winOverlay, root):
        grip = GS.GripLabel(parentWindow, False, True, False)
        grip.assignOverlay(winOverlay, root)

        return grip

    def __configureBorders(self, parentFrame):
        borderWidth = parentFrame.winfo_width()
        borderHeight = parentFrame.winfo_height()
        borderColor = CS.D_GRAY
        WS.emborder(parentFrame,
                    [0, 0, borderWidth, borderHeight],
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor])
    # endregion initialization functions

