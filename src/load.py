import sqlite3

DATABASE = "database/service_data.db"

def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_requests (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        municipality TEXT NOT NULL,
        service TEXT NOT NULL,
        area TEXT NOT NULL,
        status TEXT NOT NULL 
        )
    """)

    connection.commit
    connection.close()

def load_data(rows):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    for row in rows:
        cursor.execute(""" 
            INSERT INTO service_requests
            (id, date, micipality, service, area, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["id"],
            row["date"],
            row["municipality"],
            row["service"],
            row["area"],
            row["status"]
        ))

    connection.commit()
    connection.close()