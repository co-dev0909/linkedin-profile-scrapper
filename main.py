from scraper.main import search_person_profile_links
from CONSTANTS import LINKEDIN_URL

persons_data = search_person_profile_links(data={
    "url": LINKEDIN_URL,
})

raise_exception = persons_data.get("raise_exception")
if raise_exception:
    print("raise_exception: ", raise_exception)

print(persons_data)
