A Python library for tabulating and analyzing sar (sysstat) data.

**scansar provides builtin features for:**
1. Parsing and loading sar (sysstat) data into table (tuple-list) structure for in-depth analysis.
2. Basic analysis of sar data contained in single file / StringIO stream.
3. JSON based setting control on scope of data analysis.
4. Library of utilities for expanding sar data analysis.


Third party libraries (e.g., Pandas) can alternatively be used to analyze data that is loaded by scansar.

**Examples (Please refer to /test/ folder for additional test case scenarios):**

**sar**

```
mhega@... scansar % python3
Python 3.12.7 (main, Oct 16 2024, 20:21:06) [Clang 16.0.0 (clang-1600.0.26.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> 
>>> from sar import sar
>>> with open ('test/saru.txt') as filehandle:
...     sarData=sar(filehandle)
... 
>>>
>>> len(sarData.tableList)
31
>>>
>>> len(sarData.fetchtables('%user'))
0
>>>
>>> len(sarData.fetchtables('%usr'))
5
>>>
>>> sarData.fetchtables('%usr')
[<sar.utils.table.Table object at 0x100c511f0>, <sar.utils.table.Table object at 0x100c51700>, :::]
>>>
>>> from sar.utils import Table
>>> 
>>> usrTables=sarData.fetchtables('%usr')
>>> usrTables[0].print()
Timestamp     CPU     %usr      %nice     %sys     %iowait     %steal     %irq     %soft     %guest     %idle     
---------     ---     ----      -----     ----     -------     ------     ----     -----     ------     -----     
00:05:31      1       3.21      0.00      1.81     8.17        0.00       0.00     0.06      0.00       86.75     
00:10:01      1       2.22      0.00      0.66     0.04        0.00       0.00     0.01      0.00       97.06     
00:15:01      1       2.56      0.00      0.57     0.06        0.00       0.00     0.02      0.00       96.80     
00:20:01      1       2.33      0.00      0.72     0.06        0.00       0.00     0.02      0.00       96.87     
00:25:01      1       2.22      0.00      0.58     0.03        0.00       0.00     0.01      0.00       97.15     
00:30:01      1       2.23      0.00      0.67     0.07        0.00       0.00     0.01      0.00       97.01     
00:35:02      1       2.95      0.00      0.65     0.04        0.00       0.00     0.03      0.00       96.33     
00:40:01      1       2.74      0.00      0.78     0.04        0.00       0.00     0.03      0.00       96.41
:::
>>> usrTables[0].get(('Timestamp','CPU','%usr'))
[('00:05:31', '1', '3.21'), ('00:10:01', '1', '2.22'), ('00:15:01', '1', '2.56'), ('00:20:01', '1', '2.33'), :::]
:::
```

#
**scansar**

