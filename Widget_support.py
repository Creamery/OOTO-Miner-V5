import Tkinter as tk

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

from ctypes import windll

import PIL.Image
import PIL.ImageTk

import Color_support as CS
import UI_support as US
import Icon_support as IS
import Function_support as FS



GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

""" CREATORS """
# region creator functions

def createDefaultToplevelWindow(root, placeInfo = [800, 600],
                                isOverrideRedirect = True, isTaskbar = True):
    top = Toplevel(root)

    # remove title bar
    top.overrideredirect(isOverrideRedirect)
    if isTaskbar:
        top.after(10, lambda: showInTaskBar(top))

    top.transient(root)
    top.grab_set()

    # top.protocol("WM_DELETE_WINDOW", onTopClose)  # TODO return this
    top.resizable(0, 0)

    top.style = ttk.Style()
    if sys.platform == "win32":
        top.style.theme_use('winnative')

    top.style.configure('.', font = "TkDefaultFont")

    # center window
    strDimensions = str(placeInfo[0]) + "x" + str(placeInfo[1])
    top.geometry(strDimensions)
    root.update()
    newX, newY = FS.centerWindow(top, root, 0, -FS.gripHeight)
    top.geometry(strDimensions + "+" + str(newX) + "+" + str(newY))

    return top


def createOverlayWindow(root, bgColor = CS.BLACK):
    wX = root.winfo_x()
    wY = root.winfo_y()
    wWidth = root.winfo_width()
    wHeight = root.winfo_height()

    print "x y is " + str(wX) + " and " + str(wY)
    top = createDefaultToplevelWindow(root, [wWidth, wHeight], True, False)
    top.wm_attributes('-alpha', 0.7)

    label = Label(top)
    label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
    label.configure(background = bgColor)

    strDimensions = str(wWidth) + "x" + str(wHeight)
    root.update()
    top.geometry(strDimensions + "+" + str(wX) + "+" + str(wY))

    return top


def createDefaultFrame(parentFrame, placeInfo = [0, 0, 1, 1],
                       isRelative = [True, True], bgColor = CS.WHITE, fgColor = CS.D_BLUE):
    wX = placeInfo[0]
    wY = placeInfo[1]
    wWidth = placeInfo[2]
    wHeight = placeInfo[3]

    lfFrame = LabelFrame(parentFrame, bd = 0)
    lfFrame.place(x = wX, y = wY,)

    # region relative conditions
    if isRelative[0]: # width is relative
        lfFrame.place(relwidth = wWidth)
    else:
        lfFrame.place(width = wWidth)

    if isRelative[1]: # height is relative
        lfFrame.place(relheight = wHeight)
    else:
        lfFrame.place(height = wHeight)
    # endregion relative conditions


    lfFrame.configure(
        background = bgColor, foreground = fgColor,
        relief = FLAT)

    lfFrame.update()

    return lfFrame


def createDefaultHeader(parentFrame, wText = "", placeInfo = [0,0,1,1],
                        isRelative = [True, True], bgColor = CS.D_BLUE, fgColor = CS.WHITE,
                        wFont = US.FONT_DEFAULT_BOLD):
    wX = placeInfo[0]
    wY = placeInfo[1]
    wWidth = placeInfo[2]
    wHeight = placeInfo[3]

    lblHeader = Label(parentFrame)

    lblHeader.place(x = wX, y = wY,)
    # region relative conditions
    if isRelative[0]: # width is relative
        lblHeader.place(relwidth = wWidth)
    else:
        lblHeader.place(width = wWidth)

    if isRelative[1]: # height is relative
        lblHeader.place(relheight = wHeight)
    else:
        lblHeader.place(height = wHeight)
    # endregion relative conditions

    lblHeader.configure(
        background =bgColor, foreground = fgColor,
        bd = 0, relief = FLAT,
        text = wText,
        font = wFont,
    )

    lblHeader.update()
    return lblHeader


def createDefaultListbox(parentFrame,
                         selectMode = SINGLE,
                         placeInfo = [0,0,1,1],
                         isRelative = [True, True],
                         bg = CS.PALER_YELLOW,
                         bgSelect = CS.DISABLED_ORANGE,
                         fg = CS.D_BLUE,
                         fgSelect = CS.D_BLUE):
    wX = placeInfo[0]
    wY = placeInfo[1]
    wWidth = placeInfo[2]
    wHeight = placeInfo[3]

    listbox = Listbox(parentFrame)
    listbox.place(x = wX, y = wY)
    # region relative conditions
    if isRelative[0]: # width is relative
        listbox.place(relwidth = wWidth)
    else:
        listbox.place(width = wWidth)

    if isRelative[1]: # height is relative
        listbox.place(relheight = wHeight)
    else:
        listbox.place(height = wHeight)
    # endregion relative conditions

    listbox.configure(
        background = bg, foreground = fg,
        selectmode = selectMode, exportselection = "0",
        activestyle = "none",
        selectbackground = bgSelect,
        selectforeground = fgSelect,
        font = US.SELECT_LABEL_FONT,
        bd = 0,
        relief = GROOVE,
        highlightthickness = 0
    )

    listbox.update()
    return listbox


def createDefaultStripe(parentFrame, placeInfo = [0,0,1,1],
                        isRelative = [True, True],
                        texture = IS.TEXTURE_STRIPE_PINK):
    wX = placeInfo[0]
    wY = placeInfo[1]
    wWidth = placeInfo[2]
    wHeight = placeInfo[3]

    lblStripes = Label(parentFrame, bd = 0, relief = GROOVE)

    lblStripes.place(x = wX, y = wY,)
    # region relative conditions
    if isRelative[0]: # width is relative
        lblStripes.place(relwidth = wWidth)
    else:
        lblStripes.place(width = wWidth)

    if isRelative[1]: # height is relative
        lblStripes.place(relheight = wHeight)
    else:
        lblStripes.place(height = wHeight)
    # endregion relative conditions

    im = PIL.Image.open(texture)
    icoStripes = PIL.ImageTk.PhotoImage(im)
    lblStripes.configure(
        image = icoStripes,
        anchor = SW
    )
    lblStripes.image = icoStripes  # < ! > Required to make images appear

    lblStripes.update()
    return lblStripes


