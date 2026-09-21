import unittest

from src.weather_transform import transform_weather


class TestWeatherTransform(unittest.TestCase):

    def test_transforms_weather_record(self):
        rows = [
            {
                "municipality": "Johannesburg",
                "current": {
                    "time": "2026-09-21T10:00",
                    "temperature_2m": 21.5,
                    "relative_humidity_2m": 45,
                    "precipitation": 0.0,
                    "weather_code": 1,
                },
            }
        ]

        result = transform_weather(rows)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0].municipality,
            "Johannesburg",
        )
        self.assertEqual(
            result[0].temperature,
            21.5,
        )
        self.assertEqual(
            result[0].humidity,
            45,
        )


if __name__ == "__main__":
    unittest.main()