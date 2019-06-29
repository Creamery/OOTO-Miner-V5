
import Tkinter as tk
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


# _FONT = "TkDefaultFont"
_FONT = "TkDefaultFont"
_FONT_VSMALL = 9
_FONT_SMALL = 10
_FONT_MED = 12
_FONT_LARGE = 14

FONT_DEFAULT = (_FONT, _FONT_VSMALL)
FONT_DEFAULT_BOLD = (_FONT, _FONT_VSMALL, "bold")


FONT_SMALL = (_FONT, _FONT_SMALL)
FONT_SMALL_BOLD = (_FONT, _FONT_SMALL, "bold")

FONT_VSMALL = (_FONT, _FONT_VSMALL)
FONT_VSMALL_BOLD = (_FONT, _FONT_VSMALL, "bold")


FONT_MED = (_FONT, _FONT_MED)
FONT_MED_BOLD = (_FONT, _FONT_MED, "bold")
FONT_LARGE_BOLD = (_FONT, _FONT_LARGE, "bold")


# DATA tab entries


TITLE_DATASET = '''Dataset'''

LBL_DATASET_VARDESC = '''Variable Description:'''
BTN_DATASET_UPLOAD = '''Upload'''
LBL_DATASET_POPULATION = '''Population Dataset:'''

BTN_START = '''Start'''
TITLE_VARDESC = '''Variable Description Generator (Not yet functional)'''


LBL_VARDESC_VARFILE = '''Variable File:'''
BTN_VARDESC_UPLOAD = '''Choose File...'''

LBL_VARDESC_VALFILE = '''Values File:'''


# TEST tab entries
LBL_SELECT_NO_DATA = '''NO DATA'''
LBL_SELECT_READY = '''READY'''

# ABOUT tab entries
TITLE_ABOUT = '''About'''

LBL_ABOUT_VER = '''Version:'''
STR_ABOUT_VER = '''OOTO Miner v. 2.0.0'''

LBL_ABOUT_AUTHOR = '''Author:'''
STR_ABOUT_AUTHOR = '''TE3D House'''


LBL_ABOUT_AFFILIATION = '''Affiliation:'''
STR_ABOUT_AFFILIATION = '''De La Salle University - Laguna'''


# Constant values

# TAB Indices
TAB_DATA_INDEX = 0
TAB_TEST_INDEX = 1
TAB_INFO_INDEX = 2

# TABS Parent frame
TAB_REL_X = 0
TAB_REL_Y = 0
TAB_REL_W = 1
TAB_REL_H = 1

TAB_CHILD_PADDING_TOP = 0.02

# TABS Element
TAB_ELEMENT_REL_X = 0
TAB_ELEMENT_REL_W = 1

TAB_DATA_ELEMENT_REL_X = 0
TAB_DATA_ELEMENT_REL_W = 0.8

# TABS Child frames
TAB_CHILD_REL_X = 0.01
TAB_CHILD_REL_Y = 0.01
TAB_CHILD_REL_W = 0.98
TAB_CHILD_REL_H = 0.25 # (3 elements)

TAB_CHILD_REL_H_SMALL = 0.15 # (2 elements)


# TABS Child frames (DATASET)
TAB_DATASET_REL_X = 0.1
TAB_DATASET_REL_Y = 0.01
TAB_DATASET_REL_W = 0.80
TAB_DATASET_REL_H = TAB_CHILD_REL_H_SMALL # TAB_CHILD_REL_H


# TABS Child frames (VARDESC)
TAB_VARDESC_REL_X = TAB_DATASET_REL_X
TAB_VARDESC_REL_Y = TAB_DATASET_REL_Y
TAB_VARDESC_REL_W = TAB_DATASET_REL_W
TAB_VARDESC_REL_H = TAB_DATASET_REL_H



