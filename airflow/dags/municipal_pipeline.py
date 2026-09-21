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
    def extract_weather_task():
        from weather_extract import extract_weather

        rows = extract_weather()

        print(f"Extracted {len(rows)} weather records.")

        return rows


    @task
    def transform_weather_task(rows):
        from weather_transform import transform_weather

        transformed = transform_weather(rows)

        print(f"Transformed {len(transformed)} weather records.")

        return transformed


    @task
    def load_weather_task(rows):
        from weather_load import load_weather

        load_weather(rows)

        print(f"Loaded {len(rows)} weather records.")

    weather_raw = extract_weather_task()

    weather_clean = transform_weather_task(weather_raw)

    weather_loaded = load_weather_task(weather_clean)
    
[service_loaded, weather_loaded] >> report()
municipal_service_pipeline()