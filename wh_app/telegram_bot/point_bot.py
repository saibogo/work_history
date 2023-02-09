from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations import get_all_works_points, get_statistic, get_point, get_equip_in_point,\
    get_maximal_points_id

functions.info_string(__name__)


async def all_points(message: types.Message):
    """Return to telegram-bot all points"""
    with Database() as base:
        _, cursor = base
        points = get_all_works_points(cursor)
        msg = []
        for point in points:
            msg = msg + point_message(point)
        msg_del = await message.answer('\n'.join(msg))
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


def point_message(point: List[Any]) -> List[str]:
    """Create point-info message"""
    msg = list()
    msg.append(separator)
    msg.append('ID = {}'.format(point[0]))
    msg.append('{}'.format(point[1]))
    msg.append('Адрес {}'.format(point[2]))
    msg.append('{}'.format(point[3]))
    return msg


async def send_statistic(message: types.Message):
    """Return to telegram-bot statistic from all works"""
    with Database() as base:
        _, cursor = base
        stat = get_statistic(cursor)
        msg = []
        for line in stat:
            msg.append(separator)
            msg.append(line[1])
            msg.append('{} ед. обор.'.format(line[2]))
            msg.append('Всего работ {}'.format(line[3]))
            msg.append('Дата последней {}'.format(line[4]))
        msg_del = await message.answer('\n'.join(msg))
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


async def point_info(message: types.Message):
    """Return to telegram-bot information from point with current point_id"""
    with Database() as base:
        _, cursor = base
        point_id = message['text'].split()[1]
        found_error_data = False
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
            msg += point_message(point)
            equips = get_equip_in_point(cursor, point_id)
            msg.append('Перечень оборудования {} ед.:'.format(len(equips)))
            for equip in equips:
                msg += equip_message(equip)
        except IndexError:
            msg = ['Предприятие с ID = {} не найдено'.format(point_id)]
            found_error_data = True
        except KeyError:
            msg = [user_not_access_read(user_name)]
            found_error_data = True
        if not found_error_data:
            kb = [
                [InlineKeyboardButton(text='Новое оборудование (Point_ID={})'.format(point_id)),
                 InlineKeyboardButton(text='Отмена')]
            ]
        try:
            msg_del = await message.answer('\n'.join(msg))
            asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
            if not found_error_data:
                msg_del1 = await message.answer('Зарегистрировать новое оборудование?', reply_markup=standart_keyboard(kb))
                asyncio.create_task(delete_message(msg_del1, telegram_delete_message_pause))
        except aiogram.utils.exceptions.MessageIsTooLong:
            tmp = '\n'.join(msg)
            msg_dels = list()
            for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
                msg_dels.append(await message.answer(tmp[i : i + MAX_CHAR_IN_MSG]))
                asyncio.create_task(delete_message(msg_dels[-1], telegram_delete_message_pause))
            msg_del1 = await message.answer('Зарегистрировать новое оборудование?', reply_markup=standart_keyboard(kb))
            asyncio.create_task(delete_message(msg_del1, telegram_delete_message_pause))


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
            msg = [user_not_access_read(user_name)]
            msg_del = await message.answer('\n'.join(msg))
            asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