# endregion creator functions


""" UTILITIES """
# region utility functions
""" Returns the widget name """
def getWidgetName(widget):
    return str(widget).split(".")[-1]


""" A recursive call that updates all Widgets and their Widget children """
def redraw(parentFrame):
    parentFrame.update()

    for item in parentFrame.winfo_children():
        # print 'item type is ' + str(type(item))
        item.place(
            relx = 0, rely = 0, relwidth = 0, relheight = 0,
            x = item.winfo_x(), y = item.winfo_y(), width = item.winfo_width(), height = item.winfo_height())
        if isinstance(item, Widget):
            redraw(item)
        else:
            return "break"

    parentFrame.update()

def copyWidget(widget, parent):
    # parent = widget.nametowidget(widget.winfo_parent())

    widgetClass = widget.__class__
    clone = widgetClass(parent)


    # set configuration according to class
    copyWidgetConfiguration(clone, widget)
    return clone

def copyWidgetConfiguration(widget, reference):
    reference.update()
    widget.place(
        x = reference.winfo_x(),
        y = reference.winfo_y(),
        width = reference.winfo_width(),
        height = reference.winfo_height(),
    )

    if isinstance(widget, LabelFrame):
        widget.configure(
            bd = reference['bd'],
            background = reference['background']
        )

    elif isinstance(widget, Label):
        widget.configure(
            font = reference['font'],
            background = reference['background'], foreground = reference['foreground'],
            text = reference['text'],
            bd = reference['bd'], relief = reference['relief'],
            anchor = reference['anchor'],
            image = reference['image'],
        )
        widget.image = reference['image']  # < ! > Required to make images appear

    elif isinstance(widget, Button):
        widget.configure(
            background = reference['background'], foreground = reference['foreground'],
            activebackground = reference['activebackground'],
            highlightthickness = reference['highlightthickness'], padx = reference['padx'], pady = reference['pady'],
            bd = reference['bd'], relief = reference['relief'], overrelief = reference['overrelief'],
            anchor = reference['anchor'],
            image = reference['image']
        )
        widget.image = reference['image']  # < ! > Required to make images appear

    elif isinstance(widget, Entry):
        widget.configure(
            background = reference['background'], foreground = reference['foreground'],
            bd = reference['bd'],
            font = reference['font'], insertwidth = reference['insertwidth'],
            selectbackground = reference['selectbackground'],
            insertbackground = reference['insertbackground'],
            takefocus = reference['takefocus'], justify = reference['justify']
        )

    elif isinstance(widget, Listbox):
        widget.configure(
            background = reference['background'], foreground = reference['foreground'],
            selectmode = reference['selectmode'], exportselection = reference['exportselection'],
            activestyle = reference['activestyle'],
            selectbackground = reference['selectbackground'],
            selectforeground = reference['selectforeground'],
            font =reference['font'],
            bd = reference['bd'],
            relief = reference['relief'],
            highlightthickness = reference['highlightthickness']
        )

def emborder(parentFrame, placeInfo = [0, 0, None, None],
             conditions = [True, True, True, True], colors = [None, None, None, None]):
    # region handle defaults
    borderX = placeInfo[0]
    borderY = placeInfo[1]
    borderW = placeInfo[2]
    borderH = placeInfo[3]
    # use default color if not specified by the user
    colors = [CS.L_GRAY if color is None else color for color in colors]
    # use parentFrame width and height if not specified by the user
    if borderW is None:
        borderW = parentFrame.winfo_width()
    if borderH is None:
        borderH = parentFrame.winfo_height()
    # endregion handle defaults

    borderW = borderW - 1  # done so that the end borders won't get cut off
    borderH = borderH - 1  # done so that the end borders won't get cut off

    index = 0
    if conditions[index]:
        sepCommandTop = Label(parentFrame)
        sepCommandTop.place(
            x = borderX,
            y = borderY,
            width = borderW,
            height = 1)
        sepCommandTop.configure(background = colors[index])

    index = 2
    if conditions[index]:
        sepCommandBottom = Label(parentFrame)
        sepCommandBottom.place(
            x = borderX,
            y = borderY + borderH,
            width = borderW,
            height = 1)
        sepCommandBottom.configure(background = colors[index])

    index = 3
    if conditions[index]:
        sepCommandLeft = Label(parentFrame)
        sepCommandLeft.place(
            x = borderX,
            y = borderY,
            width = 1,
            height = borderH)
        sepCommandLeft.configure(background = colors[index])

    index = 1
    if conditions[index]:
        sepCommandRight = Label(parentFrame)
        sepCommandRight.place(
            x = borderX + borderW,
            y = borderY,
            width = 1,
            height = borderH)
        sepCommandRight.configure(background = colors[index])

""" Make the root window wait until the modal window is closed """
def makeModal(modalWindow, root):
    root.wait_window(modalWindow)  # make the window modal by setting root's wait_window


""" Allows windows to appear in taskbar when overideredirect is set to True """
def showInTaskBar(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

def enterSplashscreen(root):
    root.wm_attributes('-alpha', '0.0')
    # TODO show the window with splash image

def exitSplashscreen(root):
    root.wm_attributes('-alpha', '1.0')
    # TODO hide the window with splash image

# endregion utility functions

