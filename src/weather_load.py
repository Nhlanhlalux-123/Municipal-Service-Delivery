from repositories.weather_repository import WeatherRepository


repository = WeatherRepository()


def load_weather(rows):
    repository.upsert_many(rows)