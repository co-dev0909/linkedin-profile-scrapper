from typing import Dict

from selenium.common.exceptions import WebDriverException
from .linked_in_login import LoginLinkedin
from .search_person import PersonSearchScrap


def linkedin_login(data=None) -> Dict:
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
    if data is None:
        data = {}
    try:
        login = LoginLinkedin(proxy=data.get('proxy', ''))
        response = login.login()
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
        j = PersonSearchScrap(proxy=data.get('proxy', ''), linkedin_url=data.get("url"), file_name=data.get("name"))
        result_data, raise_exception = j.search_profile_links()
        if result_data == 404:
            return {"Response": "Page Not Found", "StatusCode": 404, "data": None}
        if result_data == 401:
            return {"Response": "Invalid Username Password", "StatusCode": 401, "data": None}
        return {"Response": "Success", "StatusCode": 200, "data": result_data, "raise_exception": raise_exception}
    except (Exception, WebDriverException) as e:
        return {"Response": "Something went wrong!", "StatusCode": 400, "error": str(e)}
