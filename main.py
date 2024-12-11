from scraper.main import search_person_profile_links
from CONSTANTS import LINKEDIN_URL

persons_data = search_person_profile_links(data={
    "linkedin_url": LINKEDIN_URL,
})

print(persons_data)
