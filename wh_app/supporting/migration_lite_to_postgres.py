"""This module contain subprogram execute migration LiteSQL database to Postgres database"""

import sqlite3

import psycopg2

from wh_app.config_and_backup import config
from wh_app.supporting import functions


functions.info_string(__name__)

CON_POSGRESQL = psycopg2.connect(database=config.database_name,
                                 user=config.user_name,
                                 password=config.user_password,
                                 host=config.database_host,
                                 port=config.database_port)

CON_LITE = sqlite3.connect(config.database_name)

CUR_POSGRESQL = CON_POSGRESQL.cursor()
CUR_LITE = CON_LITE.cursor()

CUR_POSGRESQL.execute('DELETE FROM works')
CUR_POSGRESQL.execute('DELETE FROM oborudovanie')
CUR_POSGRESQL.execute('DELETE FROM workspoints')
CON_POSGRESQL.commit()

CUR_LITE.execute('SELECT * FROM workspoints')
ROWS = CUR_LITE.fetchall()
for row in ROWS:
    sql_ins = 'INSERT INTO workspoints VALUES ' + str(row)
    CUR_POSGRESQL.execute(sql_ins)

CON_POSGRESQL.commit()

CUR_LITE.execute('SELECT * FROM oborudovanie')
for row in CUR_LITE.fetchall():
    sql_ins = 'INSERT INTO oborudovanie VALUES ' + str(row)
    sql_ins = sql_ins.replace('None', str(row[0]))
    CUR_POSGRESQL.execute(sql_ins)

CON_POSGRESQL.commit()


CUR_LITE.execute('SELECT * FROM works')
for row in CUR_LITE.fetchall():
    sql_ins = 'INSERT INTO works VALUES ('
    for elem in row:
        tmp = elem.replace("'", "") if type(elem) is str else elem
        sql_ins = sql_ins  + ("'" + tmp + "'" if type(tmp) is str else str(tmp)) + ', '
    sql_ins = sql_ins[:len(sql_ins) - 2] + ')'
    CUR_POSGRESQL.execute(sql_ins)

CON_POSGRESQL.commit()

CON_POSGRESQL.close()
CON_LITE.close()
