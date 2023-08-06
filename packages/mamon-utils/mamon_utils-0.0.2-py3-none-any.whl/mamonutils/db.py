import os
import psycopg2
from psycopg2 import Error
from typing import Optional


class Database:
    def __init__(self, dbname: str):
        self.dbname = dbname
        self.host = os.environ.get('DB_HOST')
        self.port = os.environ.get('DB_PORT')
        self.user = os.environ.get('DB_USER')
        self.password = os.environ.get('DB_PASSWORD')
        self._connection: Optional[psycopg2.extensions.connection] = None
        self._cursor: Optional[psycopg2.extensions.cursor] = None

    def connect(self):
        try:
            self._connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def disconnect(self):
        if self._connection:
            self._connection.close()

    @property
    def cursor(self):
        if self._connection is None:
            raise Exception("Not connected to the database.")
        if self._cursor is None or self._cursor.closed:
            self._cursor = self._connection.cursor()
        return self._cursor

    @property
    def connection(self):
        if self._connection is None:
            raise Exception("Not connected to the database.")
        return self._connection
