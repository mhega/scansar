#**************************************************
# sarscanner V 1.3
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 1/4/2025
#**************************************************

import os
import sys
#parentDir = os.path.abspath('..')
#sys.path.append(parentDir)

from .sar import sar
#import utils
from .utils import table, BarPlot, printList, getListDisplayText, printStreamBuffer, stack, underline, Stage
#from utils.table import Table
#from utils.BarPlot import BarPlot
#from utils.ListTables import printList, getListDisplayText, printStreamBuffer, stack, underline
#from utils.InfoRecord import Stage
import json
#import sys

class sarscanner:
    def singleFileScan(fhand):
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
                        data=BarPlot.appendBarPlot(t.get(('Timestamp',group,sort),filterFunc=lambda x:True, sortKey=lambda x:float(x(sort)), reverse=True)[:5],2)
                        lists.append(getListDisplayText(header=('Timestamp',group,sort,''), data=data))
                    else:
                        data=BarPlot.appendBarPlot(t.get(('Timestamp',sort),filterFunc=lambda x:True, sortKey=lambda x:float(x(sort)), reverse=True)[:5],1)
                        lists.append(getListDisplayText(header=('Timestamp',sort,''), data=data))
            return lists

        try:
            sarData=sar(fhand)
        except sar.SarException as e:
            raise e
        
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