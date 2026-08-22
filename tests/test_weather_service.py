# tests/test_weather_service.py
import httpx
import pytest

from src.weather_service import CityNotFoundError, WeatherServiceError, get_weather


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