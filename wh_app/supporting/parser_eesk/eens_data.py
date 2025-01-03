import requests
from datetime import date, datetime

from wh_app.supporting.parser_eesk.parser_config import url_eens, separated
from wh_app.supporting.parser_eesk.eens_exception import EeensException
from wh_app.supporting import functions
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations.select_operations import get_all_find_patterns

functions.info_string(__name__)


def get_eens_data() -> list:
    """Return List with all correct eens data or raize Exception"""

    date_start = date.today()
    filtred_date = []
    pattern_list = []
    with Database() as base:
        _, cursor = base
        pattern_list = get_all_find_patterns(cursor)
    try:
        print(separated)
        print("Попытка получения данных с {}".format(url_eens))
        json_data = requests.get(url_eens).json()
    except (requests.exceptions.RequestException):
            raise EeensException
    else:
        for phone in json_data:
            phone_date = datetime.strptime(phone['startDate'], "%d.%m.%Y").date()
            if phone_date >= date_start:
                phone_obj = phone['objects']
                phone_street = phone['street']
                for pattern in pattern_list:
                    if pattern.lower() in phone_obj.lower() or pattern.lower() in phone_street.lower():
                        print(phone_date, pattern, phone)
                        filtred_date.append(phone)
                        break

    return filtred_date