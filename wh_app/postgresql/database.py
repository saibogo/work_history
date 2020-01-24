import psycopg2

from wh_app.config_and_backup import config
from wh_app.supporting import functions

functions.info_string(__name__)


class Database:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(database=config.database_name,
                                               user=config.user_name,
                                               password=config.user_password,
                                               host=config.database_host,
                                               port=config.database_port)
            self.cursor = self.connection.cursor()
        except psycopg2.ConnectionException:
            print("База данных недоступна!")
            exit(1)

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
