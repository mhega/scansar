#**************************************************
# ListTables class V 1.0
# Author: Mohamed Hegazy
#**************************************************

class BarPlot:

        
    def addWeights(table, columnIndex):

        def weight(valueList, valueIndex):
            if valueList[valueIndex+1] == 0:
                return valueList[valueIndex]
            updatedValueList = list(filter(lambda num: num != 0, valueList))        
            return valueList[valueIndex] / (sum(valueList[valueIndex+1:])/len(updatedValueList[valueIndex+1:]))

        valueList = [x[columnIndex] for x in table]
        valueWeights = []
        for i in range(len(valueList)):
            try:
                if i+2 < len(valueList):
                    if valueList[i+2] == 0: 
                        # Looking ahead to make sure
                        #  we will not accidentally devide by 0
                        #  while calculating the weight of the next element
                        valueWeights.append(weight(valueList, i))
                    else: 
                        valueWeights.append(weight(valueList, i) / weight(valueList, i+1))
                elif i+1 < len(valueList):
                    valueWeights.append(weight(valueList, i))
                else:
                    valueWeights.append(0)
            except:
                valueWeights.append(0)
        return [table[i]+(str(format(valueWeights[i],'.2f'))
        #+(' <===' if True in [bool(valueWeights[r] > float(3)) for r in list(range(i,min([5,len(valueWeights)])))] and i<5 else '')
        ,) for i in range(len(table))]


    def appendBarPlot(tupList, dataColumnIndex): ## ALWAYS call this function with tuple list that is sorted (descending) by the data column which is to be plotted
        if len(tupList) == 0:
            return tupList
        # The bar lines are appended to the right of each displayed table/histogram
        # We need to identify the largest length in the table's last column in order to calculate the length of the largest bar.
        maxValueLength = len(str(int(float(tupList[0][dataColumnIndex]))))
        
        # For any max value that is bigger than two-digit (99),
        #  the bar length will be suppressed to an appropriate scale,
        #  where we cannot have a longest bar of more than 99 character length.
        # i.e., 100, 1000, 10000, etc. will all be shrunk to 10., through devision by the calculated devident.
        #       110, 1100, 11000, etc. will be shrunk to 11. etc.
        if int(float(tupList[0][dataColumnIndex])) > 60:
            _scale = 1
        else:
            _scale = 2
        divident = (10**(maxValueLength-_scale)) if maxValueLength > _scale else 1

        # Concatenating bar lines to the tuple list so they will be printed as part of the list. 

        return [tup+(''.join([u"\u2584" for i in range(int(int(float(tup[dataColumnIndex]))/divident))]),) for tup in tupList]
