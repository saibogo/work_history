import psycopg2

import functions
import view_sql

functions.info_string(__name__)


def commit(connection: psycopg2.connect) -> None:
    """Applies changes to the database"""

    connection.commit()


def create_view(cursor, sql: str) -> None:
    """Create virtual table"""

    cursor.execute(sql)


def create_or_replace_second_bindings(cursor) -> None:
    """Create virtual table second bindings"""

    create_view(cursor, view_sql.second_bindings_view())


def create_or_replace_firsts_bindings(cursor) -> None:
    """Create virtual table firsts bindings"""

    create_view(cursor, view_sql.firsts_bindings_view())