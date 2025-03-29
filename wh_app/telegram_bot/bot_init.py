"""This module is creating new session telegram-bot"""
import asyncio

from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.utils.exceptions import MessageTextIsEmpty

from wh_app.supporting import functions
from wh_app.postgresql.database import Database
from wh_app.sql_operations.select_operations.select_operations import get_all_telegram_chats, get_order_from_id
from wh_app.telegram_bot.bot_state_machine import BotStateMachine
from wh_app.config_and_backup.config import path_to_telegram_token, path_to_messages
from wh_app.telegram_bot.point_bot import all_points, send_statistic, point_info, not_create_record, get_svu, \
    get_tech_info
from wh_app.telegram_bot.equip_bot import equip_info, start_add_new_equip, save_new_equip, equip_repler, start_download_detail
from wh_app.telegram_bot.any_bot import send_welcome, send_help, send_status, send_command_not_found, send_changelog, \
    send_top10, power_outages
from wh_app.telegram_bot.bugs_bot import all_bugs, start_create_new_bug, new_bug_repler, bug_from_bug_id, \
    invert_bug_status_from_bot
from wh_app.telegram_bot.work_bot import start_create_record
from wh_app.telegram_bot.work_bot import problem_repler, work_repler, get_work_record
from wh_app.telegram_bot.support_bot import standart_delete_message
from wh_app.telegram_bot.find_bot import main_find_menu, find_menu, find_repler, last_day_message
from wh_app.telegram_bot.workers_bot import send_workers_message, today_schedule_message, week_schedule_message
from wh_app.telegram_bot.orders_bot import all_noclosed_orders, order_from_id, order_message
from wh_app.telegram_bot.meter_devices_bot import start_view_meter_devices, start_view_reading_meter_device,\
    start_create_readings_record, new_reading_repler

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
bot_state = BotStateMachine.get_instance()
new_orders_dict = {}


def repeat(coro, loop):
    """Create event loop for telegram bot"""
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(TIMEOUT_TO_SEND_INFO_MESSAGE, repeat, coro, loop)


def start_telegram_bot():
    """This function starting session"""
    bot_state.set_on_status()
    loop = asyncio.get_event_loop()
    loop.call_later(TIMEOUT_TO_SEND_INFO_MESSAGE, repeat, start_message_with_new_order, loop)
    executor.start_polling(dp, loop=loop)


def add_new_order_in_loop(order_id) -> None:
    global new_orders_dict
    new_orders_dict[order_id] = True


async def start_message_with_new_order():
    """Send all users in chats-list message with a new order"""
    global new_orders_dict
    messages_del = []
    if True in new_orders_dict.values():
        for order in new_orders_dict.keys():
            if new_orders_dict[order]:
                with Database() as base:
                    _, cursor = base
                    chats_db = get_all_telegram_chats(cursor)
                    order_info = get_order_from_id(cursor, order)
                    message = order_message(order_info)
                    for chat in chats_db:
                        messages_del.append(await bot.send_message(chat, 'Зарегистрирована новая заявка!'))
                        standart_delete_message(messages_del[-1])
                        messages_del.append(await bot.send_message(chat, message))
                        standart_delete_message(messages_del[-1])
                new_orders_dict[order] = False
        new_orders_dict = dict(filter(lambda item: item == True, new_orders_dict.items()))


@dp.message_handler(filters.Command(commands=['start'], ignore_case=True))
async def start_command(message: types.Message):
    await send_welcome(message)


@dp.message_handler(filters.Command(commands=['help'], ignore_case=True))
async def help_command(message: types.Message):
    """Return to telegram-bot HELP-message"""
    await send_help(message)


@dp.message_handler(filters.Command(commands=['status'], ignore_case=True))
async def status_command(message: types.Message):
    """Return to telegram-bot system-status"""
    await send_status(message)


@dp.message_handler(filters.Command(commands=['power_outages'], ignore_case=True))
async def power_outages_command(message: types.Message):
    """Return to telegram-bot system-status"""
    await power_outages(message)


@dp.message_handler(filters.Command(commands=['statistic'], ignore_case=True))
async def statistic_command(message: types.Message):
    await send_statistic(message)


@dp.message_handler(filters.Command(commands=['points'], ignore_case=True))
async def points_command(message: types.Message):
    await all_points(message)


@dp.message_handler(filters.Command(commands=['changelog'], ignore_case=True))
async def changelog_command(message: types.Message):
    await send_changelog(message)


