from scraper import linkedin_login
from CONSTANTS import (
    EMAIL,
    PASSWORD
)

cred = {
    "email": EMAIL,
    "password": PASSWORD,
}

login_response = linkedin_login(cred)
print(login_response)
