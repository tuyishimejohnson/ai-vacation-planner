from dotenv import load_dotenv
import os
import requests

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


def _require_api_key() -> str | None:
    if not GOOGLE_MAPS_API_KEY:
        return "GOOGLE_MAPS_API_KEY is not set."
    return None


def search_places(query: str, limit: int = 5) -> dict:
    """Search Google Maps for places by name, type, or area.

    Use for cities, landmarks, hotels, restaurants, parks, or addresses
    (e.g. 'hotels in Kigali', 'Nyungwe Forest', 'cafes near Musanze').
    """
    if error := _require_api_key():
        return {"error": error}

    response = requests.get(
        PLACES_URL,
        params={
            "query": query,
            "key": GOOGLE_MAPS_API_KEY,
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") not in {"OK", "ZERO_RESULTS"}:
        return {
            "error": data.get(
                "error_message", data.get("status", "Places search failed.")
            )
        }

    places = []
    for place in data.get("results", [])[: max(1, min(limit, 10))]:
        location = place.get("geometry", {}).get("location", {})
        places.append(
            {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "lat": location.get("lat"),
                "lng": location.get("lng"),
                "types": place.get("types", [])[:5],
                "rating": place.get("rating"),
                "place_id": place.get("place_id"),
                "maps_url": (
                    f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}"
                    if place.get("place_id")
                    else None
                ),
            }
        )

    return {"query": query, "places": places}
