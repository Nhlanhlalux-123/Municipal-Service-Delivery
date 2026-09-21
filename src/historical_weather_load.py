from src.repositories.historical_weather_repository import (
    HistoricalWeatherRepository,
)


repository = HistoricalWeatherRepository()


def load_historical_weather(rows):
    repository.upsert_many(rows)