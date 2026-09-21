from src.models.weather_record import WeatherRecord

def transform_weather(rows):
    transformed_rows = []

    for row in rows:
        current = row["current"]

        weather = WeatherRecord(
            municipality=row["municipality"],
            time=current["time"],
            temperature=current["temperature_2m"],
            humidity=current["relative_humidity_2m"],
            precipitation=current["precipitation"],
            weather_code=current["weather_code"],
        )

        transformed_rows.append(weather)

    return transformed_rows