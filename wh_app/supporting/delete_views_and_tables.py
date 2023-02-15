"""This module delete all views and all data in workhistory database"""

import getpass

from wh_app.postgresql import database
from wh_app.supporting import functions
from wh_app.supporting import backup_operations

functions.info_string(__name__)

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
               'days_names',
               'performers',
               'works_days',
               'workers',
               'posts',
               'works',
               'oborudovanie',
               'workspoints',
               'orders',
               'customer']


def drop_all_data() -> None:
    """This function delete all table and views in workhistory"""

    answer = input("Вы уверены что хотите уничтожить все таблицы и"
                   " представления в базе данных workhistory? (Y/y - Да)")

    if answer in ['Y', 'y']:
        password = getpass.getpass("Требуется пароль администратора системы:")
        if functions.is_superuser_password(password):
            print('Выполняется очистка текущей базы данных!')
            backup_operations.create_dump()
            with database.Database() as base:
                connection, cursor = base
                for view in VIEWS_LIST:
                    sql = """DROP VIEW IF EXISTS {0}""".format(view)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()

                for table in TABLES_LIST:
                    sql = """DROP TABLE IF EXISTS {0}""".format(table)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()
        else:
            print("Пароль неверный! В доступе отказано!")
    else:
        pass
