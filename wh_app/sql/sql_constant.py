from wh_app.supporting import functions

functions.info_string(__name__)


sql_consts_dict = {"point_id": "point_id",
                   "point_name": "point_name",
                   "point_address": "point_address",
                   "workspoints": "workspoints",
                   "point": "point",
                   "cast_open_close": "CASE WHEN is_work = true THEN 'Работает' ELSE 'Закрыто' END",
                   "point_working": "is_work = true",
                   "oborudovanie": "oborudovanie",
                   "id": "id",
                   "name": "name",
                   "model": "model",
                   "serial_num": "serial_num",
                   "pre_id": "pre_id",
                   "works_likes": "works_likes",
                   "works": "works",
                   "id_obor": "id_obor",
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
                   "seconds_bindings": "seconds_bindings"}
