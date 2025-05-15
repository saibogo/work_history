"""This module contain any supporting functions"""

import hashlib
from datetime import datetime
from typing import Iterable, Any, List, Tuple
from flask import session

from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations.select_operations import get_cold_water_point_info, get_sewerage_point_info,\
    get_electric_point_info, get_heating_point_info, get_hot_water_point_info, user_in_customers, get_hash_to_customer,\
    get_last_id_in_sessions, get_session_hash_from_id
from wh_app.sql_operations.insert_operation.insert_operations import insert_new_session_in_sessions
from wh_app.sql_operations.update_operations.update_operations import update_set_session_inactive
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
NO_ROLE = 'no_role'
ROLES_IERARH = [ROLE_SUPERUSER, ROLE_WORKER, ROLE_CUSTOMER, NO_ROLE]

SESSION_KEYS_TO_HASH = ['access_is_allowed', 'login', 'role', 'time_login']
FULL_SESSIONS_KEYS = ['session_id', 'theme_number', 'session_hash']


def create_session_hash() -> int:
    """Create hash-sum to current session"""

    return create_hash(''.join([str(session[elem]) for elem in SESSION_KEYS_TO_HASH]))


def add_new_session_in_db() -> None:
    """Generate session_id, session_hash and insert into database"""

    new_hash = create_session_hash()
    with Database() as base:
        connection, cursor = base
        insert_new_session_in_sessions(cursor, str(new_hash))
        connection.commit()
        session_id = get_last_id_in_sessions(cursor)
        session['session_id'] = session_id
        session['session_hash'] = new_hash
        session.modified = True


def close_session() -> None:
    """close session in database and in browser"""
    with Database() as base:
        connection, cursor = base
        session_id = session['session_id']
        update_set_session_inactive(cursor, session_id)
        connection.commit()
        session['session_id'] = 0
        session['session_hash'] = 0
        session.modified = True


def current_session_is_valid() -> bool:
    """True if session_hash and hash in database =="""

    with Database() as base:
        _, cursor = base
        try:
            session_id = session['session_id']
            current_hash = session['session_hash']
            return str(current_hash) == get_session_hash_from_id(cursor, session_id)
        except IndexError:
            print('Session  with ID = {} not valid or closed'.format(session_id))
            return False


def get_role_description(role: str) -> str:
    """Return role description in russian lang"""
    if role == NO_ROLE:
        result = "Без роли(Возможен только частичный просмотр)"
    elif role == ROLE_CUSTOMER:
        result = "Заказчик(Возможен частичный просмотр и ограниченный ввод)"
    elif role == ROLE_WORKER:
        result = "Сотрудник техслужбы(Доступно большинство функций системы)"
    elif role == ROLE_SUPERUSER:
        result = "Администратор системы(Доступны все функции)"
    else:
        result = "Роль не определена"
    return result


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
    """Function return dict contain all users in workhistory system liked {user_name: hash_of_password}"""

    result = {}
    try:
        file_passwords = open(config.path_to_passwords(), mode='r')
        for line in file_passwords:
            user, pass_hash, role = line.split()
            result[user] = int(pass_hash)
        file_passwords.close()
    except FileNotFoundError:
        print("File {0} not found!".format(config.path_to_passwords()))
    return result


def save_all_users(users: dict) -> None:
    """Save users and hashes in file. User dict liked {'user_name': [hash, 'user_role']}"""

    file_passwords = open(config.path_to_passwords(), mode='w')
    for user in users:
        file_passwords.write('{0} {1} {2}\n'.format(user, users[user][0], users[user][1]))
    file_passwords.close()


def add_record_in_login_log(user: str, role: str, ip: str) -> None:
    """Save datetime, username and role for login in system"""

    log_file = open(config.path_to_login_log(), mode='a')
    log_file.write('{}\n'.format('=' * 10))
    log_file.write('Login user {0} with user role = {1} in {2} from IP = {3}\n'.format(user, role, datetime.now().isoformat(), ip))
    log_file.close()


def add_record_in_logout_log(user: str, ip: str) -> None:
    """Save datetime and username for logout system"""
    log_file = open(config.path_to_login_log(), mode='a')
    log_file.write('{}\n'.format('=' * 10))
    log_file.write('Logout user {0} in {1} from IP = {2}\n'.format(user, datetime.now().isoformat(), ip))
    log_file.close()


def create_hash(pattern: str) -> int:
    """Create hash from string"""

    return int(hashlib.sha256(pattern.encode('utf-8')).hexdigest(), 16)


def is_valid_password(password: str) -> bool:
    """Function compare password and passwords hashes"""
    username = session['login']
    user_role = session['role']
    if user_role in [ROLE_SUPERUSER, ROLE_WORKER, NO_ROLE]:
        all_users = read_all_users()
        result = (username in all_users.keys()) and (create_hash(password) == all_users[username])
    elif user_role == ROLE_CUSTOMER:
        result = is_valid_customer(username, password)
    else:
        result = False
    return result


def is_valid_customers_password(password: str, hash_in_db: str) -> bool:
    """Function compare password and passwords hashes from customer"""
    return str(create_hash(password)) == str(hash_in_db)


def is_valid_customer(login: str, password: str) -> bool:
    """Function find user with login and password in Database"""
    with Database() as base:
        _, cursor = base
        if user_in_customers(cursor, login):
            try:
                hash = get_hash_to_customer(cursor, login)
                return is_valid_customers_password(password, hash)
            except IndexError:
                return False
        else:
            return False


def is_superuser_password(password: str) -> bool:
    """Function compare password and superuser password hash"""
    username = session['login']
    all_users = read_all_users()
    return (username in all_users.keys()) \
           and (create_hash(password) == all_users[username]) \
           and get_user_role(username) == ROLE_SUPERUSER


def is_superuser_password_cli(password: str) -> bool:
    """Function compare password and superuser password hash (ONLY command string )"""
    all_users = read_all_users()
    for user in all_users.keys():
        if user == config.user_name() and create_hash(password) == all_users[user]:
            return True
    return False


def is_login_and_password_correct(login: str, password: str) -> bool:
    """Function examine login and password pair"""

    try:
        return read_all_users()[login] == create_hash(password)
    except KeyError:
        return False


def get_user_role(login: str) -> str:
    """Return ROLE of user"""
    result = NO_ROLE
    try:
        file_passwords = open(config.path_to_passwords(), mode='r')
        for line in file_passwords:
            user, pass_hash, role = line.split()
            if user == login:
                if role == ROLE_SUPERUSER:
                    result = ROLE_SUPERUSER
                elif role == ROLE_WORKER:
                    result = ROLE_WORKER
                elif role == ROLE_CUSTOMER:
                    result = ROLE_CUSTOMER
        if result == NO_ROLE:
            with Database() as base:
                _, cursor = base
                if user_in_customers(cursor, login):
                    result = ROLE_CUSTOMER
                else:
                    result = NO_ROLE
        file_passwords.close()
    except FileNotFoundError:
        print("File {0} not found!".format(config.path_to_passwords()))
    return result


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
