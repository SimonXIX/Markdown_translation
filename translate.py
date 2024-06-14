# @name: translate.py
# @creation_date: 2023-08-24
# @license: GNU Affero General Public License, Version 3 <https://www.gnu.org/licenses/agpl-3.0.en.html>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Sends batches of Markdown files to a locally-running LibreTranslate API and outputs translated Markdown files
# @acknowledgements:

import json
from pathlib import Path

import re
import requests
import frontmatter  # pip install python-frontmatter

# VARIABLES
input_language = 'en'
output_language = 'fr'
url = "http://localhost:5000/translate"
base_directory = Path('/Users/ad7588/projects/translation/test_files')
input_directory = base_directory / input_language 
output_directory = base_directory / output_language

# SUBROUTINES

# function to extract and replace text that we do not want translated (specifically anything between ``` and ``` code blocks)
def preprocess_text(text, placeholders):
    # placeholder pattern (you can customize this)
    pattern = r'```(.*?)```'
    #pattern = r'\[NO_TRANSLATE\](.*?)\[/NO_TRANSLATE\]'
    matches = re.findall(pattern, text, re.DOTALL)
    for i, match in enumerate(matches):
        placeholder = f'__PLACEHOLDER_{i}__'
        placeholders[placeholder] = match
        text = text.replace(f'```{match}```', placeholder)
        #text = text.replace(f'[NO_TRANSLATE]{match}[/NO_TRANSLATE]', placeholder)
    return text

# function to reinsert the original segments back into the text
def postprocess_text(translated_text, placeholders):
    for placeholder, original_text in placeholders.items():
        translated_text = translated_text.replace(placeholder, f'```{original_text}```')
        #translated_text = translated_text.replace(placeholder, '[NO_TRANSLATE]' + original_text + '[/NO_TRANSLATE]')
    return translated_text

# function to translate text using LibreTranslate API
def translate_text(text, input_language, output_language):

    # build Json payload to send to LibreTranslate API
    payload = {
        "q": text,
        "source": input_language,
        "target": output_language,
        "format": "html",
        "api_key": ""
    }
    headers = {"Content-Type": "application/json"}

    # send payload to LibreTranslate API
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    return response.json()['translatedText']

# MAIN PROGRAM

# iterate over files with .md suffix in the input directory
for file_path in Path(input_directory).rglob("*.md"):    
    # read Markdown file
    text = frontmatter.load(file_path)

    placeholders = {}

    # preprocess text content of Markdown file to replace not-to-be-translated segments of text with placeholders
    text.content = preprocess_text(text.content, placeholders)

    # translate the processed text using LibreTranslate API
    text.content = translate_text(text.content, input_language, output_language)

    # postprocess to reinsert the original segments
    text.content = postprocess_text(text.content, placeholders)

    # create output subdirectory if it doesn't exist
    relative_file_path = file_path.parent.relative_to(input_directory)
    write_directory = output_directory / relative_file_path
    write_directory.mkdir(parents=True, exist_ok=True)
    
    write_file_path = write_directory / file_path.name
 
    # write new Markdown file
    with open(write_file_path, 'w') as f:
        f.write(frontmatter.dumps(text))
