from extract import extract_data
from transform import clean_data
from report import generate_report
from load import create_database, load_data


def main():
    print("Starting data pipeline...\n")

    raw_data = extract_data()

    cleaned_data, quality_report = clean_data(raw_data)

    create_database()
    load_data(cleaned_data)

    print("DATA QUALITY REPORT")
    print("-------------------")
    print(f"Records extracted: {quality_report['total_records']}")
    print(f"Duplicate records: {quality_report['duplicate_records']}")
    print(f"Missing fields:    {quality_report['missing_fields']}")
    print(f"Records loaded:    {quality_report['clean_records']}")

    print("\nREJECTED RECORDS")
    print("----------------")

    for record in quality_report["rejected_records"]:
        print(f"ID: {record['id']} | Reason: {record['reason']}")

    print("\nPipeline complete.")

    generate_report()


if __name__ == "__main__":
    main()