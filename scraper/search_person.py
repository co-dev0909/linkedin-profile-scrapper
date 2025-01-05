import logging
import os.path
import uuid

from selenium.webdriver.common.by import By

from . import actions, linkedin_scrapper_api_calls as link_api
from .objects import Scraper, PersonSearch

logging.basicConfig()


class PersonSearchScrap(Scraper):
    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5
    first_name = ""
    last_name = ""
    location = ""
    company_name = ""
    keywords = ""

    def __init__(
            self,
            linkedin_url=None,
            file_name=None,
            driver=None,
            scrape=True,
            proxy=None
    ):
        self.linkedin_url = linkedin_url
        self.file_name = file_name
        self.driver = driver
        self.logged_in = False
        self.limit = None
        self.base_url = "https://www.linkedin.com/"

        if not self.driver:
            self.driver = self.initialize(proxy=proxy)

        if scrape:
            actions.login(driver=self.driver)
            self.scrape()

    def scrape(self):
        if self.is_signed_in():
            self.logged_in = True
        else:
            self.logged_in = False

    def search(
            self,
            first_name: str = "",
            last_name: str = "",
            location: str = "",
            keywords: str = "",
            company_name: str = "",
            limit: int = None
    ):
        self.company_name = company_name
        self.first_name = first_name
        self.last_name = last_name
        self.location = location
        self.keywords = keywords
        self.limit = limit
        if self.invalid_link():
            return 404
        if self.logged_in:
            return self.scrape_logged_in()
        return 401

    def scrape_logged_in(self):

        page, persons = 0, []

        if self.location:
            geo_data = link_api.get_geo_location_ids_by_name_search(name=self.location)

            self.location = geo_data[0].get("id", "") if len(geo_data) > 0 else ""

        if self.company_name:
            company_data = link_api.get_company_ids_by_name_search(name=self.company_name)
            company_ids = [comp.get("id", None) for comp in company_data if
                           comp.get("displayName", None) == self.company_name]
            self.company_name = ",".join(company_ids)

        while True:
            page = page + 1
            self.linkedin_url = f"{self.base_url}search/results/people/?"
            if self.first_name:
                self.linkedin_url = f"{self.linkedin_url}firstName={self.first_name.replace(' ', '+').strip()}&"
            if self.last_name:
                self.linkedin_url = f"{self.linkedin_url}lastName={self.last_name.replace(' ', '+').strip()}&"
            if type(self.company_name) is str:
                self.linkedin_url = f"{self.linkedin_url}&f_C={self.company_name}"
            self.linkedin_url = f"{self.linkedin_url}page={page}&"
            if self.keywords:
                self.linkedin_url = f"{self.linkedin_url}keywords={self.keywords.replace(' ', '+').strip()}&"
            if self.location:
                self.linkedin_url = f"{self.linkedin_url}geoUrn={self.location}"

            self.driver.get(self.linkedin_url)
            self.wait(5)
            self.scroll_to_half()
            self.scroll_to_bottom()
            self.wait(2)
            li = self.get_elements_by_time(
                by=By.CLASS_NAME,
                value="reusable-search__result-container",
                seconds=10,
                single=False
            )
            if not li:
                break
            for item in li:

                link = item.find_elements(By.XPATH, './/a')[-1]
                name = link.text.split('\n')[0]
                link = link.get_attribute("href")

                text = item.text.split('\n')[4:-1]
                description = text[0] if len(text) > 0 else ""
                location = text[1] if len(text) > 1 else ""
                description = description + "\n" + text[2] if len(text) > 2 else ""
                p = PersonSearch(
                    link=link,
                    name=name,
                    description=description,
                    location=location
                )
                persons.append(p)
                if self.limit and len(persons) >= self.limit:
                    return [p.__repr__() for p in persons]

        return [p.__repr__() for p in persons]

    def search_profile_links(self):
        if self.invalid_link():
            return 404
        if self.logged_in:
            return self.__search_profile_links_logged_in()
        return 401

    def __search_profile_links_logged_in(self):
        self.driver.get(self.linkedin_url)
        self.wait(5)
        self.scroll_to_half()
        self.scroll_to_bottom()
        self.wait(2)

        total_links = []

        retries = 0
        previous_page = ""
        raise_exception = None

        while True:
            try:
                with open("temp.txt", 'w') as temp_file:
                    temp_file.write(self.driver.current_url)
                elements = self.get_elements_by_time(
                    by=By.XPATH,
                    value='//a[contains(@href, "www.linkedin.com/in/")]',
                    single=False
                )

                if not elements and retries < 3:
                    self.wait(2)
                    self.scroll_to_half()
                    self.wait(1)
                    self.scroll_to_bottom()
                    self.wait(2)
                    retries = retries + 1
                    continue

                retries = 0

                if elements:
                    links = [element.get_attribute("href") for element in elements]
                    total_links.extend(list(set(links)))

                self.wait(2)
                self.scroll_to_half()
                self.wait(1)
                self.scroll_to_bottom()
                self.wait(2)

                self.click_button_error(
                    element=self.get_elements_by_time(
                        by=By.XPATH,
                        value='//button[@aria-label="Next"]',
                    )
                )
                print(len(total_links))

                current_page = self.get_elements_by_time(
                    by=By.XPATH,
                    value='//ul[@role="list"]'
                ).text

                if current_page == previous_page:
                    break
                previous_page = current_page
            except Exception as e:
                print(e)
                raise_exception = True
                break

        if not os.path.exists("profiles"):
            os.mkdir("profiles")
        file_path = "profiles/" + (self.file_name or f"profile_links_{uuid.uuid4()}") + ".txt"

        try:
            with open(file_path, 'r') as file:
                old_data = file.read()
        except FileNotFoundError:
            old_data = ""
        total_links = [
            item.split("/in/")[-1].split('?')[0]
            for item in total_links
        ]
        total_links.extend(old_data.split('\n'))

        total_links = "\n".join([
            item
            for item in total_links
        ])

        with open(file_path, "w") as file:
            file.write(total_links)
        return total_links, raise_exception