# TABS Child frames (TYPE) 04%
TAB_TEST_TYPE_REL_X = 0.005
TAB_TEST_TYPE_REL_Y = 0.01
TAB_TEST_TYPE_REL_W = 0.75
TAB_TEST_TYPE_REL_H = 0.02

# TABS Child frames (SELECT) 31 % # 28%
TAB_TEST_SELECT_REL_X = TAB_TEST_TYPE_REL_X
TAB_TEST_SELECT_REL_W = TAB_TEST_TYPE_REL_W
TAB_TEST_SELECT_REL_H = 0.28 + 0.03 # 0.37

# SELECT sub elements
# SELECT QUERY H - 12.9%
TAB_TEST_SELECT_QUERY_REL_X = 0.075
TAB_TEST_SELECT_QUERY_REL_Y = 0.1 # 0.01
TAB_TEST_SELECT_QUERY_REL_W = 0.85 # 0.90
TAB_TEST_SELECT_QUERY_REL_H = 0.125

TAB_TEST_SELECT_DATASET_REL_W = 0.4

TAB_TEST_SELECT_LBL_REL_X = 0
TAB_TEST_SELECT_LBL_REL_Y = 0
TAB_TEST_SELECT_LBL_REL_W = 0.35

TAB_TEST_SELECT_ENTRY_REL_W = 0.55
TAB_TEST_SELECT_BTN_REL_W = 0.10

# SELECT LIST BOX H - 55.5%
TAB_TEST_LISTBOX_QUERY_REL_X = TAB_TEST_SELECT_QUERY_REL_X #  * 2
TAB_TEST_LISTBOX_QUERY_REL_Y = 0 # 0.05
TAB_TEST_LISTBOX_QUERY_REL_W = TAB_TEST_SELECT_QUERY_REL_W # - (2 * TAB_TEST_SELECT_QUERY_REL_X)
TAB_TEST_LISTBOX_QUERY_REL_H = 0.5 # 0.555 # 0.595

# SELECT COMMANDS H - 23%
TAB_TEST_COMMANDS_QUERY_REL_Y = 0.035 + 0.0325 # TAB_TEST_LISTBOX_QUERY_REL_Y
TAB_TEST_COMMANDS_QUERY_REL_W = 0.70 # 0.95
TAB_TEST_COMMANDS_QUERY_REL_X = (1 - TAB_TEST_COMMANDS_QUERY_REL_W) / 2 # TAB_TEST_SELECT_QUERY_REL_X
TAB_TEST_COMMANDS_QUERY_REL_H = 0.21 # 0.23

TAB_TEST_SELECT_COUNT_REL_H = 0.55 # 0.64
TAB_TEST_SELECT_COUNT_TEXT_REL_H = 0.45 # 0.36

# TABS Child frames (FILTER) 30%

TAB_TEST_FILTER_REL_X = TAB_TEST_TYPE_REL_X
TAB_TEST_FILTER_REL_W = TAB_TEST_TYPE_REL_W
TAB_TEST_FILTER_REL_H = 0.36


# TITLE ELEMENTS
TAB_TEST_FILTER_TITLE_H = 30 # 25 # Note: This is Height not Relative Height
TAB_TEST_FILTER_TITLE_REL_H = 0.101# 0.1
TAB_TEST_PROCESS_TITLE_REL_H = 0.13


# FILTER sub elements
TAB_TEST_FILTER_QUERY_REL_W = TAB_TEST_SELECT_QUERY_REL_W - 0.01 # TAB_TEST_SELECT_QUERY_REL_W * 0.44 # 0.86
TAB_TEST_FILTER_QUERY_REL_X = (1 - TAB_TEST_FILTER_QUERY_REL_W) / 2 # 0.07
TAB_TEST_FILTER_QUERY_REL_Y = 0.075 # 0.095 # 0.065
TAB_TEST_FILTER_QUERY_REL_H = 0.097 # 0.095 # > 1

