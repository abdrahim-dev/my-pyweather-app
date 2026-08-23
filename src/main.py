from fastapi import FastAPI, HTTPException

from src.models import WeatherResponse
from src.weather_service import CityNotFoundError, WeatherServiceError, get_weather

app = FastAPI()


@app.get("/weather/{city}", response_model=WeatherResponse)
def read_weather(city: str):
    try:
        data = get_weather(city)
    except CityNotFoundError:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found") from None
    except WeatherServiceError:
        raise HTTPException(status_code=503, detail="Weather service unavailable") from None

    return data

