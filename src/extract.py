import csv

def extract_data():
    with open("data/service_requests.csv", "r") as file:
        reader = csv.DictReader(file)

        return list(reader)