# FILTER QUERY
TAB_TEST_FILTER_QUERY_LBL_REL_X = 0
TAB_TEST_FILTER_QUERY_LBL_REL_Y = 0
TAB_TEST_FILTER_QUERY_LBL_REL_W = TAB_TEST_SELECT_LBL_REL_W * TAB_TEST_SELECT_DATASET_REL_W # 1 (* 0.4)

TAB_TEST_FILTER_QUERY_BTN_REL_W = 0.1 * TAB_TEST_SELECT_DATASET_REL_W # 1 (* 0.4)
TAB_TEST_FILTER_QUERY_ENTRY_REL_W = 1 - (TAB_TEST_FILTER_QUERY_BTN_REL_W + TAB_TEST_FILTER_QUERY_LBL_REL_W) # 1 Distribute remaining space here

# FILTER LIST

TAB_TEST_FILTER_QUERY_FEATURE_NAME_REL_H = 0.12 # > 1 # > 2

TAB_TEST_FILTER_LIST_DATA_REL_X = TAB_TEST_FILTER_QUERY_REL_X
TAB_TEST_FILTER_LIST_DATA_REL_W = TAB_TEST_FILTER_QUERY_REL_W # TAB_TEST_SELECT_QUERY_REL_W
TAB_TEST_FILTER_LIST_DATA_REL_H = 0.685 # > 1

TAB_TEST_FILTER_LISTBOX_REL_X = 0
TAB_TEST_FILTER_LISTBOX_REL_W = 0.5
TAB_TEST_FILTER_LISTBOX_REL_H = 0.65 # 0.88 # > 2

TAB_TEST_FILTER_LISTBOX_LIST_REL_X = 0
TAB_TEST_FILTER_LISTBOX_LIST_REL_W = 1
TAB_TEST_FILTER_LISTBOX_LIST_REL_H = 0.81 # 0.86 # > 3

TAB_TEST_FILTER_LISTBOX_STATUS_REL_X = 0
TAB_TEST_FILTER_LISTBOX_STATUS_REL_W = 1
TAB_TEST_FILTER_LISTBOX_STATUS_REL_H = 0.19 # 0.14 # > 3



# PROCESS sub elements
TAB_TEST_PROCESS_COMMANDS_REL_X = TAB_TEST_FILTER_QUERY_REL_X
TAB_TEST_PROCESS_COMMANDS_REL_Y = 0.12
TAB_TEST_PROCESS_COMMANDS_REL_W = TAB_TEST_FILTER_QUERY_REL_W
TAB_TEST_PROCESS_COMMANDS_REL_H = 0.57 # 0.67 # FULL is 0.77 # TITLE is 0.13


TAB_TEST_PROCESS_Z_TEST_TITLE_REL_X = 0.05 # 0.005
TAB_TEST_PROCESS_Z_TEST_TITLE_REL_W = 0.9 # 0.99
TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y = 0.005
TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H = 0.19


TAB_TEST_PROCESS_Z_TEST_SPINNER_ELEMENTS_REL_H = 0.355 # 0.35
TAB_TEST_PROCESS_Z_TEST_SPINNER_ELEMENTS_REL_Y = \
    (1 - \
    (TAB_TEST_PROCESS_Z_TEST_TITLE_REL_Y + TAB_TEST_PROCESS_Z_TEST_TITLE_REL_H + \
    TAB_TEST_PROCESS_Z_TEST_SPINNER_ELEMENTS_REL_H)) / 3 # Y padding


TEST_PROCESS_Z_TEST_PARENT = 0.3333 # 0.325
TEST_PROCESS_CHI_SQUARE_PARENT = 0.3333 # 0.35
TEST_PROCESS_RUN_PARENT = 0.3333 # 0.325
'''
TEST_PROCESS_Z_TEST_PARENT = 0.3525
TEST_PROCESS_CHI_SQUARE_PARENT = 0.3525
TEST_PROCESS_RUN_PARENT = 0.25
'''
TAB_TEST_PROCESS_QUEUE_TEXT_REL_H = TAB_TEST_SELECT_COUNT_TEXT_REL_H



