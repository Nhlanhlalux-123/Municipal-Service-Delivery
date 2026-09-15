import pandas as pd

FILE = "data/service_requests.csv"


def load_data():
    return pd.read_csv(FILE)


def show_data(data):
    print("\nDATA")
    print(data)


def show_basic_information(data):
    print("\nDATA INFORMATION")
    print(data.info())


def show_service_counts(data):
    print("\nREQUESTS BY SERVICE")
    print(data["service"].value_counts())


def show_resolution_rate(data):
    resolved = (data["status"] == "Resolved").sum()
    total = len(data)

    rate = (resolved / total) * 100

    print(f"\nResolution rate: {rate:.2f}%")


def add_resolution_flag(data):
    data["resolved"] = data["status"] == "Resolved"
    return data

def main():
    data = load_data()

    data = add_resolution_flag(data)

    show_data(data)
    show_basic_information(data)
    show_service_counts(data)
    show_resolution_rate(data)


if __name__ == "__main__":
    main()
