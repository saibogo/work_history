from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations.select_operations import get_all_bugz_in_bugzilla, get_bug_by_id,\
    get_all_bugz_in_work_in_bugzilla
from wh_app.sql_operations.insert_operation.insert_operations import add_new_bug_in_bugzilla
from wh_app.sql_operations.update_operations.update_operations import invert_bug_status_in_bugzilla

functions.info_string(__name__)


@not_reader_decorator
async def all_bugs(message: types.Message):
    """Return to telegram-bot all bugs"""
    with Database() as base:
        _, cursor = base
        bugs = get_all_bugz_in_bugzilla(cursor)
        msg = list()
        for bug in bugs:
            msg.append(bug_message(bug))
        try:
            msg_del = await message.answer('\n'.join(msg))
            standart_delete_message(msg_del)
        except (MessageIsTooLong, BadRequest) as e:
            tmp = '\n'.join(msg)
            msg_dels = list()
            for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
                msg_dels.append(await message.answer(tmp[i: i + MAX_CHAR_IN_MSG]))
                standart_delete_message(msg_dels[-1])
        kb = [
            [InlineKeyboardButton(text='Новая проблема'),
             InlineKeyboardButton(text='Отмена')]
        ]
        msg_del1 = await message.answer('Зарегистрировать новую проблему?', reply_markup=standart_keyboard(kb))
        standart_delete_message(msg_del1)


@not_reader_decorator
async def all_no_closed_bugs(message: types.Message):
    """Return to telegram-bot all bugs"""
    with Database() as base:
        _, cursor = base
        bugs = get_all_bugz_in_work_in_bugzilla(cursor)
        msg = list()
        for bug in bugs:
            msg.append(bug_message(bug))
        try:
            msg_del = await message.answer('\n'.join(msg))
            standart_delete_message(msg_del)
        except (MessageIsTooLong, BadRequest) as e:
            tmp = '\n'.join(msg)
            msg_dels = list()
            for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
                msg_dels.append(await message.answer(tmp[i: i + MAX_CHAR_IN_MSG]))
                standart_delete_message(msg_dels[-1])
        kb = [
            [InlineKeyboardButton(text='Новая проблема'),
             InlineKeyboardButton(text='Отмена')]
        ]
        msg_del1 = await message.answer('Зарегистрировать новую проблему?', reply_markup=standart_keyboard(kb))
        standart_delete_message(msg_del1)


def bug_message(bug: List[Any]) -> str:
    """Create standart message from bug"""
    msg = list()
    msg.append(separator)
    msg.append('\nID = {}\n'.format(bug[0]))
    msg.append('Описание: {}\n'.format(bug[1]))
    msg.append('Статус: {}\n'.format(bug[2]))
    msg.append('Дата регистрации: {}\n'.format(bug[3]))
    if len(bug) > 4 and bug[4]:
        msg.append('Дата закрытия: {}\n'.format(bug[4]))
    return ''.join(msg)


@not_writer_decorator
async def start_create_new_bug(message: types.Message):
    """Start registration new bug"""
    with Database() as base:
        _, cursor = base
        msg_del = await message.answer('Начинаем регистрацию работ новой проблемы\n'
                                    'Используйте функцию ОТВЕТ на сообщение ниже и проблема будет записана',
                                    reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)
        msg_del1 = await message.answer('/new_bug\nОписание проблемы')
        standart_delete_message(msg_del1)


@not_writer_decorator
async def new_bug_repler(message: types.Message):
    """Handler to reply message /new_bug"""
    user_id = get_user_id(message)
    worker_id = get_malachite_id(user_id)
    if worker_id is None:
        msg_del = await message.answer(write_not_access)
        standart_delete_message(msg_del)
    else:
        with Database() as base:
            connection, cursor = base
            add_new_bug_in_bugzilla(cursor, message.text)
            connection.commit()
            msg_del = await message.answer('Создано новое обращение!')
            standart_delete_message(msg_del)


@not_reader_decorator
async def bug_from_bug_id(message: types.Message):
    """Create message with bug = bug_id"""
    with Database() as base:
        _, cursor = base
        try:
            bug_id = message.text.split()[1]
            msg = bug_message(get_bug_by_id(cursor, bug_id))
            msg_del = await message.answer(msg, reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del)
            kb = [
                [InlineKeyboardButton(text='Изменить статус ID={}'.format(bug_id)),
                 InlineKeyboardButton(text='Отмена')]
            ]
            msg_del1 = await message.answer('Изменить статус проблемы?', reply_markup=standart_keyboard(kb))
            standart_delete_message(msg_del1)
        except IndexError:
            msg = "Проблема с таким номером отсутствует в базе данных!"
            msg_del = await message.answer(msg)
            standart_delete_message(msg_del)


@not_writer_decorator
async def invert_bug_status_from_bot(message: types.Message):
    """ON-OFF bug status in database"""
    with Database() as base:
        connection, cursor = base
        bug_id = message.text.split('ID=')[1]
        try:
            invert_bug_status_in_bugzilla(cursor, bug_id)
            connection.commit()
            msg_del = await message.answer('Статус проблемы изменен!')
            standart_delete_message(msg_del)
            msg = bug_message(get_bug_by_id(cursor, bug_id))
            msg_del1 = await message.answer(msg, reply_markup=ReplyKeyboardRemove())
            standart_delete_message(msg_del1)
            kb = [
                [InlineKeyboardButton(text='Изменить статус ID={}'.format(bug_id)),
                    InlineKeyboardButton(text='Отмена')]
            ]
            msg_del2 = await message.answer('Изменить статус проблемы?', reply_markup=standart_keyboard(kb))
            standart_delete_message(msg_del2)
        except IndexError:
            msg = "Проблема с таким номером отсутствует в базе данных!"
            msg_del = await message.answer(msg)
            standart_delete_message(msg_del)

