"""This module contain class Auto load Configuration"""

import threading
import datetime
import time

from wh_app.config_and_backup.config import load_config
from wh_app.supporting import functions

functions.info_string(__name__)


class AutoLoadConfig(threading.Thread):
    """This class contains an autoloader mechanism"""
    __instance = None
    __timeinterval = 5 * 60  # in seconds

    def __init__(self):
        if not AutoLoadConfig.__instance:
            threading.Thread.__init__(self)
            self.last_update = time.time()
            self.thread_work = True
            AutoLoadConfig.__instance = self

    @classmethod
    def get_instance(cls) -> threading.Thread:
        """Method return singletone autoload-object"""
        if not cls.__instance:
            cls.__instance = AutoLoadConfig()
        return cls.__instance

    @classmethod
    def get_status(cls) -> bool:
        """Method return current status autoload-object"""
        return cls.get_instance().is_alive()

    def stop(self) -> None:
        """Method stopping autoload-object"""
        self.thread_work = False

    def run(self) -> None:
        while self.thread_work:
            time_now = time.time()
            if time_now - self.last_update >= AutoLoadConfig.__timeinterval:
                load_config()
                self.last_update = time.time()

            time.sleep(60)