"""
{Description}
Contains constant values used by the Output Module in OutputModule.py
TODO : Separate export functions from various scripts into a single script called OutputModule.py
"""
__author__ = "Candy"
__copyright__ = "Copyright 2019, TE3D House"


# import enum

class ChiTest:
    # Singleton
    __instance = None

    # Properties
    HEADER_feature = "Feature"
    HEADER_question = "Question"
    HEADER_chiValue = "Chi"
    HEADER_highLow = "Higher Or Lower"
    HEADER_dof = "Degrees of Freedom"
    HEADER_cutOff = "Cut-off"
    HEADER_isSignificant = "Is significant"


    COLUMN_HEADERS = [HEADER_feature,
                      HEADER_question,
                      HEADER_chiValue,
                      HEADER_highLow,
                      HEADER_dof,
                      HEADER_cutOff,
                      HEADER_isSignificant]

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ChiTest.__instance == None:
            ChiTest()
        return ChiTest.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ChiTest.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ChiTest.__instance = self

    def getHeaderIndex(self, columnName):
        return self.COLUMN_HEADERS.index(columnName)

