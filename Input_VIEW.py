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

import UI_support
import Color_support

class Input_View:
    def __init__(self, parentFrame):
        print()


        # Create the parent frame
        self.dataTabParentFrame = LabelFrame(parentFrame, bd = 0)
        self.dataTabParentFrame.place(
            relx = UI_support.TAB_REL_X, rely = UI_support.TAB_REL_Y,
            relwidth = UI_support.TAB_REL_W, relheight = UI_support.TAB_REL_H)
        self.dataTabParentFrame.configure(background = Color_support.TAB_BG_COLOR, foreground = Color_support.FG_COLOR)

        # Create the left separator
        self.dataTabLeftSeparator = ttk.Separator(self.dataTabParentFrame, orient = VERTICAL)
        self.dataTabLeftSeparator.place(relx = 0, rely = 0, relheight = 1)

        self.configureDatasetElements()
        self.configureVariableDescriptionElements()
        self.configureStartElements()


    ''' -> Elements under the DATASET ("Dataset") HEADER <- '''

    def configureDatasetElements(self):

        # Create the Dataset parent frame
        self.labelFrameDataset = LabelFrame(self.dataTabParentFrame, bd = 0)
        self.labelFrameDataset.configure(
            background = Color_support.DATASET_BG, foreground = Color_support.FG_COLOR, text = UI_support.TITLE_DATASET)
        self.labelFrameDataset.place(
            relx = UI_support.TAB_DATASET_REL_X, rely = UI_support.TAB_DATASET_REL_Y + UI_support.TAB_CHILD_PADDING_TOP,
            relwidth = UI_support.TAB_DATASET_REL_W, relheight = UI_support.TAB_DATASET_REL_H)

        # Create the Dataset element parent frame
        self.labelFrameDatasetElements = LabelFrame(self.labelFrameDataset, bd = 0)
        self.labelFrameDatasetElements.configure(
            background = Color_support.DATASET_BG, foreground = Color_support.FG_COLOR)
        self.labelFrameDatasetElements.place(
            relx = UI_support.TAB_ELEMENT_REL_X, rely = 0.1,
            relwidth = UI_support.TAB_ELEMENT_REL_W, relheight = 0.80)

        # DATASET ELEMENTS

        # Variable Description label
        self.labelInitialVarDesc = Label(self.labelFrameDatasetElements)
        self.labelInitialVarDesc.place(
            relx = UI_support.TAB_3CHILD_LBL_REL_X, rely = UI_support.TAB_3CHILD_LBL_REL_Y_SMALL,
            relwidth = UI_support.TAB_3CHILD_LBL_REL_W, relheight = UI_support.TAB_3CHILD_LBL_REL_H_SMALL)
        self.labelInitialVarDesc.configure(
            background = Color_support.DATASET_LBL_BG, foreground = Color_support.DATASET_LBL_FG,
            text = UI_support.LBL_DATASET_VARDESC,
            disabledforeground = Color_support.FG_DISABLED_COLOR,
            bd = 1)

        # Previous values (1.1)
        prevLblRelX = float(self.labelInitialVarDesc.place_info()['relx'])
        prevLblRelY = float(self.labelInitialVarDesc.place_info()['rely'])
        prevLblRelW = float(self.labelInitialVarDesc.place_info()['relwidth'])
        prevLblRelH = float(self.labelInitialVarDesc.place_info()['relheight'])

        newRelX = UI_support.TAB_3CHILD_LBL_REL_X + prevLblRelX + prevLblRelW

        # Variable Description entry
        self.entryInitialVarDesc = Entry(self.labelFrameDatasetElements)
        self.entryInitialVarDesc.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = UI_support.TAB_3CHILD_ENTRY_REL_W, relheight = prevLblRelH)
        self.entryInitialVarDesc.configure(
            background = Color_support.DATASET_ENTRY_BG, foreground = Color_support.DATASET_ENTRY_FG,
            bd = 1,
            font = UI_support.FONT_DEFAULT,
            disabledforeground = Color_support.FG_DISABLED_COLOR
        )

        # Previous values (1.2)
        prevEntryRelX = float(self.entryInitialVarDesc.place_info()['relx'])
        prevEntryRelW = float(self.entryInitialVarDesc.place_info()['relwidth'])
        prevEntryRelH = float(self.entryInitialVarDesc.place_info()['relheight'])

        newRelX = UI_support.TAB_3CHILD_LBL_REL_X + prevEntryRelX + prevEntryRelW

        # Variable Description upload
        self.buttonInitialVarDesc = Button(self.labelFrameDatasetElements)
        self.buttonInitialVarDesc.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = UI_support.TAB_3CHILD_BTN_REL_W, relheight = prevLblRelH)

        self.buttonInitialVarDesc.configure(
            background = Color_support.DATASET_BTN_BG, foreground = Color_support.DATASET_BTN_FG,
            text = UI_support.BTN_DATASET_UPLOAD,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = Color_support.DATASET_BTN_BG_ACTIVE,
            activeforeground = Color_support.DATASET_BTN_FG_ACTIVE,
            disabledforeground = Color_support.FG_DISABLED_COLOR)
        # Previous values (1.3)
        prevBtnRelX = float(self.buttonInitialVarDesc.place_info()['relx'])
        prevBtnRelY = float(self.buttonInitialVarDesc.place_info()['rely'])
        prevBtnRelW = float(self.buttonInitialVarDesc.place_info()['relwidth'])
        prevBtnRelH = float(self.buttonInitialVarDesc.place_info()['relheight'])

        newRelY = UI_support.TAB_3CHILD_LBL_REL_Y_SMALL + prevBtnRelY + prevBtnRelH

        # Population Dataset label
        self.labelInitialVarDesc = Label(self.labelFrameDatasetElements)
        self.labelInitialVarDesc.place(
            relx = prevLblRelX, rely = newRelY,
            relwidth = prevLblRelW, relheight = prevLblRelH)
        self.labelInitialVarDesc.configure(
            background = Color_support.VARDESC_LBL_BG, foreground = Color_support.VARDESC_LBL_FG,
            text = UI_support.LBL_DATASET_POPULATION,
            disabledforeground = Color_support.FG_DISABLED_COLOR,
            bd = 1)

        # Population Dataset entry
        self.entryQueryPopulation = Entry(self.labelFrameDatasetElements)
        self.entryQueryPopulation.place(
            relx = prevEntryRelX, rely = newRelY,
            relwidth = prevEntryRelW, relheight = prevEntryRelH)
        self.entryQueryPopulation.configure(
            background = Color_support.VARDESC_ENTRY_BG, foreground = Color_support.VARDESC_ENTRY_FG,
            bd = 1,
            disabledforeground = Color_support.FG_DISABLED_COLOR)

        # Population Dataset upload
        self.buttonQueryPopulation = Button(self.labelFrameDatasetElements)
        self.buttonQueryPopulation.place(
            relx = prevBtnRelX, rely = newRelY,
            relwidth = prevBtnRelW, relheight = prevBtnRelH)
        self.buttonQueryPopulation.configure(
            background = Color_support.DATASET_BTN_BG, foreground = Color_support.DATASET_BTN_FG,
            text = UI_support.BTN_DATASET_UPLOAD,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = Color_support.DATASET_BTN_BG_ACTIVE,
            activeforeground = Color_support.DATASET_BTN_FG_ACTIVE,
            disabledforeground = Color_support.FG_DISABLED_COLOR)

    ''' -> Elements under the VARIABLE DESCRIPTION ("Variable Description Generator") HEADER <- '''

    def configureVariableDescriptionElements(self):
        prevFrameRelY = float(self.labelFrameDataset.place_info()['rely'])
        prevFrameRelH = float(self.labelFrameDataset.place_info()['relheight'])
        newFrameRelY = UI_support.TAB_VARDESC_REL_Y + prevFrameRelY + prevFrameRelH

        # Create the Variable Description Generator parent frame
        self.labelFrameVariableDescriptor = LabelFrame(self.dataTabParentFrame, bd = 0)
        self.labelFrameVariableDescriptor.configure(
            background = Color_support.VARDESC_BG, foreground = Color_support.FG_COLOR, text = UI_support.TITLE_VARDESC)
        self.labelFrameVariableDescriptor.place(
            relx = UI_support.TAB_VARDESC_REL_X, rely = newFrameRelY,
            relwidth = UI_support.TAB_VARDESC_REL_W, relheight = UI_support.TAB_VARDESC_REL_H)

        # Create the Variable Descriptor element parent frame
        self.labelFrameVarDescElements = LabelFrame(self.labelFrameVariableDescriptor, bd = 0)
        self.labelFrameVarDescElements.configure(
            background = Color_support.VARDESC_BG, foreground = Color_support.FG_COLOR)
        self.labelFrameVarDescElements.place(
            relx = UI_support.TAB_ELEMENT_REL_X, rely = 0.1,
            relwidth = UI_support.TAB_ELEMENT_REL_W, relheight = 0.80)

        # > VARDESC ELEMENTS

        # Variable File

        # Variable File label
        self.labelVariableFile = Label(self.labelFrameVarDescElements)
        self.labelVariableFile.place(
            relx = UI_support.TAB_3CHILD_LBL_REL_X, rely = UI_support.TAB_3CHILD_LBL_REL_Y_SMALL,
            relwidth = UI_support.TAB_3CHILD_LBL_REL_W, relheight = UI_support.TAB_3CHILD_LBL_REL_H_SMALL)
        self.labelVariableFile.configure(
            background = Color_support.VARDESC_LBL_BG, foreground = Color_support.VARDESC_LBL_FG,
            text = UI_support.LBL_VARDESC_VARFILE,
            disabledforeground = Color_support.FG_DISABLED_COLOR,
            bd = 1)


        # Previous values (1.1)
        prevLblRelX = float(self.labelVariableFile.place_info()['relx'])
        prevLblRelY = float(self.labelVariableFile.place_info()['rely'])
        prevLblRelW = float(self.labelVariableFile.place_info()['relwidth'])
        prevLblRelH = float(self.labelVariableFile.place_info()['relheight'])

        newRelX = UI_support.TAB_3CHILD_LBL_REL_X + prevLblRelX + prevLblRelW

        # Variable File entry
        self.entryVariableFile = Entry(self.labelFrameVarDescElements)
        self.entryVariableFile.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = UI_support.TAB_3CHILD_ENTRY_REL_W, relheight = prevLblRelH)
        self.entryVariableFile.configure(
            background = Color_support.VARDESC_ENTRY_BG, foreground = Color_support.VARDESC_ENTRY_FG,
            bd = 1,
            disabledforeground = Color_support.FG_DISABLED_COLOR)

        # Previous values (1.2)
        prevEntryRelX = float(self.entryVariableFile.place_info()['relx'])
        prevEntryRelW = float(self.entryVariableFile.place_info()['relwidth'])
        prevEntryRelH = float(self.entryVariableFile.place_info()['relheight'])

        newRelX = UI_support.TAB_3CHILD_LBL_REL_X + prevEntryRelX + prevEntryRelW

        # Variable File upload
        self.buttonVariableFile = Button(self.labelFrameVarDescElements)
        self.buttonVariableFile.place(
            relx = newRelX, rely = prevLblRelY,
            relwidth = UI_support.TAB_3CHILD_BTN_REL_W, relheight = prevLblRelH)
        self.buttonVariableFile.configure(
            background = Color_support.VARDESC_BTN_BG, foreground = Color_support.VARDESC_BTN_FG,
            text = UI_support.BTN_VARDESC_UPLOAD,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = Color_support.VARDESC_BTN_BG_ACTIVE,
            activeforeground = Color_support.VARDESC_BTN_FG_ACTIVE,
            disabledforeground = Color_support.FG_DISABLED_COLOR)

        # Previous values (1.3)
        prevBtnRelX = float(self.buttonVariableFile.place_info()['relx'])
        prevBtnRelY = float(self.buttonVariableFile.place_info()['rely'])
        prevBtnRelW = float(self.buttonVariableFile.place_info()['relwidth'])
        prevBtnRelH = float(self.buttonVariableFile.place_info()['relheight'])

        newRelY = UI_support.TAB_3CHILD_LBL_REL_Y_SMALL + prevBtnRelY + prevBtnRelH

        # Values File label
        self.labelValuesFile = Label(self.labelFrameVarDescElements)
        self.labelValuesFile.place(
            relx = prevLblRelX, rely = newRelY,
            relwidth = prevLblRelW, relheight = prevLblRelH)
        self.labelValuesFile.configure(
            background = Color_support.VARDESC_LBL_BG, foreground = Color_support.VARDESC_LBL_FG,
            text = UI_support.LBL_VARDESC_VALFILE,
            disabledforeground = Color_support.FG_DISABLED_COLOR,
            bd = 1)

        # Values File entry
        self.entryValuesFile = Entry(self.labelFrameVarDescElements)
        self.entryValuesFile.place(
            relx = prevEntryRelX, rely = newRelY,
            relwidth = prevEntryRelW, relheight = prevEntryRelH)
        self.entryValuesFile.configure(
            background = Color_support.VARDESC_ENTRY_BG, foreground = Color_support.VARDESC_ENTRY_FG,
            bd = 1,
            disabledforeground = Color_support.FG_DISABLED_COLOR)

        # Values File upload
        self.buttonValuesFile = Button(self.labelFrameVarDescElements)
        self.buttonValuesFile.place(
            relx = prevBtnRelX, rely = newRelY,
            relwidth = prevBtnRelW, relheight = prevBtnRelH)
        self.buttonValuesFile.configure(
            background = Color_support.VARDESC_BTN_BG, foreground = Color_support.VARDESC_BTN_FG,
            text = UI_support.BTN_VARDESC_UPLOAD,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = Color_support.VARDESC_BTN_BG_ACTIVE,
            activeforeground = Color_support.VARDESC_BTN_FG_ACTIVE,
            disabledforeground = Color_support.FG_DISABLED_COLOR)

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
        buttonY = UI_support.TAB_VARDESC_REL_Y + prevFrameRelY + prevFrameRelH

        buttonHeight = self.buttonValuesFile.winfo_height()
        buttonWidth = self.buttonValuesFile.winfo_width()

        self.buttonStartDatasetUpload = Button(self.dataTabParentFrame)
        self.buttonStartDatasetUpload.place(
            relx = buttonX, rely = buttonY,
            width = buttonWidth, height = buttonHeight, anchor = CENTER)
        self.buttonStartDatasetUpload.configure(
            background = Color_support.START_BTN_BG, foreground = Color_support.START_BTN_FG,
            text = UI_support.BTN_START,
            bd = 1, relief = FLAT, overrelief = GROOVE,
            activebackground = Color_support.START_BTN_BG_ACTIVE, activeforeground = Color_support.START_BTN_FG_ACTIVE,
            disabledforeground = Color_support.FG_DISABLED_COLOR)



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