#**************************************************
# ListTables class V 1.0
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 12/27/2024
#**************************************************

import sys
from utils.table import Table
from utils.stringbuffer import Stringbuffer
import re
import statistics
from utils.BarPlot import BarPlot
from utils.ListTables import printList, getListDisplayText, printStreamBuffer, stack, underline
from utils.InfoRecord import Stage
import json


try:
    fileName=sys.argv[1].strip()
except:
    print("Invalid command")
    exit(1)
try:
    fhand=open(fileName)
except:
    print("Invalid Input")
    exit(1)



def parseFile(fhand):
    rawTableList=[]
    currentRawTable=Stringbuffer()
    emptyLinePattern=r'^\s*$'
    for line in fhand:
        if re.match(emptyLinePattern,line):
            if currentRawTable.len() > 0 and (len(rawTableList) == 0 or rawTableList[-1] != currentRawTable):
                rawTableList.append(currentRawTable.stringValue())
                currentRawTable=Stringbuffer()
        else:
            currentRawTable.append(line)

    if currentRawTable.len() > 0 and (len(rawTableList) == 0 or rawTableList[-1] != currentRawTable):
        rawTableList.append(currentRawTable.stringValue())
    return rawTableList


@printStreamBuffer
def algorithm1(rawTable):
    timestampPattern=r'^([0-9:]+( [AP]M)?)'
    headerFieldPattern=r'[A-Za-z:]'
    lines=rawTable.strip().split('\n')
    currentTable=Table()
    headertup=None
    if len(lines) < 2:
        print('Not a table')
        return currentTable
    for line in lines:
        match=re.search(timestampPattern,line.strip())
        if not match:
            continue
        tup=[match.groups()[0]]+match.re.split(line.strip())[3].split()
        # We started from the fourth element ([3]) in the split, since the second and third are capturing the two groups of the timestamp pattern.
        # Even if AM/PM pattern does not exist in the sar file, its group will still be captured with a None value.
        if (False not in [True if re.search(headerFieldPattern,field) else False for field in tup]):
            if headertup == None:
                headertup=tup
            else:
                print('Duplicate Header!')
            headertup[0]=re.sub(timestampPattern,'Timestamp',headertup[0])
            currentTable.setHeaderNames(headertup)
        else:
            if headertup and len(tup) == len(headertup):
                currentTable.append(tup)
            else:
                print('Inconsistent data row!')
    return currentTable

def algorithm2(rawTable):
    timestampPattern=r'^([0-9:]+( [AP]M)?)'
    headerFieldPattern=r'[A-Za-z:]'
    lines=rawTable.strip().split('\n')
    currentTable=Table()
    header=None
    spaceLocations=[]
    def stripTimestamp(line):
        match=re.search(timestampPattern,line)
        return match.re.split(line)[3]
        
    for line in lines:
        if not header:
            match=re.search(timestampPattern,line.strip())
            if not match:
                continue
            tup=[match.groups()[0]]+match.re.split(line.strip())[3].split()
            if (False not in [True if re.search(headerFieldPattern,field) else False for field in tup]):
                header=line.strip()
        
        spaceLocations.append([n for n,c in enumerate(stripTimestamp(line.strip())) if c == ' '])
    intersect=None
    for y in [set(x) for x in spaceLocations]:
        if not intersect:
            intersect=y
        else:
            intersect=intersect & y
    intersect=list(intersect)
    indexes=[0]+[intersect[n] for n in range(len(intersect)) if intersect[n]-1 not in intersect]
    splitIndexes=[]
    for i,j in zip(indexes, indexes[1:]+[None]):
        if not re.search(r'^[ ]*$',stripTimestamp(header)[i:j]):
            splitIndexes.append(i)
    for line in lines:
        match=re.search(timestampPattern,line)
        tup=[match.groups()[0]]+list(stripTimestamp(line.strip())[i:j].strip() for i,j in zip(splitIndexes, splitIndexes[1:]+[None]))
        if line.strip() == header:
            tup[0]=re.sub(timestampPattern,'Timestamp',tup[0])
            currentTable.setHeaderNames(tup)
        else:
            currentTable.append(tup)
    return currentTable    
    
def loadTables(rawTableList):
    
    def splitTable(parentTable, by=None, startfrom=None):
        if not by:
            return {(None,None):parentTable}
        grouper=parentTable.get(by)
        result=(startfrom if startfrom else {})
        header=parentTable.headerNames
        for val in list(set(grouper)):
            key=(by,val)
            subtable=parentTable.get(filterFunc=lambda x:x(by)==val)
            result[key]=Table(headerNames=header, data=subtable)
        return result

    tableList=[]
    index=0
    for rawTable in rawTableList:
        buffer={}
        currentTable=algorithm1(rawTable, buffer=buffer)
        if 'Not a table' in buffer['value']:
            continue
        if 'Inconsistent data row' in buffer['value']:
            currentTable2=algorithm2(rawTable)
            if currentTable2.len() > currentTable.len():
                currentTable=currentTable2
        allcapPattern=r'^[A-Z0-9]+$'
        tableDict={}
        if currentTable.len() > 0:
            for field in currentTable.headerNames:
                if re.search(allcapPattern,field):
                    tableDict=splitTable(parentTable=currentTable,by=field)
            if len(tableDict) == 0:
                tableDict=splitTable(parentTable=currentTable)
            tableList.append(tableDict)

    return tableList

def fetchtables(fieldname, tableList):
    result={}
    for tableDict in tableList:
        for item in tableDict.items():
            if fieldname in item[1].headerNames:
                result[item[0]]=result.get(item[0],Table())+item[1]

    return result

rawTableList=parseFile(fhand)
tableList=[]
if len(rawTableList) > 0:
    tableList=loadTables(rawTableList)
else:
    print('No Tables found')
    exit(0)

if len(tableList) == 0:
    print('No Tables loaded')
    exit(0)

with open('sar.json','r') as jsontst:
    jsonfields=json.load(jsontst)

reportsDict={}
for d in jsonfields['fields']:
    reportName=d.get('report','Others')
    reportsDict[reportName]=reportsDict.get(reportName,[])+[d]

def analyzeFields(fields, tableList):
    lists=[]
    for field in fields:
        sort=field.get('sort')
        tables=fetchtables(sort, tableList)
        group=field.get('group',None)
        for t in list(tables.values()):
            if group:
                data=BarPlot.appendBarPlot(t.get(('Timestamp',group,sort),filterFunc=lambda x:True, sortKey=lambda x:float(x(sort)), reverse=True)[:5],2)
                lists.append(getListDisplayText(header=('Timestamp',group,sort,''), data=data))
            else:
                data=BarPlot.appendBarPlot(t.get(('Timestamp',sort),filterFunc=lambda x:True, sortKey=lambda x:float(x(sort)), reverse=True)[:5],1)
                lists.append(getListDisplayText(header=('Timestamp',sort,''), data=data))
    return lists

for report in reportsDict.items():
    lists=analyzeFields(report[1], tableList)
    if len(lists) > 0:
        print(Stage('Analyzing '+report[0]).stringValue())
        stack(*lists, padding=20, lineCapacity=200)
