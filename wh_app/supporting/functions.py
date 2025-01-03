"""This module contain any supporting functions"""

import hashlib
from datetime import datetime
from typing import Iterable, Any, List, Tuple

from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations.select_operations import get_cold_water_point_info, get_sewerage_point_info,\
    get_electric_point_info, get_heating_point_info, get_hot_water_point_info, user_in_customers, get_hash_to_customer
from wh_app.supporting import metadata


def info_string(name_module):
    """This function printing module-info while module loading"""
    print('Import module {}. Version: {}, Author: {}, License: {}'.format(name_module,
                                                                          metadata.__version__,
                                                                          metadata.__author__,
                                                                          metadata.__license__))
from wh_app.web.universal_html import FIND_REQUEST
from wh_app.web.universal_html import EDIT_CHAR


NOT_VALUES = "Нет данных"
ROLE_SUPERUSER = 'superuser'
ROLE_WORKER = 'worker'
ROLE_CUSTOMER = 'customer'
NO_ROLE = 'no role'
ROLES_IERARH = [ROLE_SUPERUSER, ROLE_WORKER, ROLE_CUSTOMER, NO_ROLE]


def str_to_str_n(old_string: str, max_len: int) -> str:
    """Function return new string, separated \n"""

    tmp = old_string
    chunks = []
    if max_len == 0:
        return str_to_str_n(old_string, 1)
    while len(tmp) >= max_len:
        chunks.append(tmp[:max_len])
        tmp = tmp[max_len:]
    if tmp:
        chunks.append(tmp)
    return '\n'.join(chunks)


def num_to_time_str(num: int) -> str:
    """Function return number in time standart. Example 10 -> 10, 1 -> 01"""

    return str(num) if num > 9 else '0' + str(num)


def full_equip_to_view(equip: list) -> list:
    """Function return list in format correct to view table"""

    len_equip_record = 6
    point, _, name, model, serial, pre_id = range(len_equip_record)
    if len(equip) != len_equip_record:
        result = []
    else:
        result = list(map(str, [equip[point],
                                equip[name],
                                equip[model],
                                equip[serial],
                                equip[pre_id]]))

    return result


def read_all_users() -> dict:
    """Function return dict contain all users in workhistory system"""

    result = {}
    try:
        file_passwords = open(config.path_to_passwords(), mode='r')
        for line in file_passwords:
            user, pass_hash = line.split()
            result[user] = int(pass_hash)
        file_passwords.close()
    except FileNotFoundError:
        print("File {0} not found!".format(config.path_to_passwords()))
    return result


def save_all_users(users: dict) -> None:
    """Save users and hashes in file"""

    file_passwords = open(config.path_to_passwords(), mode='w')
    for user in users:
        file_passwords.write('{0} {1}\n'.format(user, users[user]))
    file_passwords.close()


def create_hash(pattern: str) -> int:
    """Create hash from string"""

    return int(hashlib.sha256(pattern.encode('utf-8')).hexdigest(), 16)


def is_valid_password(password: str) -> bool:
    """Function compare password and passwords hashes"""

    return create_hash(password) in read_all_users().values()


def is_valid_customers_password(password: str, hash_in_db: str) -> bool:
    """Function compare password and passwords hashes from customer"""
    return str(create_hash(password)) == str(hash_in_db)


def is_valid_customer(login: str, password: str) -> bool:
    """Function find user with login and password in Database"""
    with Database() as base:
        _, cursor = base
        if user_in_customers(cursor, login):
            hash = get_hash_to_customer(cursor, login)
            return is_valid_customers_password(password, hash)
        else:
            return False


def is_superuser_password(password: str) -> bool:
    """Function compare password and superuser password hash"""

    try:
        return read_all_users()["saibogo"] == create_hash(password)
    except KeyError:
        return False


def is_login_and_password_correct(login: str, password: str) -> bool:
    """Function examine login and password pair"""

    try:
        return read_all_users()[login] == create_hash(password)
    except KeyError:
        return False


def form_to_data(form: dict) -> dict:
    """Function create dict contain all data in form"""

    fields = [k for k in form]
    values = [form[k] for k in form]
    values = list(map(lambda elem: elem.replace('"', '\"').replace("'", "\""), values))
    data = dict(zip(fields, values))
    if FIND_REQUEST in data.keys():
        data[FIND_REQUEST] = data[FIND_REQUEST].replace(" ", '')
        if data[FIND_REQUEST] == '' or data[FIND_REQUEST] == ' ':
            data[FIND_REQUEST] = '*'
    return data


def date_to_browser() -> str:
    """Return current datetime string to browser format"""

    curr_datetime = datetime.now()
    year = str(curr_datetime.year)
    month = str(curr_datetime.month) if curr_datetime.month > 9 else '0' + str(curr_datetime.month)
    day = str(curr_datetime.day) if curr_datetime.day > 9 else '0' + str(curr_datetime.day)
    hour = str(curr_datetime.hour) if curr_datetime.hour > 9 else '0' + str(curr_datetime.hour)
    minute = str(curr_datetime.minute) if curr_datetime.minute > 9 \
        else '0' + str(curr_datetime.minute)
    return "{}-{}-{}T{}:{}".format(year, month, day, hour, minute)


def works_table_add_new_performer(works: list) -> list:
    """Add to all works string link ADD-Performer"""

    new_works = []

    for work in works:
        new_works.append([])
        for elem in work:
            new_works[-1].append(str(elem))
        if work:
            new_works[-1][-1] += ('<a href="/add-performer-to-work/{0}" title="Добавить исполнителя">+</a>'
                                  ' <a href="/remove-performer-to-work/{0}" title="Удалить исполнителя">-</a> '.
                                  format(new_works[-1][0]))

    return new_works


def works_table_add_edit(works: list) -> list:
    """Add to all works string EDIT-link"""

    new_works = []
    for work in works:
        new_works.append([str(elem) for elem in work] +
                         ['<a href="/work-edit/{0}"> {1} </a>'.format(work[0], EDIT_CHAR)])
    return new_works


def list_of_pages(all_records: list) -> list:
    """Return list any elem is number page in html-view"""

    result = [i + 1 for i in range(len(all_records) // config.max_records_in_page())]
    if len(all_records) % config.max_records_in_page() != 0:
        result.append(len(result) + 1)
    return result if all_records else [1]


def get_first_non_list(collection: Iterable) -> Any:
    """Return first element non-collection"""

    try:
        elem = collection[0]
        return get_first_non_list(elem)
    except TypeError:
        return collection


def get_technical_info(point_id: int) -> List[Tuple]:
    """Return all techncal information from workspoint [electric, cold_water, hot_water, heating, sewerage]"""
    def if_tech_list_empthy(lst: list) -> list:
        """Replace data if data not found"""

        if not lst:
            return [NOT_VALUES] * 4
        else:
            return lst[0]

    with Database() as base:
        _, cursor = base
        result = [get_electric_point_info(cursor, str(point_id)),
                  get_cold_water_point_info(cursor, str(point_id)),
                  get_hot_water_point_info(cursor, str(point_id)),
                  get_heating_point_info(cursor, str(point_id)),
                  get_sewerage_point_info(cursor, str(point_id))]
        for i in range(len(result)):
            result[i] = if_tech_list_empthy(result[i])
        return result


def list_to_numer_list(lst: list) -> List[Tuple]:
    """Create numer list. Example: [a, b, c] -> [(1, a), (2, b), (3, c)]"""
    result = list()
    for i in range(len(lst)):
        result.append((i + 1, lst[i]))
    return result


info_string(__name__)
