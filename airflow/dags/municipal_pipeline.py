import csv
import os
import sys

import pendulum
import psycopg

from airflow.sdk import dag, task


PROJECT_SRC = "/opt/airflow/project_src"

if PROJECT_SRC not in sys.path:
    sys.path.append(PROJECT_SRC)


def get_database_config():
    return {
        "host": os.getenv("MUNICIPAL_DB_HOST"),
        "port": os.getenv("MUNICIPAL_DB_PORT"),
        "dbname": os.getenv("MUNICIPAL_DB_NAME"),
        "user": os.getenv("MUNICIPAL_DB_USER"),
        "password": os.getenv("MUNICIPAL_DB_PASSWORD"),
    }


@dag(
    dag_id="municipal_service_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(
        2026,
        9,
        18,
        tz="Africa/Johannesburg"
    ),
    catchup=False,
    tags=["municipal", "etl"],
)
def municipal_service_pipeline():

    @task
    def extract():
        file_path = (
            "/opt/airflow/project_data/"
            "service_requests.csv"
        )

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        print(f"Extracted {len(rows)} records.")

        return rows

    @task
    def transform(rows):

        from transform import clean_data

        cleaned_rows, quality_report = clean_data(rows)

        print("DATA QUALITY REPORT")
        print("-------------------")
        print(
            f"Records extracted: "
            f"{quality_report['total_records']}"
        )
        print(
            f"Duplicate records: "
            f"{quality_report['duplicate_records']}"
        )
        print(
            f"Missing fields: "
            f"{quality_report['missing_fields']}"
        )
        print(
            f"Records cleaned: "
            f"{quality_report['clean_records']}"
        )

        for record in quality_report["rejected_records"]:
            print(
                f"Rejected ID {record['id']}: "
                f"{record['reason']}"
            )

        return cleaned_rows

    @task
    def load(rows):

        config = get_database_config()

        with psycopg.connect(**config) as connection:

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

                for row in rows:

                    cursor.execute("""
                        INSERT INTO service_requests
                        (
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
                        row["id"],
                        row["date"],
                        row["municipality"],
                        row["service"],
                        row["area"],
                        row["status"]
                    ))

        print(f"Loaded {len(rows)} records.")

    @task
    def report():

        config = get_database_config()

        with psycopg.connect(**config) as connection:

            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM service_requests
                """)

                total = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT service, COUNT(*)
                    FROM service_requests
                    GROUP BY service
                    ORDER BY COUNT(*) DESC
                """)

                services = cursor.fetchall()

                cursor.execute("""
                    SELECT status, COUNT(*)
                    FROM service_requests
                    GROUP BY status
                    ORDER BY COUNT(*) DESC
                """)

                statuses = cursor.fetchall()

        print("\n" + "=" * 45)
        print("       MUNICIPAL SERVICE REPORT")
        print("=" * 45)

        print(f"\nTOTAL REQUESTS")
        print(total)

        print("\nREQUESTS BY SERVICE")
        print("-" * 25)

        for service, count in services:
            print(f"{service:<15} {count}")

        print("\nREQUEST STATUS")
        print("-" * 25)

        for status, count in statuses:
            print(f"{status:<15} {count}")

        print("\n" + "=" * 45)

    raw_data = extract()

    cleaned_data = transform(raw_data)

    load_task = load(cleaned_data)

    load_task >> report()


municipal_service_pipeline()