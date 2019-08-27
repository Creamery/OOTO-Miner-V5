def setFocusFeatureValues(listBox, dataset, selectedItems, label, isWarn):
    datasets = []
    allValues = []

    listBox.selection_clear(0, END)  # Deselect all
    for i in selectedItems:  # Select items specified in selectedItems
        # print ("i is " + str(i))
        listBox.selection_set(i)

    tempAV = listBox.get(0, END)
    tempSV = [listBox.get(i) for i in listBox.curselection()]

    allValuesRaw = parseListBoxValues(tempAV, " | ", 4)
    selectedValues = parseListBoxValues(tempSV, " | ", 4)

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

        if (isWarn is True and set(allValues) == set(selectedValues)):
            tkMessageBox.showwarning("Z-Test Warning",
                                     "WARNING: You selected all of the valid values of " + dataset['Focus Feature'][
                                         'Code'] + " (those that are not in group -1). Z-Test will not work if all valid values are selected.")





for filter in dataset[KS.FILTER_LIST]:
    datasetCopy = copy.deepcopy(dataset[KS.SAMPLES])
    filteredDataset = applyFilter(datasetCopy, filter)

    filteredDatasets.append( filteredDataset )


# given a list of dataset samples,
# apply all filter conditions specified in the filter,
# and return the new list of (filtered) samples
def applyFilter(self, datasetSamples, filter):
    filteredSamples = []
    for sample in datasetSamples:
        for featureID, value in filter.iteritems():
            sampleCode = sample[featureID]
            codeList = self.getCodeList(featureID, value)

            if sampleCode in codeList:
                filteredSamples.append(sample)

    return filteredSamples


# returns the included codes in the given group
def getCodeList(self, featureID, group):
    self.getFeatureDescription()[featureID][KS.RESPONSES][group][KS.CODE]

