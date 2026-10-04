from dotenv import load_dotenv
import os
import requests
from langchain.tools import tool

load_dotenv()
REST_COUNTRIES_API_KEY = os.getenv("REST_COUNTRIES_API_KEY")
COUNTRIES_URL = "https://api.restcountries.com/countries/v5"


@tool
def get_countries_and_cities(query: str) -> dict:
    """Look up a country and its capital cities, plus basic country info."""
    if not REST_COUNTRIES_API_KEY:
        return {"error": "REST_COUNTRIES_API_KEY is not set."}

    response = requests.get(
        COUNTRIES_URL,
        params={
            "q": query,
            "limit": 5,
            "response_fields": (
                "names.common,names.official,codes.alpha_2,capitals,"
                "region,subregion,population,currencies,languages,"
                "flag.emoji,timezones"
            ),
        },
        headers={"Authorization": f"Bearer {REST_COUNTRIES_API_KEY}"},
        timeout=15,
    )
    data = response.json()

    if not response.ok:
        errors = data.get("errors") or [{"message": response.reason}]
        return {"error": errors[0].get("message", "Country lookup failed.")}

    countries = []
    for country in data.get("data", {}).get("objects", []):
        countries.append(
            {
                "name": country.get("names", {}).get("common"),
                "official_name": country.get("names", {}).get("official"),
                "code": country.get("codes", {}).get("alpha_2"),
                "region": country.get("region"),
                "subregion": country.get("subregion"),
                "population": country.get("population"),
                "cities": [
                    city.get("name") if isinstance(city, dict) else city
                    for city in country.get("capitals") or []
                ],
                "currencies": [
                    currency.get("name") if isinstance(currency, dict) else currency
                    for currency in country.get("currencies") or []
                ],
                "languages": [
                    language.get("name") if isinstance(language, dict) else language
                    for language in country.get("languages") or []
                ],
                "timezones": country.get("timezones"),
                "flag": (country.get("flag") or {}).get("emoji"),
            }
        )

    return {"query": query, "countries": countries}
