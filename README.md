# Weather App

A small three-layer weather application built to learn how REST APIs and FastAPI work in practice. Given a city name, it fetches current weather data from the OpenWeatherMap API and displays it through a desktop GUI.

## Architecture

The project is split into three independent layers, each testable on its own:

```
GUI (CustomTkinter)  --HTTP-->  FastAPI server  --calls-->  Weather service  --HTTP-->  OpenWeatherMap API
     src/gui.py                   src/main.py                src/weather_service.py
```

- **`src/weather_service.py`** — talks to the OpenWeatherMap API directly. Raises `CityNotFoundError` or `WeatherServiceError` on failure so callers don't need to know anything about HTTP internals.
- **`src/models.py`** — Pydantic model (`WeatherResponse`) describing the shape of data the API returns. Used by FastAPI to validate responses and auto-generate documentation.
- **`src/config.py`** — loads the OpenWeatherMap API key from `.env` via `pydantic-settings`, so no other file needs to know how configuration is loaded.
- **`src/main.py`** — the FastAPI server. Exposes `GET /weather/{city}` and translates exceptions from `weather_service.py` into proper HTTP status codes (404, 503).
- **`src/gui.py`** — a CustomTkinter desktop client. Makes its own HTTP requests to the locally running FastAPI server and displays the result.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for dependency management
- A free [OpenWeatherMap](https://openweathermap.org/) API key

## Setup

1. Clone the repository and install dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root with your OpenWeatherMap API key:
   ```
   WEATHER_API_KEY=your_key_here
   ```
   Note: newly generated OpenWeatherMap keys can take up to a couple of hours to activate.

## Running the app

The server and the GUI are two separate processes and need to run in two separate terminals.

**Terminal 1 — start the API server:**

```bash
uv run uvicorn src.main:app --reload
```

Interactive API docs are then available at http://localhost:8000/docs.

**Terminal 2 — start the GUI:**

```bash
uv run python src/gui.py
```

Type a city name and click "Search". The status label at the bottom reports what happened — success, city not found, weather service unavailable, or unable to reach the server (e.g. if Terminal 1 isn't running).

## Running the tests

```bash
uv run pytest -v
```

Tests use `pytest-mock` to fake network calls (`httpx.get`) and FastAPI's `TestClient` to test the API layer without a real server running — no real internet connection or API quota is used.

## Project structure

```
.
├── architecture/
│   ├── WeatherApp-architecture.svg     # Architecture of the WeatherApp
├── src/
│   ├── weather_service.py              # OpenWeatherMap client + custom exceptions
│   ├── models.py                       # Pydantic response models
│   ├── config.py                       # Settings loaded from .env
│   ├── main.py                         # FastAPI app and routes
│   └── gui.py                          # CustomTkinter desktop client
├── tests/
│   ├── test_weather_service.py
│   └── test_main.py
├── .env                                # API key — not committed
├── .gitignore
├── pyproject.toml
└── README.md
```

## API reference

### `GET /weather/{city}`

Returns current weather for the given city.

**Success response — `200 OK`**

```json
{
  "city": "Berlin",
  "temperature": 15.43,
  "conditions": "scattered clouds",
  "humidity": 75
}
```

**City not found — `404 Not Found`**

```json
{ "detail": "City 'Nonexistentcity123' not found" }
```

**Weather service unavailable — `503 Service Unavailable`**

```json
{ "detail": "Weather service unavailable" }
```

## Notes

- Temperatures are returned in Celsius (`units=metric`).
- Looking up cities by name is a legacy OpenWeatherMap feature; a future improvement could switch to their geocoding endpoint (lat/lon) for more robust city resolution.

## Possible next steps

- Multi-day forecast
- Celsius / Fahrenheit toggle
- Simple response caching
- Comparing multiple cities at once
