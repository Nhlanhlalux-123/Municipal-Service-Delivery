import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


DATABASE_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}


def get_connection():
    return psycopg.connect(**DATABASE_CONFIG)