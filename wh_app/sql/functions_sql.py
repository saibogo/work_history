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


@log_decorator
def total_last_month() -> str:
    """Create or replace function to calculate consumption to last month from meter device"""

    return """CREATE OR REPLACE FUNCTION total_last_month(integer) RETURNS NUMERIC(13, 3) AS $$
    DECLARE 
        dev_id ALIAS FOR $1; d1 DATE; d2 DATE; d3 DATE; r1 NUMERIC; r3 NUMERIC; delta NUMERIC;
	    days INTEGER; K INTEGER; days_in_month INTEGER; tmp NUMERIC;
    BEGIN
	    d1 = (SELECT read_date FROM meter_readings WHERE (devices_id = dev_id AND read_date <= NOW()::DATE) ORDER BY read_date DESC LIMIT 1);
	    d2 = d1 - INTERVAL '1 MONTH';
	    d3 = (SELECT read_date FROM meter_readings WHERE (devices_id = dev_id AND read_date <= d2::DATE) ORDER BY read_date DESC LIMIT 1);
	    r1 = (SELECT reading FROM meter_readings WHERE (devices_id = dev_id AND read_date = d1));
	    r3 = (SELECT reading FROM meter_readings WHERE (devices_id = dev_id AND read_date = d3));
	    delta = r1 - r3;
	    days = d1 - d3;
	    K = (SELECT Kt FROM meter_devices WHERE id = dev_id);
	    days_in_month = (SELECT EXTRACT(EPOCH FROM INTERVAL '1 MONTH') / (24*60*60));
	    tmp = (delta * K  * days_in_month / days) :: NUMERIC(13, 3);
	    RETURN (CASE WHEN tmp ISNULL THEN 0::NUMERIC(13, 3) ELSE tmp END);
    END;
    $$ LANGUAGE plpgsql;"""


def average_from_last_readings() -> str:
    """Create or replace function to calculate average from two last reading to meter device"""

    return """CREATE OR REPLACE FUNCTION average_from_last_readings(integer) RETURNS NUMERIC(13,3) AS $$
    DECLARE dev_id ALIAS FOR $1; d1 DATE; d2 DATE; r1 NUMERIC; r2 NUMERIC;
	    delta NUMERIC;
	    K INTEGER;
	    days INTEGER;
    BEGIN
	    d1 = (SELECT read_date FROM meter_readings WHERE devices_id = dev_id ORDER BY read_date DESC LIMIT 1);
	    d2 = (SELECT read_date FROM meter_readings WHERE (devices_id = dev_id AND read_date < d1) ORDER BY read_date DESC LIMIT 1);
	    r1 = (SELECT reading FROM meter_readings WHERE (devices_id = dev_id AND read_date = d1));
	    r2 = (SELECT reading FROM meter_readings WHERE (devices_id = dev_id AND read_date = d2));
	    delta = r1 - r2;
	    K = (SELECT Kt FROM meter_devices WHERE id = dev_id);
	    days = d1 - d2;
	    RETURN (CASE WHEN delta ISNULL THEN 0 ELSE (delta * K / days) END):: NUMERIC(13, 3);
    END;
    $$ LANGUAGE plpgsql;"""


