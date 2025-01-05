#**************************************************
# scansar V 1.3
# Author: Mohamed Hegazy
# Last updated by Mohamed Hegazy - 1/2/2025
#**************************************************

from sar import sarscanner
#from sar.sarscanner import sarscanner
import sys

try:
    fileName=sys.argv[1].strip()
except:
    print("Invalid command")
    exit(1)

try:
    with open(fileName) as fhand:
        sarscanner.singleFileScan(fhand)
except sar.SarException as e:
    print(e.message)