import datetime
from wh_app.postgresql.database import Database
from wh_app.sql_operations.insert_operations import create_new_equip


class CreateEquipObject:
    """This class create new Equip Object to next save in Database"""

    __timepattern = '%Y-%m-%d %H:%M:%S'

    def __init__(self, point_id: str, user_id: str):
        """Create new equip-object to save in database"""
        self._user_id = user_id
        self.point_id = point_id
        self.equip_name = None
        self.model = 'not model'
        self.serial = 'not number'
        self.pre_id = ''
        print('Начата регистрация оборудования {}'.format(datetime.datetime.now().strftime(self.__timepattern)))

    def get_point_id(self) -> str:
        """Return point_id"""
        return self.point_id

    def get_user_id(self):
        """Return telegram id"""
        return self._user_id

    def create_name(self, name: str):
        """Name from new equip"""
        self.equip_name = name

    def create_model(self, model: str):
        """Model from new equip"""
        self.model = model

    def create_serial(self, serial: str):
        """Serial num from new equip"""
        self.serial = serial

    def create_pre_id(self, pre_id: str):
        """Pre Equip_ID from new equip"""

    def is_complete_data(self) -> bool:
        """All fields in record created"""
        return self.equip_name and isinstance(self.equip_name, str) and len(self.equip_name) > 0

    def write_in_database(self):
        """Create new record in database"""
        if self.is_complete_data():
            with Database() as base:
                connection, cursor = base
                create_new_equip(cursor, self.point_id,
                                 self.equip_name, self.model, self.serial, self.pre_id)
                connection.commit()
                print('Оборудование занесено в базу данных!\n{}'.format(self))
                self.equip_name = None
                self.model = 'not model'
                self.serial = 'not number'
                self.pre_id = ''
        else:
            pass

    def __str__(self) -> str:
        """Return string, contain all fields object"""
        return "Point_ID: {}\nName: {}\nModel: {}\nSerial Num: {}\nPre_ID: {}".format(self.point_id,
                                                                                      self.equip_name,
                                                                                      self.model,
                                                                                      self.serial,
                                                                                      self.pre_id)