import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", 5432),
}


def get_connection():
    return psycopg2.connect(**DB_PARAMS)


def set_city(user_id, city, name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users(user_id, city, name, weather_requests)
                VALUES (%s, %s, %s, 0)
                ON CONFLICT(user_id)
                DO UPDATE SET city = EXCLUDED.city, name = EXCLUDED.name
            """, (user_id, city, name))


def get_city(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT city FROM users WHERE user_id = %s", (user_id, ))
            row = cur.fetchone()
            return row[0] if row else None


def increment_weather_counter(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
                cur.execute("""
                UPDATE users
                SET weather_requests = weather_requests + 1
                WHERE user_id = %s
            """, (user_id,))


def get_profile(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT name, city, weather_requests
                FROM users
                WHERE user_id = %s
            """, (user_id,))
            row = cur.fetchone()
            if row:
                return {"name": row[0], "city": row[1], "weather_requests": row[2]}
            return {}


def delete_profile(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id, ))
            return cur.rowcount > 0
