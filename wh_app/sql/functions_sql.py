from wh_app.supporting import functions
from wh_app.sql.select_sql.select_sql import log_decorator

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
    return """
    CREATE OR REPLACE FUNCTION bug_status_to_string(st order_status) RETURNS text AS $$ 
    BEGIN 
    IF st = 'in_work' THEN RETURN 'В обработке'::text;
    ELSIF st = 'canceled' THEN RETURN 'Отменена'::text; 
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


@log_decorator
def last_day_funct() -> str:
    """Create or replace SQL function SELECT current day - 1"""
    return """CREATE OR REPLACE FUNCTION last_day_date() RETURNS DATE as $$ 
    BEGIN 
    RETURN NOW()::DATE - 1; END $$ LANGUAGE plpgsql;"""


@log_decorator
def last_week_funct() -> str:
    """Create or replace SQL function SELECT current day - 7"""
    return """CREATE OR REPLACE FUNCTION last_week_date() RETURNS DATE as $$ 
    BEGIN 
    RETURN NOW()::DATE - 7; END $$ LANGUAGE plpgsql;"""


@log_decorator
def last_month_funct() -> str:
    """Create or replace SQL function SELECT current day - 7"""
    return """CREATE OR REPLACE FUNCTION last_month_date() RETURNS DATE as $$ 
    BEGIN 
    RETURN NOW()::DATE - 30; END $$ LANGUAGE plpgsql;"""


@log_decorator
def last_year_funct() -> str:
    """Create or replace SQL function SELECT current day - 7"""
    return """CREATE OR REPLACE FUNCTION last_year_date() RETURNS DATE as $$ 
    BEGIN 
    RETURN NOW()::DATE - 365; END $$ LANGUAGE plpgsql;"""


@log_decorator
def work_day_type_to_string() -> str:
    """Create or replace SQL function mapping work_day_type to sting"""

    return """CREATE OR REPLACE FUNCTION work_day_type_to_string(st work_day_type) RETURNS text AS $$ 
    BEGIN 
    IF st = 'schedule_8_18'::work_day_type THEN RETURN '09:00 - 18:00'::text; 
    ELSIF st = 'schedule_7_19'::work_day_type THEN RETURN '07:00 - 19-00'::text; 
    ELSIF st = 'shedule_service'::work_day_type THEN RETURN 'По графику ТО'::text; 
    ELSE RETURN 'Спецграфик'::text; 
    END IF; 
    END; 
    $$ LANGUAGE plpgsql;"""


@log_decorator
def date_to_date_and_day_of_week() -> str:
    """Create or replace SQL function mapping date to string likes YYYY-MM-DD(Day of week)"""

    return """CREATE OR REPLACE FUNCTION date_to_date_and_day_string(d DATE) RETURNS text AS $$
    BEGIN
    RETURN d || '(' || To_Char(d, 'TMDAY') || ')' :: text;
    END;
    $$ LANGUAGE plpgsql;"""


@log_decorator
def meter_type_to_string() -> str:
    """Create or replace SQL function mapping meter_type to humans string"""

    return """CREATE OR REPLACE FUNCTION meter_type_to_string(m meter_type) RETURNS text AS $$
    BEGIN 
    IF m = 'electricity'::meter_type THEN RETURN 'электроэнергия':: text;
    ELSIF m ='cold_water'::meter_type THEN RETURN 'ХВС'::text;
    ELSIF m = 'hot_water'::meter_type THEN RETURN 'ГВС'::text;
    ELSIF m = 'warm_energy'::meter_type THEN RETURN 'тепловая энергия Гкал'::text;
    ELSE RETURN 'тепловая энергия м.куб.'::text;
    END IF;
    END;
    $$ LANGUAGE plpgsql;"""


@log_decorator
def units_of_measure() -> str:
    """Create or replace SQL function to convert meter_type to units of measure"""

    return """CREATE OR REPLACE FUNCTION units_of_measure_string(m meter_type) RETURNS text AS $$
        BEGIN 
        IF m = 'electricity'::meter_type THEN RETURN 'кВт*час':: text;
        ELSIF m ='cold_water'::meter_type THEN RETURN 'м.куб.'::text;
        ELSIF m = 'hot_water'::meter_type THEN RETURN 'м.куб.'::text;
        ELSIF m = 'warm_energy'::meter_type THEN RETURN 'Гкал'::text;
        ELSE RETURN 'м.куб.'::text;
        END IF;
        END;
        $$ LANGUAGE plpgsql;"""