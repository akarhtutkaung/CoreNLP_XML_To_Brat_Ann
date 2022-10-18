## Converter

This tool will generate the ***Enhanced++ Dependencies*** from CoreNLP into Brat ann file.

Enhanced++ Dependencies includes Part-of-Speech (POS) and the relations between them (dependencies)

## Usage

```
python3 converter.py [fileToConvert.xml]
```
This will generate 3 files:
  - fileToConvert.ann
  - visual.conf
  - annotation.conf

## Warning
The purpose of this tool is to convert only one file and NOT multiple file.