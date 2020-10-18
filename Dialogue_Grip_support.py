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


class DialogueGripLabel:

    def __init__(self, parentFrame, hasClose = True, showOverlay = True):
        self.top = parentFrame
        self.isDialogueHidden = False
        self.hasOverlay = False
        self.winOverlay = None
        self.root = None
        self.winOverlayWidth = None
        self.winOverlayHeight = None
        self.showOverlay = showOverlay
        self.isActive = True

        self.parentWidth = parentFrame.winfo_width()
        self.parentHeight = parentFrame.winfo_height()

        # add grip on top of parentFrame
        self.strRootWidth = str(self.parentWidth)
        self.strRootHeight = str(self.parentHeight + FS.gripHeight)
        self.top.geometry(self.strRootWidth + "x" + self.strRootHeight)

        self.grip = self.createGrip(parentFrame)
        if hasClose:
            self.btnClose = self.createGripButtons(self.grip)

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
        self.winOverlayWidth = self.winOverlay.winfo_width()
        self.winOverlayHeight = self.winOverlay.winfo_height()

        if not self.showOverlay:
            self.hideOverlay()

    def resizeOverlay(self, x, y, width, height):
        self.winOverlayWidth = width
        self.winOverlayHeight = height

        strX = str(x)
        strY = str(y)
        strWidth = str(self.winOverlayWidth)
        strHeight = str(self.winOverlayHeight)
        self.winOverlay.geometry(strWidth + "x" + strHeight + "+" + strX + "+" + strY)

        if not self.showOverlay:
            self.hideOverlay()

    def unbindOverlay(self):
        self.root.unbind('<Configure>')

    def hideOverlay(self):
        self.showOverlay = False
        strHideWidth = str(0)
        strHideHeight = str(0)
        self.winOverlay.geometry(strHideWidth + "x" + strHideHeight)

    def showOverlay(self):
        self.showOverlay = True
        strShowWidth = str(self.winOverlayWidth)
        strShowHeight = str(self.winOverlayHeight)
        self.winOverlay.geometry(strShowWidth + "x" + strShowHeight)


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

    def createGripButtons(self, parentFrame):
        parentFrame.update()
        parentWidth = parentFrame.winfo_width()
        parentHeight = parentFrame.winfo_height()

        button = Button(parentFrame)
        button.place(x = parentWidth - parentHeight, y = 0,
                     width = parentHeight, height = parentHeight)

        button.configure(
            background = CS.SELECT_BG, foreground = CS.FG_COLOR,
            bd = 0, relief = FLAT, overrelief = FLAT)

        offset = 6
        iconSize = (parentHeight - offset, parentHeight - offset)
        im = PIL.Image.open(IS.TAB_ICO_CROSS).resize(iconSize, PIL.Image.ANTIALIAS)
        icoClose = PIL.ImageTk.PhotoImage(im)
        button.configure(image = icoClose)
        button.image = icoClose  # < ! > Required to make images appear

        # button.bind("<ButtonRelease-1>", self.onTopClose)
        button.bind("<Button-1>", lambda event: self.onTopClose())
        return button

    '''
        Minimize the window by setting its width and height to zero.
        Does not destroy the window.
    '''
    def hideDialogue(self):
        self.isDialogueHidden = True
        self.top.geometry(str(0) + "x" + str(0))
        self.hideOverlay()

    def showDialogue(self):
        self.isDialogueHidden = False
        self.top.geometry(self.strRootWidth + "x" + self.strRootHeight)

    def onTopClose(self):
        print("DIALOGUE GRIP CLOSED")
        self.hideDialogue()
        self.destroyOverlay()
        self.isActive = False
        self.top.destroy()
        self.top = None
        # return "break"

    def destroyOverlay(self):
        if self.hasOverlay:
            self.unbindOverlay()
            self.winOverlay.destroy()
            self.winOverlay = None

    """ Functions for draggable window """
    def startWinMove(self, event):
        if self.isActive:
            self.gripX = event.x
            self.gripY = event.y

    def stopWinMove(self, event):
        if self.isActive:
            self.top.x = None
            self.top.y = None

    def onWinMove(self, event):
        if self.isActive:
            deltaX = event.x - self.gripX
            deltaY = event.y - self.gripY
            x = self.top.winfo_x() + deltaX
            y = self.top.winfo_y() + deltaY
            self.top.geometry("+%s+%s" % (x, y))

    """ GETTERS """
    def getGrip(self):
        return self.grip

    def isHidden(self):
        return self.isDialogueHidden


