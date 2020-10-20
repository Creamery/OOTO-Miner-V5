
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

import tkMessageBox
import SampleVsSample as svs
import os
import numpy as np
import Color_support as CS
from collections import Counter

import csv
import copy


gripHeight = 25

rootWidth = 1000
rootHeight = 700
rootTabWidth = 50

sfWidth = 480
sfHeight = 300


headerWidth = 100  # blue header
headerHeight = 23
stripeWidth = 0  # pink stripe
stripeHeight = headerHeight

commandsHeight = 60

arrQueryCriticalValue = ["0.80", "0.90", "0.95", "0.98", "0.99"]
arrQueryCriticalValueMapping = {"0.80": 1.28, "0.90": 1.645, "0.95": 1.96, "0.98": 2.33, "0.99": 2.58}


def checkKey(dictionary, key):
    if key in dictionary.keys():
        return True
    else:
        return False


"""
Reads features and their responses from the Variable Description file
"""
def readFeatures(filename, varMark):
    features = []
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                if (row[0] == varMark):
                    new_feature = {'Description': row[2], 'Code': row[1], 'Responses': []}
                    features.append(new_feature)
                else:
                    new_response = {'Group': row[0], 'Code': row[1], 'Description': row[2]}
                    new_feature['Responses'].append(new_response)
        return features
    except:
        return []


"""
Reads a .csv file and returns a list of dictionaries where the header of the file 
has all of the dictionary keys
"""
def readCSVDict(filename):
    rows = csv.DictReader(open(filename))
    return rows


"""
Saves the dataset as a .csv file
"""
def saveDatasetFile(dataset):
    fileName = makeFileName(dataset)
    writeCSVDict(fileName, dataset['Data'])
    return fileName


"""
Writes a list of dictionaries into a .csv file
"""
def writeCSVDict(filename, dataset):
    with open(filename, 'wb') as f:
        w = csv.DictWriter(f, dataset[0].keys())
        w.writeheader()
        w.writerows(dataset)


