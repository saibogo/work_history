from wh_app.supporting import functions

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


def statistic_view() -> str:
    """Return SQL-string contain query to create or replace statictics view"""

    return """CREATE OR REPLACE VIEW statistic AS 
    SELECT MAX(workspoints.point_id) AS point_id, workspoints.point_name AS name_point, 
    COUNT(DISTINCT oborudovanie.id) AS equips_count, COUNT(works.id) AS works_count, MAX(works.date) AS last_date 
    FROM workspoints JOIN oborudovanie ON oborudovanie.point_id = workspoints.point_id JOIN works 
    ON works.id_obor = oborudovanie.id GROUP BY name_point ORDER BY name_point"""


def works_from_worker() -> str:
    """Return SQL-string contain query to create or replace view works from worker"""

    return """CREATE OR REPLACE VIEW works_from_worker AS 
    SELECT works.id, workspoints.point_name, oborudovanie.name, 
    oborudovanie.model, oborudovanie.serial_num, works.date, works.problem, works.result, 
    tmp.all_workers FROM works JOIN performers ON works.id = performers.work_id JOIN oborudovanie 
    ON oborudovanie.id = works.id_obor JOIN workspoints ON workspoints.point_id = oborudovanie.point_id 
    JOIN (SELECT works.id AS work_id, string_agg(workers.sub_name, ' ') AS all_workers FROM works 
    JOIN oborudovanie ON works.id_obor = oborudovanie.id JOIN performers ON works.id = performers.work_id 
    JOIN workers ON workers.id = performers.worker_id GROUP BY works.id) AS tmp ON tmp.work_id = works.id"""


def all_workers() -> str:
    """Return SQL-string contain query to create or replace view all workers"""

    return """CREATE OR REPLACE VIEW all_workers AS 
    SELECT workers.id, workers.sub_name, workers.name, workers.phone_number, CASE WHEN workers.is_work=true 
    THEN 'Работает' ELSE 'Уволен' END , posts.post_name FROM workers JOIN posts 
    ON posts.id = workers.post_id ORDER BY sub_name, name"""


def works_likes() -> str:
    """Return SQL-string contain query to create or replace view works likes"""

    return """CREATE OR REPLACE VIEW works_likes AS 
    SELECT works.id, workspoints.point_name, oborudovanie.name, oborudovanie.model, 
    oborudovanie.serial_num, works.date, works.problem, works.result, tmp.all_workers FROM works 
    JOIN oborudovanie ON oborudovanie.id = works.id_obor JOIN workspoints 
    ON workspoints.point_id = oborudovanie.point_id JOIN (SELECT works.id AS work_id, 
    string_agg(workers.sub_name, ' ') AS all_workers FROM works JOIN oborudovanie 
    ON works.id_obor = oborudovanie.id JOIN performers ON works.id = performers.work_id 
    JOIN workers ON workers.id = performers.worker_id GROUP BY works.id) AS tmp ON tmp.work_id = works.id"""
