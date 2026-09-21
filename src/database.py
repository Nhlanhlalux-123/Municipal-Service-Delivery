import psycopg

from config import get_database_config


def get_connection():
    config = get_database_config()

    return psycopg.connect(
        host=config.host,
        port=config.port,
        dbname=config.name,
        user=config.user,
        password=config.password,
    )