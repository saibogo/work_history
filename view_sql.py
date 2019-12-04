import functions

functions.info_string(__name__)


def second_bindings_view() -> str:
    """Return SQL-string contain query to create or replace seconds bindings view"""

    return """CREATE OR REPLACE VIEW seconds_bindings AS 
    SELECT workspoints.point_name AS point, string_agg(workers.sub_name, ', ') AS alter_workers 
    FROM workspoints JOIN bindings ON bindings.point_id = workspoints.point_id 
    AND bindings.is_main = false JOIN workers ON workers.id = bindings.worker_id GROUP BY workspoints.point_name"""


def firsts_bindings_view() -> str:
    """Return SQL-string contain query to create or replace firsts bindings view"""

    return """CREATE OR REPLACE VIEW firsts_bindings AS 
    SELECT workspoints.point_name, CASE WHEN wd.day1 = true 
    THEN (SELECT sub_name FROM workers WHERE workers.id = bindings.worker_id AND bindings.is_main = true) 
    ELSE '--' END AS "monday", CASE WHEN wd.day2 = true 
    THEN (SELECT sub_name FROM workers WHERE workers.id = bindings.worker_id AND bindings.is_main = true) 
    ELSE '--' END AS "thuesday", CASE WHEN wd.day3 = true 
    THEN (SELECT sub_name FROM workers WHERE workers.id = bindings.worker_id AND bindings.is_main = true) 
    ELSE '--' END AS "wednesday", CASE WHEN wd.day4 = true 
    THEN (SELECT sub_name FROM workers WHERE workers.id = bindings.worker_id AND bindings.is_main = true) 
    ELSE '--' END AS "thoursday", CASE WHEN wd.day5 = true 
    THEN (SELECT sub_name FROM workers WHERE workers.id = bindings.worker_id AND bindings.is_main = true) 
    ELSE '--' END AS "friday", CASE WHEN wd.day6 = true 
    THEN (SELECT sub_name FROM workers WHERE workers.id = bindings.worker_id AND bindings.is_main = true) 
    ELSE '--' END AS "saturday", CASE WHEN wd.day7 = true 
    THEN (SELECT sub_name FROM workers WHERE workers.id = bindings.worker_id AND bindings.is_main = true) 
    ELSE '--' END AS "sunday" 
    FROM workspoints JOIN bindings ON bindings.point_id = workspoints.point_id 
    JOIN works_days AS wd ON wd.worker_id = bindings.worker_id AND bindings.is_main = true 
    ORDER BY workspoints.point_name"""
