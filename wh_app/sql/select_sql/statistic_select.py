"""This module contain all SELECT to STATISTIC"""

from wh_app.sql.sql_constant import sql_consts_dict

from wh_app.sql.select_sql.points_select import log_decorator


@log_decorator
def sql_select_statistic() -> str:
    """Return SQL-string contain query to statistic from database records"""

    return """SELECT * FROM %(statistic)s""" % sql_consts_dict


@log_decorator
def sql_select_size_database() -> str:
    """Return SQL-string contain query to size database workhistory"""

    return """SELECT pg_size_pretty(pg_database_size(current_database()))"""


@log_decorator
def sql_select_top_workers() -> str:
    """Return SQL-string, to  select TOP-10 workers"""

    query = ("""SELECT %(workers)s.%(id)s, %(workers)s.%(name)s, %(workers)s.%(sub_name)s, COUNT(%(work_id)s) AS all_works, """ +
             """ (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s JOIN %(performers)s ON %(performers)s.%(worker_id)s = %(workers)s.%(id)s""" +
             """ AND %(works)s.%(id)s = %(performers)s.%(work_id)s WHERE %(works)s.%(date)s::DATE >= last_year_date()) """ +
             """ AS last_year, (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s JOIN %(performers)s ON """ +
             """ %(performers)s.%(worker_id)s = %(workers)s.%(id)s AND %(works)s.%(id)s = %(performers)s.%(work_id)s WHERE """ +
             """ %(works)s.%(date)s::DATE >= last_month_date()) AS last_month, (SELECT COUNT(%(works)s.%(id)s) """ +
             """FROM %(works)s JOIN %(performers)s ON %(performers)s.%(worker_id)s = %(workers)s.%(id)s AND %(works)s.%(id)s = """ +
             """ %(performers)s.%(work_id)s WHERE %(works)s.%(date)s::DATE >= last_week_date()) AS last_week FROM """ +
             """ %(workers)s JOIN %(performers)s ON %(workers)s.%(id)s = %(performers)s.%(worker_id)s """ +
             """GROUP BY %(workers)s.%(id)s ORDER BY all_works DESC""") %sql_consts_dict

    return query


@log_decorator
def sql_counter(sql_query: str) -> str:
    """Return SELECT likes SELECT COUNT..."""

    return """SELECT COUNT (*) FROM ({0}) AS foo""".format(sql_query)


@log_decorator
def sql_select_count_uniques_dates() -> str:
    """Return SQL-string contain query to count unique dates in works table"""

    return """SELECT  COUNT(DISTINCT DATE(%(date)s)) FROM %(works)s""" % sql_consts_dict


@log_decorator
def sql_select_top_works() -> str:
    """Return query contain SELECT-strintg to 10 first string in equip -> sum works"""

    query = ("""SELECT %(oborudovanie)s.%(id)s, %(workspoints)s.%(point_name)s, %(name)s,  COUNT(%(works)s.%(id)s) AS
     all_works, (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s WHERE %(works)s.%(date)s::DATE >= last_year_date() 
     AND %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s) AS lastyear, (SELECT COUNT(%(works)s.%(id)s) FROM %(works)s
      WHERE %(works)s.%(date)s::DATE >= last_month_date() AND %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s) 
      AS lastmonth FROM %(oborudovanie)s JOIN %(works)s ON %(works)s.%(id_obor)s = %(oborudovanie)s.%(id)s JOIN
       %(workspoints)s ON %(workspoints)s.%(point_id)s = %(oborudovanie)s.%(point_id)s GROUP BY 
       %(workspoints)s.%(point_name)s, %(oborudovanie)s.%(id)s ORDER BY all_works DESC LIMIT 10""") % sql_consts_dict

    return query