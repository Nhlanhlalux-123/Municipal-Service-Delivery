import os
import sqlite3
import tempfile
import unittest

from src.transform import clean_data


class TestPipeline(unittest.TestCase):

    def test_clean_data_can_be_loaded_into_database(self):
        rows = [
            {
                "id": "1",
                "date": "2026-01-05",
                "municipality": "Johannesburg",
                "service": "Water",
                "area": "Soweto",
                "status": "Resolved"
            },
            {
                "id": "2",
                "date": "2026-01-06",
                "municipality": "Tshwane",
                "service": "Refuse",
                "area": "Pretoria",
                "status": "Pending"
            }
        ]

        cleaned, _ = clean_data(rows)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            database = temp_file.name

        try:
            connection = sqlite3.connect(database)
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE service_requests (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    municipality TEXT NOT NULL,
                    service TEXT NOT NULL,
                    area TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)

            for row in cleaned:
                cursor.execute("""
                    INSERT INTO service_requests
                    (id, date, municipality, service, area, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    row["id"],
                    row["date"],
                    row["municipality"],
                    row["service"],
                    row["area"],
                    row["status"]
                ))

            connection.commit()

            cursor.execute("SELECT COUNT(*) FROM service_requests")
            count = cursor.fetchone()[0]

            self.assertEqual(count, 2)

            connection.close()

        finally:
            os.remove(database)


if __name__ == "__main__":
    unittest.main()