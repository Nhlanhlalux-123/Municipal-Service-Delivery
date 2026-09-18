import json
from urllib.parse import urlencode
from urllib.request import urlopen


MUNICIPALITIES = {
    "Johannesburg": {
        "latitude": -26.2041,
        "longitude": 28.0473
    },
    "Tshwane": {
        "latitude": -25.7479,
        "longitude": 28.2293
    },
    "Ekurhuleni": {
        "latitude": -26.1778,
        "longitude": 28.4428
    }
}


def get_weather(municipality, latitude, longitude):
    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "weather_code"
        ),
        "timezone": "Africa/Johannesburg"
    }

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        + urlencode(parameters)
    )

    with urlopen(url) as response:
        weather = json.loads(
            response.read().decode("utf-8")
        )

    current = weather["current"]

    return {
        "municipality": municipality,
        "time": current["time"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "precipitation": current["precipitation"],
        "weather_code": current["weather_code"]
    }


def get_all_weather():
    results = []

    for municipality, coordinates in MUNICIPALITIES.items():
        weather = get_weather(
            municipality,
            coordinates["latitude"],
            coordinates["longitude"]
        )

        results.append(weather)

    return results


if __name__ == "__main__":
    weather_data = get_all_weather()

    for weather in weather_data:
        print(weather)