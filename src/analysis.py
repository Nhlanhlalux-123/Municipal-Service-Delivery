import sqlite3

DATABASE = "database/service_data.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def show_all_requests():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM service_requests    
""")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connection.close()

if __name__ == "__main__":
    show_all_requests()