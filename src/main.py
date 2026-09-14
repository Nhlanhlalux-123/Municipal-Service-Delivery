import csv

from transform import clean_data

def extract_data():
    with open("data/service_requests.csv", "r") as file:
        reader = csv.DictReader(file)
        return list(reader)

def main():
    raw_data = extract_data()

    print("Raw records:", len(raw_data))

    cleaned_data = clean_data(raw_data)

    print("Clean records:", len(cleaned_data))

    print("\nCleaned data:")

    for row in cleaned_data:
        print(row)

if __name__ == "__main__":
    main()