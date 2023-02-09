from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations import get_all_bugz_in_bugzilla
from wh_app.sql_operations.insert_operations import add_new_bug_in_bugzilla

functions.info_string(__name__)


async def all_bugs(message: types.Message):
    """Return to telegram-bot all bugs"""
    with Database() as base:
        _, cursor = base
        bugs = get_all_bugz_in_bugzilla(cursor)
        msg = list()
        for bug in bugs:
            msg.append(separator)
            msg.append('ID = {}'.format(bug[0]))
            msg.append('Описание: {}'.format(bug[1]))
            msg.append('Статус: {}'.format(bug[2]))
        msg_del = await message.answer('\n'.join(msg))
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
        kb = [
            [InlineKeyboardButton(text='Новая проблема'),
             InlineKeyboardButton(text='Отмена')]
        ]
        msg_del1 = await message.answer('Зарегистрировать новую проблему?', reply_markup=standart_keyboard(kb))
        asyncio.create_task(delete_message(msg_del1, telegram_delete_message_pause))


async def start_create_new_bug(message: types.Message):
    """Start registration new bug"""
    with Database() as base:
        _, cursor = base
        msg_del = await message.answer('Начинаем регистрацию работ новой проблемы\n'
                                       'Используйте функцию ОТВЕТ на сообщение ниже и проблема будет записана',
                                       reply_markup=ReplyKeyboardRemove())
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
        msg_del1 = await message.answer('/new_bug\nОписание проблемы')
        asyncio.create_task(delete_message(msg_del1, telegram_delete_message_pause))


async def new_bug_repler(message: types.Message):
    """Handler to reply message /new_bug"""
    user_id = get_user_id(message)
    worker_id = get_malachite_id(user_id)
    if worker_id is None:
        msg_del = await message.answer(write_not_access)
        asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))
    else:
        with Database() as base:
            connection, cursor = base
            add_new_bug_in_bugzilla(cursor, message.text)
            connection.commit()
            msg_del = await message.answer('Создано новое обращение!')
            asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))