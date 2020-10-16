import csv
import math
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import chi2
import sys
import string

import xlsxwriter

from Table import Table
from clean import ColConverter
import Output_support as out
from collections import OrderedDict

import Loader_support as LS

class ChiTest:
    # Singleton
    __instance = None

    # Properties
    significance = 0
    degreeFreedom = 0
    # chiCritical = 0
    # rawCritical = 0

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


    def writeOnCSV(self, rows, filename):
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(rows)


    def writeonXLSX(self, rows, filename, header):
        wb = xlsxwriter.Workbook(filename, {'strings_to_numbers': True})
        wb.guess_types = True
        ws = wb.add_worksheet()

        # TODO Header constants
        sig_col = header.index("Is significant")
        cutoff_col = header.index("Cut-off")
        df_col = header.index("Degrees of Freedom")
        header_index = self.findHeader(rows, header)
        ws.write('A1', 'Probability(0.05/0.01/0.001)') # Change label to Significance, not Probability
        ws.write('B1', self.significance)  ### TODO - Change significance
        for row in range(0, len(rows)):
            for col in range(0, len(rows[row])):
                # If the element is under the Is Significant column and is not the header
                if (col == sig_col and row != header_index):
                    ws.write_formula(row + 1, col, "IF(C:C>F:F,1,0)")

                # Write the Cut-off
                elif (col == cutoff_col and row != header_index):
                    # ws.write_formula(row + 1, col,
                    #                  # "=IF(B1=0.05,IF(E:E=1,3.84,IF(E:E=2,5.99,-1)),IF(B1=0.01,IF(E:E=1,6.635,IF(E:E=2,9.21,-1)),IF(B1=0.001,IF(E:E=1,10.8,IF(E:E=2,13.8,-1)),-1)))")
                    #                  "=IF(B1=0.05,IF(E:E=1,3.84,IF(E:E=2,5.99,-1)),"
                    #                  "IF(B1=0.01,IF(E:E=1,6.635,IF(E:E=2,9.21,-1)),"
                    #                  "IF(B1=0.001,IF(E:E=1,10.8,IF(E:E=2,13.8,-1)),-1)))")

                    degreeFreedom = rows[row][df_col]
                    probability = 1 - self.significance
                    rawCritical = chi2.ppf(probability, degreeFreedom)  # Compute critical value
                    chiCritical = round(rawCritical, 3)  # Round critical value by 3 decimal places
                    ws.write(row + 1, col, str(chiCritical))

                # If the element is a list
                elif (isinstance(rows[row][col], list)):
                    # Write the first element of it
                    ws.write(row + 1, col, rows[row][col][0])

                elif (isinstance(rows[row][col], basestring)):
                    string = str(rows[row][col])
                    '''
                                    try:
                                            string.decode('utf8')
                                    except UnicodeDecodeError:
                                            string.decode('latin-1')
                                    '''
                    ws.write(row + 1, col, string)
                else:
                    try:
                        ws.write(row + 1, col, rows[row][col])
                    except TypeError:
                        ws.write(row + 1, col, "")
        try:
            wb.close()
        except UnicodeDecodeError:
            print 'Error in writing .xlsx file. Check your Variable Description for characters out of the UTF-8 character set.  Saving instead as .csv'
            self.writeOnCSV(rows, filename + '.csv')


    '''
    Returns index of the header in a set of rows
    '''


    def findHeader(self, rows, header):
        for i in range(0, len(rows)):
            if (rows[i][0] == header[0]):
                return i
        return -1


    def readHeader(self, filename):
        num = 0
        rows = []

        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            for row in readCSV:
                if (num == 0):
                    return row


    def readCSVDict(self, filename):
        f = open(filename, 'rU')
        rows = csv.DictReader(f)
        return rows


    def readCSVtoDouble(self, filename):
        num = 0
        rows = []

        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')

            for row in readCSV:
                if (num == 0):
                    header = row
                else:
                    rows.append([float(i) for i in row])
                num = num + 1
        return header, rows


    def readCSV(self, filename, isHead = True):
        rows = []
        count = 0
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            for row in readCSV:  # Iterate through each row in the dataset
                if (not (count == 0 and isHead)):  # If not the row is not the header
                    for i in range(0, len(row)):  # Iterate over the answers in each row
                        if (self.RepresentsInt(row[i])):
                            # print "REPRESENTS " + row[i]
                            temp = int(row[i])
                            row[i] = str(temp)

                        elif (self.RepresentsFloat(row[i])):
                            # print "REPRESENTS " + row[i]
                            temp = float(row[i])
                            temp = int(temp)
                            row[i] = str(temp)

                    rows.append(row)
                count = count + 1
        return rows


    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False


    def RepresentsFloat(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False


    def getPercentColumn(self, body, colIdx):
        total = 0
        percents = []
        boygirl = []
        for i in range(0, len(body)):
            total = total + int(body[i][colIdx])

        for i in range(0, len(body)):
            boygirl.append(body[i][colIdx])
            percents.append(float(float(body[i][colIdx]) / total))

        return percents, boygirl


    def getSumRows(self, rows):
        return np.sum(rows, axis = 1).reshape(-1, 1)


    def getProportions(self, rows, totals):
        proportions = np.copy(rows)
        proportions = proportions / totals.reshape(-1, 1)

        index = 0
        self.getStandardError(proportions, totals)
        return proportions


    def getStandardError(self, proportions, totals):
        return np.sqrt(proportions * (1 - proportions) / totals.reshape(-1, 1))


    def getProportionPerColumn(self, numpiRows):
        colSum = np.sum(numpiRows, axis = 0)
        return colSum


    def sortTableColumns(self, header, rows):
        newheader = header[1:]
        newheader = [str(i) for i in newheader]

        pihead = np.asarray(newheader[0:])
        pirows = np.asarray(rows)
        labelCols = pirows[:, 0]
        pirows = np.delete(pirows, 0, axis = 1)
        i = np.argsort(pihead)
        pirows = pirows[:, i]
        pihead = pihead[i]
        pirows = np.hstack((labelCols.reshape(-1, 1), pirows))

        return [header[0]] + [str(i) for i in pihead.tolist()], pirows.tolist()


    def doAccumulate(self, header, rows):
        newheader = [str(header[1]) + "+" + str(header[2])]
        newheader = [header[0]] + newheader

        # for i in range(3,len(header)-1):
        temp = ""
        for y in range(3, len(header) - 1):
            temp = temp + "+" + str(header[y])
        newheader.append(temp)

        print "new header"
        print newheader
        newrow = []

        for row in rows:
            temprow = []
            temprow.append(row[1] + row[2])
            # print "len of row"+str(len(row))
            # for i in range(3,len(row)-1):
            temp = 0
            for y in range(3, len(row) - 1):
                # print row[y]
                temp = temp + row[y]
            temprow.append(temp)
            # print "add"
            newrow.append([row[0]] + temprow)

        return newheader, newrow


    def readTableToFloat(self, table):
        rows = []
        for x in range(1, len(table.rows)):
            rows.append([float(i) for i in table.rows[x]])
        return table.rows[0], rows


    def doFile(self, table, fileNum, results, converter, z, H):
        header, rows = self.readTableToFloat(table)
        header, rows = self.sortTableColumns(header, rows)

        ## TODO Remove lol
        # print "Header after i killed it " + str(header)
        # print "diz are da header"
        # print header
        # print "diz are the rows"
        # print rows

        numpiRows = np.asarray(rows)
        labelCols = numpiRows[:, 0]
        numpiRows = np.delete(numpiRows, 0, axis = 1)

        if (len(numpiRows[0]) > 2 and numpiRows[0][0] == 0):
            numpiRows = np.delete(numpiRows, 0, axis = 1)

        print "numpiRows: " + str(numpiRows)

        totals = self.getSumRows(numpiRows)
        print "total: "+str(totals)

        proportions = self.getProportions(numpiRows, totals)

        print "proportions " + str(proportions)

        proportions_list = proportions.tolist()
        # print "proportion list " + str(proportions_list)


        #### TODO Momentarily commented out
        # for group in proportions_list:  # for every group
        #     if (len(group) >= 2):
        #         '''
        #         This specific if statement deletes any 0 values in the proportions list in case
        #         there is one as the first element of the group array.
        #         There should only be a proportion value for a and b. The proportion for everything
        #         else is 1 - (a+b).
        #         '''
        #         if (len(group) > 2):
        #             del group[0]

        errors = self.getStandardError(proportions, totals)  # Retrieve standard error of proportion

        upperBounds = proportions + errors * z
        lowerBounds = proportions - errors * z

        colSum = self.getProportionPerColumn(numpiRows)
        PopulationCount = np.sum(colSum)
        PopQuestionProp = colSum / PopulationCount  # Actual Population Proportion

        expected = np.copy(numpiRows)
        grandTotal = np.sum(colSum)
        # print ("grandTotal: " + str(grandTotal))

        # print "totals"
        # # print totals
        # lenrow = len(totals)

        # print ("colsum: " + str(colSum))
        # lencol = len(colSum)

        # print "expected"
        # print expected

        for i in range(0, len(expected)):
            for y in range(0, len(expected[i])):
                # print colSum[y]
                expected[i][y] = totals[i][0] * colSum[y] / grandTotal

        print "Expected " + str(expected)
        # print expected

        # print "the data"
        # print numpiRows

        chi = ((numpiRows - expected) * (numpiRows - expected)) / expected ## TODO Chi-square is performed here
        # print "Expected"
        # print expected
        print "Observed " + str(numpiRows)

        shapeexpected = np.reshape(expected, (-1, 1))
        print "Shape expected " + str(shapeexpected)

        chistat = np.sum(chi)

        # if(chistat > z): #If the chi score is greater than the chi-square critical value, add it to the results
        higherOrLower = ""

        '''
        tolerableFive =  expected.size
        tolerableFive = int(tolerableFive*0.20)
    
    
        numFive = 0
        for el in range(0,shapeexpected.size):
                if shapeexpected[el][0] < 5:
                        numFive = numFive +1
    
        if numFive > tolerableFive:
                chistat = np.nan
        '''
        if (not np.isnan(chistat)):
            print "observed",
            try:
                print numpiRows[0][1]
            except IndexError:
                print 'empty'
            print "expected",
            try:
                print expected[0][1]
            except IndexError:
                print 'empty'
            try:
                if (expected[0][1] < numpiRows[0][1]):
                    higherOrLower = "+"
                else:
                    higherOrLower = "-"
            except IndexError:
                higherOrLower = "-1"

        # print chistat

        print "Chi-Square"
        print chi
        print "Chi -stat"
        print chistat
        """
        print "Population count "+ str(PopulationCount)
        print "Pop Count "+ str(colSum)
        print "Errors" + str(errors)
        print "Pop Proportions "+ str(PopQuestionProp) 
        print "Lower "+ str(lowerBounds)
        print "Upper "+str(upperBounds)
        """
        # if(chistat > z):
        thequestion = converter.convert(fileNum)
        print "The H " + str(H)
        print "The Question " + thequestion

        if (np.isnan(chistat)):
            chistat = ""

        # print colSum.size
        # print totals.size

        self.degreeFreedom = (colSum.size - 1) * (totals.size - 1)

        totals_list = totals.tolist()  # populations for all groups

        thequestion = string.capwords(thequestion)

        results_temp = [thequestion, H, chistat, higherOrLower, self.degreeFreedom];

        # results_temp.extend(proportions_list[:,1])

        # Determine the chi critical value to compare chi score with
        # based on the degree of freedom

        # chiCritical = 0.0
        # TODO Make these editable
        self.significance = 0.01 ## TODO edit significance
        probability = 1 - self.significance
        # stat, p, dof, expected = chi2_contingency(table)
        rawCritical = chi2.ppf(probability, self.degreeFreedom)  # Compute critical value
        # print ("scipy critical i: " + str(rawCritical))
        chiCritical = round(rawCritical, 3)  # Round critical value by 3 decimal places
        results_temp.append(str(chiCritical))

        # @ Candy : ___________________________________________________
        # This is the original hard-coded implementation for reference.
        # I already deleted the rest of the elif statements
        # _____________________________________________________________
        # if degreeFreedom == 1:
        #     chiCritical = '6.635'
        #     results_temp.append(str(chiCritical))
        # elif degreeFreedom == 2:
        #     chiCritical = '9.21'
        #     results_temp.append(str(chiCritical))

        # Determine if the chi score is > than the chi critical value

        if (not (type(chistat) is str) and (float(chistat) > float(chiCritical))):  # If yes
            results_temp.append('1')  # Chi score is significant
        else:  # otherwise
            results_temp.append('0')  # Chi score is insignificant

        results_temp.extend(totals_list)  # append populations for all groups

        print "proportion list " + str(proportions_list)
        # for group in proportions_list:  # for every group
        for group in proportions_list:  # for every group
            print ("group contains " + str(group))
            if (len(group) >= 2):
                results_temp.append(
                    str(round(float(group[0]) * 100, 2)) + '%')  # append proportion of answer a for each group
                results_temp.append(
                    str(round(float(group[1]) * 100, 2)) + '%')  # append proportion of answer b for each group
                results_temp.append(str(round((1 - (float(group[0]) + float(group[1]))) * 100,
                                              2)) + '%')  # append proportion of other answers for each group
                # results_temp.append(group[i]) #append each proportion of every answer for each group
                # print group[i]
        print ("results_temp GROUP " + str(results_temp))
        results.append(results_temp)


    def group(self, index, rows, V, header):
        groups = OrderedDict()  # {}
        # 1 Because first index is question name
        if header not in V.keys():
            print "Warning " + header + " " + "not in Variable description"
        else:
            for i in range(1, len(V[header])):
                entry = V[header][i][0]
                groups[V[header][i][0]] = []
                # print ("b3 " + str(i) + " groups | header " + str(V[header][i][0]))

        # if (header == "b3"):
        #     print ("b3 groups INIT " + str(groups))

        for i in range(0, len(rows)):

            entry = rows[i][index]
            # if (header == "b3"):
            #     print ("b3 i " + str(i))
            #     print ("b3 entry " + str(entry))

            if (entry != '-1' and entry != '' and entry != '-1.0'):

                if entry in groups:
                    groups[entry].append(i)
                else:
                    print "Warning  " + str(entry) + " is not declared in variable description for question " + header
                    groups[entry] = []
                    groups[entry].append(i)

            # if (header == "b3"):
            #     print ("b3 groups " + str(groups))
        return groups


    def getTable(self, col, clusters, V, header):
        groups = []
        # if (header == 'b3'):
        #     print('b3 header ' + str(header))
        #     print('col ' + str(col))
        #     print('clusters ' + str(clusters))
        #     print('V ' + str(V))

        for c in clusters:
            # if (header == 'b3'):
            #     print('b3 cluster col ' + str(col))
            #     print('c ' + str(c))
            #     print('V ' + str(V))
            #     print('header ' + str(header))
            groups.append(self.group(col, c, V, header))

        # if (header == 'b3'):
        #     print('b3 groups ' + str(groups))
        keys = []
        for g in groups:

            for key in g:

                if key not in keys:
                    keys.append(key)

        return Table(groups, keys, header)


    def getVariableList(self, filename, varMarker):  # Reads the question
        variables = {}

        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            for row in readCSV:
                if (row[0] == varMarker):
                    variables[row[1]] = [row[2]]
                    lastVar = row[1]
                else:
                    variables[lastVar].append((row[0], row[1]))
        return variables


    def chiTest(self, datasetPaths, queueNum):
        reload(sys)
        # sys.setdefaultencoding('utf8')
        # sys.stdin.encoding = 'utf8'

        # change to ur own.
        vList = self.getVariableList('Updated-Variables.csv',
                                '^')  # Get Variable Description # TODO This should always match the output in OOTO.py
        # print("!------ readHeader")
        # print(datasetPaths[0])
        header = self.readHeader(datasetPaths[0])  # Read the header from one of the datasets which include the question codes
        # print("ex_header: " + str(header))
        results = []
        converter = ColConverter(header)

        # print header
        clusternames = datasetPaths  # Read the filepaths of the datasets
        # print ("CLUSTER NAMES: " + str(clusternames))

        clusters = []  # clusters contains all of the respondents and their answer in per dataset

        # For each data set
        for clustername in clusternames:
            # print ("~CLUSTER NAME: " + str(clustername))
            clusterRow = self.readCSV(clustername)  # Get all of the respondent's IDs and answers in the dataset
            # print clusterRow
            clusters.append(clusterRow)  # Add to the clusters

        tableList = []  # list of contingency tables

        # z = [6.64]
        z = [0.0]  # TODO Clean this function
        # zstr = ['1960']

        fileName = ""

        for y in range(0, len(z)):
            results = []  # The resulting content that will be written in save.csv
            dataset_headers = []
            dataset_names = []

            for x in range(0, len(clusternames)):
                clustername_arr = clusternames[x].split('\\')
                dataset_names.append(
                    clustername_arr[len(clustername_arr) - 1])  # Getting the dataset name from its file path
                dataset_headers.append("Dataset " + str(x + 1))

            results.append(dataset_headers)
            results.append(dataset_names)  # Append dataset names

            population_and_proportionHeaders = []  # Headers Ni and Pi for each cluster i
            # print("Cluster NAMES : " + str(len(clusternames)))

            for x in range(0, len(clusternames)):
                population_and_proportionHeaders.append("N" + str(x + 1))  # Add Header "Nx" for each cluster x. Total of x

            # for x in range(0, len(clusternames)):
                population_and_proportionHeaders.append(
                    "P" + str(x + 1) + "(a)")  # Add Header "Px" for each cluster x. Proportion of x
                population_and_proportionHeaders.append("P" + str(x + 1) + "(b)")
                population_and_proportionHeaders.append("P" + str(x + 1) + "(etc)")

            results_headers = out.ChiTest.getInstance().COLUMN_HEADERS  # Results headers TODO Constant

            # Append the population and proportion headers for each cluster to results headers
            results_headers.extend(population_and_proportionHeaders)
            results.append(results_headers)  # Append these as header names to the results
            # print results

            for i in range(0, len(header)):  # Iterate over each question
                if header[i] not in vList.keys():  # If the question code is not found in Variable Description
                    # print "Warning " + header[
                    #     i] + " " + " question name not in Variable description will be assigned to null"
                    H = "null"
                else:
                    H = vList[header[i]][0]  # H is the question itself
                # print "col " + str(i) + " " + header[i]

                # TODO check if 3-choice values are correct ( a and c seem reversed )
                theTable = self.getTable(i, clusters, vList, header[i])  # Generates a table matrix for all datasets to do the chi-test for the question

                # print "~Table 0 (pre-doFile)"
                # print theTable.rows

                # print "~Table 0 (pre-doFile) HEADERS",
                # print header
                self.doFile(theTable, i, results, converter, z[y], H)  # Chi test on the question and then writing it in the file

                # Remove the column with -1 in the table.
                if '-1' in theTable.rows[0]:
                    position = theTable.rows[0].index('-1')  # Get index of the -1 column.
                    for row in theTable.rows:  # Delete the entire -1 column.
                        del row[position]

                # print "~Table 1",
                # print theTable.rows

                theTable.getPrintable(tableList)


            # Print results

            # fileName = str("(Q" + str(queueNum) + ") ")
            # fileName = str(fileName + "- Chi-Test -")  # Get filename of save file TODO
            for name in dataset_names:
                fileName = fileName + name + " "

            # print("results contain: " + str(results))

            # Sort results by Chi-value column
            rowStart = results.index(results_headers) + 1
            chiValueColumn = out.ChiTest.getInstance().getHeaderIndex(out.ChiTest.getInstance().HEADER_chiValue)

            # Replace empty chi-value to 0 TODO : Optimize
            for i in results[rowStart:]:
                if i[chiValueColumn] == '':
                    i[chiValueColumn] = 0


            sortColumn = chiValueColumn
            results[rowStart:] = sorted(results[rowStart:], key = lambda temp: temp[sortColumn], reverse = True)
            # results[rowStart:].sort(key = lambda temp: temp[sortColumn])

            # print("rowStart: " + str(rowStart))
            # print("sortColumn: " + str(sortColumn))
            # print("results now contain: " + str(results))


            fileName = fileName.replace(".csv", "")
            queueStr = "(Q" + str(queueNum) + ")"
            fileName = fileName.replace(queueStr, "")

            fileName = str(queueStr + " - Chi-Test -" + fileName)
            LS.checkDirectory(LS.GL_MM_OUTPUT_PATH)

            path_csv = LS.GL_MM_OUTPUT_PATH + fileName
            self.writeonXLSX(results, path_csv + '.xlsx', results_headers)


            # Print interim chi-square tables
            self.writeOnCSV(tableList, path_csv + "(Tables)" + ".csv")  # TODO: Comment out
            return fileName

        # print "results"
        # print results
