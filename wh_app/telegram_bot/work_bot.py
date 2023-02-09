from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations import get_full_equip_information, get_works_from_equip_id
from wh_app.telegram_bot.create_work_object import CreateWorkObject

functions.info_string(__name__)


create_works_list = []


async def start_create_record(message: types.Message):
    """Start registration new work"""
    with Database() as base:
        _, cursor = base
        first_num = message['text'].index('=')
        last_num = message['text'].index(')')
        equip_id = message['text'][first_num + 1 : last_num]
        equip_name = get_full_equip_information(cursor, equip_id)[1]
        msg_del = await message.answer('Начинаем регистрацию работ по "{}"\n'
                                       'Используйте функцию ОТВЕТ на два сообщения ниже и произведенные работы будут записаны'.
                                       format(equip_name) ,
                                       reply_markup=ReplyKeyboardRemove())
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
        create_works_list.append(CreateWorkObject(equip_id, str(message.from_id)))
        msg_del1 = await message.answer('/problem ID={}\nПричина производства работ'.format(equip_id))
        asyncio.create_task(delete_message(msg_del1, telegram_delete_message_pause))
        msg_del2 = await message.answer('/exec ID={}\nЧто произведено?'.format(equip_id))
        asyncio.create_task(delete_message(msg_del2, telegram_delete_message_pause))


async def exec_or_problem_handler(message: types.Message, select: str='work'):
    """Handler for new work dialogue. Possible select = ['work' or 'problem']"""
    start_message = message.reply_to_message.text
    first = start_message.index('=')
    last = start_message.index('\n')
    equip_id = start_message[first + 1: last]
    create_object = find_in_object_list(equip_id, str(message.from_id))
    if select == 'work':
        work = message.text
        create_object.create_work(work)
    elif select == 'problem':
        problem = message.text
        create_object.create_problem(problem)
    else:
        pass
    user_id = get_user_id(message)
    worker_id = get_malachite_id(user_id)
    create_object.set_malachite_user_id(worker_id)
    if worker_id is None:
        msg_del = await message.answer(write_not_access)
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
    elif create_object.is_complete_data():
        create_object.write_in_database()
        remove_from_object_list(equip_id)
        msg_del = await message.answer(add_work_message(equip_id))
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


def remove_from_object_list(equip_id: str):
    """Remove object after write in database"""
    num = None
    for i in range(len(create_works_list)):
        if create_works_list[i].get_equip_id() == equip_id:
            num = i
            break
    if not num is None:
        create_works_list.pop(i)


def find_in_object_list(equip_id: str, user_id: str) -> CreateWorkObject:
    """Return object if exist"""

    for elem in create_works_list:
        if elem.get_equip_id() == equip_id and elem.get_user_id() == user_id:
            return elem
    return None


def add_work_message(equip_id: str) -> str:
    """Create string Add work in database etc"""
    return 'Произведена запись в базу данных!\n{}'.format(get_last_work_from_equip_id(equip_id))


def get_last_work_from_equip_id(equip_id: str) -> str:
    """Return string contain last work description"""
    with Database() as base:
        _, cursor = base
        work = get_works_from_equip_id(cursor, equip_id)[-1]
        equip = [equip_id] + get_full_equip_information(cursor, equip_id)
        msg = equip_message(equip)
        msg += work_message(work)
        return "\n".join(msg)


async def problem_repler(message: types.Message):
    """Handler to reply message"""
    await exec_or_problem_handler(message, 'problem')


async def work_repler(message: types.Message):
    """Handler to reply message"""
    await exec_or_problem_handler(message, 'work')