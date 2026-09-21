import sys

import pendulum

from airflow.sdk import dag, task


PROJECT_SRC = "/opt/airflow/project_src"

if PROJECT_SRC not in sys.path:
    sys.path.append(PROJECT_SRC)


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
        from extract import extract_data

        rows = extract_data()

        print(f"Extracted {len(rows)} service records.")

        return rows


    @task
    def transform_service_task(rows):
        from transform import clean_data

        cleaned_rows, quality_report = clean_data(rows)

        print("\nDATA QUALITY REPORT")
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
    def load_service_task(rows):
        from load import create_database, load_data

        create_database()
        load_data(rows)

        print(f"Loaded {len(rows)} service records.")

    @task
    def extract_weather_task():
        from weather_extract import extract_weather

        rows = extract_weather()

        print(f"Extracted {len(rows)} weather records.")

        return rows


    @task
    def transform_weather_task(rows):
        from weather_transform import transform_weather

        transformed = transform_weather(rows)

        print(
            f"Transformed "
            f"{len(transformed)} weather records."
        )

        return transformed


    @task
    def load_weather_task(rows):
        from weather_load import load_weather

        load_weather(rows)

        print(f"Loaded {len(rows)} weather records.")


    @task
    def report():
        from report import generate_report

        generate_report()

    service_raw = extract_service_task()

    service_clean = transform_service_task(service_raw)

    service_loaded = load_service_task(service_clean)

    weather_raw = extract_weather_task()

    weather_clean = transform_weather_task(weather_raw)

    weather_loaded = load_weather_task(weather_clean)

    [service_loaded, weather_loaded] >> report()


municipal_service_pipeline()