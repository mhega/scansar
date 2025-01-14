#**************************************************
# sar class V 1.4.2
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 1/15/2025
#**************************************************

from .utils import Table, printStreamBuffer
import re
from io import StringIO

class sar:
    def __init__(self,fhand):
        self.rawTableList=sar._parseFile(fhand)
        if len(self.rawTableList) == 0:
            raise sar.SarException('No tables found')
        self.tableList=self._loadTables()
        if len(self.tableList) == 0:
            raise sar.SarException('No tables loaded')

    class SarException(Exception):
        def __init__(self,message="Unexpected Error!"):
            self.message=message
            super().__init__(self.message)
        
    def _parseFile(fhand):
        """After a file handle has been initialized for the input sar file, parseFile() is in charge of walking through the file
        , and breaking it down into a list of raw tables.
        An empty line pattern is used to signal a termination of the current table and potentially a start of a new table."""
        rawTableList=[]
        currentRawTable=StringIO()
        emptyLinePattern=r'^\s*$'
        for line in fhand:
            if re.match(emptyLinePattern,line):
                if len(currentRawTable.getvalue().split('\n')) > 1 and (len(rawTableList) == 0 or rawTableList[-1] != currentRawTable):
                    rawTableList.append(currentRawTable.getvalue())
                    currentRawTable=StringIO()
            else:
                currentRawTable.write(line)
    
        if len(currentRawTable.getvalue().split('\n')) > 1 and (len(rawTableList) == 0 or rawTableList[-1] != currentRawTable):
            rawTableList.append(currentRawTable.getvalue())
        return rawTableList

    def _loadTables(self):
        """loadTables serves as the moderator for tabulating individual raw data snippets that are read from the file.
        """


        # Suppress printed text into a buffer as opposed to displaying it to standard output
        @printStreamBuffer
        def algorithm1(rawTable):
            """algorithm1 is the primary algorithm for transforming a table from raw text format into an analyzable structure.
            It is based on splitting each row (line) within the raw table by space characters to generate list of columns (fields).
            A lump of multiple consecutive space characters represent one separator between two fields.
            A table object is instantiated to encapsulate each of the list of tuples that comes out of looping over and splitting the table lines."""
        
            timestampPattern=r'^([0-9:]+( [AP]M)?)'
            headerFieldPattern=r'[A-Za-z:]'
            lines=rawTable.strip().split('\n')
            currentTable=Table()
            headertup=None
            if len(lines) < 2:
        
                # The printed string here will flag to the caller routine (through printStreamBuffer decorator) to skip over this table since it is technically just a single line and so is not a table.
                print('Not a table')
                return currentTable
            for line in lines:
        
                # The trick here is the first field of each line (Timestamp) is likely to contain space separating the time from the "AM/PM" string.
                # Unless we explicitly exclude this space during our splitting, we will end up with a separate field containing words "AM"/"PM".
                # To handle that, we are initially splitting the row by the timestamp pattern to pick and separate the whole timestamp from the rest of the row.
                match=re.search(timestampPattern,line.strip())
                if not match:
                    continue
                
                # We are starting from the fourth element ([3]) in the split, since the second and third are capturing the two groups of the timestamp pattern.
                # Even if AM/PM pattern does not exist in the sar file, its group will still be captured with a None value.
                tup=[match.groups()[0]]+match.re.split(line.strip())[3].split()
                
                # A header is and only is a line with all fields containing Alphabetic characters.
                # That is since by nature of sar data, a row that is not a header should contain at least one field that is fully numeric -likely more than just one field. 
                if (False not in [True if re.search(headerFieldPattern,field) else False for field in tup]):
                    if headertup == None:
                        headertup=tup
                        headertup[0]=re.sub(timestampPattern,'Timestamp',headertup[0])
                        currentTable.setHeaderNames(headertup)
                    else:
                        print('Duplicate Header!')            
                else:
                    if headertup and len(tup) == len(headertup):
                        currentTable.append(tup)
                    else:
                        # This will flag to the caller routine to execute the alternate loading algorithm (algorithm2)
                        print('Inconsistent data row!')
            return currentTable

        def algorithm2(rawTable):
            """While algorithm2 is more complex and costly than alg1, it should be robust enough to capture sar tables which alg1 fails to load.
            The idea is to distingush text spaces from actual column separators:
            A column separator and only a column separator should adhere to the following rules:
            1. Not be part of a timestamp pattern match - e.g., "01:08:02 AM" 
            2. Have a index (location) that is the same across all the table lines including the header.
            2. Any word that begins from that separator index should not map to an empty space in the header.
            
            To put the above rules into action, we will implement the following steps:
            1. Identify and record the header line of the table.
            2. (parallel with step 1) strip the timestamp out of each line - including header.
            3. (parallel with step 1 and after step 2) Identify space locations in each line - including the header. Result is a two-dimentional list.
            4. Identify overlapping space locations between all rows including the header by intersecting the sets represented by step 3's result.
               These can be thought of as vertical holes through the table text.
            5. filter the first index of each subsequent index group in step 4's result
            6. Add 0 to the beginning of the list in step 5's result
            7. Exclude index values -each of which together with its subsequent index value in step 6's result- correspond to all space string in the header.
            8. Construct the substrings formed by the index values in step 7 result across all rows
            For details, refer to: https://gist.github.com/mhega/7ab642f4de57f006814311c9b4d37cd3
         """
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
        
                # Step 1
                if not header:
                    match=re.search(timestampPattern,line.strip())
                    if not match:
                        continue
                    tup=[match.groups()[0]]+match.re.split(line.strip())[3].split()
                    if (False not in [True if re.search(headerFieldPattern,field) else False for field in tup]):
                        header=line.strip()
                
                # Steps 2 and 3
                spaceLocations.append([n for n,c in enumerate(stripTimestamp(line.strip())) if c == ' '])
            
            # Step 4
            intersect=None
            for y in [set(x) for x in spaceLocations]:
                if not intersect:
                    intersect=y
                else:
                    intersect=intersect & y
            intersect=list(intersect)
            
            # Steps 5 and 6
            indexes=[0]+[intersect[n] for n in range(len(intersect)) if intersect[n]-1 not in intersect]
        
            # Step 7
            splitIndexes=[]
            for i,j in zip(indexes, indexes[1:]+[None]):
                if not re.search(r'^[ ]*$',stripTimestamp(header)[i:j]):
                    splitIndexes.append(i)
        
            # Step 8
            for line in lines:
                match=re.search(timestampPattern,line)
                tup=[match.groups()[0]]+list(stripTimestamp(line.strip())[i:j].strip() for i,j in zip(splitIndexes, splitIndexes[1:]+[None]))
                if line.strip() == header:
                    tup[0]=re.sub(timestampPattern,'Timestamp',tup[0])
                    currentTable.setHeaderNames(tup)
                else:
                    currentTable.append(tup)
            return currentTable
    
        tableList=[]
        index=0
        for rawTable in self.rawTableList:
            buffer={}
    
            # We start by trying algorithm1 first.
            # This should successfully load most of the tables provided space separator results in consistent row count.
            currentTable=algorithm1(rawTable, buffer=buffer)
            if 'Not a table' in buffer['value']:
                continue
            if 'Inconsistent data row' in buffer['value']:
                # We will resort to algorithm2 in this case. Even though Alg2 is more robust, it is more costly and so we only run it when necessary
                currentTable2=algorithm2(rawTable)
                if currentTable2.len() > currentTable.len():
                    currentTable=currentTable2
    

            tableDict={}
            if currentTable.len() > 0:
                header=tuple(currentTable.headerNames)
                tableDict[hash(header)]=tableDict.get(hash(header),Table())+currentTable
                tableList.append(tableDict)
    
        return tableList



    def fetchtables(self, fieldname):
        """ fetchTables is in charge of looking up all the tables that contain certain input field in their headers.
        Since an input table list that is generated by loadTables() is structured as a list of dictionaries
        , fetchTables will perform nested iterations through the tableList to construct a result list that has a similar structure as the input tableList.
        Tables with matching header and matching "group by" column names and values will end up being merged together.
        """
        result={}
        for tableDict in self.tableList:
            for item in tableDict.items():
                if fieldname in item[1].headerNames:
                    result[item[0]]=result.get(item[0],Table())+item[1]
    
        return list(result.values())


    def printRawSar(self):
        for _table in self.rawTableList:
            print(_table)


    def query(self, queryFunc):
        queryResult={}
        for _hash,_table in [_item for _ in self.tableList for _item in _.items() ]:
            try:
                _result=_table.get(filterFunc=queryFunc)
            except:
                continue
            if len(_result) > 0:
                queryResult[_hash]=queryResult.get(_hash,Table())+Table(headerNames=_table.headerNames, data=_result)
        for _table in queryResult.values():
            print('')
            _table.print()
            
            
        
