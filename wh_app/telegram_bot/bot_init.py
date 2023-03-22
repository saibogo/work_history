"""This module is creating new session telegram-bot"""
import asyncio

from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.utils.exceptions import MessageTextIsEmpty

from wh_app.supporting import functions
from wh_app.config_and_backup.config import path_to_telegram_token, path_to_messages
from wh_app.telegram_bot.point_bot import all_points, send_statistic, point_info, not_create_record, get_svu,\
    get_tech_info
from wh_app.telegram_bot.equip_bot import equip_info, start_add_new_equip, save_new_equip, equip_repler
from wh_app.telegram_bot.any_bot import send_welcome, send_help, send_status, send_command_not_found, send_changelog
from wh_app.telegram_bot.bugs_bot import all_bugs, start_create_new_bug, new_bug_repler, bug_from_bug_id,\
    invert_bug_status_from_bot
from wh_app.telegram_bot.work_bot import start_create_record
from wh_app.telegram_bot.work_bot import problem_repler, work_repler
from wh_app.telegram_bot.read_bot_access import chats
from wh_app.telegram_bot.support_bot import standart_delete_message
from wh_app.telegram_bot.find_bot import main_find_menu, find_menu, find_repler, last_day_message
from wh_app.telegram_bot.workers_bot import send_workers_message

functions.info_string(__name__)


def load_token() -> str:
    """Load Telegram Api token from filesystem"""
    with open(path_to_telegram_token(), 'r') as token_file:
        result = token_file.readline().strip()
        return result


MAX_CHAR_IN_MSG = 4000
API_TOKEN = load_token()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
TIMEOUT_TO_SEND_INFO_MESSAGE = 60
bot_is_restarted = True


def repeat(coro, loop):
    """Create event loop for telegram bot"""
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(TIMEOUT_TO_SEND_INFO_MESSAGE, repeat, coro, loop)


def start_telegram_bot():
    """This function starting session"""
    loop = asyncio.get_event_loop()
    loop.call_later(TIMEOUT_TO_SEND_INFO_MESSAGE, repeat, start_message, loop)
    executor.start_polling(dp, loop=loop)


async def start_message():
    """Send all users in chats-list starting message"""
    global bot_is_restarted
    messages_del = []
    if bot_is_restarted:
        for chat in chats:
            messages_del.append(await bot.send_message(chat, 'Произведен перезапуск телеграмм-бота!'))
            standart_delete_message(messages_del[-1])
        bot_is_restarted = False
    else:
        message = ""
        try:
            message_file = open(path_to_messages(), 'r')
            for line in message_file:
                message += line
            for chat in chats:
                messages_del.append(await bot.send_message(chat, message))
                standart_delete_message(messages_del[-1])
        except FileNotFoundError:
            pass
        except MessageTextIsEmpty:
            pass


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await send_welcome(message)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """Return to telegram-bot HELP-message"""
    await send_help(message)


@dp.message_handler(commands=['status'])
async def status_command(message: types.Message):
    """Return to telegram-bot system-status"""
    await send_status(message)


@dp.message_handler(commands=['statistic'])
async def statistic_command(message: types.Message):
    await send_statistic(message)


@dp.message_handler(commands=['points'])
async def points_command(message: types.Message):
    await all_points(message)


@dp.message_handler(commands=['changelog'])
async def changelog_command(message: types.Message):
    await send_changelog(message)


@dp.message_handler(commands=['lastday'])
async def lastday_command(message: types.Message):
    await last_day_message(message)


@dp.message_handler(regexp='point\s+[0-9]{1,}')
async def point_command(message: types.Message):
    await point_info(message)


@dp.message_handler(regexp='svu\s+[0-9]{1,}')
async def get_svu_command(message: types.Message):
    await get_svu(message)


@dp.message_handler(regexp='tech\s+[0-9]{1,}')
async def get_tech_command(message: types.Message):
    await get_tech_info(message)


@dp.message_handler(commands=['bugs'])
async def bugs_command(message: types.Message):
    """Return to telegram-bot all bugs"""
    await all_bugs(message)


@dp.message_handler(commands=['workers'])
async def workers_command(message: types.Message):
    """Return to telegram-bot all bugs"""
    await send_workers_message(message)


@dp.message_handler(regexp='/bug\s+[0-9]{1,}')
async def bug_from_id_command(message: types.Message):
    """Return bug with id == bug_id"""
    await bug_from_bug_id(message)


