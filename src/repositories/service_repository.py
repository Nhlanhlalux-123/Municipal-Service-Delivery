from src.database import get_connection


class ServiceRequestRepository:

    def create_table(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS service_requests (
                        id INTEGER PRIMARY KEY,
                        date DATE NOT NULL,
                        municipality TEXT NOT NULL,
                        service TEXT NOT NULL,
                        area TEXT NOT NULL,
                        status TEXT NOT NULL
                    )
                """)

                cursor.execute("""
                    SELECT data_type
                    FROM information_schema.columns
                    WHERE table_name = 'service_requests'
                    AND column_name = 'date'
                """)

                result = cursor.fetchone()

                if result and result[0] in (
                    "text",
                    "character varying",
                ):
                    cursor.execute("""
                        ALTER TABLE service_requests
                        ALTER COLUMN date TYPE DATE
                        USING date::date
                    """)

    def insert_many(self, rows):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                for row in rows:
                    cursor.execute("""
                        INSERT INTO service_requests (
                            id,
                            date,
                            municipality,
                            service,
                            area,
                            status
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (
                        row.id,
                        row.date,
                        row.municipality,
                        row.service,
                        row.area,
                        row.status,
                    ))

    def count(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM service_requests
                """)

                return cursor.fetchone()[0]

    def count_by_service(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT service, COUNT(*) AS total
                    FROM service_requests
                    GROUP BY service
                    ORDER BY total DESC
                """)

                return cursor.fetchall()

    def count_by_municipality(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT municipality, COUNT(*) AS total
                    FROM service_requests
                    GROUP BY municipality
                    ORDER BY total DESC
                """)

                return cursor.fetchall()

    def count_by_status(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT status, COUNT(*) AS total
                    FROM service_requests
                    GROUP BY status
                    ORDER BY total DESC
                """)

                return cursor.fetchall()

    def resolution_rate(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        COUNT(*) AS total,
                        SUM(
                            CASE
                                WHEN status = 'Resolved' THEN 1
                                ELSE 0
                            END
                        ) AS resolved
                    FROM service_requests
                """)

                total, resolved = cursor.fetchone()

                if total == 0:
                    return 0.0

                return (resolved / total) * 100

    def get_service_weather_summary(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        s.id,
                        s.date,
                        s.municipality,
                        s.service,
                        s.area,
                        s.status,
                        h.temperature_mean,
                        h.precipitation,
                        h.weather_code
                    FROM service_requests s
                    JOIN historical_weather h
                        ON s.municipality = h.municipality
                    AND s.date = h.date
                    ORDER BY s.date, s.id
                """)

                return cursor.fetchall()

    def requests_by_municipality_and_rain(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        s.municipality,
                        COUNT(*) AS total_requests,
                        SUM(
                            CASE
                                WHEN h.precipitation > 0 THEN 1
                                ELSE 0
                            END
                        ) AS rainy_day_requests
                    FROM service_requests s
                    JOIN historical_weather h
                        ON s.municipality = h.municipality
                    AND s.date = h.date
                    GROUP BY s.municipality
                    ORDER BY total_requests DESC
                """)

                return cursor.fetchall()