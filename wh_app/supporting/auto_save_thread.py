"""This module contain class for Auto Save Procedure"""

import threading
import datetime
import time
from wh_app.supporting.backup_operations import create_dump
from wh_app.config_and_backup import config
from wh_app.supporting import functions

functions.info_string(__name__)


class AutoSaveThread(threading.Thread):
    """This class contains an autosave mechanism"""
    __instance = None

    def __init__(self):
        if not AutoSaveThread.__instance:
            threading.Thread.__init__(self)
            self.start_time = datetime.time(hour=23, minute=55, second=0)
            self.stop_time = datetime.time(hour=23, minute=59, second=59)
            self.database_saved = False
            self.thread_work = True
            AutoSaveThread.__instance = self

    @classmethod
    def get_instance(cls) -> threading.Thread:
        """Method return singletone autosave-object"""
        if not cls.__instance:
            cls.__instance = AutoSaveThread()
        return cls.__instance

    @classmethod
    def get_status(cls) -> bool:
        """Method return current status autosave-object"""
        return cls.get_instance().is_alive()

    def stop(self) -> None:
        """Method stopping autosave-object"""
        self.thread_work = False

    def run(self) -> None:
        while self.thread_work:
            time_now = datetime.datetime.now()
            current_time = datetime.time(hour=time_now.hour,
                                         minute=time_now.minute,
                                         second=time_now.second)
            if not self.database_saved:
                if self.start_time < current_time < self.stop_time:
                    create_dump(config.path_to_dump())
                    self.database_saved = True
            else:
                if current_time < self.start_time:
                    self.database_saved = False

            time.sleep(60)
