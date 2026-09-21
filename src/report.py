from database import get_connection


def get_total_requests():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*)
                FROM service_requests
            """)

            return cursor.fetchone()[0]


def get_requests_by_service():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT service, COUNT(*) AS total
                FROM service_requests
                GROUP BY service
                ORDER BY total DESC
            """)

            return cursor.fetchall()


def get_requests_by_municipality():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT municipality, COUNT(*) AS total
                FROM service_requests
                GROUP BY municipality
                ORDER BY total DESC
            """)

            return cursor.fetchall()


def get_requests_by_status():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT status, COUNT(*) AS total
                FROM service_requests
                GROUP BY status
                ORDER BY total DESC
            """)

            return cursor.fetchall()


def get_resolution_rate():
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

            return (resolved / total) * 100


def generate_report():
    total = get_total_requests()
    services = get_requests_by_service()
    municipalities = get_requests_by_municipality()
    statuses = get_requests_by_status()
    resolution_rate = get_resolution_rate()
    service_weather = get_service_weather_summary()

    print("\n" + "=" * 45)
    print("       MUNICIPAL SERVICE REPORT")
    print("=" * 45)

    print("\nTOTAL REQUESTS")
    print(total)

    print("\nREQUESTS BY SERVICE")
    print("-" * 25)

    for service, count in services:
        print(f"{service:<15} {count}")

    print("\nREQUESTS BY MUNICIPALITY")
    print("-" * 25)

    for municipality, count in municipalities:
        print(f"{municipality:<15} {count}")

    print("\nREQUEST STATUS")
    print("-" * 25)

    for status, count in statuses:
        print(f"{status:<15} {count}")

    print("\nRESOLUTION RATE")
    print("-" * 25)
    print(f"{resolution_rate:.2f}%")

    print("\nSERVICE REQUESTS + CURRENT WEATHER")
    print("-" * 50)

    for municipality, requests, temperature, humidity, precipitation in service_weather:
        print(  
            f"{municipality:<15} "
            f"Requests: {requests:<3} "
            f"Temp: {temperature}°C "
            f"Humidity: {humidity}% "
            f"Rain: {precipitation}mm"
        )

    print("\n" + "=" * 45)

    

def get_service_weather_summary():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    s.municipality,
                    COUNT(*) AS total_requests,
                    w.temperature,
                    w.humidity,
                    w.precipitation
                FROM service_requests s
                JOIN weather_data w
                    ON s.municipality = w.municipality
                GROUP BY
                    s.municipality,
                    w.temperature,
                    w.humidity,
                    w.precipitation
                ORDER BY total_requests DESC
            """)

            return cursor.fetchall()


if __name__ == "__main__":
    generate_report()