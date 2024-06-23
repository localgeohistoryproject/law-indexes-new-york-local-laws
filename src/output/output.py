import os
from pathlib import Path
import re

data1969To2003 = ''
file1969To2003 = '../../intermediate/1969-2003.txt'
if os.path.isfile(file1969To2003):
    file1969To2003 = open(file1969To2003, 'r', encoding='Windows-1252', newline="\r\n")
    while fileLine := file1969To2003.readline():
        data1969To2003 += fileLine
    data1969To2003 = re.sub(r'~\r', '', data1969To2003)
    data1969To2003 = re.sub(r'\r\n' , '~', data1969To2003)
    data1969To2003 = re.sub(r'  *' , ' ', data1969To2003)
    data1969To2003 = re.sub(r' *~~* *' , '~', data1969To2003)
    data1969To2003 = re.sub(r'[~ ]*[|][~ ]*' , '|', data1969To2003) # Ok through this line
    data1969To2003 = re.sub(r'¨', 'a', data1969To2003)
    data1969To2003 = 'Municipality Type|Municipality Name|Year|Number of Law|Filing Date|Title|Subject|Pages|Entry Date\n' + data1969To2003