class EeskException(Exception):

    def __str__(self):
        return "Данные с сайта Екатербургской Электросетевой Компании недоступны"