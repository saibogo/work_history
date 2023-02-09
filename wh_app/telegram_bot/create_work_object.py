"""This class add data to create work in database"""

import datetime

from wh_app.postgresql.database import Database
from wh_app.sql_operations.insert_operations import create_new_work


class CreateWorkObject:
    """This class create new Work Object to next save in Database"""

    __timepattern = '%Y-%m-%d %H:%M:%S'

    def __init__(self, equip_id: str, user_id: str):
        """Init new object"""
        self._user_id = user_id
        self._worktime = datetime.datetime.now()
        self._equip_id = equip_id
        self._malachite_user_id = None
        self._problem = None
        self._work = None
        print('Начата регистрация работ {}'.format(self._worktime.strftime(self.__timepattern)))

    def get_equip_id(self) -> str:
        """Return current Equip_ID"""
        return self._equip_id

    def create_problem(self, problem):
        """Write problem"""
        self._problem = problem

    def create_work(self, work):
        """Write work description"""
        self._work = work

    def is_complete_data(self):
        """True if _problem and _work is string and not empty"""
        return self._problem and\
               self._work and\
               isinstance(self._problem, str) and\
               isinstance(self._work, str) and\
               len(self._problem) > 0 and\
               len(self._work) > 0

    def set_malachite_user_id(self, malachite_user_id):
        """Write malachite worker ID"""
        self._malachite_user_id = malachite_user_id

    def get_user_id(self):
        """Return telegram id"""
        return self._user_id

    def __str__(self):
        """return all elems in object"""
        return 'Equip_id = {}\nProblem = {}\nWork = {}\nDate and Time = {}'.format(self._equip_id,
                                                                                   self._problem,
                                                                                   self._work,
                                                                                   self._worktime.strftime(self.__timepattern))

    def write_in_database(self):
        """Write data in database and clear all elements except equip_id"""
        with Database() as base:
            connection, cursor = base
            create_new_work(cursor, self._equip_id, self._worktime.strftime(self.__timepattern),
                            self._problem, self._work, self._malachite_user_id)
            connection.commit()
            print('{} -- Add new work in database from telegram-bot'.format(datetime.datetime.now().strftime(self.__timepattern)))
            print(self)
            self._worktime = None
            self._malachite_user_id = None
            self._problem = None
            self._work = None