def sum_pu_in_scheme() -> str:
    """Create or replace function return (average, average for month future, average sum between two last reading)"""

    return """CREATE OR REPLACE FUNCTION sum_pu_in_scheme(integer) RETURNS NUMERIC[] AS $$
    DECLARE
	    schm_id ALIAS FOR $1; pos_arr INTEGER[]; neg_arr INTEGER[]; tmp NUMERIC; tmp1 NUMERIC; pu INTEGER;
	    days INTEGER; result_arr NUMERIC[];
    BEGIN
	    tmp = 0;
	    tmp1 = 0;
	    pos_arr = (SELECT positive_calc FROM calculation_schemes WHERE id = schm_id);
	    neg_arr = (SELECT negative_calc FROM calculation_schemes WHERE id = schm_id);
	    IF pos_arr ISNULL THEN pos_arr = '{}'::INTEGER[]; END IF;
	    IF neg_arr ISNULL THEN neg_arr = '{}'::INTEGER[]; END IF;
	
	    FOREACH pu IN ARRAY pos_arr LOOP
		    tmp = tmp + average_from_last_readings(pu);
		    tmp1 = tmp1 + total_last_month(pu);
	    END LOOP;
	
	    FOREACH pu IN ARRAY neg_arr LOOP
		    tmp = tmp - average_from_last_readings(pu);
		    tmp1 = tmp1 - total_last_month(pu);
	    END LOOP;

	    days = (SELECT EXTRACT(EPOCH FROM INTERVAL '1 MONTH') / (24*60*60));
	    result_arr = array_append(result_arr, tmp::NUMERIC(13, 3));
	    result_arr = array_append(result_arr, (tmp * days)::NUMERIC(13, 3));
	    result_arr = array_append(result_arr, tmp1::NUMERIC(13, 3));
	    RETURN result_arr;
    END;
    $$ LANGUAGE plpgsql;"""


def full_calculation_in_scheme() -> str:
    """Create or replace function return dta from scheme liked [type, positive devices, negative_devices, comment,
     type units, avr, avr in month, total last month]. All elements are TEXT"""

    return """CREATE OR REPLACE FUNCTION full_calc_to_scheme(integer) RETURNS text[] AS $$
    DECLARE schm ALIAS FOR $1; all_data text[]; pos_arr INTEGER[]; neg_arr  INTEGER[]; averages NUMERIC[];
    BEGIN
        all_data = ARRAY[schm];
	    all_data = array_append(all_data, (SELECT meter_type_to_string(devices_type) FROM calculation_schemes WHERE id = schm));
	    pos_arr = (SELECT positive_calc FROM calculation_schemes WHERE id = schm);
	    if pos_arr ISNULL THEN pos_arr = '{}'::INTEGER[]; END IF;
	    all_data = array_append(all_data, array_to_string(pos_arr, ' ,'));
	    neg_arr = (SELECT negative_calc FROM calculation_schemes WHERE id = schm);
	    if neg_arr ISNULL THEN neg_arr = '{}'::INTEGER[]; END IF;
	    all_data = array_append(all_data, array_to_string(neg_arr, ' ,'));
	    all_data = array_append(all_data, (SELECT comment FROM calculation_schemes WHERE id = schm));
	    all_data = array_append(all_data, (SELECT units_of_measure_string(devices_type) FROM calculation_schemes WHERE id = schm));
	    averages = (SELECT sum_pu_in_scheme(schm));
	    all_data = array_append(all_data, averages[1]::TEXT);
	    all_data = array_append(all_data, averages[2]::TEXT);
	    all_data = array_append(all_data, averages[3]::TEXT);
	RETURN all_data;
    END;
    $$ LANGUAGE plpgsql;"""


def full_calc_all_schemes_in_point() -> str:
    """Create SQL function return ARRAY liked [str1, str2, ...., strN]"""

    return """CREATE OR REPLACE FUNCTION full_calc_all_schemes_in_point(integer) RETURNS TEXT ARRAY AS $$
    DECLARE
	    p_id ALIAS FOR $1; all_data TEXT ARRAY; schm INTEGER; schemes INTEGER[];
    BEGIN
	    schemes = (SELECT ARRAY_AGG(t.id) FROM calculation_schemes AS t WHERE point_id = p_id);
	    IF schemes ISNULL THEN schemes = '{}'::INTEGER[]; END IF;
	    FOREACH schm IN ARRAY schemes LOOP
		    all_data = all_data || (SELECT full_calc_to_scheme(schm));
	    END LOOP;
	    RETURN all_data;
    END;
    $$ LANGUAGE plpgsql;"""