@dp.message_handler(lambda message: message.text and 'Новая проблема' in message.text)
async def new_bug_command(message: types.Message):
    await start_create_new_bug(message)


@dp.message_handler(lambda message: message.reply_to_message and '/new_bug' in message.reply_to_message.text)
async def new_bug_done_message(message: types.Message):
    await new_bug_repler(message)


@dp.message_handler(lambda message: message.text and 'Изменить статус ID=' in message.text)
async def invert_bug_status_message(message: types.Message):
    await invert_bug_status_from_bot(message)


@dp.message_handler(lambda message: message.text and 'Новое оборудование' in message.text)
async def create_new_equip_command(message: types.Message):
    await start_add_new_equip(message)


@dp.message_handler(lambda message: message.reply_to_message and '/equip_name' in message.reply_to_message.text)
async def new_equip_name_command(message: types.Message):
    await equip_repler(message, 'name')


@dp.message_handler(lambda message: message.reply_to_message and '/equip_model' in message.reply_to_message.text)
async def new_equip_model_command(message: types.Message):
    await equip_repler(message, 'model')


@dp.message_handler(lambda message: message.reply_to_message and '/equip_serial' in message.reply_to_message.text)
async def new_equip_model_command(message: types.Message):
    await equip_repler(message, 'serial')


@dp.message_handler(lambda message: message.reply_to_message and '/equip_pre_id' in message.reply_to_message.text)
async def new_equip_model_command(message: types.Message):
    await equip_repler(message, 'pre_id')


@dp.message_handler(lambda message: 'ЗАПИСАТЬ' in message.text and 'ID=' in message.text)
async def save_new_equip_command(message: types.message):
    await save_new_equip(message)


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['equip\s+[0-9]{1,}\s+all', 'equip\s+[0-9]{1,}']))
async def equip_info_command(message: types.Message):
    await equip_info(message)


@dp.message_handler(text=['Отмена'])
async def not_create_command(message: types.Message):
    await not_create_record(message)


@dp.message_handler(lambda message: message.text and 'Регистрация' in message.text)
async def new_work_command(message: types.Message):
    """Start registration new work"""
    await start_create_record(message)


@dp.message_handler(lambda message: message.reply_to_message and '/problem' in message.reply_to_message.text)
async def problem_in_new_work(message: types.Message):
    """Handler to reply message"""
    await problem_repler(message)


@dp.message_handler(lambda message: message.reply_to_message and '/exec' in message.reply_to_message.text)
async def exec_in_new_work(message: types.Message):
    """Handler to reply message"""
    await work_repler(message)


@dp.message_handler(commands=['find'])
async def find_command(message: types.Message):
    """Start menu select find-type"""
    await main_find_menu(message)


@dp.message_handler(lambda message: 'Предприятие' in message.text)
async def find_point_command(message: types.Message):
    """Start find point menu"""
    await find_menu(message, 'point')


@dp.message_handler(lambda message: message.reply_to_message and '/find_point' in message.reply_to_message.text)
async def find_point_repler_command(message: types.Message):
    """Start find in workspoints"""
    await find_repler(message, 'point')


@dp.message_handler(lambda message: 'Оборудование' in message.text)
async def find_equip_command(message: types.Message):
    """Start find point menu"""
    await find_menu(message, 'equip')


@dp.message_handler(lambda message: message.reply_to_message and '/find_equip' in message.reply_to_message.text)
async def find_equip_repler_command(message: types.Message):
    """Start find in workspoints"""
    await find_repler(message, 'equip')


@dp.message_handler(lambda message: 'Работы' in message.text)
async def find_work_command(message: types.Message):
    """Start find point menu"""
    await find_menu(message, 'work')


@dp.message_handler(lambda message: message.reply_to_message and '/find_work' in message.reply_to_message.text)
async def find_work_repler_command(message: types.Message):
    """Start find in workspoints"""
    await find_repler(message, 'work')


@dp.message_handler(lambda message: 'Исполнители' in message.text)
async def find_performer_command(message: types.Message):
    """Start find point menu"""
    await find_menu(message, 'performer')


@dp.message_handler(lambda message: message.reply_to_message and '/find_performer' in message.reply_to_message.text)
async def find_performer_repler_command(message: types.Message):
    """Start find in workspoints"""
    await find_repler(message, 'performer')


@dp.message_handler()
async def not_correct_command(message: types.Message):
    """Return to telegram-bot system-status"""
    await send_command_not_found(message)






