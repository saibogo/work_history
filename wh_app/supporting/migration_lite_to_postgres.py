import sqlite3

import psycopg2

from wh_app.config_and_backup import config
from wh_app.supporting import functions

# This program execute migration LiteSQL database to Postgres database

functions.info_string(__name__)

con_postgres = psycopg2.connect(
  database=config.database_name,
  user=config.user_name,
  password=config.user_password,
  host=config.database_host,
  port=config.database_port
)

con_lite = sqlite3.connect(config.database_name)

cur_postgres = con_postgres.cursor()
cur_lite = con_lite.cursor()

cur_postgres.execute('DELETE FROM works')
cur_postgres.execute('DELETE FROM oborudovanie')
cur_postgres.execute('DELETE FROM workspoints')
con_postgres.commit()

cur_lite.execute('SELECT * FROM workspoints')
rows = cur_lite.fetchall()
for row in rows:
    sql_ins = 'INSERT INTO workspoints VALUES ' + str(row)
    cur_postgres.execute(sql_ins)

con_postgres.commit()

cur_lite.execute('SELECT * FROM oborudovanie')
for row in cur_lite.fetchall():
    sql_ins = 'INSERT INTO oborudovanie VALUES ' + str(row)
    sql_ins = sql_ins.replace('None', str(row[0]))
    cur_postgres.execute(sql_ins)

con_postgres.commit()


cur_lite.execute('SELECT * FROM works')
for row in cur_lite.fetchall():
    sql_ins = 'INSERT INTO works VALUES ('
    for elem in row:
        tmp = elem.replace("'", "") if type(elem) is str else elem
        sql_ins = sql_ins  + ("'" + tmp + "'" if type(tmp) is str else str(tmp)) + ', '
    sql_ins = sql_ins[:len(sql_ins) - 2] + ')'
    cur_postgres.execute(sql_ins)

con_postgres.commit()


con_postgres.close()
con_lite.close()