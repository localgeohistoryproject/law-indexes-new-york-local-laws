from io import StringIO
import numpy
import os
import pandas
from pathlib import Path
import re

def getGovernmentList():
    data = ''
    file = 'government-lookup.tsv'
    if os.path.isfile(file):
        data = pandas.read_table(file, sep='\t', dtype='str', keep_default_na=False, quoting=3)
        data = data.assign(govLookup=data.lookup_name+'|'+data.lookup_type)
    return data

def changeList(data, file):
    if os.path.isfile(file):
        file = open(file, 'r')
        isHeader = True
        while fileLine := file.readline():
            if isHeader:
                isHeader = False
            else:
                fileLine = fileLine.split('\t')
                data.at[int(fileLine[0]), fileLine[1]] = fileLine[2].strip()
    return data

def convert1969To2003():
    data = ''
    file = '../../intermediate/1969-2003.txt'
    if os.path.isfile(file):
        file = open(file, 'r', encoding='Windows-1252', newline="\r\n")
        while fileLine := file.readline():
            data += fileLine
        file.close()
        data = re.sub(r'~\r', '', data)
        data = re.sub(r'\r\n' , '~', data)
        data = re.sub(r'  *' , ' ', data)
        data = re.sub(r' *~~* *' , '~', data)
        data = re.sub(r'[~ ]*[|][~ ]*' , '|', data)
        data = re.sub(r'¨', 'a', data)
        data = 'muni_type|muni_name|doc_year|law_number|date_filed|doc_subject|Subject|Pages|EntryDate\n' + data
        data = pandas.read_table(StringIO(data), sep='|', dtype='str', keep_default_na=False, quoting=3)
        data = data.assign(docClassId='dos_local_law_doc')
        data = data.reindex(['docClassId', 'muni_name', 'muni_type', 'doc_year', 'law_number', 'date_filed', 'doc_subject'], axis=1)
        data = data.replace(to_replace={'date_filed': r'^(\d{2})[/](\d{2})[/](\d{4})$'}, value=r'\3-\1-\2', regex=True)
        originalData = data.copy()
        file = '../../intermediate/1969-2003-change.tsv'
        data = changeList(data, file)
        comparison = originalData.compare(data, keep_equal=True)
        comparison.to_csv('../intermediate/private/1969-2003-compare.tsv', sep='\t', quoting=3)
    return data

def convert1998To2024():
    data = ''
    file = '../../intermediate/1998-2024.txt'
    if os.path.isfile(file):
        file = Path(file).read_text()
        addFile = '../../intermediate/1998-2024-add.txt'
        addText = ''
        if os.path.isfile(addFile):
            addFile = open(addFile, 'r')
            isHeader = True
            while fileLine := addFile.readline():
                if isHeader:
                    isHeader = False
                else:
                    fileLine = fileLine.split('|')
                    fileLine.pop()
                    addText += '\n' + ('|'.join(fileLine).strip())
            addFile.close()
        file += addText
        data = pandas.read_table(StringIO(file), sep='|', dtype='str', keep_default_na=False, quoting=3)
        data = data.replace(to_replace={'date_filed': r'^(\d{4})(\d{2})(\d{2})\d{6}'}, value=r'\1-\2-\3', regex=True)
        data = data.replace(to_replace={'date_filed': 'nulldate'}, value='')
        originalData = data.copy()
        file = '../../intermediate/1998-2024-change.tsv'
        data = changeList(data, file)
        comparison = originalData.compare(data, keep_equal=True)
        comparison.to_csv('../intermediate/private/1998-2024-compare.tsv', sep='\t', quoting=3)
    return data

def convertConcat(data):
    data = data.replace(to_replace={'docClassId': 'dos_local_law_doc'}, value='Local Laws')
    data = data.replace(to_replace={'docClassId': 'dos_codified_law_doc'}, value='County Codes')
    data = data.fillna('')
    data = data.assign(munLookup=data.muni_name+'|'+data.muni_type)
    data = data.merge(getGovernmentList(), how='outer', left_on='munLookup', right_on='govLookup')
    data = data.fillna('')
    # data = data[data.standard_gnis != '']
    data = data.rename(columns={'standard_name': 'Name', 'standard_type': 'Type', 'standard_gnis': 'GNIS', 'docClassId': 'Law Type', 'doc_year': 'Law Year', 'law_number': 'Law Number', 'date_filed': 'Date Filed', 'doc_subject': 'Subject'})
    data = data.reindex(['Name', 'Type', 'GNIS', 'Law Type', 'Law Year', 'Law Number', 'Date Filed', 'Subject'], axis=1)
    data = data.groupby(['Name', 'Type', 'GNIS', 'Law Type', 'Law Year', 'Law Number', 'Date Filed'], as_index=False).max()
    data['numberNumber'] = data['Law Number'].str.zfill(3)
    data = data.replace(to_replace={'numberNumber': r'^(.*[A-Za-z])$'}, value=r'0\1', regex=True)
    data = data.sort_values(['Name', 'Type', 'GNIS', 'Law Type', 'Law Year', 'numberNumber', 'Date Filed', 'Subject'])
    data = data.drop(columns=['numberNumber'])
    return data

def main():
    data1969To2003 = convert1969To2003()
    data1998To2024 = convert1998To2024()
    data = convertConcat(pandas.concat([data1969To2003, data1998To2024], ignore_index=True))
    data.to_csv('../../output/NYLocalLawIndex.tsv', sep='\t', index=False, quoting=3)

if __name__ == '__main__':
    main()