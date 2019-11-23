import psycopg2

import config
import functions

functions.info_string(__name__)


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(database=config.database_name,
                            user=config.user_name,
                            password=config.user_password,
                            host=config.database_host,
                            port=config.database_port)
        self.cursor = self.connection.cursor()


    def __enter__(self):
        return self.connection, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def connection(self):
        return self.connection

    def cursor(self):
        return self.cursor