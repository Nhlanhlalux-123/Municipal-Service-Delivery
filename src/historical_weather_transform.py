from src.models.historical_weather import HistoricalWeather


def transform_historical_weather(rows):
    transformed = []

    for row in rows:
        record = HistoricalWeather(
            municipality=row["municipality"],
            date=row["date"],
            temperature_mean=row["temperature_mean"],
            precipitation=row["precipitation"],
            weather_code=row["weather_code"],
        )

        transformed.append(record)

    return transformed