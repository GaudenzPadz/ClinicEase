import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()  # Reads .env from the current project directory


def get_connection():
    """Return a MySQL connection, or None if configuration or connection fails."""
    config = {
        "host": os.getenv("CLINICEASE_DB_HOST", "localhost"),
        "port": int(os.getenv("CLINICEASE_DB_PORT", "3306")),
        "database": os.getenv("CLINICEASE_DB_NAME", "clinicease_db"),
        "user": os.getenv("CLINICEASE_DB_USER", "root"),
        "password": os.getenv("CLINICEASE_DB_PASSWORD"),
    }

    if not config["password"]:
        print("[DATABASE ERROR] CLINICEASE_DB_PASSWORD is missing from .env.")
        return None

    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection

        connection.close()
    except Error as exc:
        # Avoid printing connection details or credentials in logs.
        print(f"[DATABASE ERROR] MySQL connection failed ({exc.__class__.__name__}).")

    return None
