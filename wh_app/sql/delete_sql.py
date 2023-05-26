"""This module contain function. create RAW-query to DELETE in database"""

from wh_app.supporting import functions
from wh_app.sql.sql_constant import sql_consts_dict

functions.info_string(__name__)


def sql_delete_binding(binding_id: str) -> str:
    """Return SQL-string to delete binding with selected id"""
    query = """DELETE FROM %(bindings)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(binding_id)