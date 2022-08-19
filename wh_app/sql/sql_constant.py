"""This module contain all names from database"""

from wh_app.supporting import functions

functions.info_string(__name__)

any_consts = {"id": "id",
              "statistic": "statistic",
              "firsts_bindings": "firsts_bindings",
              "seconds_bindings": "seconds_bindings",
              "bindings": "bindings",
              "is_main": "is_main",
              "last_date": "last_date",
              "tmp": "tmp",
              "phone_number": "phone_number",
              "bugzilla": "bugzilla",
              "status": "status",
              "customer_table": "customer",
              "electric": "electric",
              "cold_water": "cold_water",
              "hot_water": "hot_water",
              "heating": "heating",
              "sewerage": "sewerage"
              }

workers_const = {"all_workers": "all_workers",
                 "performers": "performers",
                 "worker_id": "worker_id",
                 "workers": "workers",
                 "alter_workers": "alter_workers",
                 "sub_name": "sub_name",
                 "wd": "wd",
                 "works_days": "works_days",
                 "posts": "posts",
                 "post_name": "post_name",
                 "post_id": "post_id",
                 "case": "case"
                 }

works_const = {"works_likes": "works_likes",
               "works": "works",
               "date": "date",
               "problem": "problem",
               "result": "result",
               "works_from_worker": "works_from_worker",
               "work_id": "work_id",
               "works_count": "works_count"
               }

equip_const = {"oborudovanie": "oborudovanie",
               "name": "name",
               "model": "model",
               "serial_num": "serial_num",
               "pre_id": "pre_id",
               "equips_count": "equips_count",
               "id_obor": "id_obor",
               }

replace_consts = {"cast_open_close": "CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END",
                  "point_working": "is_work = true",
                  "select_main_binding": "SELECT sub_name FROM workers WHERE" +
                                         " workers.id = bindings.worker_id " +
                                         "AND bindings.is_main = true",
                  "worker_status": "CASE WHEN workers.is_work=true THEN 'Работает'" +
                                   " ELSE 'Уволен' END",
                  "bug_in_work": "CASE WHEN status = true THEN 'В работе' ELSE 'Исправлено' END"
                  }

point_consts = {"point_id": "point_id",
                "point_name": "point_name",
                "point_address": "point_address",
                "workspoints": "workspoints",
                "point": "point",
                "name_point": "name_point",
                "is_work": "is_work",
                "treaty": "treaty",
                "resume": "resume"
                }

any_consts.update(point_consts)
any_consts.update(replace_consts)
any_consts.update(equip_const)
any_consts.update(works_const)
any_consts.update(workers_const)
sql_consts_dict = any_consts
