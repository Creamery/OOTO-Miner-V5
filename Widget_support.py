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

import PIL.Image
import PIL.ImageTk

import Color_support as CS
import UI_support as US
import Icon_support as IS


def createDefaultFrame(parentFrame, wX, wY, wWidth, wHeight,
                       isRelative = [False, False], bgColor = CS.WHITE, fgColor = CS.D_BLUE):

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

def createDefaultHeader(parentFrame, wX, wY, wWidth, wHeight, wText = "",
                        isRelative = [False, False], bgColor = CS.D_BLUE, fgColor = CS.WHITE,
                        wFont = US.FONT_DEFAULT_BOLD):

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



def createDefaultStripe(parentFrame, wX, wY, wWidth, wHeight,
                        isRelative = [False, False],
                        texture = IS.TEXTURE_STRIPE_PINK):

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



