## Converter

This script converts Core NLP XML files to Brat Ann format ***Enhanced++ Dependencies***. It takes the name of the input XML file as a command-line argument and produces two output files: annotation.conf and visual.conf.

Enhanced++ Dependencies includes Part-of-Speech (POS) and the relations between them (dependencies)


## Usage
To use this script, simply run it from the command line, providing the name of the input XML file as an argument:

```
python3 converter.py [fileToConvert.xml]
```

This will generate 3 files:
  - fileToConvert.ann
  - visual.conf
  - annotation.conf

## Warning
- Note that this script requires the xml.etree.ElementTree module, which is part of the Python Standard Library. Therefore, no additional dependencies are required to run this script.

- Also, the script assumes that the input XML file has the correct format, with a document element containing sentences elements, each of which contains tokens and dependencies elements. If the input file has a different structure, the script may not work correctly.

- The purpose of this tool is to convert only one file and NOT multiple file.
