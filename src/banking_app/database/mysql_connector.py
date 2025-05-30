import pymysql
from pymysql.cursors import DictCursor
from src.banking_app.logger.logger import log
import os

class Mysqldb:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "password")
        self.database = os.getenv("DB_NAME", "banking")
        self.port = int(os.getenv("DB_PORT", 3306))

    def _connect(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            cursorclass=DictCursor
        )

    def read_mysqldb(self, query, params=None):
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchall()
                    log.info(f"Read query executed: {query}")
                    return result
        except Exception as e:
            log.error(f"Read failed: {str(e)}")
            raise

    def insert_mysqldb(self, query, params=None):
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    log.info(f"Insert successful: {query}")
        except Exception as e:
            log.error(f"Insert failed: {str(e)}")
            raise

    def update_mysqldb(self, query, params=None):
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    log.info(f"Update successful: {query}")
        except Exception as e:
            log.error(f"Update failed: {str(e)}")
            raise
