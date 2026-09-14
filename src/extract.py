import csv

with open("data/service_requests.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)