from src.database import get_connection


class WeatherRepository:

    def create_table(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS weather_data (
                        municipality TEXT NOT NULL,
                        observed_at TEXT NOT NULL,
                        temperature REAL,
                        humidity REAL,
                        precipitation REAL,
                        weather_code INTEGER,
                        PRIMARY KEY (municipality, observed_at)
                    )
                """)

    def upsert_many(self, rows):
        self.create_table()

        with get_connection() as connection:
            with connection.cursor() as cursor:

                for row in rows:
                    cursor.execute("""
                        INSERT INTO weather_data (
                            municipality,
                            observed_at,
                            temperature,
                            humidity,
                            precipitation,
                            weather_code
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (municipality, observed_at)
                        DO UPDATE SET
                            temperature = EXCLUDED.temperature,
                            humidity = EXCLUDED.humidity,
                            precipitation = EXCLUDED.precipitation,
                            weather_code = EXCLUDED.weather_code
                    """, (
                        row.municipality,
                        row.time,
                        row.temperature,
                        row.humidity,
                        row.precipitation,
                        row.weather_code,
                    ))

    def get_all(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        municipality,
                        observed_at,
                        temperature,
                        humidity,
                        precipitation,
                        weather_code
                    FROM weather_data
                    ORDER BY municipality, observed_at
                """)

                return cursor.fetchall()