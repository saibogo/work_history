"""This module is creating new session telegram-bot"""
import asyncio

import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from contextlib import suppress
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from wh_app.supporting import functions
from wh_app.supporting.system_status import SystemStatus
from wh_app.config_and_backup.config import path_to_telegram_token, path_to_project, telegram_delete_message_pause
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations import get_statistic, get_all_works_points, get_point, get_equip_in_point,\
    get_full_equip_information, get_works_from_equip_id, get_maximal_points_id
from wh_app.telegram_bot.read_bot_access import read_dict, read_id_dict
from wh_app.telegram_bot.write_bot_access import write_access_dict
from wh_app.telegram_bot.create_work_object import CreateWorkObject

functions.info_string(__name__)


def load_token() -> str:
    """Load Telegram Api token from filesystem"""
    with open(path_to_telegram_token, 'r') as token_file:
        result = token_file.readline().strip()
        return result


MAX_CHAR_IN_MSG = 4000
API_TOKEN = load_token()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
create_works_list = []
_separator = '=' * 10


async def delete_message(message: types.Message, sleep_time: int = 0):
    """Create timer to auto delete bot-message"""
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Create Hello-message in telegram bot"""
    msg_del = await message.reply("Привет!\nТелеграм-бот системы учета выполненных работ компании Малахит!\n" +
                                  "Список возможных команд /help")
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """Return to telegram-bot HELP-message"""
    msg = ['/start -- запуск бота', '/help -- вызов данной справки', '/status -- получение статуса системы',
           '/statistic -- статистика работ', '/points -- все зарегистрированные предприятия',
           'Внимание! Следующие команды требуют Разрешения на чтение.',
           '<Параметр> обозначает число и вводится через пробел',
           '/point <point ID> -- перейти к предприятию с данным ID',
           '/svu <point ID> -- Получить схему вводного устройства предприятия, если она имеется в базе',
           '/equip <equip_id> -- перейти к нужной единице оборудования',
           'Регистрация новых работ возможна только, если вы имеете разрешение на запись данных',
           'Внимание! Сообщения бота автоматически удаляются из чата через 2 часа после публикации.']
    msg_del = await message.answer("\n".join(msg))
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(commands=['status'])
async def send_status(message: types.Message):
    """Return to telegram-bot system-status"""
    msg = ['{0}: {1}\n'.format(key, SystemStatus.get_status()[key]) for key in SystemStatus.get_status()]
    msg_del = await message.answer("".join(msg))
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(commands=['statistic'])
async def send_statistic(message: types.Message):
    """Return to telegram-bot statistic from all works"""
    with Database() as base:
        _, cursor = base
        stat = get_statistic(cursor)
        msg = []
        for line in stat:
            msg.append(_separator)
            msg.append(line[1])
            msg.append('{} ед. обор.'.format(line[2]))
            msg.append('Всего работ {}'.format(line[3]))
            msg.append('Дата последней {}'.format(line[4]))
        msg_del = await message.answer('\n'.join(msg))
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(commands=['points'])
async def all_points(message: types.Message):
    """Return to telegram-bot all points"""
    with Database() as base:
        _, cursor = base
        points = get_all_works_points(cursor)
        msg = []
        for point in points:
            msg.append(_separator)
            msg.append('ID = {}'.format(point[0]))
            msg.append('{}'.format(point[1]))
            msg.append('Адрес {}'.format(point[2]))
            msg.append('{}'.format(point[3]))
        msg_del = await message.answer('\n'.join(msg))
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(regexp='point\s+[0-9]{1,}')
async def point_info(message: types.Message):
    """Return to telegram-bot information from point with current point_id"""
    with Database() as base:
        _, cursor = base
        point_id = message['text'].split()[1]
        try:
            user_id = message['from']['id']
            user_name = message['from']['username']
        except:
            user_name = 'User ID {}'.format(user_id)
        try:
            if user_name not in read_id_dict and user_id not in read_id_dict:
                raise KeyError
            if point_id == '0':
                raise IndexError
            point = get_point(cursor, point_id)[0]
            msg = []
            msg.append(_separator)
            msg.append('ID = {}'.format(point[0]))
            msg.append('{}'.format(point[1]))
            msg.append('Адрес {}'.format(point[2]))
            msg.append('{}'.format(point[3]))
            equips = get_equip_in_point(cursor, point_id)
            msg.append('Перечень оборудования {} ед.:'.format(len(equips)))
            for equip in equips:
                msg.append(_separator)
                msg.append('ID = {}'.format(equip[0]))
                msg.append('{}'.format(equip[2]))
                msg.append('Мод. {}'.format(equip[3]))
                msg.append('Ser. № {}'.format(equip[4]))
        except IndexError:
            msg = ['Предприятие с ID = {} не найдено'.format(point_id)]
        except KeyError:
            msg = ['Пользователь {} не имеет прав на чтение'.format(user_name)]
        try:
            msg_del = await message.answer('\n'.join(msg))
            asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
        except aiogram.utils.exceptions.MessageIsTooLong:
            tmp = '\n'.join(msg)
            msg_dels = list()
            for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
                msg_dels.append(await message.answer(tmp[i : i + MAX_CHAR_IN_MSG]))
                asyncio.create_task(delete_message(msg_dels[-1], telegram_delete_message_pause))


@dp.message_handler(regexp='equip\s+[0-9]{1,}')
async def equip_info(message: types.Message):
    """Return to telegram-bot information from equip with current equip_id"""
    with Database() as base:
        _, cursor = base
        equip_id = message['text'].split()[1]
        try:
            user_id = message['from']['id']
            user_name = message['from']['username']
        except:
            user_name = 'User ID {}'.format(user_id)
        try:
            if user_name not in read_id_dict and user_id not in read_id_dict:
                raise KeyError
            if equip_id == '0':
                raise IndexError
            equip = get_full_equip_information(cursor, equip_id)
            msg = ['ID = {}'.format(equip_id)]
            msg.append('Расположение: {}'.format(equip[0]))
            msg.append('{}'.format(equip[1]))
            msg.append('Мод. {}'.format(equip[2]))
            msg.append('Ser. № {}'.format(equip[3]))
            works = get_works_from_equip_id(cursor, equip_id)
            for work in works:
                msg.append(_separator)
                msg.append('Work_ID = {}'.format(work[0]))
                msg.append('Дата/время: {}'.format(work[5]))
                msg.append('Заявка: {}'.format(work[6]))
                msg.append('Описание работ: {}'.format(work[7]))
                msg.append('Исполнители: {}'.format(work[8]))
        except IndexError:
            msg = ['Оборудование с ID = {} не найдено'.format(equip_id)]
        except KeyError:
            msg = ['Пользователь {} не имеет прав на чтение'.format(user_name)]
        kb = [
            [InlineKeyboardButton(text='Регистрация (ID={})'.format(equip_id)),
             InlineKeyboardButton(text='Отмена')]
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Машины восстанут! Поцелуйте мой блестящий металлический зад!"
        )
        try:
            msg_del = await message.answer('\n'.join(msg))
            asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
            msg_del1 = await message.answer('Зарегистрировать выполнение работы?', reply_markup=keyboard)
            asyncio.create_task(delete_message(msg_del1, telegram_delete_message_pause))
        except aiogram.utils.exceptions.MessageIsTooLong:
            tmp = '\n'.join(msg)
            msg_dels = list()
            for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
                msg_dels.append(await message.answer(tmp[i : i + MAX_CHAR_IN_MSG]))
                asyncio.create_task(delete_message(msg_dels[-1], telegram_delete_message_pause))
            msg_del = await message.answer('Зарегистрировать выполнение работы?', reply_markup=keyboard)
            asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(text=['Отмена'])
async def not_create_record(message: types.Message):
    """Clear keyboard"""
    msg_del = await message.answer('Отмена операции' ,reply_markup=ReplyKeyboardRemove())
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(lambda message: message.text and 'Регистрация' in message.text)
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
        create_works_list.append(CreateWorkObject(equip_id))
        msg_del1 = await message.answer('/problem ID={}\nПричина производства работ'.format(equip_id))
        asyncio.create_task(delete_message(msg_del1, telegram_delete_message_pause))
        msg_del2 = await message.answer('/exec ID={}\nЧто произведено?'.format(equip_id))
        asyncio.create_task(delete_message(msg_del2, telegram_delete_message_pause))


@dp.message_handler(lambda message: message.reply_to_message and '/problem' in message.reply_to_message.text)
async def problem_repler(message: types.Message):
    """Handler to reply message"""

    start_message = message.reply_to_message.text
    first = start_message.index('=')
    last = start_message.index('\n')
    equip_id = start_message[first + 1 : last]
    problem = message.text
    create_object = find_in_object_list(equip_id)
    create_object.create_problem(problem)
    user_id = get_user_id(message)
    worker_id =  get_malachite_id(user_id)
    create_object.set_user_id(worker_id)
    if worker_id is None:
        msg_del = await message.answer('Вам не разрешена запись в базу данных')
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
    elif create_object.is_complete_data():
        create_object.write_in_database()
        remove_from_object_list(equip_id)
        msg_del = await message.answer('Произведена запись в базу данных!\n{}'.
                                       format(get_last_work_from_equip_id(equip_id)))
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(lambda message: message.reply_to_message and '/exec' in message.reply_to_message.text)
async def work_repler(message: types.Message):
    """Handler to reply message"""

    start_message = message.reply_to_message.text
    first = start_message.index('=')
    last = start_message.index('\n')
    equip_id = start_message[first + 1 : last]
    work = message.text
    create_object = find_in_object_list(equip_id)
    create_object.create_work(work)
    user_id = get_user_id(message)
    worker_id = get_malachite_id(user_id)
    create_object.set_user_id(worker_id)
    if worker_id is None:
        msg_del = await message.answer('Вам не разрешена запись в базу данных')
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
    elif create_object.is_complete_data():
        create_object.write_in_database()
        remove_from_object_list(equip_id)
        msg_del = await message.answer('Произведена запись в базу данных!\n{}'.
                                       format(get_last_work_from_equip_id(equip_id)))
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler(regexp='svu\s+[0-9]{1,}')
async def get_svu(message: types.Message):
    """Return to telegram-bot SVU-file from selected point"""
    with Database() as base:
        _, cursor = base
        point_id = int(message['text'].split()[1])
        try:
            user_id = message['from']['id']
            user_name = message['from']['username']
        except:
            user_name = 'User ID {}'.format(user_id)
        try:
            if user_name not in read_id_dict and user_id not in read_id_dict:
                raise KeyError
            if point_id > int(get_maximal_points_id(cursor)) or point_id < 1:
                raise IndexError
            try:
                doc = open('{}wh_app/web/static/image/svu/svu_{}.jpg'.format(path_to_project, point_id), 'rb')
                msg_del = await message.reply_document(doc)
                asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
            except FileNotFoundError:
                msg_del = await message.answer('Схема Вводного Устройства для Предприятия с ID = {} не найдена'.format(point_id))
                asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
        except IndexError:
            msg = ['Предприятие с ID = {} не найдено\n Перечень предприятий /points'.format(point_id)]
            msg_del = await message.answer('\n'.join(msg))
            asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
        except KeyError:
            msg = ['Пользователь {} не имеет прав на чтение'.format(user_name)]
            msg_del = await message.answer('\n'.join(msg))
            asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


@dp.message_handler()
async def send_command_not_found(message: types.Message):
    """Return to telegram-bot system-status"""
    print(message)
    msg_del = await message.answer('Команда {} некорректна'.format(message['text']))
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


def start_telegram_bot():
    """This function starting session"""
    executor.start_polling(dp)


def find_in_object_list(equip_id: str) -> CreateWorkObject:
    """Return object if exist"""

    for elem in create_works_list:
        if elem.get_equip_id() == equip_id:
            return elem
    return None


def remove_from_object_list(equip_id: str):
    """Remove object after write in database"""
    num = None
    for i in range(len(create_works_list)):
        if create_works_list[i].get_equip_id() == equip_id:
            num = i
            break
    if not num is None:
        create_works_list.pop(i)


def get_user_id(message: types.Message) -> str:
    """get user from message"""

    return message.from_user.id


def get_malachite_id(telegram_id: str) -> str:
    """Return data from Write Access List Malachite Database"""

    return write_access_dict[telegram_id] if telegram_id in write_access_dict else None


def get_last_work_from_equip_id(equip_id: str) -> str:
    """Return string contain last work description"""
    with Database() as base:
        _, cursor = base
        work = get_works_from_equip_id(cursor, equip_id)[-1]
        equip = get_full_equip_information(cursor, equip_id)
        msg = ['ID = {}'.format(equip_id)]
        msg.append('Расположение: {}'.format(equip[0]))
        msg.append('{}'.format(equip[1]))
        msg.append('Мод. {}'.format(equip[2]))
        msg.append('Ser. № {}'.format(equip[3]))
        msg.append(_separator)
        msg.append('Work_ID = {}'.format(work[0]))
        msg.append('Дата/время: {}'.format(work[5]))
        msg.append('Заявка: {}'.format(work[6]))
        msg.append('Описание работ: {}'.format(work[7]))
        msg.append('Исполнители: {}'.format(work[8]))
        return "\n".join(msg)
