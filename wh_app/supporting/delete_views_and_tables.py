"""This module delete all views and all data in workhistory database"""

import getpass

from wh_app.postgresql import database
from wh_app.supporting import functions
from wh_app.supporting import backup_operations

functions.info_string(__name__)

TYPES = ['equips_meta_type', 'meter_type', 'order_status', 'point_status', 'work_day_type', 'worker_status']

VIEWS_LIST = ['all_workers',
              'firsts_bindings',
              'seconds_bindings',
              'statistic',
              'works_from_worker',
              'works_likes']


TABLES_LIST = ['electric',
               'heating',
               'hot_water',
               'cold_water',
               'sewerage',
               'bindings',
               'bugzilla',
               'performers',
               'works_days',
               'chats',
               'calculation_schemes', 'meter_readings', 'points_meter_devices', 'meter_devices',
               'sessions_hashs', 'workers_schedule',
               'find_patterns',
               'works',
               'oborudovanie', 'equip_details', 'equip_sub_types',
               'orders', 'customer',
               'workers',
               'posts',
               'workspoints']


PROCEDURES_LIST = ['update_old_sessions', 'delete_not_active_sessions', 'vacuum_tables']

FUNCTIONS_LIST = ['all_works_from_equip(eid integer)', 'average_from_last_readings(integer)',
                  'bug_status_to_string(st boolean)', 'bug_status_to_string(st order_status)',
                  'complexes_and_points_all()', 'complexes_and_points_not_closed()',
                  'date_to_date_and_day_string(d date)',
                  'first_day_of_months(dt date)', 'full_calc_all_schemes_in_point(integer)', 'full_calc_to_scheme(integer)',
                  'last_day_date()', 'last_month_date()', 'last_n_first_dates(n integer)',
                  'last_n_nearest_readings(dev_id integer, n integer)', 'last_week_date()', 'last_year_date()',
                  'meter_type_to_string(m meter_type)', 'point_status_to_string(st boolean)', 'point_status_to_string(st point_status)',
                  'readings_with_the_nearest_date(dev_id integer, date_1 date)',
                  'sum_pu_in_scheme(integer)',
                  'total_last_month(integer)',
                  'units_of_measure_string(m meter_type)',
                  'work_day_type_to_string(st work_day_type)',
                  'worker_status_to_string(st worker_status)']


def drop_all_data() -> None:
    """This function delete all table and views in workhistory"""

    answer = input("Вы уверены что хотите уничтожить все таблицы и"
                   " представления в базе данных workhistory? (Y/y - Да)")

    if answer in ['Y', 'y']:
        password = getpass.getpass("Требуется пароль администратора системы:")
        if functions.is_superuser_password_cli(password):
            print('Выполняется очистка текущей базы данных!')
            answer = input("Создать дамп текущей базы данных?(Y/y - Создать)")
            if answer in ['Y', 'y']:
                print("Создаем:")
                backup_operations.create_dump()
            with database.Database() as base:
                connection, cursor = base

                for view in VIEWS_LIST:
                    sql = "DROP VIEW IF EXISTS {0}".format(view)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()
                
                for table in TABLES_LIST:
                    sql = "DROP TABLE IF EXISTS {0}".format(table)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()

                for procedure in PROCEDURES_LIST:
                    sql = "DROP PROCEDURE IF EXISTS {0}".format(procedure)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()

                for funct in FUNCTIONS_LIST:
                    sql = "DROP FUNCTION IF EXISTS {0}".format(funct)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()

                for t in TYPES:
                    sql = "DROP TYPE IF EXISTS {0}".format(t)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()

        else:
            print("Пароль неверный! В доступе отказано!")
    else:
        pass
