from wh_app.supporting import functions
from wh_app.sql.select_sql import log_decorator

functions.info_string(__name__)


@log_decorator
def worker_status_to_text() -> str:
    """Create or replace SQL function mapping worker_status to text"""

    return """CREATE OR REPLACE FUNCTION worker_status_to_string(st worker_status) RETURNS text AS $$ 
    BEGIN 
    IF st = 'works'::worker_status THEN RETURN  'Работает'::text; 
    ELSIF st = 'fired'::worker_status THEN RETURN 'Уволен'::text; 
    ELSIF st = 'on_holyday'::worker_status THEN RETURN 'В отпуске'::text; 
    ELSE RETURN 'На больничном'::text; 
    END IF; 
    END; 
    $$ LANGUAGE plpgsql;"""


@log_decorator
def bug_status_to_text() -> str:
    """Create or replace SQL function mapping bug_status to text"""
    return """CREATE OR REPLACE FUNCTION bug_status_to_string(st bool) RETURNS text AS $$ 
    BEGIN 
    IF st = true THEN RETURN 'В обработке'::text; 
    ELSE RETURN 'Решено'::text; 
    END IF; 
    END; 
    $$ LANGUAGE plpgsql;"""


@log_decorator
def point_status_to_text() -> str:
    """Create or replace SQL function mapping point_status to text"""
    return """CREATE OR REPLACE FUNCTION point_status_to_string(st bool) RETURNS text AS $$ 
    BEGIN 
    IF st = true THEN RETURN 'Работает'::text; 
    ELSE RETURN 'Не работает'::text; 
    END IF; 
    END; 
    $$ LANGUAGE plpgsql;"""


@log_decorator
def all_works_from_equip_id_funct() -> str:
    """Create or replace SQL function return SELECT all works from equip_id to text"""
    return """CREATE OR REPLACE FUNCTION all_works_from_equip(eid integer) RETURNS Table(id integer) AS $$ 
    SELECT id FROM works where id_obor = eid; 
    $$ LANGUAGE sql;"""