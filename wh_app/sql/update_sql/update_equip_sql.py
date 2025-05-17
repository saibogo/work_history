from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_update_equip(equip_id: str, equip_name: str, equip_model: str,
                     equip_serial: str, equip_pre_id: str) -> str:
    """Return the query string to update equip information"""

    query = ("""UPDATE %(oborudovanie)s SET %(name)s = '{0}', %(model)s = '{1}',""" +
             """ %(serial_num)s = '{2}', %(pre_id)s = '{3}'""" +
             """ WHERE %(id)s = '{4}';""") % sql_consts_dict

    return query.format(str(equip_name),
                        str(equip_model),
                        str(equip_serial),
                        str(equip_pre_id),
                        str(equip_id))


@log_decorator
def sql_set_deleted_status(equip_id: str) -> str:
    """Create query to set deleted = true """

    query = """UPDATE %(oborudovanie)s SET %(deleted)s = true WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(equip_id)


@log_decorator
def sql_update_equip_in_works(work_id: str, equip_id) -> str:
    """Create query to update equip_id in work-record"""
    query = "UPDATE %(works)s SET %(id_obor)s = '{0}' WHERE %(id)s = {1}""" % sql_consts_dict
    return query.format(equip_id, work_id)


@log_decorator
def sql_update_attach_detail_to_equip(equip_id: int, detail_id: int) -> str:
    """Set detail_id in equip information"""

    query = """UPDATE %(oborudovanie)s SET %(detail_id)s = {0} WHERE id = {1}""" % sql_consts_dict
    return query.format(detail_id, equip_id)


@log_decorator
def sql_update_attach_manual_to_equip(equip_id: int, manual_id: int) -> str:
    """Set detail_id in equip information"""

    query = """UPDATE %(oborudovanie)s SET %(manual_id)s = {0} WHERE id = {1}""" % sql_consts_dict
    return query.format(manual_id, equip_id)