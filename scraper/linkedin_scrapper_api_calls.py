import requests

BASE_URL = "https://www.linkedin.com/jobs-guest/api/typeaheadHits"


def get_company_ids_by_name_search(name: str) -> dict:
    return requests.get(
        url=BASE_URL, params={"typeaheadType": "COMPANY", "query": name}
    ).json()


def get_geo_location_ids_by_name_search(name: str) -> dict:
    return requests.get(
        url=BASE_URL,
        params={
            "typeaheadType": "GEO",
            "query": name,
            "geoTypes": "POPULATED_PLACE,ADMIN_DIVISION_2,MARKET_AREA,COUNTRY_REGION",
        },
        timeout=30,
    ).json()
