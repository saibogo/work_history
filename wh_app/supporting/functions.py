import hashlib
from datetime import datetime

from wh_app.config_and_backup import config
from wh_app.supporting import metadata


def info_string(name_module):
    print('Import module {}. Version: {}, Author: {}, License: {}'.format(name_module,
                                                                          metadata.__version__,
                                                                          metadata.__author__,
                                                                          metadata.__license__))


def str_to_str_n(s: str, max_len: int) -> str:
    """Function return new string, separated \n"""

    tmp = s
    chunks = []
    if max_len == 0:
        return str_to_str_n(s, 1)
    while len(tmp) >= max_len:
        chunks.append(tmp[:max_len])
        tmp = tmp[max_len:]
    if len(tmp) != 0:
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
        result =  list(map(str, [equip[point], equip[name], equip[model], equip[serial], equip[pre_id]]))

    return result


def is_valid_password(password: str) -> bool:
    """Function compare password and config-password"""

    return config.pass_hash == int(hashlib.sha256(password.encode('utf-8')).hexdigest(), 16)


def form_to_data(form: dict) -> dict:
    """Function create dict contain all data in form"""

    fields = [k for k in form]
    values = [form[k] for k in form]
    data = dict(zip(fields, values))
    return data


def date_to_browser() -> str:
    """Return current datetime string to browser format"""

    curr_datetime = datetime.now()
    year = str(curr_datetime.year)
    month = str(curr_datetime.month) if curr_datetime.month > 9 else '0' + str(curr_datetime.month)
    day = str(curr_datetime.day) if curr_datetime.day > 9 else '0' + str(curr_datetime.day)
    hour = str(curr_datetime.hour) if curr_datetime.hour > 9 else '0' + str(curr_datetime.hour)
    minute = str(curr_datetime.minute) if curr_datetime.minute > 9 else '0' + str(curr_datetime.minute)
    return "{}-{}-{}T{}:{}".format(year, month, day, hour, minute)


def works_table_add_new_performer(works: list) -> list:
    """Add to all works string link ADD-Performer"""

    new_works = []

    for work in works:
        new_works.append([])
        for elem in work:
            new_works[-1].append(str(elem))
        if work != []:
            new_works[-1][-1] += ('<a href="/add-performer-to-work/' + str(new_works[-1][0]) + '">+</a>')

    return new_works


def list_of_pages(all_records: list) -> list:
    """Return list any elem is number page in html-view"""

    result = [i + 1 for i in range(len(all_records) // config.max_records_in_page)]
    if len(all_records) % config.max_records_in_page != 0:
        result.append(len(result) + 1)
    return result if len(all_records) > 0 else [1]


info_string(__name__)