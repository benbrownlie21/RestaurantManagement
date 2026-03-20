import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def execute_all(self, query, parameters=None):
        self.cursor.execute(query, parameters)
        return self.cursor.fetchall()

    def execute_one(self, query, parameters=None):
        self.cursor.execute(query, parameters)
        return self.cursor.fetchone()

    def execute_update(self, query, parameters=None):
        self.cursor.execute(query, parameters)
        self.conn.commit()

    def execute_delete(self, query, parameters=None):
        self.cursor.execute(query, parameters)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
