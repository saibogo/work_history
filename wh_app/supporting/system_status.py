"""This module implement status-operations from program components"""

import psycopg2

from wh_app.postgresql.database import Database
from wh_app.supporting import functions
from wh_app.supporting import stop_start_web
from wh_app.supporting.auto_save_thread import AutoSaveThread

functions.info_string(__name__)


class SystemStatus:
    """This class contain base information from components workhistory"""

    @classmethod
    def database_server_is_work(cls) -> bool:
        """Return database status"""
        try:
            with Database() as base:
                _, _ = base
            return True
        except psycopg2.ConnectionException:
            return False

    @classmethod
    def flask_is_work(cls) -> bool:
        """Return web-server status"""
        return stop_start_web.status_server()

    @classmethod
    def autosave_database_is_work(cls) -> bool:
        """Return autosave-procedure status"""
        return AutoSaveThread.get_status()

    @classmethod
    def get_status(cls) -> dict:
        """Return full system-status"""
        result = {"Сервер PostgreSql":
                      "Доступен" if cls.database_server_is_work() else "Не доступен",
                  "Веб-сервер":
                      "Работает" if cls.flask_is_work() else "Не работает",
                  "Автосохранение базы данных":
                      "Включено" if cls.autosave_database_is_work() else "Выключено",
                  "Версия ПО": functions.metadata.__version__}
        return result
