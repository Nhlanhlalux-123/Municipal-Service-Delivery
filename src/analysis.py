from database import get_connection


def requests_by_service():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT service, COUNT(*) AS total
                FROM service_requests
                GROUP BY service
                ORDER BY total DESC
            """)

            rows = cursor.fetchall()

            print("\nREQUESTS BY SERVICE")

            for service, total in rows:
                print(f"{service}: {total}")


def requests_by_municipality():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT municipality, COUNT(*) AS total
                FROM service_requests
                GROUP BY municipality
                ORDER BY total DESC
            """)

            rows = cursor.fetchall()

            print("\nREQUESTS BY MUNICIPALITY")

            for municipality, total in rows:
                print(f"{municipality}: {total}")


def requests_by_status():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT status, COUNT(*) AS total
                FROM service_requests
                GROUP BY status
                ORDER BY total DESC
            """)

            rows = cursor.fetchall()

            print("\nREQUESTS BY STATUS")

            for status, total in rows:
                print(f"{status}: {total}")


if __name__ == "__main__":
    requests_by_service()
    requests_by_municipality()
    requests_by_status()