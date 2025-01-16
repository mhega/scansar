#**************************************************
# sarscanner V 1.4.2
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 1/15/2025
#**************************************************

import os
import sys
from .sar import sar
from .utils import Table, BarPlot, printList, getListDisplayText, printStreamBuffer, stack, underline, Stage
import json

class sarscanner:

    def splitTable(parentTable, by=None):
        """Given the nature of sar data and the intent of our analysis, a table might need to be broken down into multiple children table depending on certain columns.
        A table is split by a column that can be generally thought of as "group by" column - that has a finite list of values.
        In other word, splitting a parent table into subtables can be thought of as the inverse of UNION operation against the subtables to make up the input parent table."""
            
        header=tuple(parentTable.headerNames)
    
    
        # grouper is the finite list of values under "by" column.
        grouper=parentTable.get(by)
    
        result=[]
            
        for val in list(set(grouper)):
            subtable=parentTable.get(filterFunc=lambda x:x(by)==val)
            result.append(Table(headerNames=header, data=subtable))
        return result
    
    def singleObjectScan(sarData):
        def analyzeFields(fields, sarDataInstance):
            """analyzeFields runs once for every report.
            Each json field maps to a report name using "report" key. If a field specifies no report name, it will default to "Others"
            At this time, analyzeFields performs a sorting of each field referenced in sar.json using "sort" key.
            Fields are sorted in descending order - presuming the highest values are the ones of interest.
            A group column is displayed when specified in sar.json using "group" key."""
            lists=[]
            for field in fields:
                sort=field.get('sort')
                tables=sarDataInstance.fetchtables(sort)
        
                # A group is the field name for the "group by" column within a table
                # It is used to decide if the same field will be included in the table display.
                group=field.get('group',None)
                for t in tables:
                    if group:
                        for subt in sarscanner.splitTable(t, by=group):
                            data=BarPlot.appendBarPlot(subt.get(('Timestamp',group,sort),filterFunc=lambda x:True, sortKey=lambda x:float(x(sort)), reverse=True)[:5],2)
                            lists.append(getListDisplayText(header=('Timestamp',group,sort,''), data=data))
                    else:
                        data=BarPlot.appendBarPlot(t.get(('Timestamp',sort),filterFunc=lambda x:True, sortKey=lambda x:float(x(sort)), reverse=True)[:5],1)
                        lists.append(getListDisplayText(header=('Timestamp',sort,''), data=data))
            return lists
       
        # Let's start the analysis:
        curPath=os.path.dirname(sys.modules[__name__].__file__)
        with open(f'{curPath}/../conf/sar.json','r') as jsontst:
            jsonfields=json.load(jsontst)
        
        # A report generally contains all data that come from the same table.
        # We need to extract all the ditinct report names from our json fields
        #  and construct a new dictionary that allows us to process each report individually
        reportsDict={}
        for d in jsonfields['fields']:
            reportName=d.get('report','Others')
            reportsDict[reportName]=reportsDict.get(reportName,[])+[d]
        
        
        for report in reportsDict.items():
            lists=analyzeFields(report[1], sarData)
            if len(lists) > 0:
                print(Stage('Analyzing '+report[0]).stringValue())
                stack(*lists, padding=20, lineCapacity=200)

    def singleFileScan(fhand):
        try:
            sarData=sar(fhand)
        except sar.SarException as e:
            raise e

        sarscanner.singleObjectScan(sarData)
         
