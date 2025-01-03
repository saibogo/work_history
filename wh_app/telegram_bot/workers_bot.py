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
