# Law Indexes: New York (Local Laws)

## Summary

Under [Article IX (Local Governments) of the Constitution of the State of New York](https://www.nysenate.gov/legislation/laws/CNS/A9), adopted in 1963, local governments in the State of New York have the power to adopt local laws. To effectuate the article, the Legislature enacted the [Municipal Home Rule Law](https://www.nysenate.gov/legislation/laws/MHR/) ([1963 N.Y. Laws 2697, Ch. 843](https://hdl.handle.net/2027/uc1.a0001834712?urlappend=%3Bseq=893%3Bownerid=113368669-899)), which outlines the process that local governments must follow to adopt local laws. [Section 27 of the Law](https://www.nysenate.gov/legislation/laws/MHR/27) requires local governments to file local laws with the Secretary of State before they can become effective.

This data set contains index records for over 130,000 local laws filed with the Secretary of State, mostly between 1969 and 2003. Under Freedom of Information Law (FOIL) Request No. DOS-22-02-052, a copy of the index database, created using DataPerfect, was released by the State on March 17, 2022. These records were requested to expand the Local Geohistory Project, which aims to educate users and disseminate information concerning the geographic history and structure of political subdivisions and local government.

This data set complements local law volumes published with session laws through 1973, along with printed indexes covering the years 1974 through 1982. Original local law filings for this time period have been accessioned by the New York State Archives as part of [Series Number 13241](https://iarchives.nysed.gov/xtf/view?docId=ead/findingaids/13241.xml;query=).

## Files

### Input files

The following files were created by the State of New York and included in their FOIL response. Thousands of other files, many of which were zero bytes in length, are not included in this repository, as they are not required for accessing the index data:

- **input/LGSS.STR:** *DataPerfect structure file.* This contains the field definitions and panel layouts.
- **input/LGSS.TXX:** *DataPerfect variable-length text field file.* This contains data for the Title field in the index.
- **input/LGSSLAWS:** *DataPerfect data file.* This contains data for all of the remaining fields.

### Output files

The following files were not created by the State of New York, and are derived from the input files:

- **output/LocalLawsIndex.tsv:** *Tab-separated values (TSV) file.* Created using the entire Methodology, including Post-Processing.
- **output/LocalLawsIndex.txt:** *Text file.* Direct DataPerfect output created using all but the Post-Processing portion of the Methodology.

## Methodology

The following instructions can be used to re-create the included output files from the three included input files. These instructions were created using Lubuntu; however, URLs to software instructions for key packages are provided to facilitate installations on other operating systems.

### Prerequisites

Internet Archive hosts a copy of [DataPerfect](https://archive.org/details/freesoftwarefordos_dbase_dataperfect), the software used to view the source data files. Because modern computers cannot run DOS-based programs like DataPerfect natively, an emulator like [DOSBox](https://www.dosbox.com/) must be installed first.

On Lubuntu, run the following code via QTerminal to install both software packages, import the necessary files from this repository, and start DOSBox:

```bash
sudo apt-get install awk dosbox git iconv sed
wget https://archive.org/download/freesoftwarefordos_dbase_dataperfect/dp26x.zip
unzip dp26x.zip -d ~/dataperfect
git clone https://github.com/localgeohistoryproject/law-indexes-new-york-local-laws.git ~/law-indexes-new-york-local-laws
cp ~/law-indexes-new-york-local-laws/input/LGSS* ~/dataperfect
rm ~/dataperfect/LGSS.IND
dosbox
```

Once DOSBox starts, we also have to mount the folder where the program is installed. Run the following commands to mount the folder and start DataPerfect:

```bash
MOUNT P ~/dataperfect
P:\
DP.EXE
```

### Using DataPerfect

- DataPerfect should open to a list of databases. Select **LGSS** from the options and press enter.
- Note that the DataPerfect index file (**.IND**) has been omitted, as it is not necessary to perform data extracts. If a warning appears because this file is not found, press **1** to select **Create a New Index File with New Indexes for All Data Files**. (For users who have the index file, this step may be unnecessary).
- The database should now be open with a list of panels. Select **Local Laws Index** from the options and press enter.
- If the index file is omitted, another warning due to the missing index may appear. Two options are available:
  - Pressing **4** to select **Export Data Without Using Index** allows one to quickly continue on to create the report; however, the sort order of the rows may differ from other options.
  - Pressing **3** to select **Re-create the Indexes for All Files** takes several hours to reconstruct the index file; however, the order of the rows will match the order had the original index file been included. This option was used for the output in this repository. Once complete, press **Shift-F7** for the report list.
- For users who have the index file (omitted from this repository) who did not receive the last warning, press **Shift-F7** for the report list.
- The report list should now be open. Select **Built-In Short Reports** and press enter.
- In the **Built-In Report/Export** dialog, make the following changes:
  - Press **2 (Disk File On/Off)**, then press **1 (Create File)**, then type in the desired name of the output file, then press enter.
  - Press **8 (Report/Export Format)**, then press **6 (Export DOS Delimited Text)**, then enter through the remaining default options for delimiter and line ending types.
- Press **Shift-F7** to begin the report. It may take several hours to complete, and the export row count may return to 0 during the process.
- Once the report is complete, it will return to the **Built-In Report/Export** dialog. You can then exit out of DataPerfect and DOSBox.

The exported report should be saved under the previously-selected file name in the **~/dataperfect** folder.

For more information about DataPerfect, see Ralph Alvy's [Mastering DataPerfect®](https://web.archive.org/web/20061014032117/http://dataperfect.nl/files/masteringdataperfect.pdf).

The work and information about its 2005 PDF release are preserved on the Internet Archive's [Wayback Machine](https://web.archive.org/web/20060306035547/http://lists.dataperfect.nl/pipermail/dataperf/2005-June/000436.html).

### Post-Processing

The report as exported by DataPerfect has some formatting challenges, such as mid-row line breaks, and tildes at the ends of rows. Some dates have empty values, which renders imports into PostgreSQL difficult without substituting **\\N** placeholders. In at least two places, diacritic marks are used in lieu of a lowercase letter a. The report is also not consistent with other Local Geohistory Project open data exports.

The following can be run to address these challenges, along with removing extraneous spaces, and adding a header row. Before running, the file should be renamed as **LocalLawsIndex.txt**.

```bash
sed "s/~\r//g" LocalLawsIndex.txt > LocalLawsIndex.tsv
sed -i -z "s/\r\n/~/g" LocalLawsIndex.tsv
sed -i 's/  */ /g' LocalLawsIndex.tsv
sed -i 's/ *~~* */~/g' LocalLawsIndex.tsv
sed -i "s/~* *~*|~* *~*/|/g" LocalLawsIndex.tsv
sed -i "s/|/\t/g" LocalLawsIndex.tsv
awk -F'\t' -v OFS='\t' '!$5{ $5="\\N" }1' LocalLawsIndex.tsv > temp.tsv
awk -F'\t' -v OFS='\t' '!$9{ $9="\\N" }1' temp.tsv > LocalLawsIndex.tsv
rm temp.tsv
cp LocalLawsIndex.tsv Win1252.tsv
iconv -f WINDOWS-1252 -t UTF-8 Win1252.tsv > LocalLawsIndex.tsv
rm Win1252.tsv
sed -i 's/¨/a/g' LocalLawsIndex.tsv
sed -i '1 i\Municipality Type\tMunicipality Name\tYear\tNumber of Law\tFiling Date\tTitle\tSubject\tPages\tEntry Date' LocalLawsIndex.tsv
```

## Next steps

### Using the tab-separated values (TSV) file

TSV files do not use quotation marks to escape fields containing tabs; therefore, the **String delimiter** option in LibreOffice Calc or the **Text qualifier** option in Microsoft Excel must be left blank to ensure the file imports accurately.

The file uses Unix-style [line endings](https://en.wikipedia.org/wiki/Newline#Representations) (LF), which may have to be adjusted in applications that expect Windows-style line endings (CR LF).

A header row containing column names determined by examining the DataPerfect data panels manually is included. When importing into a relational database system, like PostgreSQL, it may be necessary to remove this header line, particularly when using the [PostgreSQL COPY function](https://www.postgresql.org/docs/15/sql-copy.html) in the Text Format.
