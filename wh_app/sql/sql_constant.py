"""This module contain all names from database"""


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
              "date_start": "date_start",
              "date_close": "date_close",
              "status": "status",
              "customer_table": "customer",
              "electric": "electric",
              "cold_water": "cold_water",
              "hot_water": "hot_water",
              "heating": "heating",
              "sewerage": "sewerage",
              "case": "case"
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
                 "case": "case",
                 "emloyee_date": "emloyee_date",
                 "dismissal_date": "dismissal_date"
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

replace_consts = {"cast_open_close": "point_status_to_string(is_work)",
                  "point_working": "is_work = true",
                  "worker_is_work": "workers.status != 'fired'",
                  "select_main_binding": "SELECT sub_name FROM workers WHERE" +
                                         " workers.id = bindings.worker_id " +
                                         "AND bindings.is_main = true",
                  "worker_status": 'worker_status_to_string(workers.status) AS "case"',
                  "bug_in_work": "bug_status_to_string(status)"
                  }

point_consts = {"point_id": "point_id",
                "point_name": "point_name",
                "point_address": "point_address",
                "workspoints": "workspoints",
                "point": "point",
                "name_point": "name_point",
                "is_work": "is_work",
                "treaty": "treaty",
                "resume": "resume",
                "deleted": "deleted"
                }

order_conts = {"customer": "customer",
               "full_name": "full_name",
               "orders": "orders",
               "closed_date": "closed_date",
               "customer_id": "customer_id"}

any_consts.update(point_consts)
any_consts.update(replace_consts)
any_consts.update(equip_const)
any_consts.update(works_const)
any_consts.update(workers_const)
any_consts.update(order_conts)
sql_consts_dict = any_consts

tech_tables = {'electric': "electric", "cold-water": "cold_water", "hot-water": "hot_water",
              "heating": "heating", "sewerage": "sewerage"}
