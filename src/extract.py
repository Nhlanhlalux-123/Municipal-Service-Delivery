from pathlib import Path
import csv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "service_requests.csv"


def extract_data(file_path=DATA_FILE):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)