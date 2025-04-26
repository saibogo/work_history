from wh_app.supporting import functions
from wh_app.sql.select_sql.select_sql import log_decorator

functions.info_string(__name__)


@log_decorator
def sql_proc_delete_not_active_sessions() -> str:
    """Create or replace procedure to delete all session who have status = NOT ACTIVE"""
    query = """CREATE OR REPLACE PROCEDURE delete_not_active_sessions()
    LANGUAGE SQL AS $$
        DELETE FROM sessions_hashs WHERE is_active = false;
    $$;"""
    return query


@log_decorator
def sql_proc_update_all_sessions_older_48h() -> str:
    """Create or replace procedure to find and update all session where age > 48 hours"""
    query = """CREATE OR REPLACE PROCEDURE update_old_sessions()
        LANGUAGE SQL AS $$
            UPDATE sessions_hashs SET is_active = false WHERE NOW() -  start_time > INTERVAL '2 days';
        $$;"""
    return query


@log_decorator
def sql_proc_vacuum_tables() -> str:
    """Create or replace procedure to find tables with dead strings"""

    query = """CREATE OR REPLACE PROCEDURE vacuum_tables() 
    LANGUAGE plpgsql AS $$
    DECLARE 
	tbl RECORD; 
	need_vacuum BOOLEAN;
	msg TEXT;
	BEGIN
	need_vacuum = False;
	RAISE INFO 'Поиск и таблиц с мертвыми строками...';
	FOR tbl in SELECT schemaname || '.' || relname AS tablename FROM pg_stat_all_tables WHERE (schemaname = 'public' AND n_dead_tup > 0)
	LOOP
		RAISE INFO 'Необходима очистка таблицы %', tbl.tablename;
		need_vacuum = True;
	END LOOP;
    CASE need_vacuum
		WHEN True THEN msg := 'Рекомендуется выполнить vacuumdb your_database_name или VACUUM для каждой таблицы';
		ELSE msg := 'Очистка не требуется';
	END CASE;
	RAISE INFO '%', msg;
	END;
	$$;"""
    return query