"""This module contain function. create RAW-query to UPDATE in database"""
import datetime

from wh_app.supporting import functions
from wh_app.sql.sql_constant import sql_consts_dict, tech_tables
from wh_app.sql.select_sql.select_sql import log_decorator


@log_decorator
def sql_update_point(point_id: str, point_name: str, point_address: str) -> str:
    """Returns the query string to update point information """

    query = ("""UPDATE %(workspoints)s SET %(point_name)s = '{0}', %(point_address)s = '{1}'""" +
             """ WHERE %(point_id)s = '{2}';""") % sql_consts_dict

    return query.format(point_name,
                        point_address,
                        point_id)


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
def sql_inverse_points_status(point_id: str) -> str:
    """Return the query string to invert is_work section"""

    query = ("""UPDATE %(workspoints)s SET %(is_work)s = CASE 
    WHEN %(is_work)s = 'in_work'::%(point_status)s THEN 'reconstruction'::%(point_status)s 
    WHEN %(is_work)s = 'reconstruction'::%(point_status)s THEN 'closed'::%(point_status)s 
    ELSE 'in_work'::%(point_status)s 
    END WHERE %(point_id)s = '{0}'""") % sql_consts_dict

    return query.format(point_id)


@log_decorator
def sql_inverse_worker_status(worker_id: str) -> str:
    """Return the query string to invert is_work column in workers-table"""

    query = ("""UPDATE %(workers)s SET %(is_work)s = NOT %(is_work)s where ID = {0}""") % sql_consts_dict
    return query.format(worker_id)


@log_decorator
def sql_update_worker_info(worker_id: str, name: str, sub_name: str, phone_number: str, post_id: str,
                           status: str, employee_date: datetime.date) -> str:
    """Return the query string to update worker information"""

    query = ("""UPDATE %(workers)s SET %(name)s = '{0}', %(sub_name)s = '{1}', """ +
             """ %(phone_number)s = '{2}', %(post_id)s = {3}, %(status)s = '{4}', %(emloyee_date)s = '{5}'""" +
             """ WHERE %(id)s = {6}""") % sql_consts_dict
    return query.format(name, sub_name, phone_number, post_id, status, employee_date, worker_id)


@log_decorator
def sql_update_dismissla_date(worker_id: str) -> str:
    """Return the query string to set dismissal_date"""

    query = """UPDATE %(workers)s SET %(dismissal_date)s = NOW()::DATE WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(worker_id)


@log_decorator
def sql_remove_dismissal_date(worker_id: str) -> str:
    """Return the query string to set dissmissal_date in NULL"""

    query = """UPDATE %(workers)s SET %(dismissal_date)s = NULL WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(worker_id)


@log_decorator
def sql_update_work_info(work_id: str, order_info: str, description: str, work_datetime: str) -> str:
    """return the query string to update work information"""

    query = ("""UPDATE %(works)s SET %(problem)s = '{1}', %(result)s = '{2}', %(date)s = '{3}'
     WHERE id = {0}""") % sql_consts_dict
    return query.format(work_id, order_info, description, work_datetime)


@log_decorator
def sql_set_deleted_status(equip_id: str) -> str:
    """Create query to set deleted = true """

    query = """UPDATE %(oborudovanie)s SET %(deleted)s = true WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(equip_id)


@log_decorator
def sql_invert_bug_status(bug_id: str) -> str:
    """Create query to inverted bug-status in database"""

    query = ("""UPDATE %(bugzilla)s SET %(status)s = NOT %(status)s,""" + \
             """ %(date_close)s = CASE %(status)s WHEN true THEN NOW() ELSE NULL END """ + \
             """  WHERE %(id)s = {}""") % sql_consts_dict
    return query.format(bug_id)


@log_decorator
def sql_update_tech_section(point_id: str, section: str, dogovor: str, resume: str) -> str:
    """Create query to update current technical section for workpoint"""
    query = """UPDATE {0} SET %(treaty)s = '{1}', %(resume)s = '{2}' WHERE %(point_id)s = {3}""" % sql_consts_dict
    return query.format(tech_tables[section], dogovor, resume, point_id)


@log_decorator
def sql_update_equip_in_works(work_id: str, equip_id) -> str:
    """Create query to update equip_id in work-record"""
    query = "UPDATE %(works)s SET %(id_obor)s = '{0}' WHERE %(id)s = {1}""" % sql_consts_dict
    return query.format(equip_id, work_id)


@log_decorator
def sql_update_order_info_in_work(order_id: str, comment: str) -> str:
    """Create query to set order status in in_work and update comment"""

    query = """UPDATE %(orders)s SET %(status)s = 'in_work', %(closed_date)s = NULL, %(comment)s = '{1}'
     WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(order_id, comment)


@log_decorator
def sql_update_order_info_not_work(order_id: str, status: str, comment: str) -> str:
    """Create query to set order status in in_work and update comment"""

    query = """UPDATE %(orders)s SET %(status)s = '{1}', %(closed_date)s = NOW(), %(comment)s = '{2}' WHERE %(id)s = {0}
     """ % sql_consts_dict
    return query.format(order_id, status, comment)


@log_decorator
def sql_update_schedule(worker_id: int, work_date: str, day_type: str) -> str:
    """Create query to update schedule table"""

    query = """UPDATE %(workers_schedule)s SET %(day_type)s = '{}' WHERE %(work_date)s = '{}'
     AND %(worker_id)s = {}""" % sql_consts_dict
    return query.format(day_type, work_date, worker_id)


@log_decorator
def sql_update_meter_reading(device_id: int, current_date: str, new_reading: float) -> str:
    """Update meter device reading with date and device_id"""

    query = """UPDATE %(meter_readings)s SET %(reading)s = {0} WHERE (%(devices_id)s = {1} AND %(read_date)s = '{2}')""" % sql_consts_dict

    return query.format(new_reading, device_id, current_date)


@log_decorator
def sql_update_invert_customer_status(customer_id: int) -> str:
    """Update is_active customer's status in database"""

    query = """UPDATE %(customer)s SET %(is_active)s = NOT %(is_active)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(customer_id)


@log_decorator
def sql_update_customer_password(customer_id: int, new_password_hash: str) -> str:
    """Update password to customer with id = customer_id"""

    query = """UPDATE %(customer)s SET %(hash_pass)s = '{1}' WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(customer_id, new_password_hash)


@log_decorator
def sql_update_performer_in_order(order_id: int, performer_id: int) -> str:
    """Update performer in order with id = order_id"""

    query = """UPDATE %(orders)s SET %(performer_id)s = {0} WHERE %(id)s = {1}""" % sql_consts_dict
    return query.format(performer_id, order_id)


@log_decorator
def sql_update_set_session_inactive(session_id: int) -> str:
    """Update sessions_hash -> is_active = False"""

    query = """UPDATE %(sessions_hashs)s SET %(is_active)s = False WHERE %(id)s = {0}""" % sql_consts_dict
    return query.format(session_id)


@log_decorator
def sql_update_attach_detail_to_equip(equip_id: int, detail_id: int) -> str:
    """Set detail_id in equip information"""

    query = """UPDATE %(oborudovanie)s SET %(detail_id)s = {0} WHERE id = {1}""" % sql_consts_dict
    return query.format(detail_id, equip_id)