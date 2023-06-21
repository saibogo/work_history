from wh_app.supporting import functions
from wh_app.sql.sql_constant import sql_consts_dict
from wh_app.sql.select_sql import log_decorator

functions.info_string(__name__)


@log_decorator
def second_bindings_view() -> str:
    """Return SQL-string contain query to create or replace seconds bindings view"""

    return """CREATE OR REPLACE VIEW %(seconds_bindings)s AS 
    SELECT %(workspoints)s.%(point_name)s AS %(point)s, string_agg(%(workers)s.%(sub_name)s, ', ') AS %(alter_workers)s 
    FROM %(workspoints)s 
    JOIN %(bindings)s 
    ON %(bindings)s.%(point_id)s = %(workspoints)s.%(point_id)s AND %(workspoints)s.%(point_working)s 
    AND %(bindings)s.%(is_main)s = false JOIN %(workers)s ON %(workers)s.%(id)s = %(bindings)s.%(worker_id)s 
    GROUP BY %(workspoints)s.%(point_name)s""" % sql_consts_dict


@log_decorator
def firsts_bindings_view() -> str:
    """Return SQL-string contain query to create or replace firsts bindings view"""

    return """CREATE OR REPLACE VIEW %(firsts_bindings)s AS 
    SELECT %(workspoints)s.%(point_name)s, CASE WHEN %(wd)s.day1 = true 
    THEN (%(select_main_binding)s) 
    ELSE '--' END AS "monday", CASE WHEN %(wd)s.day2 = true 
    THEN (%(select_main_binding)s) 
    ELSE '--' END AS "thuesday", CASE WHEN %(wd)s.day3 = true 
    THEN (%(select_main_binding)s) 
    ELSE '--' END AS "wednesday", CASE WHEN %(wd)s.day4 = true 
    THEN (%(select_main_binding)s) 
    ELSE '--' END AS "thoursday", CASE WHEN %(wd)s.day5 = true 
    THEN (%(select_main_binding)s) 
    ELSE '--' END AS "friday", CASE WHEN %(wd)s.day6 = true 
    THEN (%(select_main_binding)s) 
    ELSE '--' END AS "saturday", CASE WHEN %(wd)s.day7 = true 
    THEN (%(select_main_binding)s) 
    ELSE '--' END AS "sunday" 
    FROM %(workspoints)s 
    JOIN %(bindings)s 
    ON %(bindings)s.%(point_id)s = %(workspoints)s.%(point_id)s AND %(workspoints)s.%(point_working)s  
    JOIN %(works_days)s AS %(wd)s ON %(wd)s.%(worker_id)s = %(bindings)s.%(worker_id)s 
    AND %(bindings)s.%(is_main)s = true 
    ORDER BY %(workspoints)s.%(point_name)s""" % sql_consts_dict


@log_decorator
def statistic_view() -> str:
    """Return SQL-string contain query to create or replace statictics view"""

    return """CREATE OR REPLACE VIEW %(statistic)s AS 
    SELECT MAX(%(workspoints)s.%(point_id)s) AS %(point_id)s, %(workspoints)s.%(point_name)s AS %(name_point)s, 
    COUNT(DISTINCT %(oborudovanie)s.%(id)s) AS %(equips_count)s, 
    COUNT(%(works)s.%(id)s) AS %(works_count)s, MAX(%(works)s.%(date)s) AS %(last_date)s 
    FROM %(workspoints)s JOIN %(oborudovanie)s ON %(oborudovanie)s.%(point_id)s = %(workspoints)s.%(point_id)s 
    JOIN %(works)s 
    ON %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s 
    GROUP BY %(name_point)s ORDER BY %(name_point)s""" % sql_consts_dict


@log_decorator
def works_from_worker() -> str:
    """Return SQL-string contain query to create or replace view works from worker"""

    return """CREATE OR REPLACE VIEW %(works_from_worker)s AS 
    SELECT %(works)s.%(id)s, %(workspoints)s.%(point_name)s, %(oborudovanie)s.%(name)s, 
    %(oborudovanie)s.%(model)s, %(oborudovanie)s.%(serial_num)s, %(works)s.%(date)s, 
    %(works)s.%(problem)s, %(works)s.%(result)s, 
    %(tmp)s.%(all_workers)s FROM %(works)s JOIN %(performers)s 
    ON %(works)s.%(id)s = %(performers)s.%(work_id)s JOIN %(oborudovanie)s 
    ON %(oborudovanie)s.%(id)s = %(works)s.%(id_obor)s 
    JOIN %(workspoints)s ON %(workspoints)s.%(point_id)s = %(oborudovanie)s.%(point_id)s 
    JOIN (SELECT %(works)s.%(id)s AS %(work_id)s, string_agg(%(workers)s.%(sub_name)s, ' ') 
    AS %(all_workers)s FROM %(works)s 
    JOIN %(oborudovanie)s ON %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s 
    JOIN %(performers)s ON %(works)s.%(id)s = %(performers)s.%(work_id)s 
    JOIN %(workers)s ON %(workers)s.%(id)s = %(performers)s.%(worker_id)s 
    GROUP BY %(works)s.%(id)s) AS %(tmp)s ON %(tmp)s.%(work_id)s = %(works)s.%(id)s""" % sql_consts_dict


@log_decorator
def all_workers() -> str:
    """Return SQL-string contain query to create or replace view all workers"""

    return """CREATE OR REPLACE VIEW %(all_workers)s AS 
    SELECT %(workers)s.%(id)s, %(workers)s.%(sub_name)s, %(workers)s.%(name)s, 
    %(workers)s.%(phone_number)s, %(worker_status)s ,
     %(posts)s.%(post_name)s FROM %(workers)s JOIN %(posts)s 
    ON %(posts)s.%(id)s = %(workers)s.%(post_id)s ORDER BY %(sub_name)s, %(name)s""" % sql_consts_dict


@log_decorator
def works_likes() -> str:
    """Return SQL-string contain query to create or replace view works likes"""

    return """CREATE OR REPLACE VIEW %(works_likes)s AS 
    SELECT %(works)s.%(id)s, %(workspoints)s.%(point_name)s, %(oborudovanie)s.%(name)s, %(oborudovanie)s.%(model)s, 
    %(oborudovanie)s.%(serial_num)s, %(works)s.%(date)s, %(works)s.%(problem)s, 
    %(works)s.%(result)s, %(tmp)s.%(all_workers)s FROM %(works)s 
    JOIN %(oborudovanie)s ON %(oborudovanie)s.%(id)s = %(works)s.%(id_obor)s JOIN %(workspoints)s 
    ON %(workspoints)s.%(point_id)s = %(oborudovanie)s.%(point_id)s JOIN (SELECT %(works)s.%(id)s AS %(work_id)s, 
    string_agg(%(workers)s.%(sub_name)s, ' ') AS %(all_workers)s FROM %(works)s JOIN %(oborudovanie)s 
    ON %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s JOIN %(performers)s 
    ON %(works)s.%(id)s = %(performers)s.%(work_id)s 
    JOIN %(workers)s ON %(workers)s.%(id)s = %(performers)s.%(worker_id)s 
    GROUP BY %(works)s.%(id)s) AS %(tmp)s ON %(tmp)s.%(work_id)s = %(works)s.%(id)s""" % sql_consts_dict
