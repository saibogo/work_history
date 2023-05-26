from wh_app.sql.delete_sql import *

functions.info_string(__name__)


def delete_binding(cursor, binding_id: str) -> None:
    """Delete binding with selected id in database"""
    cursor.execute(sql_delete_binding(binding_id))