import csv

from transform import clean_data
from load import create_database, load_data

def extract_data():
    with open("data/service_requests.csv", "r") as file:
        reader = csv.DictReader(file)
        return list(reader)

def main():
    raw_data = extract_data()

    print("Raw records:", len(raw_data))

    cleaned_data = clean_data(raw_data)

    print("Clean records:", len(cleaned_data))

    create_database()
    load_data(cleaned_data)

    print("Data loaded successfully")

if __name__ == "__main__":
    main()