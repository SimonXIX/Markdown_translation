# @name: translate.py
# @creation_date: 2023-08-24
# @license: GNU Affero General Public License, Version 3 <https://www.gnu.org/licenses/agpl-3.0.en.html>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Sends batches of Markdown files to a locally-running LibreTranslate API and outputs translated Markdown files
# @acknowledgements:

import json
from pathlib import Path

import requests
import frontmatter  # pip install python-frontmatter

# variables
input_language = 'en'
output_language = 'eo'
url = "http://localhost:5000/translate"
base_directory = Path('/Users/ad7588/projects/copim_website_inate/copim_website/content/')
input_directory = base_directory / input_language 
output_directory = base_directory / output_language
 
# iterate over files with .md suffix in the input directory
for file_path in Path(input_directory).rglob("*.md"):    
    # read Markdown file
    text = frontmatter.load(file_path)

    # send content of Markdown file to LibreTranslate API
    payload = {
        "q": text.content,
        "source": input_language,
        "target": output_language,
        "format": "text",
        "api_key": ""
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    data = response.json()
    text.content = data['translatedText']

    # create output subdirectory if it doesn't exist
    relative_file_path = file_path.relative_to(input_directory)
    write_directory = output_directory / relative_file_path
    write_directory.parent.mkdir(parents=True, exist_ok=True)
    
    write_file_path = write_directory / file_path.name
 
    # write new Markdown file
    with open(write_file_path, 'w') as f:
        f.write(frontmatter.dumps(text))
