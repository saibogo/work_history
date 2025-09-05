"""This module contain all SELECT to TECHNICAL INFORMATION"""

from wh_app.sql.sql_constant import sql_consts_dict

from wh_app.sql.select_sql.points_select import log_decorator, limit_and_offset


__meter_devices_columns = {1: 'device_id', 2: 'point_name', 3: 'inner_type', 4: 'is_work_type', 5: 'mtdt',
                           6: 'model', 7: 'serial_num', 8: 'start_date', 9: 'stopdt', 10: 'verdt', 11: 'comment'}


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
    CASE WHEN %(is_inner)s = true THEN 'Внутренний' ELSE 'Коммерческий' END AS inner_type,
    CASE WHEN %(is_active)s = true THEN 'Работает' ELSE 'Демонтирован' END AS is_work_type,
    meter_type_to_string(%(device_type)s) AS mtdt, %(model)s, %(serial_num)s, %(start_date)s,
    CASE WHEN %(stop_date)s IS NULL THEN ''::text ELSE %(stop_date)s::text END AS stopdt,
    CASE WHEN %(verification_date)s IS NULL THEN 'Дата поверки неизвестна' ELSE %(verification_date)s::text END AS verdt,
    %(comment)s
    FROM %(points_meter_devices)s
    JOIN %(workspoints)s ON %(point_id)s = %(point)s
    JOIN %(meter_devices)s ON (%(device_id)s = %(meter_devices)s.%(id)s  {0}) ORDER BY %(point_name)s, %(device_type)s
    """ % sql_consts_dict

    return query.format(" AND is_active = true" if status == "WORKED" else "")


@log_decorator
def sql_select_all_meter_devices_limit(page_num: int, ord=False, ord_column=1, status="ALL") -> str:
    """Return SELECT-string for get all information from all meter devoces
    Status ALL return ALL devices, status WORKED return only is_active = true"""
    if ord:
        try:
            formatter = __meter_devices_columns[int(ord_column)]
        except:
            formatter = __meter_devices_columns[1]
    else:
        formatter = """%(point_name)s, %(device_type)s""" % sql_consts_dict

    query = """SELECT %(device_id)s, %(point_name)s,
    CASE WHEN %(is_inner)s = true THEN 'Внутренний' ELSE 'Коммерческий' END AS inner_type,
    CASE WHEN %(is_active)s = true THEN 'Работает' ELSE 'Демонтирован' END AS is_work_type,
    meter_type_to_string(%(device_type)s) AS mtdt, %(model)s, %(serial_num)s, %(start_date)s,
    CASE WHEN %(stop_date)s IS NULL THEN ''::text ELSE %(stop_date)s::text END AS stopdt,
    CASE WHEN %(verification_date)s IS NULL THEN 'Дата поверки неизвестна' ELSE %(verification_date)s::text END AS verdt,
    %(comment)s
    FROM %(points_meter_devices)s
    JOIN %(workspoints)s ON %(point_id)s = %(point)s
    JOIN %(meter_devices)s ON (%(device_id)s = %(meter_devices)s.%(id)s  {0}) ORDER BY {1}""" % sql_consts_dict

    return query.format(" AND is_active = true" if status == "WORKED" else "", formatter) + limit_and_offset(page_num)


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
      ROUND(diff * %(Kt)s / delta_days, 3) FROM tmp OFFSET 1""" % sql_consts_dict

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


@log_decorator
def sql_select_all_counts_worked_devices() -> str:
    """Return SQL-string to get list with pairs {device_type, count worked devices}"""

    query = """SELECT meter_type_to_string(%(device_type)s) AS tmp, COUNT(%(id)s) FROM %(meter_devices)s WHERE %(is_active)s = true 
    GROUP BY %(device_type)s ORDER BY tmp""" % sql_consts_dict
    return query


@log_decorator
def sql_select_all_awaliable_schemes_for_type_and_point(point_id: int, devices_type: str) -> str:
    """Return SQL-string to get all awaliable calculation schemes"""

    query = """SELECT %(id)s FROM %(calculation_schemes)s WHERE %(point_id)s = {0} AND %(devices_type)s = '{1}'""" \
            % sql_consts_dict
    return query.format(point_id, devices_type)


@log_decorator
def sql_select_all_positive_schemes_from_schemes_id(schemes_id: int) -> str:
    """Return SQL-string to SELECT all positive schemes from schemes with id"""

    query = """SELECT unnest(%(positive_calc)s) FROM %(calculation_schemes)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(schemes_id)


@log_decorator
def sql_select_all_negative_schemes_from_schemes_id(schemes_id: int) -> str:
    """Return SQL-string to SELECT all negative schemes from schemes with id"""

    query = """SELECT unnest(%(negative_calc)s) FROM %(calculation_schemes)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(schemes_id)


@log_decorator
def sql_select_schemes_comment_from_schemes_id(schemes_id: int) -> str:
    """Return SQL-string to get comment with current calculation scheme"""

    query = """SELECT %(comment)s FROM %(calculation_schemes)s WHERE %(id)s = {}""" % sql_consts_dict
    return query.format(schemes_id)


@log_decorator
def sql_select_all_meter_types() -> str:
    """Return all meter types in database"""

    query = """SELECT unnest(enum_range(NULL::%(meter_type)s))""" % sql_consts_dict
    return query


@log_decorator
def sql_select_unit_meter_from_type(devices_type: str) -> str:
    """Return name of unit meter in russian"""

    return """SELECT units_of_measure_string('{}')""".format(devices_type)


@log_decorator
def sql_select_russian_string_from_meter_type(devices_type: str) -> str:
    """Return russian name to meter type"""

    return """SELECT meter_type_to_string('{}')""".format((devices_type))


@log_decorator
def sql_select_last_month_from_device_id(device_id: int) -> str:
    """Return query string to get last month consumption from device"""

    return """SELECT total_last_month({})""".format(device_id)


@log_decorator
def sql_select_average_from_device_id(device_id: int) -> str:
    """Return query string to get average from two last reading"""

    return """SELECT average_from_last_readings({})""".format(device_id)


@log_decorator
def sql_select_calculate_in_scheme(scheme_id: int) -> str:
    """Return tuple contain (average, average for month future, average sum between two last reading)"""

    return """SELECT sum_pu_in_scheme({})""".format(scheme_id)


@log_decorator
def sql_select_full_calc_all_schemes_in_point(point_id: int) -> str:
    """Return array contain all data for all calculating schemes in point"""

    return """SELECT full_calc_all_schemes_in_point({})""".format(point_id)


@log_decorator
def sql_select_last_24_monthly_expense(device_id: int) -> str:
    """Return SELECT string to find last 24 monthly expense for meter device with id = device_id"""

    query = """WITH mounths_readings AS 
	    (SELECT * FROM %(meter_readings)s WHERE %(id)s = ANY(last_N_nearest_readings({0}, 25)) ORDER BY %(read_date)s)
        SELECT mounths_readings.%(id)s, LAG(%(read_date)s, 1) OVER (ORDER BY %(read_date)s) AS period_beg,
         %(read_date)s AS period_end,
		(%(reading)s - LAG(%(reading)s, 1) OVER (ORDER BY %(read_date)s)) * %(Kt)s AS total
        FROM mounths_readings
        JOIN %(meter_devices)s ON  %(meter_devices)s.%(id)s = {0}
        OFFSET 1;""" % sql_consts_dict

    return query.format(device_id)