__author__ = "Andrey Gleykh"
__license__ = "GPL"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"


import psycopg2
import sqlite3
import config

# This program execute migration LiteSQL database to Postgres database

con_postgres = psycopg2.connect(
  database="workhistory",
  user="saibogo",
  password="begemot100",
  host="127.0.0.1",
  port="5432"
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