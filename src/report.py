from repositories.service_repository import (
    ServiceRequestRepository,
)
from repositories.weather_repository import WeatherRepository


service_repository = ServiceRequestRepository()
weather_repository = WeatherRepository()


def get_total_requests():
    return service_repository.count()


def get_requests_by_service():
    return service_repository.count_by_service()


def get_requests_by_municipality():
    return service_repository.count_by_municipality()


def get_requests_by_status():
    return service_repository.count_by_status()


def get_resolution_rate():
    return service_repository.resolution_rate()


def get_current_weather():
    return weather_repository.get_all()


def generate_report():
    total = get_total_requests()
    services = get_requests_by_service()
    municipalities = get_requests_by_municipality()
    statuses = get_requests_by_status()
    resolution_rate = get_resolution_rate()
    weather = get_current_weather()

    print("\n" + "=" * 50)
    print("       MUNICIPAL SERVICE REPORT")
    print("=" * 50)

    print("\nTOTAL REQUESTS")
    print(total)

    print("\nREQUESTS BY SERVICE")
    print("-" * 30)

    for service, count in services:
        print(f"{service:<20} {count}")

    print("\nREQUESTS BY MUNICIPALITY")
    print("-" * 30)

    for municipality, count in municipalities:
        print(f"{municipality:<20} {count}")

    print("\nREQUEST STATUS")
    print("-" * 30)

    for status, count in statuses:
        print(f"{status:<20} {count}")

    print("\nRESOLUTION RATE")
    print("-" * 30)
    print(f"{resolution_rate:.2f}%")

    print("\nCURRENT WEATHER")
    print("-" * 50)

    for (
        municipality,
        observed_at,
        temperature,
        humidity,
        precipitation,
        weather_code,
    ) in weather:

        print(
            f"{municipality:<15} "
            f"{temperature}°C | "
            f"Humidity: {humidity}% | "
            f"Rain: {precipitation}mm"
        )

    print("\n" + "=" * 50)

if __name__ == "__main__":
    generate_report()