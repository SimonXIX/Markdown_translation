# Open source machine translation for Markdown files

A script and Docker environment for running automated open source machine translations of batches of Markdown files, suitable for quickly providing translations for [Hugo](https://gohugo.io/) websites or [Flask](https://flask.palletsprojects.com/en/2.3.x/) web applications. This uses [LibreTranslate](https://libretranslate.com/), a free and open source machine translation API initiated as a submodule to this repository: https://github.com/LibreTranslate/LibreTranslate.

As with all machine translations, the outputted translation may be imperfect and ideally all translations should be checked by a human translator.

## LibreTranslate API

To start the LibreTranslate server for accessing the API, first ensure Docker is installed. Then simply run

`./startLibreTranslate.sh`

to run LibreTranslate's own run.sh Bash script for bring the Docker container up. You can then access the locally running LibreTranslate server at http://localhost:5000. 

## Python script

To run the Python script for machine translation of batches of Markdown files, ensure that Python is installed and run 

`pip install -r requirements.txt`

to install required Python libraries.

Adjust the variables in translate.py to point to whatever directory contains the Markdown files you want translated. By default the script looks at a base directory and looks for a 'en' subdirectory containing English language Markdown files. Set the output_language variable to the language you wish to translate into using the language's two-letter [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) code. 

Then run

`python3 ./translate.py`

This will output translated Markdown files into a subdirectory in the base directory using the two-letter ISO 639-1 code for the output language. It will also replicate any directory structure present in the input directory.