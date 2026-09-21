from src.extract import extract_data
from src.transform import clean_data
from src.load import create_database, load_data


def run_pipeline():
    print("Starting data pipeline...\n")

    # Extract
    raw_data = extract_data()

    # Transform
    cleaned_data, quality_report = clean_data(raw_data)

    # Load
    create_database()
    load_data(cleaned_data)

    # Data quality report
    print("\nDATA QUALITY REPORT")
    print("-------------------")
    print(f"Records extracted: {quality_report['total_records']}")
    print(f"Duplicate records: {quality_report['duplicate_records']}")
    print(f"Missing fields:    {quality_report['missing_fields']}")
    print(f"Records loaded:    {quality_report['clean_records']}")

    print("\nREJECTED RECORDS")
    print("----------------")

    for record in quality_report["rejected_records"]:
        print(
            f"ID: {record['id']} | "
            f"Reason: {record['reason']}"
        )

    print("\nPipeline complete.")

    return quality_report