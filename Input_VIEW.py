
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"
'''
    The View class for the Input tab. It handles
    all UI generation for its tab.
    [Candy]
'''


try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk

    py3 = 0
except ImportError:
    import tkinter.ttk as ttk

    py3 = 1

import UI_support as US
import Color_support as CS
import Widget_support as WS

class Input_View:
    def __init__(self, parentFrame):
        # print()

        # Create the parent frame
        self.dataTabParentFrame = LabelFrame(parentFrame, bd = 0)
        self.dataTabParentFrame.place(
            relx = US.TAB_REL_X, rely = US.TAB_REL_Y,
            relwidth = US.TAB_REL_W, relheight = US.TAB_REL_H)
        self.dataTabParentFrame.configure(background = CS.TAB_BG_COLOR, foreground = CS.FG_COLOR)

        # Create the left separator
        # self.dataTabLeftSeparator = ttk.Separator(self.dataTabParentFrame, orient = VERTICAL)
        # self.dataTabLeftSeparator.place(relx = 0, rely = 0, relheight = 1)

        self.configureDatasetElements()
        self.configureVariableDescriptionElements()
        self.configureStartElements()
        self.configureSeparators(self.dataTabParentFrame)

    def configureSeparators(self, parentFrame):
        parentFrame.update()
        # region emborder for tab
        WS.emborder(parentFrame,
                    [0, 0, 1, None],
                    [False, False, False, True])
        # endregion emborder for tab

    ''' -> Elements under the DATASET ("Dataset") HEADER <- '''

    def configureDatasetElements(self):

        # Create the Dataset parent frame
        self.labelFrameDataset = LabelFrame(self.dataTabParentFrame, bd = 0)
        self.labelFrameDataset.configure(
            background = CS.DATASET_BG, foreground = CS.FG_COLOR, text = US.TITLE_DATASET)
        self.labelFrameDataset.place(
            relx = US.TAB_DATASET_REL_X, rely = US.TAB_DATASET_REL_Y + US.TAB_CHILD_PADDING_TOP,
            relwidth = US.TAB_DATASET_REL_W, relheight = US.TAB_DATASET_REL_H)

        # Create the Dataset element parent frame
        self.labelFrameDatasetElements = LabelFrame(self.labelFrameDataset, bd = 0)
        self.labelFrameDatasetElements.configure(
            background = CS.DATASET_BG, foreground = CS.FG_COLOR)
        self.labelFrameDatasetElements.place(
            relx = US.TAB_ELEMENT_REL_X, rely = 0.1,
            relwidth = US.TAB_ELEMENT_REL_W, relheight = 0.80)

        # DATASET ELEMENTS

        # Variable Description label
        self.labelInitialVarDesc = Label(self.labelFrameDatasetElements)
        self.labelInitialVarDesc.place(
            relx = US.TAB_3CHILD_LBL_REL_X, rely = US.TAB_3CHILD_LBL_REL_Y_SMALL,
            relwidth = US.TAB_3CHILD_LBL_REL_W, relheight = US.TAB_3CHILD_LBL_REL_H_SMALL)
        self.labelInitialVarDesc.configure(
            background = CS.DATASET_LBL_BG, foreground = CS.DATASET_LBL_FG,
            text = US.LBL_DATASET_VARDESC,
            disabledforeground = CS.FG_DISABLED_COLOR,
            bd = 1)

        # Previous values (1.1)
        prevLblRelX = float(self.labelInitialVarDesc.place_info()['relx'])
        prevLblRelY = float(self.labelInitialVarDesc.place_info()['rely'])
        prevLblRelW = float(self.labelInitialVarDesc.place_info()['relwidth'])
        prevLblRelH = float(self.labelInitialVarDesc.place_info()['relheight'])

        newRelX = US.TAB_3CHILD_LBL_REL_X + prevLblRelX + prevLblRelW

        # Variable Description entry
        self.entryInitialVarDesc = Entry(self.labelFrameDatasetElements)
        self.entryInitialVarDesc.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = US.TAB_3CHILD_ENTRY_REL_W, relheight = prevLblRelH)
        self.entryInitialVarDesc.configure(
            background = CS.DATASET_ENTRY_BG, foreground = CS.DATASET_ENTRY_FG,
            bd = 1,
            font = US.FONT_DEFAULT,
            disabledforeground = CS.FG_DISABLED_COLOR
        )

        # Previous values (1.2)
        prevEntryRelX = float(self.entryInitialVarDesc.place_info()['relx'])
        prevEntryRelW = float(self.entryInitialVarDesc.place_info()['relwidth'])
        prevEntryRelH = float(self.entryInitialVarDesc.place_info()['relheight'])

        newRelX = US.TAB_3CHILD_LBL_REL_X + prevEntryRelX + prevEntryRelW

        # Variable Description upload
        self.buttonInitialVarDesc = Button(self.labelFrameDatasetElements)
        self.buttonInitialVarDesc.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = US.TAB_3CHILD_BTN_REL_W, relheight = prevLblRelH)

        self.buttonInitialVarDesc.configure(
            background = CS.DATASET_BTN_BG, foreground = CS.DATASET_BTN_FG,
            text = US.BTN_DATASET_UPLOAD,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = CS.DATASET_BTN_BG_ACTIVE,
            activeforeground = CS.DATASET_BTN_FG_ACTIVE,
            disabledforeground = CS.FG_DISABLED_COLOR)
        # Previous values (1.3)
        prevBtnRelX = float(self.buttonInitialVarDesc.place_info()['relx'])
        prevBtnRelY = float(self.buttonInitialVarDesc.place_info()['rely'])
        prevBtnRelW = float(self.buttonInitialVarDesc.place_info()['relwidth'])
        prevBtnRelH = float(self.buttonInitialVarDesc.place_info()['relheight'])

        newRelY = US.TAB_3CHILD_LBL_REL_Y_SMALL + prevBtnRelY + prevBtnRelH

        # Population Dataset label
        self.labelInitialVarDesc = Label(self.labelFrameDatasetElements)
        self.labelInitialVarDesc.place(
            relx = prevLblRelX, rely = newRelY,
            relwidth = prevLblRelW, relheight = prevLblRelH)
        self.labelInitialVarDesc.configure(
            background = CS.VARDESC_LBL_BG, foreground = CS.VARDESC_LBL_FG,
            text = US.LBL_DATASET_POPULATION,
            disabledforeground = CS.FG_DISABLED_COLOR,
            bd = 1)

        # Population Dataset entry
        self.entryQueryPopulation = Entry(self.labelFrameDatasetElements)
        self.entryQueryPopulation.place(
            relx = prevEntryRelX, rely = newRelY,
            relwidth = prevEntryRelW, relheight = prevEntryRelH)
        self.entryQueryPopulation.configure(
            background = CS.VARDESC_ENTRY_BG, foreground = CS.VARDESC_ENTRY_FG,
            bd = 1,
            disabledforeground = CS.FG_DISABLED_COLOR)

        # Population Dataset upload
        self.buttonQueryPopulation = Button(self.labelFrameDatasetElements)
        self.buttonQueryPopulation.place(
            relx = prevBtnRelX, rely = newRelY,
            relwidth = prevBtnRelW, relheight = prevBtnRelH)
        self.buttonQueryPopulation.configure(
            background = CS.DATASET_BTN_BG, foreground = CS.DATASET_BTN_FG,
            text = US.BTN_DATASET_UPLOAD,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = CS.DATASET_BTN_BG_ACTIVE,
            activeforeground = CS.DATASET_BTN_FG_ACTIVE,
            disabledforeground = CS.FG_DISABLED_COLOR)

    ''' -> Elements under the VARIABLE DESCRIPTION ("Variable Description Generator") HEADER <- '''

    def configureVariableDescriptionElements(self):
        prevFrameRelY = float(self.labelFrameDataset.place_info()['rely'])
        prevFrameRelH = float(self.labelFrameDataset.place_info()['relheight'])
        newFrameRelY = US.TAB_VARDESC_REL_Y + prevFrameRelY + prevFrameRelH

        # Create the Variable Description Generator parent frame
        self.labelFrameVariableDescriptor = LabelFrame(self.dataTabParentFrame, bd = 0)
        self.labelFrameVariableDescriptor.configure(
            background = CS.VARDESC_BG, foreground = CS.FG_COLOR, text = US.TITLE_VARDESC)
        self.labelFrameVariableDescriptor.place(
            relx = US.TAB_VARDESC_REL_X, rely = newFrameRelY,
            relwidth = US.TAB_VARDESC_REL_W, relheight = US.TAB_VARDESC_REL_H)

        # Create the Variable Descriptor element parent frame
        self.labelFrameVarDescElements = LabelFrame(self.labelFrameVariableDescriptor, bd = 0)
        self.labelFrameVarDescElements.configure(
            background = CS.VARDESC_BG, foreground = CS.FG_COLOR)
        self.labelFrameVarDescElements.place(
            relx = US.TAB_ELEMENT_REL_X, rely = 0.1,
            relwidth = US.TAB_ELEMENT_REL_W, relheight = 0.80)

        # > VARDESC ELEMENTS

        # Variable File

        # Variable File label
        self.labelVariableFile = Label(self.labelFrameVarDescElements)
        self.labelVariableFile.place(
            relx = US.TAB_3CHILD_LBL_REL_X, rely = US.TAB_3CHILD_LBL_REL_Y_SMALL,
            relwidth = US.TAB_3CHILD_LBL_REL_W, relheight = US.TAB_3CHILD_LBL_REL_H_SMALL)
        self.labelVariableFile.configure(
            background = CS.VARDESC_LBL_BG, foreground = CS.VARDESC_LBL_FG,
            text = US.LBL_VARDESC_VARFILE,
            disabledforeground = CS.FG_DISABLED_COLOR,
            bd = 1)


        # Previous values (1.1)
        prevLblRelX = float(self.labelVariableFile.place_info()['relx'])
        prevLblRelY = float(self.labelVariableFile.place_info()['rely'])
        prevLblRelW = float(self.labelVariableFile.place_info()['relwidth'])
        prevLblRelH = float(self.labelVariableFile.place_info()['relheight'])

        newRelX = US.TAB_3CHILD_LBL_REL_X + prevLblRelX + prevLblRelW

        # Variable File entry
        self.entryVariableFile = Entry(self.labelFrameVarDescElements)
        self.entryVariableFile.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = US.TAB_3CHILD_ENTRY_REL_W, relheight = prevLblRelH)
        self.entryVariableFile.configure(
            background = CS.VARDESC_ENTRY_BG, foreground = CS.VARDESC_ENTRY_FG,
            bd = 1,
            disabledforeground = CS.FG_DISABLED_COLOR)

        # Previous values (1.2)
        prevEntryRelX = float(self.entryVariableFile.place_info()['relx'])
        prevEntryRelW = float(self.entryVariableFile.place_info()['relwidth'])
        prevEntryRelH = float(self.entryVariableFile.place_info()['relheight'])

        newRelX = US.TAB_3CHILD_LBL_REL_X + prevEntryRelX + prevEntryRelW

        # Variable File upload
        self.buttonVariableFile = Button(self.labelFrameVarDescElements)
        self.buttonVariableFile.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = US.TAB_3CHILD_BTN_REL_W, relheight = prevLblRelH)
        self.buttonVariableFile.configure(
            background = CS.VARDESC_BTN_BG, foreground = CS.VARDESC_BTN_FG,
            text = US.BTN_VARDESC_UPLOAD,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = CS.VARDESC_BTN_BG_ACTIVE,
            activeforeground = CS.VARDESC_BTN_FG_ACTIVE,
            disabledforeground = CS.FG_DISABLED_COLOR)

        # Previous values (1.3)
        prevBtnRelX = float(self.buttonVariableFile.place_info()['relx'])
        prevBtnRelY = float(self.buttonVariableFile.place_info()['rely'])
        prevBtnRelW = float(self.buttonVariableFile.place_info()['relwidth'])
        prevBtnRelH = float(self.buttonVariableFile.place_info()['relheight'])

        newRelY = US.TAB_3CHILD_LBL_REL_Y_SMALL + prevBtnRelY + prevBtnRelH

        # Values File label
        self.labelValuesFile = Label(self.labelFrameVarDescElements)
        self.labelValuesFile.place(
            relx = prevLblRelX, rely = newRelY,
            relwidth = prevLblRelW, relheight = prevLblRelH)
        self.labelValuesFile.configure(
            background = CS.VARDESC_LBL_BG, foreground = CS.VARDESC_LBL_FG,
            text = US.LBL_VARDESC_VALFILE,
            disabledforeground = CS.FG_DISABLED_COLOR,
            bd = 1)

        # Values File entry
        self.entryValuesFile = Entry(self.labelFrameVarDescElements)
        self.entryValuesFile.place(
            relx = prevEntryRelX, rely = newRelY,
            relwidth = prevEntryRelW, relheight = prevEntryRelH)
        self.entryValuesFile.configure(
            background = CS.VARDESC_ENTRY_BG, foreground = CS.VARDESC_ENTRY_FG,
            bd = 1,
            disabledforeground = CS.FG_DISABLED_COLOR)

        # Values File upload
        self.buttonValuesFile = Button(self.labelFrameVarDescElements)
        self.buttonValuesFile.place(
            relx = prevBtnRelX, rely = newRelY,
            relwidth = prevBtnRelW, relheight = prevBtnRelH)
        self.buttonValuesFile.configure(
            background = CS.VARDESC_BTN_BG, foreground = CS.VARDESC_BTN_FG,
            text = US.BTN_VARDESC_UPLOAD,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = CS.VARDESC_BTN_BG_ACTIVE,
            activeforeground = CS.VARDESC_BTN_FG_ACTIVE,
            disabledforeground = CS.FG_DISABLED_COLOR)

    ''' -> Elements under the START (" ") HEADER <- '''

    def configureStartElements(self):
        # START
        # Always update to reflect height and width values in winfo when using relheight/relwidth
        self.buttonValuesFile.update()
        self.labelFrameVariableDescriptor.update()

        # print "height " + str(self.buttonValuesFile.winfo_height())
        # print "width " + str(self.buttonValuesFile.winfo_width())

        buttonX = 0.5  # self.labelFrameVariableDescriptor.winfo_x()

        prevFrameRelY = float(self.labelFrameVariableDescriptor.place_info()['rely'])
        prevFrameRelH = float(self.labelFrameVariableDescriptor.place_info()['relheight'])
        buttonY = US.TAB_VARDESC_REL_Y + prevFrameRelY + prevFrameRelH

        buttonHeight = self.buttonValuesFile.winfo_height()
        buttonWidth = self.buttonValuesFile.winfo_width()

        self.buttonStartDatasetUpload = Button(self.dataTabParentFrame)
        self.buttonStartDatasetUpload.place(
            relx = buttonX, rely = buttonY,
            width = buttonWidth, height = buttonHeight, anchor = CENTER)
        self.buttonStartDatasetUpload.configure(
            background = CS.START_BTN_BG, foreground = CS.START_BTN_FG,
            text = US.BTN_START,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = CS.START_BTN_BG_ACTIVE, activeforeground = CS.START_BTN_FG_ACTIVE,
            disabledforeground = CS.FG_DISABLED_COLOR)



    ''' -> GETTERS <- '''
    def getButtonInitialVarDesc(self):
        return self.buttonInitialVarDesc

    def getButtonQueryPopulation(self):
        return self.buttonQueryPopulation

    def getButtonVariableFile(self):
        return self.buttonVariableFile

    def getButtonValuesFile(self):
        return self.buttonValuesFile

    def getButtonStartDatasetUpload(self):
        return self.buttonStartDatasetUpload

    def getEntryInitialVarDesc(self):
        return self.entryInitialVarDesc

    def getEntryVariableFile(self):
        return self.entryVariableFile

    def getEntryValuesFile(self):
        return self.entryValuesFile

    def getEntryQueryPopulation(self):
        return self.entryQueryPopulation