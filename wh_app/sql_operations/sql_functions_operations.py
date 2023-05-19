import psycopg2

from wh_app.supporting import functions
from wh_app.sql import functions_sql

functions.info_string(__name__)


def commit(connection: psycopg2.connect) -> None:
    """Applies changes to the database"""

    connection.commit()


def create_function(cursor, sql: str) -> None:
    """Create virtual table"""

    cursor.execute(sql)


def create_or_replace_status_to_text(cursor) ->None:
    """Add or replace in database function worker_status to text"""
    create_function(cursor, functions_sql.worker_status_to_text())


def all_sql_functions_list() -> list:
    """Return list contain all function to create virtual tables"""

    return [create_or_replace_status_to_text]