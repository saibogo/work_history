import hashlib

import config
import metadata


def info_string(name_module):
    print('Import module {}. Version: {}, Author: {}, License: {}'.format(name_module,
                                                                          metadata.__version__,
                                                                          metadata.__author__,
                                                                          metadata.__license__))


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


def full_equip_to_view(equip: list) -> list:
    """Function return list in format correct to view table"""

    point, _, name, model, serial, pre_id = range(6)
    return list(map(str, [equip[point], equip[name], equip[model], equip[serial], equip[pre_id]]))


def is_valid_password(password: str) -> bool:
    """Function compare password and config-password"""

    return config.pass_hash == int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16)


def form_to_data(form: dict) -> dict:
    """Function create dict contain all data in form"""

    fields = [k for k in form]
    values = [form[k] for k in form]
    data = dict(zip(fields, values))
    return data


info_string(__name__)