#**************************************************
# InfoRecord class V 1.0
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 4/8/2022
#**************************************************

import re
class Stringbuffer:
    def __init__(self, buf = ['',]):
        self.buf = list(buf)

    def append(self, subst):
        self.buf+=list(subst) if not isinstance(subst, list) else subst

    def stringValue(self):
        return ''.join([x for x in self.buf])

    def len(self):
        return len(self.buf)

class InfoRecord:
    def __init__(self, indentLength=20, block = '+', topTitle=': System Dat :', titleMaxLength=25):
        self.indentLength = indentLength
        self.block = block
        self.topTitle = topTitle
        self.titleMaxLength = titleMaxLength
        self._padding = 0
        self.stringValueBuffer = Stringbuffer(['',])

    def appendRightBlocks(self, input):
        p = re.compile('([\r\n][ ]*(['+self.block+'].*))')
        tokens = input.stringValue().split('\n')
        for i in range(len(tokens)):
            tokens[i]+=self.padding((2*self._padding+len(self.topTitle))-len(tokens[i].lstrip())-1+len(self.block),' ')+self.block
        return ''.join([x+'\n' for x in tokens]).strip()

    def setRecord(self, title, value):
        tokens = value.replace('\t', ' ').split('\n')
        for i in range(len(tokens)):
            self.stringValueBuffer.append('\n')
            self.stringValueBuffer.append(self.padding(self.indentLength,' '))
            self.stringValueBuffer.append(self.block)
            self.stringValueBuffer.append(self.padding(self.titleMaxLength-len(title),' '))
            self.stringValueBuffer.append(title if i==0 else self.padding(len(title),' '))
            self.stringValueBuffer.append(' : ' if i==0 and not title == '' else '   ')
            self.stringValueBuffer.append(tokens[i])
            self.calcPadding(title, tokens[i])

    def padding(self, keylength, input):
        return ''.join ([input for x in range(int(keylength))])

    def calcPadding(self, title, value):
        newPadding = (4+len(value)+(2*self.titleMaxLength)-len(title)-len(self.topTitle))/2
        self._padding = int(newPadding) if self._padding < newPadding else self._padding

    def header(self):
        _blockPad = self.padding(self._padding, self.block) 
        return (
            '\n'
            +self.padding(self.indentLength,' ')
            +self.padding(self._padding, self.block[0]) 
            +self.topTitle
            +self.padding(self._padding -1 + len(self.block), self.block[0])
        )

    def footer(self):
        return (
            '\n'
            +self.padding(self.indentLength, ' ')
            +self.padding((2*self._padding)+len(self.topTitle) + 2*len(self.block)-1, self.block[0])
        )

    def stringValue(self):
        returnValue = ''
        _header = self.header()
        _footer = self.footer()
        returnValue+=_header
        returnValue+=self.appendRightBlocks(self.stringValueBuffer)
        returnValue+=_footer
        return returnValue

class Stage(InfoRecord):
    def __init__(self, text, block='=', spaceWidth=10, indentLength=0, topTitle = ''):
        super().__init__(indentLength,block,topTitle,spaceWidth-3 if spaceWidth > 3 else spaceWidth+2)
        self.setRecord('', text)