```
mhega@... scansar % python3 scansar.py test/saru.txt 

===================================
=          Analyzing Memory       =
===================================

Timestamp     %memused                                     Timestamp     kbmemused                                 Timestamp     %commit                                     
---------     --------                                     ---------     ---------                                 ---------     -------                                     
19:35:01      78.27        ▄▄▄▄▄▄▄                         19:35:01      38380936      ▄▄▄                         23:45:01      70.07       ▄▄▄▄▄▄▄                         
19:30:01      78.18        ▄▄▄▄▄▄▄                         19:30:01      38337740      ▄▄▄                         23:55:01      70.07       ▄▄▄▄▄▄▄                         
19:25:01      78.12        ▄▄▄▄▄▄▄                         19:25:01      38306944      ▄▄▄                         23:25:01      70.06       ▄▄▄▄▄▄▄                         
19:20:01      78.02        ▄▄▄▄▄▄▄                         19:20:01      38260880      ▄▄▄                         23:40:01      70.06       ▄▄▄▄▄▄▄                         
22:35:01      78.02        ▄▄▄▄▄▄▄                         22:35:01      38259020      ▄▄▄                         23:50:01      70.06       ▄▄▄▄▄▄▄                         
                                                                                                                                                                             

=================================
=          Analyzing Swap       =
=================================

Timestamp     pswpin/s                              Timestamp     pswpout/s                              
---------     --------                              ---------     ---------                              
00:05:31      0.00                                  00:05:31      0.00                                   
00:10:01      0.00                                  00:10:01      0.00                                   
00:15:01      0.00                                  00:15:01      0.00                                   
00:20:01      0.00                                  00:20:01      0.00                                   
00:25:01      0.00                                  00:25:01      0.00                                   
                                                                                                         

===============================
=          Analyzing CPU      =
===============================

Timestamp     CPU     %usr                                                                           Timestamp     CPU     %usr                                                                 
---------     ---     ----                                                                           ---------     ---     ----                                                                 
22:25:01      0       44.76     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                         22:40:01      2       34.78     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                         
22:40:01      0       41.81     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                            22:15:01      2       28.42     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                               
22:30:01      0       34.66     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                   22:30:01      2       28.16     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                               
22:20:01      0       29.88     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                        22:45:01      2       26.89     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                 
21:55:01      0       29.06     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                        22:20:01      2       25.69     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                  
                                                                                                                                                                                                

Timestamp     CPU     %usr                                                                    Timestamp     CPU     %usr                                                                       
---------     ---     ----                                                                    ---------     ---     ----                                                                       
22:40:01      all     37.12     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                         22:40:01      3       40.10     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                         
22:25:01      all     35.83     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                           22:25:01      3       35.42     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                              
22:30:01      all     28.53     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                  22:30:01      3       31.07     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                  
22:15:01      all     28.42     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                  22:15:01      3       30.15     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                   
22:45:01      all     27.41     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                   22:45:01      3       28.16     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                     
                                                                                                                                                                                               

Timestamp     CPU     %usr                                                                     Timestamp     CPU     %sys                                
---------     ---     ----                                                                     ---------     ---     ----                                
22:25:01      1       38.20     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                         00:05:31      0       2.23     ▄▄                         
22:40:01      1       31.80     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                22:40:01      0       1.16     ▄                          
21:45:01      1       30.23     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                 13:55:01      0       1.07     ▄                          
22:15:01      1       27.64     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                    19:35:01      0       1.07     ▄                          
22:45:01      1       25.85     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                                      19:40:01      0       1.07     ▄                          
                                                                                                                                                         

Timestamp     CPU     %sys                                Timestamp     CPU     %sys                                Timestamp     CPU     %sys                                
---------     ---     ----                                ---------     ---     ----                                ---------     ---     ----                                
00:05:31      2       2.00     ▄▄                         00:05:31      all     2.02     ▄▄                         00:05:31      3       2.05     ▄▄                         
19:40:01      2       1.06     ▄                          19:40:01      all     1.07     ▄                          17:20:01      3       1.03     ▄                          
15:40:01      2       1.03     ▄                          20:40:01      all     1.02     ▄                          19:40:01      3       1.02     ▄                          
21:45:01      2       1.03     ▄                          15:40:01      all     0.98                                20:40:01      3       1.00     ▄                          
15:15:01      2       0.99                                22:40:01      all     0.95                                14:40:01      3       0.95                                
                                                                                                                                                                              

Timestamp     CPU     %sys                               Timestamp     CPU     %iowait                                                 Timestamp     CPU     %iowait                                    
---------     ---     ----                               ---------     ---     -------                                                 ---------     ---     -------                                    
00:05:31      1       1.81     ▄                         00:05:31      0       19.03       ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                         00:05:31      2       6.67        ▄▄▄▄▄▄                         
20:40:01      1       1.20     ▄                         16:40:01      0       0.19                                                    21:45:01      2       0.15                                       
19:40:01      1       1.13     ▄                         15:45:01      0       0.15                                                    17:00:01      2       0.12                                       
20:20:01      1       1.10     ▄                         16:45:01      0       0.13                                                    12:40:01      2       0.11                                       
15:40:01      1       1.03     ▄                         17:40:01      0       0.13                                                    16:20:01      2       0.11                                       
                                                                                                                                                                                                        

Timestamp     CPU     %iowait                                       Timestamp     CPU     %iowait                                  Timestamp     CPU     %iowait                                      
---------     ---     -------                                       ---------     ---     -------                                  ---------     ---     -------                                      
00:05:31      all     9.65        ▄▄▄▄▄▄▄▄▄                         00:05:31      3       4.74        ▄▄▄▄                         00:05:31      1       8.17        ▄▄▄▄▄▄▄▄                         
19:40:01      all     0.12                                          22:40:01      3       0.19                                     20:40:01      1       0.16                                         
22:40:01      all     0.11                                          19:40:01      3       0.16                                     17:40:01      1       0.15                                         
16:40:01      all     0.10                                          13:40:01      3       0.15                                     19:40:01      1       0.15                                         
20:40:01      all     0.10                                          15:40:01      3       0.14                                     20:35:01      1       0.14                                         
                                                                                                                                                                                                      

===================================
=          Analyzing Others       =
===================================

Timestamp     bwrtn/s                                 
---------     -------                                 
00:05:31      23240.48     ▄▄                         
17:20:01      881.25                                  
15:40:01      858.05                                  
18:40:01      834.29                                  
16:55:01      817.32                                  
                                                      
mhega@... scansar %
```
