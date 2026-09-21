from urllib.parse import urlencode
from urllib.request import urlopen
import json


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


def fetch_weather(municipality, latitude, longitude):
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "weather_code"
        ),
        "timezone": "Africa/Johannesburg",
    }

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        + urlencode(parameters)
    )

    with urlopen(url) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


def extract_weather():
    results = []

    for municipality, coordinates in MUNICIPALITIES.items():
        weather = fetch_weather(
            municipality,
            coordinates["latitude"],
            coordinates["longitude"],
        )

        results.append({
            "municipality": municipality,
            "current": weather["current"],
        })

    return results