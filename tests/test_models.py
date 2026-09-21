import unittest

from src.models.service_request import ServiceRequest
from src.models.weather_record import WeatherRecord


class TestModels(unittest.TestCase):

    def test_service_request(self):
        request = ServiceRequest(
            id=1,
            date="2026-01-05",
            municipality="Johannesburg",
            service="Water",
            area="Soweto",
            status="Resolved",
        )

        self.assertEqual(request.id, 1)
        self.assertEqual(request.municipality, "Johannesburg")

    def test_weather_record(self):
        weather = WeatherRecord(
            municipality="Johannesburg",
            time="2026-09-21T10:00",
            temperature=21.5,
            humidity=45,
            precipitation=0.0,
            weather_code=1,
        )

        self.assertEqual(weather.temperature, 21.5)
        self.assertEqual(weather.humidity, 45)


if __name__ == "__main__":
    unittest.main()