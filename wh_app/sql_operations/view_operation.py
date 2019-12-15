import psycopg2

from wh_app.supporting import functions
from wh_app.sql import view_sql

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


def create_or_replace_statistic(cursor) -> None:
    """Create virtual table statistic"""

    create_view(cursor, view_sql.statistic_view())


def create_or_replace_works_from_worker(cursor) -> None:
    """Create virtual table works_from_worker"""

    create_view(cursor, view_sql.works_from_worker())


def create_or_replace_all_workers(cursor) -> None:
    """Create virtual table all_workers"""

    create_view(cursor, view_sql.all_workers())


def create_or_replace_works_likes(cursor) -> None:
    """Create virtual table works likes any expression"""

    create_view(cursor, view_sql.works_likes())


def all_view_list() -> list:
    """Return list contain all function to create virtual tables"""

    return [create_or_replace_second_bindings,
            create_or_replace_firsts_bindings,
            create_or_replace_statistic,
            create_or_replace_works_from_worker,
            create_or_replace_all_workers,
            create_or_replace_works_likes]