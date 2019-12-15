from wh_app.postgresql import database

views_list = ['all_workers',
              'firsts_bindings',
              'seconds_bindings',
              'statistic',
              'works_from_worker',
              'works_likes'];


tables_list = ['bindings',
               'days_names',
               'performers',
               'works_days',
               'workers',
               'posts',
               'works',
               'oborudovanie',
               'workspoints']


def drop_all_data() -> None:
    """This function delete all table and views in workhistory"""

    answer = input("Вы уверены что хотите уничтожить все таблицы и"
                   " представления в базе данных workhistory? (Y/y - Да)")

    if answer in ['Y', 'y']:
        with database.Database() as base:
            connection, cursor = base
            for view in views_list:
                sql = """DROP VIEW IF EXISTS {0}""".format(view)
                cursor.execute(sql)
                connection.commit()

            for table in tables_list:
                sql = """DROP TABLE IF EXISTS {0}""".format(table)
                cursor.execute(sql)
                connection.commit()
    else:
        pass