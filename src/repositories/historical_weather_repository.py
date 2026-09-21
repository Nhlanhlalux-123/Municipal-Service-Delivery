from src.database import get_connection


class HistoricalWeatherRepository:

    def create_table(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS historical_weather (
                        municipality TEXT NOT NULL,
                        date DATE NOT NULL,
                        temperature_mean REAL,
                        precipitation REAL,
                        weather_code INTEGER,
                        PRIMARY KEY (municipality, date)
                    )
                """)

    def upsert_many(self, rows):
        self.create_table()

        with get_connection() as connection:
            with connection.cursor() as cursor:

                for row in rows:
                    cursor.execute("""
                        INSERT INTO historical_weather (
                            municipality,
                            date,
                            temperature_mean,
                            precipitation,
                            weather_code
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (municipality, date)
                        DO UPDATE SET
                            temperature_mean =
                                EXCLUDED.temperature_mean,
                            precipitation =
                                EXCLUDED.precipitation,
                            weather_code =
                                EXCLUDED.weather_code
                    """, (
                        row.municipality,
                        row.date,
                        row.temperature_mean,
                        row.precipitation,
                        row.weather_code,
                    ))