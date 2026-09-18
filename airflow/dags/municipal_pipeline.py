from datetime import datetime

import pendulum

from airflow.sdk import dag, task


@dag(
    dag_id="municipal_service_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 9, 18, tz="Africa/Johannesburg"),
    catchup=False,
)
def municipal_service_pipeline():

    @task
    def extract():
        print("Extracting municipal service data...")
        return [
            {"id": 1, "service": "Water", "status": "Resolved"},
            {"id": 2, "service": "Electricity", "status": "Pending"},
            {"id": 3, "service": "Refuse", "status": "Resolved"},
        ]

    @task
    def transform(rows):
        print("Transforming municipal service data...")

        cleaned_rows = []

        for row in rows:
            row["service"] = row["service"].strip().title()
            row["status"] = row["status"].strip().title()

            cleaned_rows.append(row)

        return cleaned_rows

    @task
    def load(rows):
        print("Loading municipal service data...")

        for row in rows:
            print(row)

        print("Load complete!")

    raw_data = extract()

    cleaned_data = transform(raw_data)

    load(cleaned_data)


municipal_service_pipeline()