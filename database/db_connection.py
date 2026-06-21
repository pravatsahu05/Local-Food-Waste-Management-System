import os
from pathlib import Path

import mysql.connector


def load_local_env():
    env_path = Path(__file__).resolve().parents[1] / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_config_value(key, default=None):
    env_value = os.getenv(key)

    if env_value not in (None, ""):
        return env_value

    try:
        import streamlit as st

        return st.secrets.get(key, default)
    except Exception:
        return default


def get_connection():
    load_local_env()

    return mysql.connector.connect(
        host=get_config_value("DB_HOST", "127.0.0.1"),
        port=int(get_config_value("DB_PORT", "3306")),
        user=get_config_value("DB_USER", "root"),
        password=get_config_value("DB_PASSWORD", ""),
        database=get_config_value("DB_NAME", "food_waste_management")
    )


if __name__ == "__main__":
    conn = get_connection()

    if conn.is_connected():
        print("Database Connected Successfully")

    conn.close()
