import mysql.connector
from mysql.connector import Error

# Centralized Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "clinicease_db",
    "user": "root",
    "password": "newrootpassword123",
}


def get_connection():
    """
    Establishes and returns an active MySQL database connection.
    Returns None if the connection fails.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[DATABASE ERROR] Failed to connect to MySQL: {e}")
        return None
