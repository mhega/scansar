#**************************************************
# Table V 1.0
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 12/26/2022
#**************************************************

from utils.ListTables import printList, getListDisplayText

class Table:
    def __init__(self, headerNames = [], data = []):
        self.headerNames = list(headerNames)
        self.data = list(data)

    def __add__(self, other):
        return Table((lambda x:x if x is not None and x != [] else other.headerNames)(self.headerNames), self.data+other.data)

    def setHeaderNames(self, headerNames):
        self.headerNames = headerNames
    
    def append(self, row):
        self.data.append(row)

    def len(self):
        return len(self.data)
        
    def rowfilter(fun):               # Decorator
        def new_func(*args, filterFunc = None, sortKey = None, reverse = False, **kwargs):
            def _mapperFunc(row, header):
                return lambda field:row[header.index(field)]
            if filterFunc:
                _self = Table.filtertabledata(lambda x:x)(Table(args[0].headerNames, args[0].data), filterFunc=filterFunc)
                if sortKey:
                    _self.data = sorted(_self.data, key=lambda row:sortKey(_mapperFunc(row, _self.headerNames)), reverse=reverse)
            else:
                _self = args[0]
            return fun(_self, *args[1:], **kwargs)
        return new_func

    @rowfilter
    def get(self, subtable = None):
        if not subtable:
            subtable = tuple(self.headerNames)
        if isinstance(subtable, tuple) and isinstance(subtable[0],str) and isinstance(subtable[1],type):
            return [subtable[1](x[self.headerNames.index(subtable[0])]) for x in self.data]
        elif isinstance(subtable, tuple):
            return [tuple([(x[self.headerNames.index(e)] if isinstance(e, str) else e[1]( x[self.headerNames.index(e[0])] )) for e in subtable]) for x in self.data]
        elif isinstance(subtable, str):
            return [x[self.headerNames.index(subtable)] for x in self.data]

    def __str__(self) :
        return str({'Header':self.headerNames, 'Data':self.data})


    def filtertabledata(fun):               # Decorator
        def new_func(*args, filterFunc = lambda x:True, **kwargs):
            _tables = list(filter(lambda x:isinstance(x, Table), args))
            
            def _mapperFunc(row, header):
                return lambda field:row[header.index(field)]

            for table in _tables:
                _header = table.headerNames
                table.data = list(filter(lambda row:filterFunc(_mapperFunc(row, _header)), table.data))
            return fun(*args, **kwargs)
        return new_func
    def print(self):
        printList(header=self.headerNames,data=self.data)
    def getPrintText(self):
        return getListDisplayText(header=self.headerNames, data=self.data)

