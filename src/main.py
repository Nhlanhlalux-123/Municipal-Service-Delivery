from extract import extract_data
from transform import clean_data
from load import create_database, load_data


def main():
    print("Starting data pipeline...")

    raw_data = extract_data()
    print(f"Extracted {len(raw_data)} records.")

    cleaned_data = clean_data(raw_data)
    print(f"Cleaned {len(cleaned_data)} records.")

    create_database()
    load_data(cleaned_data)

    print("Data loaded successfully.")
    print("Pipeline complete.")


if __name__ == "__main__":
    main()