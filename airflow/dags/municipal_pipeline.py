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
    def extract_services():

        import csv

        file_path = (
            "/opt/airflow/project_data/"
            "service_requests.csv"
        )

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        print(f"Extracted {len(rows)} service records.")

        return rows

    @task
    def transform_services(rows):

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
    def load_services(rows):

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
                        row["id"],
                        row["date"],
                        row["municipality"],
                        row["service"],
                        row["area"],
                        row["status"]
                    ))

        print(f"Loaded {len(rows)} service records.")

    @task
    def extract_weather():

        from weather_api import get_all_weather

        weather = get_all_weather()

        print(f"Extracted {len(weather)} weather records.")

        return weather

    @task
    def load_weather(rows):

        from weather_load import load_weather

        config = get_database_config()

        load_weather(rows, config)

    @task
    def report():

        config = get_database_config()

        with psycopg.connect(**config) as connection:
            with connection.cursor() as cursor:

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM service_requests
                """)

                total_services = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT service, COUNT(*)
                    FROM service_requests
                    GROUP BY service
                    ORDER BY COUNT(*) DESC
                """)

                services = cursor.fetchall()

                cursor.execute("""
                    SELECT
                        municipality,
                        temperature,
                        humidity,
                        precipitation
                    FROM weather_data
                    ORDER BY municipality
                """)

                weather = cursor.fetchall()

        print("\n" + "=" * 50)
        print("       MUNICIPAL SERVICE REPORT")
        print("=" * 50)

        print("\nTOTAL SERVICE REQUESTS")
        print(total_services)

        print("\nREQUESTS BY SERVICE")
        print("-" * 30)

        for service, count in services:
            print(f"{service:<20} {count}")

        print("\nCURRENT WEATHER")
        print("-" * 50)

        for municipality, temperature, humidity, precipitation in weather:
            print(
                f"{municipality:<15} "
                f"{temperature}°C | "
                f"Humidity: {humidity}% | "
                f"Rain: {precipitation}mm"
            )

        print("\n" + "=" * 50)

    service_raw = extract_services()
    service_clean = transform_services(service_raw)
    service_loaded = load_services(service_clean)

    weather_raw = extract_weather()
    weather_loaded = load_weather(weather_raw)

    [service_loaded, weather_loaded] >> report()


municipal_service_pipeline()