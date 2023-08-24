import requests
import json
import frontmatter
import os

# variables
source_language = 'en'
target_language = 'eo'
url = "http://localhost:5000/translate"
base_directory = '/Users/ad7588/projects/copim_website_inate/copim_website/content/'
source_directory = base_directory + source_language + '/'
target_directory = base_directory + target_language + '/'
 
# iterate over files in the source directory
for subdir, dirs, files in os.walk(source_directory):
    for file in files:
        # file name with extension
        file_name = os.path.basename(file)
        read_file = subdir + '/' + file_name

        # read Markdown file
        text = frontmatter.load(read_file)

        # send content of Markdown file to LibreTranslate API
        payload = {
            "q": text.content,
            "source": source_language,
            "target": target_language,
            "format": "text",
            "api_key": ""
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        data = response.json()
        text.content = data['translatedText']

        write_directory = subdir.replace(source_directory, target_directory)
        # Check if the target directory exists
        if not os.path.exists(write_directory):  
            # If it doesn't exist, create it
            os.makedirs(write_directory)

        write_file = write_directory + '/' + file_name

        # write new Markdown file
        with open(write_file, 'w') as f:
            f.write(frontmatter.dumps(text))