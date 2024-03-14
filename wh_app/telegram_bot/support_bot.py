import asyncio
from typing import List, Any, Callable
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound, MessageIsTooLong, MessageTextIsEmpty,\
    NetworkError, BadRequest
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from contextlib import suppress

from wh_app.postgresql.database import Database
from wh_app.config_and_backup.config import telegram_delete_message_pause, path_to_project
from wh_app.supporting import functions
from wh_app.sql_operations.select_operations import get_point_id_from_equip_id, get_point_name_from_id,\
    is_telegram_user_reader, is_telegram_user_writer, get_worker_id_from_chats

functions.info_string(__name__)

separator = '=' * 10
bender_message = "Машины восстанут! Поцелуйте мой блестящий металлический зад!"
write_not_access = 'Вам не разрешена запись в базу данных'
MAX_CHAR_IN_MSG = 4000


def not_reader_decorator(func: Callable) -> Callable:
    """If user not reader, to return standart answer"""
    async def wrapper(message):
        try:
            user_id = message.from_id
            user_name = message.from_user
        except:
            user_name = 'User ID {}'.format(user_id)
        if is_user_acs_read(user_id):
            await func(message)
        else:
            msg_del = await message.answer(user_not_access_read(user_name))
            standart_delete_message(msg_del)
    return wrapper


def not_writer_decorator(func: Callable) -> Callable:
    """If user not reader, to return standart answer"""
    async def wrapper(message):
        try:
            user_id = message.from_id
            user_name = message.from_user
        except:
            user_name = 'User ID {}'.format(user_id)
        if is_user_acs_write(user_id):
            await func(message)
        else:
            msg_del = await message.answer(user_not_access_write(user_name))
            standart_delete_message(msg_del)
    return wrapper


def user_not_access_read(user_name: str) -> str:
    """return message NOT ACCESS TO READ"""
    return 'Пользователь {} не имеет прав на чтение'.format(user_name)


def user_not_access_write(user_name: str) -> str:
    """return message NOT ACCESS TO READ"""
    return 'Пользователь {} не имеет прав на запись данных'.format(user_name)


async def delete_message(message: types.Message, sleep_time: int = 0):
    """Create timer to auto delete bot-message"""
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


def equip_message(equip: List[Any], with_point: bool = False) -> List[str]:
    """Create equip-info message"""
    msg = list()
    msg.append(separator)
    if with_point:
        with Database() as base:
            _, cursor = base
            point_id = get_point_id_from_equip_id(cursor, str(equip[0]))
            point_name = get_point_name_from_id(cursor, point_id)
            msg.append('Предприятие: {}'.format(point_name))
    msg.append('ID = {}'.format(equip[0]))
    msg.append('{}'.format(equip[2]))
    msg.append('Мод. {}'.format(equip[3]))
    msg.append('Ser. № {}'.format(equip[4]))
    return msg


def standart_keyboard(keyboard):
    """Return standart keyboard to messages"""
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder=bender_message)


async def not_create_record(message: types.Message):
    """Clear keyboard"""
    msg_del = await message.answer('Отмена операции' ,reply_markup=ReplyKeyboardRemove())
    standart_delete_message(msg_del)


def work_message(work: List[Any], with_equip: bool = False, with_point: bool = False) -> List[str]:
    """Create work-info message"""
    msg = list()
    msg.append(separator)
    if with_point:
        msg.append('Предприятие: {}'.format(work[1]))
    if with_equip:
        msg.append('Оборудование: {}, model: {}, № {}'.format(work[2], work[3], work[4]))
    msg.append('Work_ID = {}'.format(work[0]))
    msg.append('Дата/время: {}'.format(work[5]))
    msg.append('Заявка: {}'.format(work[6]))
    msg.append('Описание работ: {}'.format(work[7]))
    msg.append('Исполнители: {}'.format(work[8]))
    return msg


def get_user_id(message: types.Message) -> str:
    """get user from message"""

    return message.from_user.id


def get_malachite_id(telegram_id: str) -> str:
    """Return data from Write Access List Malachite Database"""
    with Database() as base:
        _, cursor = base
        return get_worker_id_from_chats(cursor, telegram_id) if is_telegram_user_writer(cursor, telegram_id) else None


def is_user_acs_read(user_id: int) -> bool:
    """Return True if user awaliable access to read database"""
    with Database() as base:
        _, cursor = base
        return is_telegram_user_reader(cursor, user_id)


def is_user_acs_write(user_id: int) -> bool:
    """Return True if user awaliable access to write database"""
    with Database() as base:
        _, cursor = base
        return is_telegram_user_writer(cursor, user_id)


def standart_delete_message(msg: types.Message):
    """Create standart message and create task to delete them for standart interval"""
    asyncio.create_task(delete_message(msg, telegram_delete_message_pause()))