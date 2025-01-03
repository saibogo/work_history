import datetime

from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations.select_operations import get_all_points_list_from_like_str,\
    get_all_equips_list_from_like_str, get_all_works_like_word, get_worker_id_from_name, get_all_works_from_worker_id,\
    get_all_works_like_word_and_date
from wh_app.telegram_bot.point_bot import point_message
from wh_app.telegram_bot.equip_bot import equip_message
from wh_app.telegram_bot.work_bot import work_message

functions.info_string(__name__)


@not_reader_decorator
async def main_find_menu(message: types.Message):
    """Create select-menu to new FIND"""

    msg_del = await message.answer('Переходим к поиску', reply_markup=ReplyKeyboardRemove())
    standart_delete_message(msg_del)
    kb = [
        [InlineKeyboardButton(text='Предприятие'),
        InlineKeyboardButton(text='Оборудование'),
        InlineKeyboardButton(text='Работы'),
        InlineKeyboardButton(text='Исполнители'),
        InlineKeyboardButton(text='Отмена')]
    ]
    msg_del1 = await message.answer('В каком разделе осуществить поиск?',
                                reply_markup=standart_keyboard(kb))
    standart_delete_message(msg_del1)


async def find_menu(message: types.Message, target: str):
    """Create find-message with point. Target in ['point', 'equip', 'work', 'performer']"""
    msg_del = await message.answer('Используйте функцию ответ на сообщение ниже и введите шаблон для поиска',
                                   reply_markup=ReplyKeyboardRemove())
    standart_delete_message(msg_del)
    if target == 'point':
        msg_del1 = await message.answer('/find_point Какое предприятие ищем?')
    elif target == 'equip':
        msg_del1 = await message.answer('/find_equip Какое оборудование ищем?')
    elif target == 'work':
        msg_del1 = await message.answer('/find_work Какие произведенные работы ищем?')
    elif target == 'performer':
        msg_del1 = await message.answer('/find_performer Имя или Фамилия сотрудника:')
    else:
        msg_del1 = await message.answer('Методика поиска не определена!')
    standart_delete_message(msg_del1)


async def find_repler(message: types.Message, target: str):
    """Reply to /find_point ... command. Target in ['point', 'equip', 'work', 'performer']"""
    pattern = message.text
    msgs = list()
    try:
        with Database() as base:
            _, cursor = base
            if target == 'point':
                find_result = get_all_points_list_from_like_str(cursor, pattern)
                msgs = ['\n'.join(point_message(point)) for point in find_result]
            elif target == 'equip':
                find_result = get_all_equips_list_from_like_str(cursor, pattern)
                msgs = ['\n'.join(equip_message(equip, True)) for equip in find_result]
            elif target == 'work':
                find_result = get_all_works_like_word(cursor, pattern)
                msgs = ['\n'.join(work_message(work, with_equip=True, with_point=True)) for work in find_result]
            elif target == 'performer':
                worker_id = get_worker_id_from_name(cursor, pattern)
                find_result = get_all_works_from_worker_id(cursor, worker_id)
                msgs = ['\n'.join(work_message(work)) for work in find_result]
            else:
                pass
            msg_del = await message.answer('\n'.join(msgs),reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)

    except (MessageIsTooLong, BadRequest) as e:
        msg_dels = list()
        tmp = '\n'.join(msgs)
        for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
            msg_dels.append(await message.answer(tmp[i: i + MAX_CHAR_IN_MSG]))
            standart_delete_message(msg_dels[-1])

    except MessageTextIsEmpty or IndexError:
        msg_del = await message.answer('Ничего не найдено!', reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)

    except NetworkError:
        msg_dels = list()
        tmp = '\n'.join(msgs)
        for i in range(len(tmp) - 5 * MAX_CHAR_IN_MSG, len(tmp), MAX_CHAR_IN_MSG):
            msg_dels.append(await message.answer(tmp[i: i + MAX_CHAR_IN_MSG]))
            standart_delete_message(msg_dels[-1])
        msg_del = await message.answer('Результатов слишком много!. Вывод был ограничен!',
                                       reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)


@not_reader_decorator
async def last_day_message(message: types.Message):
    """Create message, contain all works in last day"""

    try:
        with Database() as base:
            _, cursor = base
            current_datetime = datetime.datetime.now()
            stop_datetime = datetime.datetime(current_datetime.year, current_datetime.month, current_datetime.day,
                                             current_datetime.hour, current_datetime.minute, current_datetime.second)
            tmp_datetime  = datetime.datetime(stop_datetime.year, stop_datetime.month, stop_datetime.day)
            start_datetime = tmp_datetime - datetime.timedelta(days=1)
            works = get_all_works_like_word_and_date(cursor, '', str(start_datetime), str(stop_datetime))
            msgs = ['\n'.join(work_message(work, True, True)) for work in works]
            msg_del = await message.answer('\n'.join(msgs), reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)

    except MessageTextIsEmpty or IndexError:
        msg_del = await message.answer('Ничего не найдено!', reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)
    except MessageIsTooLong:
        msg_dels = list()
        tmp = '\n'.join(msgs)
        for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
            msg_dels.append(await message.answer(tmp[i: i + MAX_CHAR_IN_MSG]))
            standart_delete_message(msg_dels[-1])

