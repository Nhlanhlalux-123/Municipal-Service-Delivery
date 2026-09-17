from database import get_connection


def create_database():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS service_requests (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    municipality TEXT NOT NULL,
                    service TEXT NOT NULL,
                    area TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)


def load_data(rows):
    with get_connection() as connection:
        with connection.cursor() as cursor:

            for row in rows:
                cursor.execute("""
                    INSERT INTO service_requests
                    (id, date, municipality, service, area, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    row["id"],
                    row["date"],
                    row["municipality"],
                    row["service"],
                    row["area"],
                    row["status"]
                ))