from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations import get_all_no_closed_orders, get_order_from_id

functions.info_string(__name__)


async def all_noclosed_orders(message: types.Message):
    """Return to telegram-bot all no-closed orders"""
    with Database() as base:
        _, cursor = base
        orders = get_all_no_closed_orders(cursor)
        msg = list()
        for order in orders:
            msg.append(order_message(order))
        try:
            msg_del = await message.answer('\n'.join(msg))
            standart_delete_message(msg_del)
        except aiogram.utils.exceptions.MessageIsTooLong:
            tmp = '\n'.join(msg)
            msg_dels = list()
            for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
                msg_dels.append(await message.answer(tmp[i: i + MAX_CHAR_IN_MSG]))
                standart_delete_message(msg_dels[-1])


async def order_from_id(message: types.Message):
    """Return to telegram-bot order with ID = order_id"""
    with Database() as base:
        _, cursor = base
        order_id  = message.text.split()[1]
        try:
            order = get_order_from_id(cursor, order_id)
            msg = order_message(order)
            msg_del = await message.answer(msg)
            standart_delete_message(msg_del)
        except IndexError:
            msg_del = await message.answer('Заявка с данным ID не найдена')
            standart_delete_message(msg_del)


def order_message(order: List[Any]) -> str:
    """Create standart message from order"""
    msg = list()
    msg.append(separator)
    msg.append('\nID = {}\n'.format(order[0]))
    msg.append('Предприятие: {}\n'.format(order[1]))
    msg.append('Заявку создал: {}\n'.format(order[2]))
    msg.append('Дата регистрации: {}\n'.format(order[3].strftime('%Y-%m-%d %H:%M:%S')))
    if order[4]:
        msg.append('Дата закрытия: {}\n'.format(order[4].strftime('%Y-%m-%d %H:%M:%S')))
    msg.append('Заявка: {}\n'.format(order[5]))
    msg.append('Текущий статус: {}\n'.format(order[6]))
    if order[7]:
        msg.append('Комментарий: {}\n'.format(order[7]))
    return ''.join(msg)