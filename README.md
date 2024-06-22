# Law Indexes: New York (Local Laws)

[![DOI](https://zenodo.org/badge/737476182.svg)](https://zenodo.org/doi/10.5281/zenodo.10446244)

## Summary

Under [Article IX (Local Governments) of the Constitution of the State of New York](https://www.nysenate.gov/legislation/laws/CNS/A9), adopted in 1963, local governments in the State of New York have the power to adopt local laws. To effectuate the article, the Legislature enacted the [Municipal Home Rule Law](https://www.nysenate.gov/legislation/laws/MHR/) ([1963 N.Y. Laws 2697, Ch. 843](https://hdl.handle.net/2027/uc1.a0001834712?urlappend=%3Bseq=893%3Bownerid=113368669-899)), which outlines the process that local governments must follow to adopt local laws. [Section 27 of the Law](https://www.nysenate.gov/legislation/laws/MHR/27) requires local governments to file local laws with the Secretary of State before they can become effective.

This dataset contains index entries for over 200,000 local laws filed with the Secretary of State in or after 1969, and is derived from information released under 2 Freedom of Information Law (FOIL) requests. A DataPerfect database primarily covering from 1969 to 2003 was released under FOIL Request No. DOS-22-02-052. Additional information primarily covering from 1998 to 2024 was released under FOIL Request No. R000244-022024. These records were requested to expand the Local Geohistory Project, which aims to educate users and disseminate information concerning the geographic history and structure of political subdivisions and local government.

This dataset complements local law volumes published with session laws through 1973, along with printed indexes covering the years 1974 through 1982. With the exception of the most recent years, original local law filings for this time period have been accessioned by the New York State Archives as part of [Series Number 13241](https://iarchives.nysed.gov/xtf/view?docId=ead/findingaids/13241.xml;query=).

## Files

### Input files

The following files were created by the State of New York and released under FOIL Request No. DOS-22-02-052. Thousands of other files, many of which were zero bytes in length, are not included in this repository, as they are not required for accessing the index data:

- **input/LGSS.STR:** *DataPerfect structure file.* This contains the field definitions and panel layouts.
- **input/LGSS.TXX:** *DataPerfect variable-length text field file.* This contains data for the Title field in the index.
- **input/LGSSLAWS:** *DataPerfect data file.* This contains data for all of the remaining fields.

Because of their large size, none of the original files released by the State of New York under FOIL Request No. R000244-022024 are included in this repository.

### Intermediate files

The following files were not created by the State of New York, and are derived from either the input files, or other metadata files created by the State of New York:

- **intermediate/1969-2003.txt:** *Text file.* Direct DataPerfect output from the 3 DataPerfect files included in the **input** folder.

### Output files

The following files were not created by the State of New York, and are derived from the input files:

- **output/LocalLawsIndex.tsv:** *Tab-separated values (TSV) file.* Created using the entire Methodology, including Post-Processing.

## Methodology

### Input to Intermediate Processing

An explanation on how this processing was conducted is found in the **src/intermediate** folder.

### Intermediate to Output Processing

The report as exported by DataPerfect has some formatting challenges, such as mid-row line breaks, and tildes at the ends of rows. Some dates have empty values, which renders imports into PostgreSQL difficult without substituting **\\N** placeholders. In at least two places, diacritic marks are used in lieu of a lowercase letter a. The report is also not consistent with other Local Geohistory Project open data exports.

The following can be run to address these challenges, along with removing extraneous spaces, and adding a header row. Before running, the file should be renamed as **1969-2003.txt**.

```bash
sed "s/~\r//g" "1969-2003.txt" > LocalLawsIndex.tsv
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
