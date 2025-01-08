import datetime

from wh_app.telegram_bot.support_bot import *
from wh_app.config_and_backup import table_headers
from wh_app.sql_operations.select_operations.select_operations import get_all_workers_real, get_schedule_to_date


functions.info_string(__name__)


@not_reader_decorator
async def send_workers_message(message: types.Message):
    """Create message all workers, when status not fired"""
    with Database() as base:
        _, cursor = base
        workers = get_all_workers_real(cursor)
        workers_str = '\n'.join([worker_message(worker) for worker in workers])
        msg_del = await message.answer(workers_str)
        standart_delete_message(msg_del)


def worker_message(worker: List[Any]) -> str:
    """Template for worker-info message"""
    msg = list()
    msg.append(separator)
    msg.append('Сотрудник: {} {}'.format(worker[1], worker[2]))
    msg.append('Текущий статус: {}'.format(worker[4]))
    msg.append('Должность: {}'.format(worker[5]))
    msg.append('Телефон: {}'.format(worker[3]))
    return '\n'.join(msg)


async def today_schedule_message(message: types.Message):
    """Create message with all workers who works today"""
    with Database() as base:
        _, cursor = base
        today_date = str(datetime.date.today())
        msg = list()
        schedule_list = get_schedule_to_date(cursor, today_date)
        for worker in schedule_list:
            msg.append(separator)
            for i in range(len(table_headers.schedule_table)):
                msg.append('{}: {}'.format(table_headers.schedule_table[i], worker[i]))
        msg_del = await message.answer('\n'.join(msg))
        standart_delete_message(msg_del)


async def week_schedule_message(message: types.Message):
    """Create message with all workers who works today and +7 days"""
    try:
        with Database() as base:
            _, cursor = base
            msg = list()
            for i in range(7):
                msg.append(separator)
                today_date = str(datetime.date.today() + datetime.timedelta(days=i))
                schedule_list = get_schedule_to_date(cursor, today_date)
                for worker in schedule_list:
                    msg.append(separator)
                    for i in range(len(table_headers.schedule_table)):
                        msg.append('{}: {}'.format(table_headers.schedule_table[i], worker[i]))
            msg_del = await message.answer('\n'.join(msg))
            standart_delete_message(msg_del)
    except (MessageIsTooLong, BadRequest) as e:
        msg_dels = list()
        tmp = '\n'.join(msg)
        for i in range(0, len(tmp), MAX_CHAR_IN_MSG):
            msg_dels.append(await message.answer(tmp[i: i + MAX_CHAR_IN_MSG]))
            standart_delete_message(msg_dels[-1])

    except MessageTextIsEmpty or IndexError:
        msg_del = await message.answer('Ничего не найдено!', reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)

    except NetworkError:
        msg_dels = list()
        tmp = '\n'.join(msg)
        for i in range(len(tmp) - 5 * MAX_CHAR_IN_MSG, len(tmp), MAX_CHAR_IN_MSG):
            msg_dels.append(await message.answer(tmp[i: i + MAX_CHAR_IN_MSG]))
            standart_delete_message(msg_dels[-1])
        msg_del = await message.answer('Результатов слишком много!. Вывод был ограничен!',
                                       reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)
