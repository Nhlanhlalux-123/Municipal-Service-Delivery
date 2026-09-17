import psycopg


DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "municipal_services",
    "user": "municipal_user",
    "password": "municipal_password"
}


def get_connection():
    return psycopg.connect(**DATABASE_CONFIG)