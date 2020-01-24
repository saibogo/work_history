from wh_app.supporting import functions

functions.info_string(__name__)

any_consts = {
    "id": "id",
    "works_likes": "works_likes",
    "works": "works",
    "date": "date",
    "problem": "problem",
    "result": "result",
    "statistic": "statistic",
    "all_workers": "all_workers",
    "works_from_worker": "works_from_worker",
    "performers": "performers",
    "worker_id": "worker_id",
    "work_id": "work_id",
    "firsts_bindings": "firsts_bindings",
    "seconds_bindings": "seconds_bindings",
    "workers": "workers",
    "alter_workers": "alter_workers",
    "sub_name": "sub_name",
    "bindings": "bindings",
    "is_main": "is_main",
    "wd": "wd",
    "works_days": "works_days",
    "works_count": "works_count",
    "last_date": "last_date",
    "tmp": "tmp",
    "phone_number": "phone_number",
    "posts": "posts",
    "post_name": "post_name",
    "post_id": "post_id"}

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
                  "select_main_binding": "SELECT sub_name FROM workers WHERE workers.id = bindings.worker_id "
                                         "AND bindings.is_main = true",
                  "worker_status": "CASE WHEN workers.is_work=true THEN 'Работает' ELSE 'Уволен' END"
                  }

point_consts = {"point_id": "point_id",
                "point_name": "point_name",
                "point_address": "point_address",
                "workspoints": "workspoints",
                "point": "point",
                "name_point": "name_point"}

any_consts.update(point_consts)
any_consts.update(replace_consts)
any_consts.update(equip_const)
sql_consts_dict = any_consts
