# tests/test_weather_service.py
import httpx
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.weather_service import CityNotFoundError, WeatherServiceError, get_weather

client = TestClient(app)


def test_get_weather_success(mocker):
    mock_get = mocker.patch("src.weather_service.httpx.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "main": {"temp": 15.43, "humidity": 75},
        "weather": [{"description": "scattered clouds"}],
    }

    result = get_weather("Berlin")

    assert result == {
        "city": "Berlin",
        "temperature": 15.43,
        "conditions": "scattered clouds",
        "humidity": 75,
    }


def test_get_weather_city_not_found(mocker):
    mock_get = mocker.patch("src.weather_service.httpx.get")
    mock_get.return_value.status_code = 404

    with pytest.raises(CityNotFoundError):
        get_weather("Nonexistentcityxyz")


def test_get_weather_service_unreachable(mocker):
    mock_get = mocker.patch("src.weather_service.httpx.get")
    mock_get.side_effect = httpx.RequestError("Connection failed")

    with pytest.raises(WeatherServiceError):
        get_weather("Berlin")


def test_read_weather_success(mocker):
    mock_data = {
        "city": "Berlin",
        "temperature": 15.43,
        "conditions": "scattered clouds",
        "humidity": 75,
    }
    mocker.patch("src.main.get_weather", return_value=mock_data)

    response = client.get("/weather/Berlin")

    assert response.status_code == 200
    assert response.json() == mock_data


def test_read_weather_city_not_found(mocker):
    mocker.patch("src.main.get_weather", side_effect=CityNotFoundError)

    response = client.get("/weather/CityXY123")

    assert response.status_code == 404
    assert response.json()["detail"] == "City 'CityXY123' not found"


def test_read_weather_service_unavailable(mocker):
    mocker.patch("src.main.get_weather", side_effect=WeatherServiceError)

    response = client.get("/weather/Paris")

    assert response.status_code == 503
    assert response.json()["detail"] == "Weather service unavailable"