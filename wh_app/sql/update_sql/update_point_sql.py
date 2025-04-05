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
def sql_inverse_points_status(point_id: str) -> str:
    """Return the query string to invert is_work section"""

    query = ("""UPDATE %(workspoints)s SET %(is_work)s = CASE 
    WHEN %(is_work)s = 'in_work'::%(point_status)s THEN 'reconstruction'::%(point_status)s 
    WHEN %(is_work)s = 'reconstruction'::%(point_status)s THEN 'closed'::%(point_status)s 
    ELSE 'in_work'::%(point_status)s 
    END WHERE %(point_id)s = '{0}'""") % sql_consts_dict

    return query.format(point_id)


@log_decorator
def sql_update_tech_section(point_id: str, section: str, dogovor: str, resume: str) -> str:
    """Create query to update current technical section for workpoint"""
    query = """UPDATE {0} SET %(treaty)s = '{1}', %(resume)s = '{2}' WHERE %(point_id)s = {3}""" % sql_consts_dict
    return query.format(tech_tables[section], dogovor, resume, point_id)


@log_decorator
def sql_update_meter_reading(device_id: int, current_date: str, new_reading: float) -> str:
    """Update meter device reading with date and device_id"""

    query = """UPDATE %(meter_readings)s SET %(reading)s = {0} WHERE (%(devices_id)s = {1} AND %(read_date)s = '{2}')""" % sql_consts_dict

    return query.format(new_reading, device_id, current_date)