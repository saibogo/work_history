import asyncio

from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations import get_full_equip_information, get_last_works_from_equip_id,\
    get_works_from_equip_id, get_point, get_maximal_equip_id, get_equip_deleted_status
from wh_app.telegram_bot.create_equip_object import CreateEquipObject

functions.info_string(__name__)

create_equips_list = []
error_in_create_field = 'Сбой при записи нового оборудования!'


async def equip_info(message: types.Message):
    """Return to telegram-bot information from equip with current equip_id"""
    with Database() as base:
        _, cursor = base
        full_command = message.text.split()
        equip_id = full_command[1]
        only_last_works = True if len(full_command) < 3 else False
        kb = [
            [InlineKeyboardButton(text='Регистрация (ID={})'.format(equip_id)),
             InlineKeyboardButton(text='Отмена')]
        ]
        try:
            user_id = message.from_id
            user_name = message.from_user
        except:
            user_name = 'User ID {}'.format(user_id)
        try:
            if user_name not in read_id_dict and user_id not in read_id_dict:
                raise KeyError
            if equip_id == '0':
                raise IndexError
            equip = [equip_id] + get_full_equip_information(cursor, equip_id)
            msg = equip_message(equip)
            works = get_last_works_from_equip_id(cursor, equip_id) if only_last_works\
                else get_works_from_equip_id(cursor, equip_id)
            for work in works:
                msg += work_message(work)
            msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)
            if not get_equip_deleted_status(cursor, equip_id):
                msg_del1 = await message.answer('Зарегистрировать выполнение работы?',
                                                reply_markup=standart_keyboard(kb))
                standart_delete_message(msg_del1)
        except IndexError:
            msg_del = await message.answer('Оборудование с ID = {} не найдено'.format(equip_id))
            standart_delete_message(msg_del)
        except KeyError:
            msg_del = await message.answer(user_not_access_read(user_name))
            standart_delete_message(msg_del)
        except aiogram.utils.exceptions.MessageIsTooLong:
            tmp = '\n'.join(msg)
            msg_dels = list()
            for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
                msg_dels.append(await message.answer(tmp[i : i + MAX_CHAR_IN_MSG]))
                standart_delete_message(msg_dels[-1])
            if not get_equip_deleted_status(cursor, equip_id):
                msg_del = await message.answer('Зарегистрировать выполнение работы?', reply_markup=standart_keyboard(kb))
                standart_delete_message(msg_del)


async def start_add_new_equip(message: types.Message):
    with Database() as base:
        _, cursor = base
        first_num = message.text.index('=')
        last_num = message.text.index(')')
        point_id = message.text[first_num + 1: last_num]
        point = get_point(cursor, point_id)
        msg = ['Начинаем регистрацию нового оборудования!', 'Предприятие:{}'.format(point[0][1]),
               'Используйте функцию ОТВЕТ на 4 сообщения ниже.',
               'Нажмите кнопку ЗАПИСАТЬ и оборудование будет внесено в базу данных']
        msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)
        create_equips_list.append(CreateEquipObject(point_id, str(message.from_id)))
        kb = [
            [InlineKeyboardButton(text='ЗАПИСАТЬ ID={}'.format(point_id))]
        ]
        msg_del1 = await message.answer('/equip_name point_ID={}\nНаименование оборудования'.format(point_id),
                                        reply_markup=standart_keyboard(kb))
        standart_delete_message(msg_del1)
        msg_del2 = await message.\
            answer('/equip_model point_ID={}\nМодель(Если есть. Иначе не отвечайте на это сообщение)'.format(point_id))
        standart_delete_message(msg_del2)
        msg_del3 = await message.\
            answer('/equip_serial point_ID={}\nСерийный номер(Если есть. Иначе не отвечайте на это сообщение)'.
                   format(point_id))
        standart_delete_message(msg_del3)
        msg_del4 = await message.\
            answer('/equip_pre_id point_ID={}\nПредыдущий ID(Если есть. Иначе не отвечайте на это сообщение)'.
                   format(point_id))
        standart_delete_message(msg_del4)


async def equip_repler(message: types.Message, category: str):
    """Save new field in CreateEquipObject"""
    user_id = get_user_id(message)
    worker_id = get_malachite_id(user_id)
    if worker_id is None:
        msg_del = await message.answer(write_not_access)
        standart_delete_message(msg_del)
    else:
        start_message = message.reply_to_message.text
        point_id = start_message.split('=')[1].split()[0]
        create_object = find_in_object_list(point_id, str(message.from_id))
        if category == 'name' and create_object:
            create_object.create_name(message.text)
        elif category == 'model' and create_object:
            create_object.create_model(message.text)
        elif category == 'serial' and create_object:
            create_object.create_serial(message.text)
        elif category == 'pre_id' and create_object:
            create_object.create_pre_id(message.text)
        else:
            msg_del = await message.answer(error_in_create_field)
            standart_delete_message(msg_del)


async def save_new_equip(message: types.Message):
    """Examine and save new equip in database"""
    user_id = get_user_id(message)
    worker_id = get_malachite_id(user_id)
    if worker_id is None:
        msg_del = await message.answer(write_not_access)
        standart_delete_message(msg_del)
    else:
        point_id = message.text.split('=')[1]
        create_object = find_in_object_list(point_id, str(message.from_id))
        if create_object:
            if create_object.is_complete_data():
                create_object.write_in_database()
                remove_from_object_list(point_id, str(message.from_id))
                msg_del = await message.answer('Произведена запись оборудования!', reply_markup=ReplyKeyboardRemove())
                with Database() as base:
                    _, cursor = base
                    equip_id = get_maximal_equip_id(cursor)
                    equip = [equip_id] + get_full_equip_information(cursor, equip_id)
                    msg_del1 = await message.answer('\n'.join(equip_message(equip, True)))
                    standart_delete_message(msg_del1)
            else:
                msg_del = await message.answer('Введенных данных недостаточно!')
        else:
            msg_del = await message.answer(error_in_create_field)
        standart_delete_message(msg_del)


def find_in_object_list(point_id: str, user_id: str) -> CreateEquipObject:
    """Return object if its in object-list"""
    for elem in create_equips_list:
        if elem.get_point_id() == point_id and elem.get_user_id() == user_id:
            return elem
    return None


def remove_from_object_list(point_id: str, user_id: str):
    """Remove object after write in database"""
    num = None
    for i in range(len(create_equips_list)):
        elem = create_equips_list[i]
        if elem.get_point_id() == point_id and elem.get_user_id() == user_id:
            num = i
            break
    if not num is None:
        create_equips_list.pop(i)