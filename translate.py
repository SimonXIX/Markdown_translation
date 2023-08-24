# @name: translate.py
# @creation_date: 2023-08-24
# @license: GNU Affero General Public License, Version 3 <https://www.gnu.org/licenses/agpl-3.0.en.html>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Sends batches of Markdown files to a locally-running LibreTranslate API and outputs translated Markdown files
# @acknowledgements:

import requests
import json
import frontmatter
import os

# variables
input_language = 'en'
output_language = 'eo'
url = "http://localhost:5000/translate"
base_directory = '/Users/ad7588/projects/copim_website_inate/copim_website/content/'
input_directory = base_directory + input_language + '/'
output_directory = base_directory + output_language + '/'
 
# iterate over files in the input directory
for subdir, dirs, files in os.walk(input_directory):
    for file in files:
        # file name with extension
        file_name = os.path.basename(file)
        read_file = subdir + '/' + file_name

        # read Markdown file
        text = frontmatter.load(read_file)

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

        write_directory = subdir.replace(input_directory, output_directory)
        # Check if the output directory exists
        if not os.path.exists(write_directory):  
            # If it doesn't exist, create it
            os.makedirs(write_directory)

        write_file = write_directory + '/' + file_name

        # write new Markdown file
        with open(write_file, 'w') as f:
            f.write(frontmatter.dumps(text))