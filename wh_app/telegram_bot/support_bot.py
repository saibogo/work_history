import asyncio
import importlib
import aiogram.utils.exceptions
from typing import List, Any
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from contextlib import suppress

from wh_app.telegram_bot.write_bot_access import write_access_dict
from wh_app.postgresql.database import Database
from wh_app.config_and_backup.config import telegram_delete_message_pause, path_to_project
from wh_app.supporting import functions
from wh_app.sql_operations.select_operations import get_point_id_from_equip_id, get_point_name_from_id
from wh_app.telegram_bot.read_bot_access import read_dict, read_id_dict

functions.info_string(__name__)

separator = '=' * 10
bender_message = "Машины восстанут! Поцелуйте мой блестящий металлический зад!"
write_not_access = 'Вам не разрешена запись в базу данных'
MAX_CHAR_IN_MSG = 4000


def user_not_access_read(user_name: str) -> str:
    """return message NOT ACCESS TO READ"""
    return 'Пользователь {} не имеет прав на чтение'.format(user_name)


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


def work_message(work: List[Any]) -> List[str]:
    """Create work-info message"""

    msg = list()
    msg.append(separator)
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

    return write_access_dict[telegram_id] if telegram_id in write_access_dict else None


def standart_delete_message(msg: types.Message):
    """Create standart message and create task to delete them for standart interval"""
    asyncio.create_task(delete_message(msg, telegram_delete_message_pause()))