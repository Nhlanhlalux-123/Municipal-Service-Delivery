import sqlite3
import unittest


class TestServiceWeatherJoin(unittest.TestCase):

    def test_join_matches_municipality_and_date(self):
        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE service_requests (
                id INTEGER,
                date TEXT,
                municipality TEXT,
                service TEXT,
                status TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE historical_weather (
                municipality TEXT,
                date TEXT,
                temperature_mean REAL
            )
        """)

        cursor.execute("""
            INSERT INTO service_requests
            VALUES (
                1,
                '2026-01-05',
                'Johannesburg',
                'Water',
                'Resolved'
            )
        """)

        cursor.execute("""
            INSERT INTO historical_weather
            VALUES (
                'Johannesburg',
                '2026-01-05',
                23.5
            )
        """)

        cursor.execute("""
            SELECT
                s.id,
                s.municipality,
                s.date,
                h.temperature_mean
            FROM service_requests s
            JOIN historical_weather h
                ON s.municipality = h.municipality
               AND s.date = h.date
        """)

        result = cursor.fetchone()

        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], "Johannesburg")
        self.assertEqual(result[2], "2026-01-05")
        self.assertEqual(result[3], 23.5)

        connection.close()


if __name__ == "__main__":
    unittest.main()