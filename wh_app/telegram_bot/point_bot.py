from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations import get_all_works_points, get_statistic, get_point, get_equip_in_point,\
    get_maximal_points_id,  get_electric_point_info, get_heating_point_info, get_sewerage_point_info,\
    get_hot_water_point_info, get_cold_water_point_info, get_full_point_information
from wh_app.config_and_backup.table_headers import point_tech_table
from wh_app.supporting.functions import get_technical_info

functions.info_string(__name__)


async def all_points(message: types.Message):
    """Return to telegram-bot all points"""
    with Database() as base:
        _, cursor = base
        points = get_all_works_points(cursor)
        msg = []
        for point in points:
            msg = msg + point_message(point)
        msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)


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
        msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)


async def point_info(message: types.Message):
    """Return to telegram-bot information from point with current point_id"""
    with Database() as base:
        _, cursor = base
        point_id = message.text.split()[1]
        found_error_data = False
        try:
            user_id = message.from_id
            user_name = message.from_user
        except:
            user_name = 'User ID {}'.format(user_id)
        try:
            if not is_telegram_user_reader(cursor, user_id):
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
            standart_delete_message(msg_del)
            if not found_error_data:
                msg_del1 = await message.answer('Зарегистрировать новое оборудование?', reply_markup=standart_keyboard(kb))
                standart_delete_message(msg_del1)
        except MessageIsTooLong:
            tmp = '\n'.join(msg)
            msg_dels = list()
            for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
                msg_dels.append(await message.answer(tmp[i : i + MAX_CHAR_IN_MSG]))
                standart_delete_message(msg_dels[-1])
            msg_del1 = await message.answer('Зарегистрировать новое оборудование?', reply_markup=standart_keyboard(kb))
            standart_delete_message(msg_del1)


async def get_svu(message: types.Message):
    """Return to telegram-bot SVU-file from selected point"""
    with Database() as base:
        _, cursor = base
        point_id = int(message.text.split()[1])
        try:
            user_id = message.from_id
            user_name = message.from_user
        except:
            user_name = 'User ID {}'.format(user_id)
        try:
            if not is_telegram_user_reader(cursor, user_id):
                raise KeyError
            if point_id > int(get_maximal_points_id(cursor)) or point_id < 1:
                raise IndexError
            try:
                doc = open('{}wh_app/web/static/image/svu/svu_{}.jpg'.format(path_to_project(), point_id), 'rb')
                msg_del = await message.reply_document(doc)
                standart_delete_message(msg_del)
            except FileNotFoundError:
                msg_del = await message.answer('Схема Вводного Устройства для Предприятия с ID = {} не найдена'.format(point_id),
                                               reply_markup=ReplyKeyboardRemove())
                standart_delete_message(msg_del)
        except IndexError:
            msg = ['Предприятие с ID = {} не найдено\n Перечень предприятий /points'.format(point_id)]
            msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)
        except KeyError:
            msg = [user_not_access_read(user_name)]
            msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)


async def get_tech_info(message: types.Message):
    """Return technical information from workpoint"""
    with Database() as base:
        _, cursor = base
        point_id = int(message.text.split()[1])
        try:
            user_id = message.from_id
            user_name = message.from_user
        except:
            user_name = 'User ID {}'.format(user_id)
        try:
            if not is_telegram_user_reader(cursor, user_id):
                raise KeyError
            if point_id > int(get_maximal_points_id(cursor)) or point_id < 1:
                raise IndexError
            msg = list()
            point_name = get_full_point_information(cursor, str(point_id))[0]
            msg.append('Сводная техническая информация для {}'.format(point_name))
            msg.append(separator)
            list_info = get_technical_info(point_id)
            for i in range(len(list_info)):
                msg.append(separator)
                msg.append(point_tech_table[i + 1])
                msg. append('Договор: {}'.format(list_info[i][2]))
                msg.append('Описание: {}'.format(list_info[i][3]))
            msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)
        except IndexError:
            msg = ['Предприятие с ID = {} не найдено\n Перечень предприятий /points'.format(point_id)]
            msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)
        except KeyError:
            msg = [user_not_access_read(user_name)]
            msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)