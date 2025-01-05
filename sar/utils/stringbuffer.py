#**************************************************
# ListTables class V 1.0
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 12/27/2024
#**************************************************
class Stringbuffer:
    def __init__(self, buf = ['',]):
        self.buf = list(buf)

    def append(self, subst):
        self.buf+=list(subst) if not isinstance(subst, list) else subst

    def stringValue(self):
        return ''.join([x for x in self.buf])

    def len(self):
        return len(self.buf)