#**************************************************
# ListTables class V 1.0
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 12/27/2024
#**************************************************

import re
from utils.InfoRecord import Stage

def padding(input,keylength):   # Space padding for uniform display.
                                # While this generates a padding length for only one column value in a table, it puts into account the longest value (maxlength)
                                #  in the whole table column for determining
                                #  the padding length of other value within the column
    maxlength = None
    op = ''
    for i in input:
        if maxlength is None or len(str(i[0])) > maxlength:
            maxlength = len(str(i[0]))
    for j in range(maxlength-keylength+5):
        op = op+' '
    return op

def printStreamBuffer(fun):
    import io
    import sys

    def new_func(*args, buffer=None, **kwargs):
        caller = sys.argv[0].strip()
        if buffer is not None:
            _stdout = sys.stdout
            sys.stdout = _buffer = io.StringIO()
            ret = None
            try:
                ret = fun(*args, **kwargs)
            except SystemExit as e:
                sys.stdout = _stdout
                print(_buffer.getvalue())
                raise e   
            sys.stdout = _stdout
            buffer['value'] = _buffer.getvalue()
        else:
            ret = fun(*args, **kwargs)
        return ret
    return new_func


    
def titledashes(header):
    return tuple([''.join(['-' for c in range(len(k))]) if k is not None else None for k in list(header)]) 

def underline(title):
    return title+'\n'+''.join(['-' for c in range(len(title))])
    
def printList(header,data): 
    # Prints a table of any size.
    thelist = []
    if isinstance(header[0],tuple):
        header0 = header[0]
        thelist.append(header0)
        thelist.append(titledashes(header0))
        header = header[1]
    thelist.append(header)
    thelist.append(titledashes(header))
    for tup in data:
        thelist.append(tup)
    for tup in thelist:
        strToPrint = ''
        for i in range(len(tup)):
            if i+1<len(tup) and tup[i+1] is None:
                strToPrint = (strToPrint+padding([(str(x[i]),) for x in thelist],len(str(tup[i])))+str(tup[i]))
            elif tup[i] is None:
                strToPrint=(strToPrint+padding([(str(x[i]),) for x in thelist],0))
            else: 
                strToPrint=(strToPrint+str(tup[i])+padding([(str(x[i]),) for x in thelist],len(str(tup[i]))))
        print(strToPrint)

def getListDisplayText(*,header, data):         # *, enforces keyword arguments for ensuring header and data are distinguishable from the buffer input to the decorator
    tableBuffer = {}
    printStreamBuffer(printList)(buffer=tableBuffer, header=header, data=data)
    return  tableBuffer.get('value')
def printTablesSideways(tableHeader, tableCtx, allowedTabLength, tablesPerLine,topListToPrint = None, key = None, reverse=False, frameBlock = None):
    if topListToPrint is None:
        topListToPrint = len(tableCtx.keys())
    if key is None:
        key = lambda x: list(tableCtx.values()).index(x)
    topHeaderList = sorted(tableCtx.keys(), key=lambda x:key(tableCtx[x]), reverse=reverse)[:topListToPrint]
    ctxValues = sorted(tableCtx.values(), key=lambda x:key(x), reverse=reverse )[:topListToPrint]
    maxTabLength = max([len(x[:allowedTabLength]) for x in ctxValues])
    tablesInLastLine = len(topHeaderList) % tablesPerLine
    _block ='|'
    def tablesInLine(_i):
        return tablesInLastLine if _i == int(len(topHeaderList)//tablesPerLine) else tablesPerLine
    def multiply(value, times, separator):
        import itertools
        if True in [isinstance(v, list) for v in value]:
            prod = list(itertools.product( *[[x] if not isinstance(x,list) else x for x in value]))
            return sum([prod[x]+separator if x < len(prod)-1 else prod[x] for x in range(len(prod))],())                
        else: 
            return (times-1)*(value+separator)+value if times > 0 else value
    for i in range(int(len(topHeaderList)//tablesPerLine) + (lambda x:0 if x ==0 else 1)(tablesInLastLine)):
        _fullLineTable = [() for l in range(maxTabLength)] 
        for j in range(tablesInLine(i)):
            for k in range(maxTabLength):
                _fullLineTable[k]+=((_block,) if j > 0 else ())
                _fullLineTable[k]+=(list(ctxValues)[i*tablesPerLine+j][:allowedTabLength][k] if k < len(list(ctxValues)[i*tablesPerLine+j][:allowedTabLength]) else tuple(['' for x in range(len(tableHeader))]))
        print('\n\n')
        _centerHeader = tuple([list(topHeaderList)[tablesPerLine*i:tablesPerLine*i+tablesInLine(i)],None][0:(2 if len(tableHeader)%2 == 0 else 1)])
        _side = tuple([[''] for x in range((len(tableHeader)-1)//2)])
        _tableTopHeader = _side+_centerHeader+_side
        
        tableText = getListDisplayText(
            header = (multiply(_tableTopHeader,tablesInLine(i),(_block,)), multiply(tableHeader,tablesInLine(i),(_block,)))
            , data = _fullLineTable
            )
        if frameBlock is not None:
            print(Stage(re.sub('\n[\s%s]+\n' % _block, '', tableText).rstrip(),frameBlock).stringValue())
        else:
            print(re.sub('\n[\s%s]+\n' % _block, '', tableText).rstrip())

def multiline(fun):
    def new_func(*args, **kwargs):
        padding=kwargs.get('padding',12)
        tablesPerLine=kwargs.get('tablesPerLine',None)
        lineCapacity=kwargs.get('lineCapacity',200)
        tableMaxLengthArr=[max([len(x) for x in y.split('\n')]) for y in args]
        lists=[]
        currentList=[]
        currentWidth=0
        for ind in range(len(args)):
            if currentWidth+tableMaxLengthArr[ind]+padding > lineCapacity and ind > 0:
                lists.append(currentList)
                currentList=[]
                currentWidth=0
            currentList.append(args[ind])
            currentWidth+=tableMaxLengthArr[ind]+padding
    
        if len(lists) == 0 or currentList != lists[-1]:
            lists.append(currentList)
        for list in lists:
            fun(*list, padding=padding)
    return new_func

@multiline
def stack(*tables, padding):
    tableMaxLengthArr=[max([len(x) for x in y.split('\n')]) for y in tables]
    tableMaxHeight=max([len(x.split('\n')) for x in tables])
    def pad(spaceCount):
        return ''.join([' ' for x in range(spaceCount)])

    print('')
    for line in range(tableMaxHeight):
        for tabIndex in range(len(tables)):
            try:
                val=tables[tabIndex].split('\n')[line]
            except:
                val=''
            print(val+pad(tableMaxLengthArr[tabIndex]-len(val)+padding),end='')
        print('')