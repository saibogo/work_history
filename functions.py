import hashlib

import config
import metadata


def info_string(name_module):
    print('Import module {}. Version: {}, Author: {}, License: {}'.format(name_module,
                                                                          metadata.__version__,
                                                                          metadata.__author__,
                                                                          metadata.__license__))


def print_list(ls: list) -> None:
    """Function print all elements list 'one in one line'"""

    count = 1
    for elem in ls:
        print(str(count), elem)
        count += 1


def str_to_str_n(s: str, max_len: int) -> str:
    """Function return new string, separated /n"""

    tmp = s
    chunks = []
    while len(tmp) >= max_len:
        chunks.append(tmp[:max_len])
        tmp = tmp[max_len:]
    chunks.append(tmp)
    return '\n'.join(chunks)


def num_to_time_str(num: int) -> str:
    """Function return number in time standart. Example 10 -> 10, 1 -> 01"""

    return str(num) if num > 9 else '0' + str(num)


def str_to_nowcase_str(word:str) -> str:
    """Function return regexp. Example a -> [aA], ab ->[aA][bB]"""

    result = []
    for char in word:
        result.append('[' + char.lower() + char.upper() +']')
    return ''.join(result)


def full_work_to_view(work:list) -> list:
    """Function return list in format correct to view table"""

    point, _, name, model, serial, _, date, problem, comment = range(9)
    return list(map(str, [work[point], work[name], work[model],work[serial], work[date],work[problem], work[comment]]))


def full_equip_to_view(equip: list) -> list:
    """Function return list in format correct to view table"""

    point, _, name, model, serial, pre_id = range(6)
    return list(map(str, [equip[point], equip[name], equip[model], equip[serial], equip[pre_id]]))


def get_id_list(ls: list) -> list:
    """Function return all id in list ls"""
    return [elem[0] for elem in ls]


def is_valid_password(password: str) -> bool:
    """Function compare password and config-password"""
    return config.pass_hash == int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16)


def form_to_data(form: dict) -> dict:
    """Fuction create dict contain all data in form"""
    fields = [k for k in form]
    values = [form[k] for k in form]
    data = dict(zip(fields, values))
    return data

info_string(__name__)