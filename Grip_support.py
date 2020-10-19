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

import PIL.Image
import PIL.ImageTk
import tkMessageBox

import Function_support as FS
import Widget_support as WS
import Color_support as CS
import UI_support as US
import Icon_support as IS


class GripLabel:

    def __init__(self, parentFrame, hasPrompt = False, hasClose = True, hasBind = True):
        self.top = parentFrame
        self.hasPrompt = hasPrompt
        self.hasOverlay = False
        self.winOverlay = None
        self.root = None

        parentWidth = parentFrame.winfo_width()
        parentHeight = parentFrame.winfo_height()

        # add grip on top of parentFrame
        strRootWidth = str(parentWidth)
        strRootHeight = str(parentHeight + FS.gripHeight)
        self.top.geometry(strRootWidth + "x" + strRootHeight)

        self.grip = self.createGrip(parentFrame)
        if hasClose:
            self.btnClose = self.createGripButtons(self.grip, hasBind)

        WS.redraw(self.grip)
        borderColor = CS.D_GRAY
        WS.emborder(self.grip,
                    [0, 0, self.grip.winfo_width(), self.grip.winfo_height()],
                    [True, True, True, True],
                    [borderColor, borderColor, CS.L_GRAY, borderColor])


    def assignOverlay(self, overlay, root):
        self.hasOverlay = True
        self.root = root
        self.winOverlay = overlay
        # self.winOverlay.lower(self.top)
        # strDimensions = str(self.winOverlay.winfo_width()) + "x" + str(self.winOverlay.winfo_height())
        # self.winOverlay.geometry(strDimensions + "0+0")

    def unbindOverlay(self):
        self.root.unbind('<Configure>')

    def createGrip(self, parentFrame):

        parentFrame.update()
        gripWidth = parentFrame.winfo_width()
        gripHeight = FS.gripHeight

        # create grip label
        grip = LabelFrame(self.top, bd = 0)
        grip.place(x = 0, y = 0, width = gripWidth, height = gripHeight)
        grip.configure(background = CS.WHITE)

        # bind grip functionality
        grip.bind("<ButtonPress-1>", self.startWinMove)
        grip.bind("<ButtonRelease-1>", self.stopWinMove)
        grip.bind("<B1-Motion>", self.onWinMove)

        return grip

    def createGripButtons(self, parentFrame, hasBind):
        parentFrame.update()
        parentWidth = parentFrame.winfo_width()
        parentHeight = parentFrame.winfo_height()

        button = Button(parentFrame)
        button.place(x = parentWidth - parentHeight, y = 0,
                     width = parentHeight, height = parentHeight)

        button.configure(
            background = CS.WHITE, foreground = CS.FG_COLOR,
            bd = 0, relief = FLAT, overrelief = FLAT)

        offset = 6
        iconSize = (parentHeight - offset, parentHeight - offset)
        self.icoSize = iconSize
        im = PIL.Image.open(IS.TAB_ICO_CROSS).resize(iconSize, PIL.Image.ANTIALIAS)
        icoClose = PIL.ImageTk.PhotoImage(im)
        button.configure(image = icoClose)
        button.image = icoClose  # < ! > Required to make images appear

        # button.bind("<ButtonRelease-1>", self.onTopClose)
        if hasBind:
            button.bind("<Button-1>", lambda event: self.onTopClose())
        return button


    def onTopClose(self):
        print("GRIP CLOSED")
        if self.hasPrompt:
            if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
                self.destroyOverlay()
                self.top.destroy()
                self.top = None
            return "break"
        else:
            self.destroyOverlay()
            self.top.destroy()
            self.top = None

    def destroyOverlay(self):
        if self.hasOverlay:
            self.unbindOverlay()
            self.winOverlay.destroy()
            self.winOverlay = None

    """ Functions for draggable window """
    def startWinMove(self, event):
        self.gripX = event.x
        self.gripY = event.y

    def stopWinMove(self, event):
        self.top.x = None
        self.top.y = None

    def onWinMove(self, event):
        deltaX = event.x - self.gripX
        deltaY = event.y - self.gripY
        x = self.top.winfo_x() + deltaX
        y = self.top.winfo_y() + deltaY
        self.top.geometry("+%s+%s" % (x, y))

    """ GETTERS / SETTERS """
    def getGrip(self):
        return self.grip

    def getCloseButton(self):
        return self.btnClose

    def getIcoSize(self):
        return self.icoSize


