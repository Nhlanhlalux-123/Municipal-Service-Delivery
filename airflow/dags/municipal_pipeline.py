import sys

import pendulum

from airflow.sdk import dag, task


PROJECT_ROOT = "/opt/airflow/municipal_project"

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


@dag(
    dag_id="municipal_service_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(
        2026,
        9,
        18,
        tz="Africa/Johannesburg",
    ),
    catchup=False,
    tags=["municipal", "etl"],
)
def municipal_service_pipeline():

    @task
    def extract_service_task():
        from src.extract import extract_data

        rows = extract_data()

        print(f"Extracted {len(rows)} service records.")

        return rows


    @task
    def transform_service_task(rows):
        from src.transform import clean_data

        cleaned_rows, quality_report = clean_data(rows)

        print("\nDATA QUALITY REPORT")
        print("-------------------")
        print(f"Records extracted: {quality_report['total_records']}")
        print(f"Duplicate records: {quality_report['duplicate_records']}")
        print(f"Missing fields: {quality_report['missing_fields']}")
        print(f"Records cleaned: {quality_report['clean_records']}")

        for record in quality_report["rejected_records"]:
            print(
                f"Rejected ID {record['id']}: "
                f"{record['reason']}"
            )

        return [
            row.to_dict()
            for row in cleaned_rows
        ]


    @task
    def load_service_task(rows):
        from src.models.service_request import ServiceRequest
        from src.load import create_database, load_data

        service_requests = [
            ServiceRequest.from_dict(row)
            for row in rows
        ]

        create_database()
        load_data(service_requests)

    @task
    def extract_historical_weather_task():
        from src.historical_weather_extract import (
            extract_historical_weather,
        )

        rows = extract_historical_weather()

        print(
            f"Extracted "
            f"{len(rows)} historical weather records."
        )

        return rows


    @task
    def transform_historical_weather_task(rows):
        from src.historical_weather_transform import (
            transform_historical_weather,
        )

        transformed = transform_historical_weather(rows)

        print(
            f"Transformed "
            f"{len(transformed)} historical weather records."
        )

        return [
            row.to_dict()
            for row in transformed
        ]


    @task
    def load_historical_weather_task(rows):
        from src.historical_weather_load import (
            load_historical_weather,
        )
        from src.models.historical_weather import (
            HistoricalWeather,
        )

        weather_records = [
            HistoricalWeather.from_dict(row)
            for row in rows
        ]

        load_historical_weather(weather_records)

        print(
            f"Loaded "
            f"{len(weather_records)} historical weather records."
        )

    @task
    def report():
        from src.report import generate_report

        generate_report()

    service_raw = extract_service_task()

    service_clean = transform_service_task(service_raw)

    service_loaded = load_service_task(service_clean)

    historical_weather_raw = (extract_historical_weather_task())

    historical_weather_clean = (transform_historical_weather_task(historical_weather_raw))

    historical_weather_loaded = (load_historical_weather_task(historical_weather_clean))

    [service_loaded, historical_weather_loaded] >> report()


municipal_service_pipeline()