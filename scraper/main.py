from typing import Dict

from selenium.common.exceptions import WebDriverException
# from .company import Company
# from .job_search import JobSearch
# from .jobs import Job
from .linked_in_login import LoginLinkedin
# from .person import Person
# from .search_job import JobSearchScrap
from .search_person import PersonSearchScrap


def linkedin_login(data: Dict) -> Dict:
    """
    linkedin login by credentials
    Args:
        data: {
                "email": str,
                "password": str
            }

    Returns:
        result in dictionary
    """
    try:
        if "email" not in data or "password" not in data:
            return {"Response": "Missing email or password", "StatusCode": 400}
        email = data.get('email')
        password = data.get("password")
        login = LoginLinkedin(proxy=data.get('proxy', ''))
        response = login.login(email=email, password=password)
        if response:
            return {"Response": "Success", "StatusCode": 200}
        return {"Response": "Invalid Username Password", "StatusCode": 401}
    except (Exception, WebDriverException) as e:
        return {"Response": "Something went wrong!", "StatusCode": 400, "error": str(e)}

def search_persons_data(data: Dict) -> Dict:
    """
    search linkedin users by parameters
    Args:
        data: {
                "first_name": str,
                "last_name": str,
                "location": str,
                "keywords": str,
                "limit": int
            }
    Returns:
        result in dictionary
    """
    try:
        j = PersonSearchScrap(proxy=data.get('proxy', ''))
        result_data = j.search(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            location=data.get("location", ""),
            keywords=data.get("keywords", ""),
            company_name=data.get("company_name", ""),
            limit=data.get("limit", None)
        )
        if result_data == 404:
            return {"Response": "Page Not Found", "StatusCode": 404, "data": None}
        if result_data == 401:
            return {"Response": "Invalid Username Password", "StatusCode": 401, "data": None}
        return {"Response": "Success", "StatusCode": 200, "data": result_data}
    except (Exception, WebDriverException) as e:
        return {"Response": "Something went wrong!", "StatusCode": 400, "error": str(e)}


def search_person_profile_links(data: Dict) -> Dict:
    """
    search linkedin users by parameters
    Args:
        data: {
                "linkedin_url": str
            }
    Returns:
        result in dictionary
    """
    try:
        j = PersonSearchScrap(proxy=data.get('proxy', ''), linkedin_url=data.get("linkedin_url"))
        result_data = j.search_profile_links()
        if result_data == 404:
            return {"Response": "Page Not Found", "StatusCode": 404, "data": None}
        if result_data == 401:
            return {"Response": "Invalid Username Password", "StatusCode": 401, "data": None}
        return {"Response": "Success", "StatusCode": 200, "data": result_data}
    except (Exception, WebDriverException) as e:
        return {"Response": "Something went wrong!", "StatusCode": 400, "error": str(e)}
