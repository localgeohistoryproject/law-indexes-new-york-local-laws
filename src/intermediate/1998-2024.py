import lxml.etree as ET
import os
from pathlib import Path
import subprocess

# This script converts the information received under
# FOIL Request No. R000244-022024 into pipe-delimited files

# Run private script to get files for processing
# This step can be skipped if the rootFolder is prepopulated with files

missingFolder = './private/missing/'
rootFolder = './private/temporary/'
fileGetScript = './private/1998-2024.py'
if os.path.isfile(fileGetScript):
    subprocess.run(['python3', fileGetScript])

# Open intermediate file and add header

output = open('../../intermediate/1998-2024.txt', 'w', newline="\n")
output.write(
    "docClassId|muni_name|muni_type|doc_year|law_number|date_filed|doc_subject\n")

outputPath = open('./private/1998-2024-path.txt', 'w', newline="\n")
outputPath.write("Sequence|Group|Path\n")

# Prerequisites for processing files

sequence = 1
xsltText = Path('./1998-2024.xslt').read_text()

# Process files in rootFolder

if os.path.isdir(rootFolder):

    # Get file list

    fileList = os.listdir(rootFolder)
    fileList.sort()

    # Loop through files

    for file in fileList:

        filePath = rootFolder + file
        missingPath = missingFolder + file
        batchName = file.split(".")[0]

        # Process file

        if os.path.isfile(filePath):

            # Read file contents into string

            fileText = Path(filePath).read_text()

            # Some files were missing the end portion.
            # Attach blank filler tags to complete.

            if os.path.isfile(missingPath):
                fileText = fileText + Path(missingPath).read_text()

            # Transform file using stylesheet

            xml = ET.fromstring(fileText)
            xslt = ET.fromstring(xsltText)
            transform = ET.XSLT(xslt)
            xml = str(transform(xml)).rstrip("\n").split("\n")

            # Process index entries

            for xmlLine in xml:

                # Split off file name

                xmlLine = xmlLine.split('|')
                fileName = xmlLine.pop()
                xmlLine = "|".join(xmlLine)

                # Write outputs

                output.write(xmlLine + "\n")
                outputPath.write(str(sequence) + '|' +
                                 batchName + '|' + fileName + "\n")
                sequence += 1
