"""This module for operation Get Status Bot"""


class BotStateMachine(object):
    """Class singleton. Contain information Bot status"""

    __instance = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = BotStateMachine()
            cls.__instance._status = False
        return cls.__instance

    def set_on_status(self):
        self._status = True

    def set_off_status(self):
        self._status = False

    def get_status(self) -> bool:
        if not self._status:
            self.set_off_status()
        return self._status

