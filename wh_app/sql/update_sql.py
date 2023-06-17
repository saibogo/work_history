"""This module contain function. create RAW-query to UPDATE in database"""

from wh_app.supporting import functions
from wh_app.sql.sql_constant import sql_consts_dict, tech_tables

functions.info_string(__name__)


def sql_update_point(point_id:str, point_name: str, point_address: str) -> str:
    """Returns the query string to update point information """

    query = ("""UPDATE %(workspoints)s SET %(point_name)s = '{0}', %(point_address)s = '{1}'""" +
             """ WHERE %(point_id)s = '{2}';""") % sql_consts_dict

    return query.format(point_name,
                        point_address,
                        point_id)


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


def sql_inverse_points_status(point_id: str) -> str:
    """Return the query string to invert is_work section"""

    query = ("""UPDATE %(workspoints)s SET %(is_work)s = NOT %(is_work)s""" +
             """ WHERE %(point_id)s = '{0}';""") % sql_consts_dict

    return query.format(point_id)


def sql_inverse_worker_status(worker_id: str) -> str:
    """Return the query string to invert is_work column in workers-table"""

    query = ("""UPDATE %(workers)s SET %(is_work)s = NOT %(is_work)s where ID = {0}""") % sql_consts_dict
    return query.format(worker_id)


def sql_update_worker_info(worker_id: str, name: str, sub_name: str,phone_number: str, post_id: str, status: str) -> str:
    """Return the query string to update worker information"""

    query = ("""UPDATE %(workers)s SET %(name)s = '{0}', %(sub_name)s = '{1}', """ +
             """ %(phone_number)s = '{2}', %(post_id)s = {3}, %(status)s = '{4}' WHERE %(id)s = {5}""") % sql_consts_dict
    return query.format(name, sub_name, phone_number, post_id, status, worker_id)


def sql_update_work_info(work_id: str, order_info: str, description: str, work_datetime: str) -> str:
    """return the query string to update work information"""

    query = ("""UPDATE %(works)s SET %(problem)s = '{1}', %(result)s = '{2}', %(date)s = '{3}'
     WHERE id = {0}""") % sql_consts_dict
    return query.format(work_id, order_info, description, work_datetime)


def sql_set_deleted_status(equip_id: str) -> str:
    """Create query to set deleted = true """

    query = """UPDATE %(oborudovanie)s SET %(deleted)s = true WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(equip_id)


def sql_invert_bug_status(bug_id: str) -> str:
    """Create query to inverted bug-status in database"""

    query = ("""UPDATE %(bugzilla)s SET %(status)s = NOT %(status)s,""" +\
            """ %(date_close)s = CASE %(status)s WHEN true THEN NOW() ELSE NULL END """ +\
            """  WHERE %(id)s = {}""") % sql_consts_dict
    return query.format(bug_id)


def sql_update_tech_section(point_id: str, section: str, dogovor: str, resume: str) -> str:
    """Create query to update current technical section for workpoint"""
    query = """UPDATE {0} SET %(treaty)s = '{1}', %(resume)s = '{2}' WHERE %(point_id)s = {3}""" % sql_consts_dict
    return query.format(tech_tables[section], dogovor, resume, point_id)


def sql_update_equip_in_works(work_id: str, equip_id) -> str:
    """Create query to update equip_id in work-record"""
    query = "UPDATE %(works)s SET %(id_obor)s = '{0}' WHERE %(id)s = {1}""" % sql_consts_dict
    return query.format(equip_id, work_id)
