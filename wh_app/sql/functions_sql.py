from wh_app.supporting import functions

functions.info_string(__name__)


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


def bug_status_to_text() -> str:
    """Create or replace SQL function mapping bug_status to text"""
    return """CREATE OR REPLACE FUNCTION bug_status_to_string(st bool) RETURNS text AS $$ 
    BEGIN 
    IF st = true THEN RETURN 'В обработке'::text; 
    ELSE RETURN 'Решено'::text; 
    END IF; 
    END; 
    $$ LANGUAGE plpgsql;"""


def point_status_to_text() -> str:
    """Create or replace SQL function mapping point_status to text"""
    return """CREATE OR REPLACE FUNCTION point_status_to_string(st bool) RETURNS text AS $$ 
    BEGIN 
    IF st = true THEN RETURN 'Работает'::text; 
    ELSE RETURN 'Не работает'::text; 
    END IF; 
    END; 
    $$ LANGUAGE plpgsql;"""