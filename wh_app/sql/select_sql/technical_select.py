"""This module contain all SELECT to TECHNICAL INFORMATION"""

from wh_app.sql.sql_constant import sql_consts_dict

from wh_app.sql.select_sql.points_select import log_decorator


@log_decorator
def sql_select_electric_info(point_id: str) -> str:
    """Return SELECT-string for get electric information to point"""

    query = ("""SELECT * FROM %(electric)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_cold_water_info(point_id: str) -> str:
    """Return SELECT-string for get cold_water information to point"""

    query = ("""SELECT * FROM %(cold_water)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_hot_water_info(point_id: str) -> str:
    """Return SELECT-string for get hot_water information to point"""

    query = ("""SELECT * FROM %(hot_water)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_heating_info(point_id: str) -> str:
    """Return SELECT-string for get heating information to point"""

    query = ("""SELECT * FROM %(heating)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_sewerage_info(point_id: str) -> str:
    """Return SELECT-string for get sewerage information to point"""

    query = ("""SELECT * FROM %(sewerage)s WHERE point_id={0}""") % sql_consts_dict
    return query.format(point_id)


@log_decorator
def sql_select_all_meter_devices(status="ALL") -> str:
    """Return SELECT-string for get all information from all meter devoces
    Status ALL return ALL devices, status WORKED return only is_active = true"""

    query = """SELECT %(device_id)s, %(point_name)s,
    CASE WHEN %(is_inner)s = true THEN 'Внутренний' ELSE 'Коммерческий' END,
    CASE WHEN %(is_active)s = true THEN 'Работает' ELSE 'Демонтирован' END,
    meter_type_to_string(%(device_type)s), %(model)s, %(serial_num)s, %(start_date)s,
    CASE WHEN %(stop_date)s IS NULL THEN ''::text ELSE %(stop_date)s::text END,
    CASE WHEN %(verification_date)s IS NULL THEN 'Дата поверки неизвестна' ELSE %(verification_date)s::text END,
    %(comment)s
    FROM %(points_meter_devices)s
    JOIN %(workspoints)s ON %(point_id)s = %(point)s
    JOIN %(meter_devices)s ON (%(device_id)s = %(meter_devices)s.%(id)s  {0}) ORDER BY %(point_name)s, %(device_type)s
    """ % sql_consts_dict

    return query.format(" AND is_active = true" if status == "WORKED" else "")


@log_decorator
def sql_select_all_works_meter_in_point(point_id: int) -> str:
    """Return SELECT-string for get all meter devices in point with status WORK"""

    query = """SELECT %(device_id)s, %(point_name)s,
        CASE WHEN %(is_inner)s = true THEN 'Внутренний' ELSE 'Коммерческий' END,
        CASE WHEN %(is_active)s = true THEN 'Работает' ELSE 'Демонтирован' END,
        meter_type_to_string(%(device_type)s), %(model)s, %(serial_num)s, %(start_date)s,
        CASE WHEN %(stop_date)s IS NULL THEN ''::text ELSE %(stop_date)s::text END,
        CASE WHEN %(verification_date)s IS NULL THEN 'Дата поверки неизвестна' ELSE %(verification_date)s::text END,
        %(comment)s
        FROM %(points_meter_devices)s 
        JOIN %(workspoints)s ON %(point_id)s = %(point)s AND %(point)s = {0}
        JOIN %(meter_devices)s ON %(device_id)s = %(meter_devices)s.%(id)s ORDER BY %(point_name)s, %(device_type)s""" % sql_consts_dict

    return query.format(point_id)


@log_decorator
def sql_select_reading_meter_from_id(id: int) -> str:
    """Return SELECT-string to get all reading meter device with device_id = id"""

    query = """WITH tmp AS(
    WITH reading_lst AS (SELECT * FROM %(meter_readings)s WHERE %(devices_id)s = {0} ORDER BY %(read_date)s)
    SELECT reading_lst.%(id)s, %(serial_num)s, %(read_date)s, %(reading)s, %(reading)s - LAG(%(reading)s, 1, 0)
     OVER (ORDER BY %(read_date)s) AS diff,  %(read_date)s - LAG(%(read_date)s, 1) OVER (ORDER BY %(read_date)s)
      AS delta_days , %(Kt)s FROM reading_lst
    JOIN %(meter_devices)s ON %(meter_devices)s.%(id)s = {0})
    SELECT %(id)s, %(serial_num)s, %(read_date)s, %(reading)s, diff, %(Kt)s, diff * %(Kt)s AS full_diff,
      diff * %(Kt)s / delta_days FROM tmp OFFSET 1""" % sql_consts_dict

    return query.format(str(id))


@log_decorator
def sql_select_readings_and_dates_from_device(device_id: int, last_24=False) -> str:
    """Return SQL select string to return last 24 redings records to current meter device"""

    query = """SELECT %(id)s, %(read_date)s, %(reading)s FROM %(meter_readings)s WHERE %(devices_id)s = {0} 
    ORDER BY %(read_date)s {1}""" % sql_consts_dict

    query_1 = """OFFSET( CASE WHEN (SELECT COUNT(*) FROM %(meter_readings)s WHERE %(devices_id)s = {0}) > 24 
    THEN (SELECT COUNT(*) FROM %(meter_readings)s WHERE %(devices_id)s = {0}) - 24 ELSE 0 END )""" % sql_consts_dict

    return query.format(device_id, query_1.format(device_id) if last_24 else "")


@log_decorator
def sql_select_full_information_from_meter_device(device_id: int) -> str:
    """Return SQL string to get ALL info from meter device with id = device_id"""

    query = """SELECT %(meter_devices)s.%(id)s, meter_type_to_string(%(device_type)s), %(model)s,
	%(serial_num)s, CASE WHEN %(is_active)s THEN 'Работает' ELSE 'Демонтирован' END,
	%(start_date)s, CASE WHEN %(stop_date)s IS NULL THEN '' ELSE %(stop_date)s::TEXT END,
	%(verification_date)s, %(Kt)s, CASE WHEN %(is_inner)s THEN 'Внутренний' ELSE 'Расчетный' END,
	%(point_name)s, %(comment)s FROM %(meter_devices)s JOIN %(points_meter_devices)s 
	ON (%(points_meter_devices)s.%(device_id)s = %(meter_devices)s.%(id)s AND %(meter_devices)s.%(id)s = {0})
    JOIN %(workspoints)s ON %(points_meter_devices)s.%(point)s = %(workspoints)s.%(point_id)s""" % sql_consts_dict

    return query.format(device_id)


@log_decorator
def sql_select_count_all_meter_devices() -> str:
    """Return SQL-string to COUNT(all meter devices)"""

    query = """SELECT COUNT(*) FROM %(meter_devices)s""" % sql_consts_dict
    return query


@log_decorator
def sql_select_count_worked_meter_devices() -> str:
    """Return SQL-string to COUNT(all meter devices)"""

    query = """SELECT COUNT(*) FROM %(meter_devices)s WHERE is_active = true""" % sql_consts_dict
    return query
