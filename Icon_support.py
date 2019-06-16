
import sys
import os
import PIL.Image
import PIL.ImageTk



# Define values

PATH = os.path.dirname(os.path.abspath(__file__))
TAB_ICO_SIZE = (70 , 71) # +1 pixel in height for the bottom border in the icon



# Initialize tab icons

TAB_ICO_START = PATH+'\\_icons\\ico_default.png'
TAB_ICO_TEST = PATH+'\\_icons\\ico_default.png'
TAB_ICO_INFO = PATH+'\\_icons\\ico_default.png'