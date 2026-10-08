from dotenv import load_dotenv
import requests
import os

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_current_weather(city: str) -> str:
    """Get the current weather for a city by name (e.g. 'New York', 'London,UK')."""

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }
