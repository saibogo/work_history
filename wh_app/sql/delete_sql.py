"""This module contain function. create RAW-query to DELETE in database"""

from wh_app.supporting import functions
from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql.select_sql import log_decorator

functions.info_string(__name__)


@log_decorator
def sql_delete_binding(binding_id: str) -> str:
    """Return SQL-string to delete binding with selected id"""
    query = """DELETE FROM %(bindings)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(binding_id)


@log_decorator
def sql_delete_performer(work_id: str, performer_id: str) -> str:
    """Return SQL-string to delete performer from work with selected id"""
    query = """DELETE FROM %(performers)s WHERE %(work_id)s = {0} AND %(worker_id)s = {1}""" % sql_consts_dict
    return query.format(work_id, performer_id)