def first_day_of_month() -> str:
    """Create or replace function to find first day of ANY month"""

    return """CREATE OR REPLACE FUNCTION first_day_of_months(dt DATE) RETURNS DATE AS $$
        BEGIN
	        RETURN DATE_TRUNC('MONTH', dt)::DATE;
        END;
        $$ LANGUAGE plpgsql;"""


def readings_with_the_nearest_date() -> str:
    """Create or replace function to find records ID with date and device_id nearst readings date"""

    return """CREATE OR REPLACE FUNCTION readings_with_the_nearest_date(dev_id int, date_1 DATE) RETURNS int AS $$
        BEGIN
	        RETURN (SELECT id FROM meter_readings WHERE devices_id = dev_id 
	        ORDER BY ABS(first_day_of_months(date_1::DATE) - read_date) LIMIT 1);
        END;
        $$ LANGUAGE plpgsql;"""


def last_N_first_dates() -> str:
    """Create or replace to get ARRAY with last N months"""

    return """CREATE OR REPLACE FUNCTION last_N_first_dates(N int) RETURNS DATE[] AS $$
        DECLARE all_dates DATE[]; start_date DATE; crt_date DATE; i INT;
        BEGIN
	    start_date = NOW()::DATE;
	    crt_date = start_date;
	    FOR i IN 1..N LOOP
		    all_dates = array_append(all_dates, crt_date);
		    crt_date = crt_date - INTERVAL '1 MONTH';
	    END LOOP;
	    RETURN all_dates;
        END;
        $$ LANGUAGE plpgsql;"""


def last_N_nearest_readings() -> str:
    """Create or replace function to get last N reading to device_id = dev_id"""

    return """CREATE OR REPLACE FUNCTION last_N_nearest_readings(dev_id int, N int) RETURNS INTEGER[] AS $$
        DECLARE
	        dates DATE[];
	        reads_id INTEGER[];
	        dt DATE;
        BEGIN
	        dates = last_N_first_dates(N);
	        FOREACH dt IN ARRAY dates
	        LOOP
		        reads_id  = array_append(reads_id, readings_with_the_nearest_date(dev_id, dt));
	        END LOOP;
	    RETURN reads_id;
        END;
        $$ LANGUAGE plpgsql;"""


def complexes_and_points_not_closed() -> str:
    """Create or replace function to SELECT points not closed ORDER complex and sub_points"""

    return """CREATE OR REPLACE FUNCTION complexes_and_points_not_closed() RETURNS INTEGER[] AS $$
    DECLARE 
	    result INTEGER[];
	    point INTEGER;
	    sub_point INTEGER;
    BEGIN
	    FOR point IN SELECT point_id FROM workspoints WHERE (is_work != 'closed' AND main_point_id ISNULL) ORDER BY point_name LOOP
		    result = array_append(result, point);
		    FOR sub_point IN SELECT point_id FROM workspoints WHERE main_point_id = point ORDER BY point_name LOOP
			    result = array_append(result, sub_point);
		    END LOOP;
	    END LOOP;
	    RETURN result;
    END;
    $$ LANGUAGE plpgsql;"""


def complexes_and_points_all() -> str:
    """Create or replace function to SELECT points not closed ORDER complex and sub_points"""

    return """CREATE OR REPLACE FUNCTION complexes_and_points_all() RETURNS INTEGER[] AS $$
    DECLARE 
	    result INTEGER[];
	    point INTEGER;
	    sub_point INTEGER;
    BEGIN
	    FOR point IN SELECT point_id FROM workspoints WHERE main_point_id ISNULL ORDER BY point_name LOOP
		    result = array_append(result, point);
		    FOR sub_point IN SELECT point_id FROM workspoints WHERE main_point_id = point ORDER BY point_name LOOP
			    result = array_append(result, sub_point);
		    END LOOP;
	    END LOOP;
	    RETURN result;
    END;
    $$ LANGUAGE plpgsql;"""