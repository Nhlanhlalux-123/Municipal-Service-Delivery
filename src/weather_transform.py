def transform_weather(rows):
    transformed_rows = []

    for row in rows:
        current = row["current"]

        transformed_rows.append({
            "municipality": row["municipality"],
            "time": current["time"],
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "precipitation": current["precipitation"],
            "weather_code": current["weather_code"],
        })

    return transformed_rows