"""
Writes a set of rows into a .csv file given the filename
"""
def writeOnCSV(rows, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

"""
Returns a new dataset by filtering from the old one based on a feature and its selected values
"""

def filterDataset(dataset, feature, responses):
    new_data = []
    for record in dataset['Data']:
        for response in responses:
            if record[feature['Code']] == response['Code']:
                new_data.append(copy.deepcopy(record))
                break

    return new_data

"""
For every feature, each value falls into a group.
Each value in the dataset gets converted to its corresponding group.

If a value in the dataset does not exist in the feature values in the variable description,
its group is automatically assigned to -1.

If a feature in the dataset does not exist in the variable description, assign that value to -1.
"""
def convertDatasetValuesToGroups(dataset, features):
    # response['Code'] == record[self.datasetA['Feature']['Code']] for response in self.datasetA['Selected Responses']
    for record in dataset['Data']:
        for feature in features:
            converted = False
            if feature['Code'] in record.keys():  # If the feature code exists in the record
                for response in feature['Responses']:
                    if record[feature['Code']] == response['Code']:
                        record[feature['Code']] = response['Group']
                        converted = True
                if not converted:
                    record[feature['Code']] = '-1.0'
            else:
                record[feature['Code']] = '-1.0'
    return dataset


"""
Remove the files given their filenames.
"""
def removeFiles(fileNames):
    for fileName in fileNames:
        os.remove(fileName)


"""
Returns filename of the dataset based on the features it was filtered by and selected values for 
each feature
"""
def makeFileName(dataset):
    fileName = ""

    for filterFeature in dataset['Filter Features']:
        featureCode = copy.deepcopy(filterFeature['Code'])
        for i in range(0, len(filterFeature['Selected Responses'])):
            if i == 0:
                fileName = str(fileName + str(featureCode) + " ")
                fileName = fileName + "["

            fileName = fileName + filterFeature['Selected Responses'][i]['Code']

            if i == (len(filterFeature['Selected Responses']) - 1):
                fileName = fileName + "]"
            else:
                fileName = fileName + " "

        # fileName = str(fileName + ".csv")
    # fileName = str(fileName + ".csv")

    return fileName


"""
Writes converted features (where the values are converted to their groups)
into a csv file
"""
def makeUpdatedVariables(features, fileName):
    with open(fileName, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter = ',')
        for feature in features:
            featureRow = []
            featureRow.append('^')
            featureRow.append(feature['Code'])
            featureRow.append(feature['Description'])
            # Write that featureRow
            writer.writerow(featureRow)
            groups = []
            for response in feature['Responses']:
                responseRow = []
                if response['Group'] not in groups:
                    groups.append(response['Group'])
                    responseRow.append(response['Group'])
                    responseRow.append('Group ' + response['Group'])
                    # Write that responseRow
                    writer.writerow(responseRow)


"""
Concantenates values of a list into a string using a delimiter
Example:
if delimiter is ':'
[1,2,3] -> '1:2:3'
['a',2,'x'] -> 'a:2:x'
"""
def concatListToString(lst, delimiter):
    listString = ""
    for i in range(0, len(lst)):
        if (i == (len(lst) - 1)):
            listString = listString + str(lst[i])
        else:
            listString = listString + str(lst[i]) + delimiter

    return listString


"""
Concatenates all of the focus feature values together into a string
"""
def getFocusFeatureValues(selectedFocusFeature, selectedFocusFeatureValues):
    allValues = ""
    selectedValues = ""
    responseCodes = []

    for response in selectedFocusFeature['Responses']:
        responseCodes.append(response['Code'])

    allValues = concatListToString(responseCodes, ':')
    selectedValues = concatListToString(selectedFocusFeatureValues, ':')

    return allValues, selectedValues


"""
Splits an array retrieved from a listbox based on a delimiter, and appends to a new array
which element of the split array given an index. The new array will be returned.
"""
def parseListBoxValues(raw_arr, delimiter, index):
    proc_arr = []
    for x in raw_arr:
        temp = x.split(delimiter)
        proc_arr.append(temp[index])
    return proc_arr


"""
Selects the values of the focus feature
and calculates the proportion of those values
and the total
"""
def setFocusFeatureValues(listBox, dataset, selectedItems, label, isWarn):
    datasets = []
    allValues = []

    listBox.selection_clear(0, END)  # Deselect all
    for i in selectedItems:  # Select items specified in selectedItems
        # print ("i is " + str(i))
        listBox.selection_set(i)

    tempAV = listBox.get(0, END)
    tempSV = [listBox.get(i) for i in listBox.curselection()]

    allValuesRaw = parseListBoxValues(tempAV, "|", 4)
    selectedValues = parseListBoxValues(tempSV, "|", 4)

    for val in allValuesRaw:
        for response in dataset['Focus Feature']['Responses']:
            if response['Code'] == val and response['Group'] != '-1':
                allValues.append(val)
                break

    # print str(allValues)

    if allValues != []:
        dataset['Focus Feature']['All Values'] = allValues
        dataset['Focus Feature']['Selected Values'] = selectedValues

        datasets.append(dataset)
        svs.getTotalsAndProportions(datasets, allValues, selectedValues)
        label.configure(text = "Frequency: " + str(datasets[0]['Proportion']) + " , Proportion: " + str(
            round(datasets[0]['ProportionPercent'] * 100, 2)) + "%" + ", Total: " + str(datasets[0]['Total']))

        # TODO Remove the commented code below, eventually
        # if (isWarn is True and set(allValues) == set(selectedValues)):
        #     tkMessageBox.showwarning("Z-Test Warning",
        #                              "WARNING: You selected all of the valid values of " + dataset['Focus Feature'][
        #                                  'Code'] + " (those that are not in group -1). Z-Test will not work if all valid values are selected.")


"""
Verifies if the focus features and their selected values for datasets 1 and 2 are the same.
"""
def isSameFocusFeat(dataset1, dataset2, selectedValD1, selectedValD2):
    print selectedValD1
    print selectedValD2
    if (dataset1['Focus Feature'] == dataset2['Focus Feature']):
        if (np.array_equal(selectedValD1, selectedValD2)):
            return 1
        else:
            tkMessageBox.showerror('Error: Unequal values', 'Selected values on both datasets are not equal.')
            return -1
    else:
        tkMessageBox.showerror('Error: Unequal feature', 'Feature code on both datasets are not equal.')
        return -1


"""
Set selected dataset values for that dataset. 
"""
def selectDatasetValues(evt, dataset):
    global populationDir_gl

    listbox = evt.widget
    selectedValues = [listbox.get(i) for i in listbox.curselection()]
    datasetCount = 0

    if checkKey(dataset, 'Feature'):  #### TODO in DB B

        dataset['Feature']['Selected Responses'] = []

        for sv in selectedValues:
            responseArr = sv.split(" - ")
            for response in dataset['Feature']['Responses']:
                if response['Code'] == responseArr[0]:
                    selected_response = copy.deepcopy(response)
                    dataset['Feature']['Selected Responses'].append(selected_response)

        print str(len(dataset['Data']))
        for record in dataset['Data']:
            if any(response['Code'] == record[dataset['Feature']['Code']] for response in
                   dataset['Feature']['Selected Responses']):
                datasetCount += 1

    # labelFeatCount.configure(text = str(datasetCount))
    return datasetCount



def getRelX(element):
    return float(element.place_info()['relx'])

def getRelY(element):
    return float(element.place_info()['rely'])

def getRelW(element):
    return float(element.place_info()['relwidth'])

def getRelH(element):
    return float(element.place_info()['relheight'])

def getW(element):
    return float(element.place_info()['width'])

def getH(element):
    return float(element.place_info()['height'])

def getX(element):
    return float(element.place_info()['x'])

def getY(element):
    return float(element.place_info()['y'])

def getInfoX(element):
    return float(element.winfo_x())

def getInfoY(element):
    return float(element.winfo_y())

def getInfoW(element):
    return float(element.winfo_width())

def getInfoH(element):
    return float(element.winfo_height())

def placeBelow(element, reference, offset = 0):
    element.update()
    reference.update()

    newY = reference.winfo_y() + reference.winfo_height()
    element.place(
        rely = 0, y = newY + offset
    )

def alignStart(element, reference, offset = 0):
    element.update()
    reference.update()

    newX = reference.winfo_x()
    element.place(
        relx = 0, x = newX + offset
    )

def centerWindow(window, reference = None, offsetX = 0, offsetY = 0):
    window.update()
    winWidth = window.winfo_width()
    winHeight = window.winfo_height()
    # print("winWidth " + str(winWidth))
    # print("winHeight " + str(winHeight))

    if reference is None:
        parentWidth = window.winfo_screenwidth()
        parentHeight = window.winfo_screenheight()
        newX = (parentWidth / 2) - (winWidth / 2)
        newY = (parentHeight / 2) - (winHeight / 2)
    else:
        reference.update()
        parentX = reference.winfo_x()
        parentY = reference.winfo_y()
        parentWidth = reference.winfo_width()
        parentHeight = reference.winfo_height()
        newX = parentX + ((parentWidth / 2) - (winWidth / 2))
        newY = parentY + ((parentHeight / 2) - (winHeight / 2))

    return (newX + offsetX), (newY + offsetY)

