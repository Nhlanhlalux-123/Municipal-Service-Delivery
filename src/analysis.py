import sqlite3

DATABASE = "database/service_data.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def requests_by_service():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT service, COUNT(*)
        FROM service_requests 
        GROUP BY service
    """)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()

def requests_by_municipality():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT municipality, COUNT(*) AS total_requests
        FROM service_requests
        GROUP BY municipality
        ORDER BY total_requests DESC
    """)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()



if __name__ == "__main__":
    requests_by_municipality()