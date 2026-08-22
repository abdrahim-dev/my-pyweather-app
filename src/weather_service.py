import httpx

from src.config import settings


class CityNotFoundError(Exception):
    """Exception raised when a city is not found in the weather service."""

class WeatherServiceError(Exception):
    """Exception raised for errors in the weather service."""

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str) -> dict:
    """Fetches weather data for a given city from the OpenWeatherMap API."""
    params = {
    "q": city,
    "appid": settings.weather_api_key,
    "units": "metric"
    }

    try:
        response = httpx.get(BASE_URL, params=params)
    except httpx.RequestError as e:
        raise WeatherServiceError(f"Could not reach weather service: {e}")

    if response.status_code == 404:
        raise CityNotFoundError(f"City '{city}' not found.")
    elif response.status_code != 200:
        raise WeatherServiceError(f"Weather service returned status code {response.status_code}: {response.text}")
    data = response.json()

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "conditions": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
    }
    
print(get_weather("Berlin"))

