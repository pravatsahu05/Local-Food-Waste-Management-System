import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "food_waste_management")
    )


if __name__ == "__main__":
    conn = get_connection()

    if conn.is_connected():
        print("Database Connected Successfully")

    conn.close()
