    def findFeature(self,
        entryFeat,
        listFeat,
        dataset,
        populationDatasetOriginal,
        isPrintingError = False,
        *args):
    
        global features

        # Here is how to get the value from entryFeatA
        featCode = entryFeat
        print "Entered feature code: " + featCode
        arrTempItems = []
        found = False
        hasFocusFeature = False

        # Get proper list of features from initial variable description
        for feature in features:
            if feature['Code'] == featCode:
                found = True
                for arg in args:
                    if arg == "Dataset_Feature":
                        dataset['Feature'] = copy.deepcopy(feature)
                        populationDatasetOriginal['Feature'] = copy.deepcopy(feature)

                    if arg == "Focus_Feature":
                        dataset['Focus Feature'] = copy.deepcopy(feature)
                        populationDatasetOriginal['Focus Feature'] = copy.deepcopy(feature)
                        hasFocusFeature = True
                for response in feature['Responses']:
                    tempResp = response['Code'] + " - " + response['Description']
                    arrTempItems.append(tempResp)
                break
        if not found and isPrintingError:
            tkMessageBox.showerror("Error: Feature not found", "Feature not found in Variable Descriptor. Try again.")

        # Getting the proportions and frequencies of each value (including invalid values) in the focus feature
        if hasFocusFeature == True:
            arrTempItems = []
            dataset['ColumnData'] = []
            populationDatasetOriginal['ColumnData'] = []
            for record in dataset['Data']:
                dataset['ColumnData'].append(record[featCode])
                populationDatasetOriginal['ColumnData'].append(record[featCode])
            c = Counter(dataset['ColumnData'])  # Counts the number of occurrences of each value of the focus feature

            countN = len(dataset['ColumnData'])  # N is the size of the dataset
            countn = 0  # n is the total number of values where their group is not -1

            notInGroupNega1 = []  # List that keeps track of the values whose group is not -1
            presentInData = []  # List of values that occurred at least once in the data

            for response in dataset['Focus Feature']['Responses']:
                for val in c:
                    if val == response['Code']:
                        presentInData.append(val)
                        if response['Group'] != '-1':
                            notInGroupNega1.append(val)
                            countn = countn + int(c[val])
                        break
            '''
                reminderN = "N = Total no. of records"
                remindern = "n = Total no. of records where Group is not -1\n"
                header = "Freq | p/N | p/n | Group | Code | Description"

                arrTempItems.append(reminderN)
                arrTempItems.append(remindern)
                arrTempItems.append(header)
                '''
            for response in dataset['Focus Feature']['Responses']:
                countP = 0
                print 'Value: ' + response['Code']
                print 'Frequency: ' + str(countP)
                print 'n:' + str(countn)
                print 'N:' + str(countN)

                if response['Code'] in presentInData:  # If the value has occurred in the data
                    countP = int(c[response['Code']])

                proportionOverN = round(countP / float(countN) * 100.0, 2)
                proportionOvern = round(countP / float(countn) * 100.0, 2)

                if response['Code'] not in notInGroupNega1:  # If the value is an invalid value or its group/class is -1
                    proportionOvern = proportionOvern * 0

                tempResp = str(format(countP, '04')) + " | " + str(format(proportionOverN, '05')) + "%(N) | " + str(
                    format(proportionOvern, '05')) + "%(n) | "
                isValidResponse = False
                for val in c:
                    if val == response['Code']:
                        isValidResponse = True
                        tempResp = tempResp + response['Group'] + " | " + response['Code'] + " | " + response[
                            'Description']
                        break
                if not isValidResponse:
                    if response['Code'] not in presentInData:
                        tempResp = tempResp + response['Group'] + " | " + response['Code'] + " | " + response[
                            'Description']
                    else:
                        tempResp = tempResp + "-1" + " | " + response['Code'] + " | " + "INVALID VALUE"
                arrTempItems.append(tempResp)

        listFeat.delete(0, END)
        for A in arrTempItems:
            listFeat.insert(END, A)
