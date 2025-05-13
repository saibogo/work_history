"""This module delete all views and all data in workhistory database"""

import getpass

from wh_app.postgresql import database
from wh_app.supporting import functions
from wh_app.supporting import backup_operations

functions.info_string(__name__)

TYPES = ['worker_status', 'order_status']

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
        if functions.is_superuser_password_cli(password):
            print('Выполняется очистка текущей базы данных!')
            answer = input("Создать дамп текущей базы данных?(Y/y - Создать)")
            if answer in ['Y', 'y']:
                print("Создаем:")
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

                for t in TYPES:
                    sql = """DROP TYPE IF EXISTS {0}""".format(t)
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()
        else:
            print("Пароль неверный! В доступе отказано!")
    else:
        pass
