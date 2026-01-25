import psycopg2
from psycopg2 import sql
from sniffio import current_async_library_cvar


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="123",
            port="5432"
        )

        self.cursor = self.conn.cursor()

        with self.conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY,
                user_data JSONB NOT NULL DEFAULT '{}'::JSONB
            )
            """)

        self.conn.commit()