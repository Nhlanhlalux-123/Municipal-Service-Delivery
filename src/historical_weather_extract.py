import json
from urllib.parse import urlencode
from urllib.request import urlopen

from src.extract import extract_data


MUNICIPALITIES = {
    "Johannesburg": {
        "latitude": -26.2041,
        "longitude": 28.0473,
    },
    "Tshwane": {
        "latitude": -25.7479,
        "longitude": 28.2293,
    },
    "Ekurhuleni": {
        "latitude": -26.1778,
        "longitude": 28.4428,
    },
}


def get_date_range():
    rows = extract_data()

    dates = [
        row["date"]
        for row in rows
        if row["date"]
    ]

    return min(dates), max(dates)


def fetch_historical_weather(
    municipality,
    latitude,
    longitude,
    start_date,
    end_date,
):
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": (
            "temperature_2m_mean,"
            "precipitation_sum,"
            "weather_code"
        ),
        "timezone": "Africa/Johannesburg",
    }

    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        + urlencode(parameters)
    )

    with urlopen(url) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    daily = data["daily"]

    results = []

    for date, temperature, precipitation, weather_code in zip(
        daily["time"],
        daily["temperature_2m_mean"],
        daily["precipitation_sum"],
        daily["weather_code"],
    ):
        results.append({
            "municipality": municipality,
            "date": date,
            "temperature_mean": temperature,
            "precipitation": precipitation,
            "weather_code": weather_code,
        })

    return results


def extract_historical_weather():
    start_date, end_date = get_date_range()

    print(f"Weather start date: {start_date}")
    print(f"Weather end date:   {end_date}")

    results = []

    for municipality, coordinates in MUNICIPALITIES.items():
        rows = fetch_historical_weather(
            municipality,
            coordinates["latitude"],
            coordinates["longitude"],
            start_date,
            end_date,
        )

        results.extend(rows)

    print(
        f"Extracted {len(results)} historical weather records."
    )

    return results