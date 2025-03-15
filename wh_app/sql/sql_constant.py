"""This module contain all names from database to replace in %()s expressions"""


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
              "case": "case",
              "chats": "chats",
              "chat_id": "chat_id",
              "acs_read": "acs_read",
              "acs_write": "acs_write",
              "find_patterns": "find_patterns",
              "day_type": "day_type",
              "meter_type": "meter_type",
              "device_id": "device_id",
              "is_active": "is_active",
              "device_type": "device_type",
              "start_date": "start_date",
              "stop_date": "stop_date",
              "verification_date": "verification_date",
              "points_meter_devices": "points_meter_devices",
              "meter_devices": "meter_devices",
              "meter_readings": "meter_readings",
              "devices_id": "devices_id",
              "read_date": "read_date",
              "reading": "reading",
              "Kt": "Kt",
              "is_inner": "is_inner",
              "comment": "comment",
              "positive_calc": "positive_calc",
              "calculation_schemes": "calculation_schemes",
              "devices_type": "devices_type",
              "negative_calc": "negative_calc"
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
                 "dismissal_date": "dismissal_date",
                 "work_date": "work_date",
                 "workers_schedule": "workers_schedule",
                 "is_blocked": "is_blocked"
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

#point 41 it's list of decommissioned equipment

replace_consts = {"cast_open_close": "point_status_to_string(is_work)",
                  "point_working": "is_work = 'in_work'::point_status OR is_work = 'reconstruction'::point_status",
                  "worker_is_work": "workers.status != 'fired'",
                  "select_main_binding": "SELECT sub_name FROM workers WHERE" +
                                         " workers.id = bindings.worker_id " +
                                         "AND bindings.is_main = true",
                  "worker_status": 'worker_status_to_string(workers.status) AS "case"',
                  "bug_in_work": "bug_status_to_string(status)",
                  "not_find_in_point": "41"
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
                "deleted": "deleted",
                "point_status": "point_status"
                }

order_conts = {"customer": "customer",
               "full_name": "full_name",
               "orders": "orders",
               "closed_date": "closed_date",
               "customer_id": "customer_id",
               "order_status": "order_status",
               "comment": "comment",
               "hash_pass": "hash_pass",
               "description": "description"}

any_consts.update(point_consts)
any_consts.update(replace_consts)
any_consts.update(equip_const)
any_consts.update(works_const)
any_consts.update(workers_const)
any_consts.update(order_conts)
sql_consts_dict = any_consts

tech_tables = {'electric': "electric", "cold-water": "cold_water", "hot-water": "hot_water",
              "heating": "heating", "sewerage": "sewerage"}