# TABS Child frames (PROCESS) 28%
TAB_TEST_PROCESS_REL_X = TAB_TEST_TYPE_REL_X
TAB_TEST_PROCESS_REL_W = TAB_TEST_TYPE_REL_W
TAB_TEST_PROCESS_REL_H = 0.28 # 0.18

TAB_TEST_PROCESS_CONFIDENCE_TEXT_REL_H = TAB_TEST_SELECT_COUNT_TEXT_REL_H


# TABS Child frames (CONSOLE) W - 15% | H - 100%
TAB_TEST_CONSOLE_REL_Y = TAB_TEST_TYPE_REL_Y
TAB_TEST_CONSOLE_REL_W = (1 - (2 * TAB_TEST_TYPE_REL_X))  - TAB_TEST_TYPE_REL_W
TAB_TEST_CONSOLE_REL_H = 0.98


# TABS Child frames (ABOUT)
TAB_ABOUT_REL_X = 0.1
TAB_ABOUT_REL_Y = 0.01
TAB_ABOUT_REL_W = 0.80
TAB_ABOUT_REL_H = TAB_CHILD_REL_H


# TABS Child generic elements
TAB_CHILD_REL_H = 0.18 # 0.20 minus padding

# TABS Child elements (2 in a row: label | text)
TAB_CHILD_LBL_REL_X = 0.01
TAB_CHILD_LBL_REL_Y = 0.02
TAB_CHILD_LBL_REL_W = 0.18 # 0.20
TAB_CHILD_LBL_REL_H = TAB_CHILD_REL_H

TAB_CHILD_STR_REL_W = 0.78 # 0.80



# TABS Child elements (3 in a row: label | entry | button)
TAB_3CHILD_LBL_REL_X = 0.01
TAB_3CHILD_LBL_REL_Y = 0.02
TAB_3CHILD_LBL_REL_W = 0.18 # 0.20 - (2 * TAB_3CHILD_LBL_REL_X
TAB_3CHILD_LBL_REL_H = TAB_CHILD_REL_H

TAB_3CHILD_LBL_REL_Y_SMALL = 0.05
TAB_3CHILD_LBL_REL_H_SMALL = 0.33

TAB_3CHILD_ENTRY_REL_W = 0.60

TAB_3CHILD_BTN_REL_W = 0.18
# 0.20 - (2 * TAB_3CHILD_LBL_REL_X)




# TAB GENERAL SETTINGS
INSERT_WIDTH = 2
ENTRY_TAKE_FOCUS = True
ENTRY_FONT = FONT_MED_BOLD # FONT_VSMALL_BOLD


# SELECT
SELECT_LABEL_FONT = FONT_DEFAULT # FONT_VSMALL_BOLD
SELECT_LABEL_DATASETA_TEXT = '''Feature A'''
SELECT_LABEL_DATASETB_TEXT = '''Feature B'''

SELECT_LISTBOX_FONT = FONT_DEFAULT
SELECT_LISTBOX_RELIEF = GROOVE
SELECT_LISTBOX_BORDER = 1 # Won't work unless you change FLAT to something else (i.e. GROOVE)

SELECT_STATUS_LABEL_FONT = FONT_DEFAULT_BOLD
SELECT_STATUS_LABEL_RELIEF = FLAT
SELECT_STATUS_LABEL_BORDER = 0 # Won't work unless you change FLAT to something else (i.e. GROOVE)
SELECT_STATUS_LABEL_TOP_SEPARATOR = False

SELECT_ENTRY_JUSTIFY = CENTER

# FILTER
FILTER_LABEL_FONT = SELECT_LABEL_FONT
FILTER_LABEL_QUERY_FEATURE_TEXT = '''Filter Feature'''
FILTER_ENTRY_JUSTIFY = CENTER