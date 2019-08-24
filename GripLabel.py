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
import Color_support as CS
import UI_support as US
import Icon_support as IS


class GripLabel:

    def __init__(self, parentFrame):
        self.top = parentFrame

        # add grip on top of parentFrame
        strRootWidth = str(FS.rootWidth)
        strRootHeight = str(FS.rootHeight)
        strGripHeight = str(FS.gripHeight)
        FS.rootHeight = str(strRootHeight + strGripHeight)
        self.top.geometry(strRootWidth + "x" + strRootHeight)

        self.grip = self.createGrip(parentFrame)
        self.btnClose = self.createGripButtons(self.grip)

        FS.redraw(self.grip)
        borderColor = CS.L_GRAY
        FS.emborder(self.grip, 0, 0, self.grip.winfo_width() - 1, self.grip.winfo_height() - 1,
                    [True, True, True, True],
                    [borderColor, borderColor, borderColor, borderColor])

    def createGrip(self, parentFrame):

        parentFrame.update()
        gripWidth = parentFrame.winfo_width()
        gripHeight = FS.gripHeight

        # create grip label
        # grip = Label(self.top, bitmap = "gray25")
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

        offset = 5
        iconSize = (parentHeight - offset, parentHeight - offset)
        im = PIL.Image.open(IS.TAB_ICO_CROSS).resize(iconSize, PIL.Image.ANTIALIAS)
        icoClose = PIL.ImageTk.PhotoImage(im)
        button.configure(image = icoClose)
        button.image = icoClose  # < ! > Required to make images appear



        # button.bind("<ButtonRelease-1>", self.onTopClose)
        button.bind("<Button-1>", lambda event: self.onTopClose())



        return button

    def onTopClose(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.top.destroy()
            self.top = None
        return "break"

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

    """ GETTERS """
    def getGrip(self):
        return self.grip