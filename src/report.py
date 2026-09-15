import sqlite3

DATABASE = "database/service_data.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def get_total_requests():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM service_requests
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_requests_by_service():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT service, COUNT(*) AS total
        FROM service_requests
        GROUP BY service
        ORDER BY total DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_requests_by_municipality():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT municipality, COUNT(*) AS total
        FROM service_requests
        GROUP BY municipality
        ORDER BY total DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_requests_by_status():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*) AS total
        FROM service_requests
        GROUP BY status
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_resolution_rate():
    connection = get_connection()
    cursor = connection.cursor()

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

    connection.close()

    return (resolved / total) * 100


def generate_report():
    total = get_total_requests()
    services = get_requests_by_service()
    municipalities = get_requests_by_municipality()
    statuses = get_requests_by_status()
    resolution_rate = get_resolution_rate()

    print("\n" + "=" * 45)
    print("       MUNICIPAL SERVICE REPORT")
    print("=" * 45)

    print(f"\nTOTAL REQUESTS")
    print(f"{total}")

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

    print("\n" + "=" * 45)


if __name__ == "__main__":
    generate_report()