from .actions import linkedin_login
from .objects import Scraper


class LoginLinkedin(Scraper):

    def __init__(self, proxy=None):
        self.driver = self.initialize(proxy=proxy)

    def login(self, email="", password=""):
        return linkedin_login(driver=self.driver, email=email, password=password)