@dp.message_handler(filters.Command(commands=['lastday'], ignore_case=True))
async def lastday_command(message: types.Message):
    await last_day_message(message)


@dp.message_handler(regexp='/[pP][oO][iI][nN][tT]\s+[0-9]{1,}')  # /point N
async def point_command(message: types.Message):
    await point_info(message)


@dp.message_handler(regexp='/[sS][vV][uU]\s+[0-9]{1,}') # /svu N
async def get_svu_command(message: types.Message):
    await get_svu(message)


@dp.message_handler(regexp='/[tT][eE][cC][hH]\s+[0-9]{1,}') # /tech N
async def get_tech_command(message: types.Message):
    await get_tech_info(message)


@dp.message_handler(filters.Command(commands=['bugs'], ignore_case=True))
async def bugs_command(message: types.Message):
    """Return to telegram-bot all bugs"""
    await all_bugs(message)


@dp.message_handler(filters.Command(commands=['orders'], ignore_case=True))
async def all_orders_command(message: types.Message):
    """Return in telegramm bot list of all no-closed orders"""
    await all_noclosed_orders(message)


@dp.message_handler(regexp='/[oO][rR][dD][eE][rR]\s+[0-9]{1,}')
async def order_command(message: types.Message):
    """Return message in telegram-bot with order where ID = order_id"""
    await order_from_id(message)


@dp.message_handler(filters.Command(commands=['workers'], ignore_case=True))
async def workers_command(message: types.Message):
    """Return to telegram-bot all bugs"""
    await send_workers_message(message)


@dp.message_handler(regexp='/[wW][oO][rR][kK]\s+[0-9]{1,}')
async def work_command(message: types.Message):
    """Return to telegram bot info from work whit work_id == ID
    Example /work 1546"""
    await get_work_record(message)


@dp.message_handler(regexp='/[bB][uU][gG]\s+[0-9]{1,}') # /bug 123
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


@dp.message_handler(lambda message: message.text and 'Приборы учета' in message.text)
async def view_meter_devices(message: types.Message):
    await start_view_meter_devices(message)


@dp.message_handler(regexp='/[pP][uU]\s+[0-9]{1,}') # /pu N
async def view_reading_to_meter_device(message: types.Message):
    """Return readings with id == device_id"""
    await start_view_reading_meter_device(message)


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


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['/[eE][qQ][uU][iI][pP]\s+[0-9]{1,}\s+[aA][lL][lL]',
                                                                  '/[eE][qQ][uU][iI][pP]\s+[0-9]{1,}']))
async def equip_info_command(message: types.Message):
    await equip_info(message)


@dp.message_handler(text=['Отмена'])
async def not_create_command(message: types.Message):
    await not_create_record(message)


@dp.message_handler(lambda message: message.text and 'Внести показания' in message.text)
async def new_reading_command(message: types.Message):
    """Start registration new readind to meter device"""
    await start_create_readings_record(message)


@dp.message_handler(lambda message: message.reply_to_message and '/new_reading_id' in message.reply_to_message.text)
async def insert_reading_command(message: types.Message):
    await new_reading_repler(message)


@dp.message_handler(lambda message: message.text and 'Регистрация' in message.text)
async def new_work_command(message: types.Message):
    """Start registration new work"""
    await start_create_record(message)


@dp.message_handler(lambda message: message.text and 'Деталировка' in message.text)
async def get_detail_command(message: types.Message):
    """Go to download detail if exist"""
    await start_download_detail(message)


@dp.message_handler(lambda message: message.reply_to_message and '/problem' in message.reply_to_message.text)
async def problem_in_new_work(message: types.Message):
    """Handler to reply message"""
    await problem_repler(message)


@dp.message_handler(lambda message: message.reply_to_message and '/exec' in message.reply_to_message.text)
async def exec_in_new_work(message: types.Message):
    """Handler to reply message"""
    await work_repler(message)


@dp.message_handler(filters.Command(commands=['find'], ignore_case=True))
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


@dp.message_handler(filters.Command(commands=['top10'], ignore_case=True))
async def top10_command(message: types.Message):
    await send_top10(message)


@dp.message_handler(filters.Command(commands=['schedule_today'], ignore_case=True))
async def schedule_today_command(message: types.Message):
    await today_schedule_message(message)


@dp.message_handler(filters.Command(commands=['schedule_week'], ignore_case=True))
async def schedule_week_command(message: types.Message):
    await week_schedule_message(message)


@dp.message_handler()
async def not_correct_command(message: types.Message):
    """Return to telegram-bot system-status"""
    await send_command_not_found(message)
