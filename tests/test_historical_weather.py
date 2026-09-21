import unittest

from src.historical_weather_transform import (
    transform_historical_weather,
)


class TestHistoricalWeather(unittest.TestCase):

    def test_transforms_weather_record(self):
        rows = [
            {
                "municipality": "Johannesburg",
                "date": "2026-01-05",
                "temperature_mean": 23.5,
                "precipitation": 4.2,
                "weather_code": 61,
            }
        ]

        result = transform_historical_weather(rows)

        self.assertEqual(len(result), 1)

        self.assertEqual(
            result[0].municipality,
            "Johannesburg",
        )

        self.assertEqual(
            result[0].date,
            "2026-01-05",
        )

        self.assertEqual(
            result[0].temperature_mean,
            23.5,
        )

        self.assertEqual(
            result[0].precipitation,
            4.2,
        )


if __name__ == "__main__":
    unittest.main()