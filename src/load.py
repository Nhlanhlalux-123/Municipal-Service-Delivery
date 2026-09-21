from repositories.service_repository import (
    ServiceRequestRepository,
)


repository = ServiceRequestRepository()


def create_database():
    repository.create_table()


def load_data(rows):
    repository.insert_many(rows)