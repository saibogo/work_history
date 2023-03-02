from wh_app.telegram_bot.support_bot import *
from wh_app.sql_operations.select_operations import get_all_workers_real


functions.info_string(__name__)


async def send_workers_message(message: types.Message):
    """Create message all workers, when status is Worked"""
    try:
        user_id = message.from_id
        user_name = message.from_user
    except:
        user_name = 'User ID {}'.format(user_id)

    try:
        if user_name not in read_id_dict and user_id not in read_id_dict:
            raise KeyError
        with Database() as base:
            _, cursor = base
            workers = get_all_workers_real(cursor)
            workers_str = '\n'.join([worker_message(worker) for worker in workers])
            msg_del = await message.answer(workers_str)
            standart_delete_message(msg_del)
    except KeyError:
        msg_del = await message.answer(user_not_access_read(user_name))
        standart_delete_message(msg_del)


def worker_message(worker: List[Any]) -> str:
    """Template for worker-info message"""
    msg = list()
    msg.append(separator)
    msg.append('Сотрудник: {} {}'.format(worker[1], worker[2]))
    msg.append('Должность: {}'.format(worker[5]))
    msg.append('Телефон: {}'.format(worker[3]))
    return '\n'.join(msg)