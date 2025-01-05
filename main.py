import json
import os.path

from scraper.main import search_person_profile_links

def scrape_current_data(_input_data, tries=100):
    data = search_person_profile_links(data=_input_data)
    raise_exception = data.get("raise_exception")
    if raise_exception:
        if tries == 0:
            return None
        tries = tries - 1
        try:
            with open("temp.txt", 'r') as temp_file:
                last_url = temp_file.read()
            if last_url:
                _input_data.update({
                    "url": last_url
                })
                with open("temp.txt", 'w') as temp_file:
                    temp_file.write("")
        except FileNotFoundError:
            pass
        return scrape_current_data(_input_data, tries)
    else:
        print(data)

if os.path.exists("input.json"):
    with open("input.json", 'r') as file:
        input_dataset = json.load(file)
    for input_data in input_dataset:
        scrape_current_data(input_data)
else:
    print("Please create `input.json` file first.")
