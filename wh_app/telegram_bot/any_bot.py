from wh_app.telegram_bot.support_bot import *
from wh_app.supporting.system_status import SystemStatus
from wh_app.sql_operations.select_operations import get_top_10_works, get_top_10_points, get_top_10_workers
from wh_app.config_and_backup.table_headers import top_10_points_name, top_10_points, top_10_equips_name, top_10_equips,\
    top_10_workers_table_name, top_10_workers_table

functions.info_string(__name__)


async def send_welcome(message: types.Message):
    """Create Hello-message in telegram bot"""
    msg_del = await message.reply("Привет!\nТелеграм-бот системы учета выполненных работ компании Малахит!\n" +
                                  "Список возможных команд /help")
    standart_delete_message(msg_del)


async def send_help(message: types.Message):
    """Return to telegram-bot HELP-message"""
    msg1 = ['/start -- запуск бота', '/help -- вызов данной справки', '/status -- получение статуса системы',
           '/statistic -- статистика работ','/top10 - список обьектов и оборудования с самым большим количеством работ',
            '/changelog -- просмотреть список изменений',
            '/points -- все зарегистрированные предприятия']
    msg2 = ['<b><i>Внимание! Следующие команды требуют Разрешения на чтение.</i></b>',
            '<b><i><u>&lt;Параметр&gt;</u> обозначает число и вводится через пробел</i></b>']
    msg3 = ['/bugs -- Известные проблемы с системой',
           '/bug <bug_ID> -- Перейти к конкретной проблеме',
            '/workers -- текущий список сотрудников технической службы',
            '/find -- перейти в меню поиска по базе данных',
            '/lastday -- все работы с начала предыдущих суток',
           '/point <point ID> -- перейти к предприятию с данным ID',
           '/svu <point ID> -- Получить схему вводного устройства предприятия, если она имеется в базе',
            '/tech <point ID> --сводная техническая информация по обьекту(если есть в системе)',
           '/equip <equip_id> all -- перейти к нужной единице оборудования и показать ВСЕ произведенные работы',
           '/equip <equip_id> -- перейти к нужной единице оборудования и показать только последние 20 действий',
            '/work <work_id> -- вывести информацию о работе с заданным ID']
    msg4 = ['<b><i>Регистрация нового оборудования, работ и проблем возможна только,',
            'если вы имеете разрешение на запись данных',
           'Внимание! Сообщения бота автоматически удаляются из чата через 2 часа после публикации.</i></b>']
    msg_dels = []
    msg_dels.append(await message.answer("\n".join(msg1), reply_markup=ReplyKeyboardRemove()))
    msg_dels.append(await message.answer("\n".join(msg2), parse_mode='HTML'))
    msg_dels.append(await message.answer("\n".join(msg3)))
    msg_dels.append(await message.answer("\n".join(msg4), parse_mode='HTML'))
    for elem in msg_dels:
        standart_delete_message(elem)


async def send_status(message: types.Message):
    """Return to telegram-bot system-status"""
    msg = ['{0}: {1}\n'.format(key, SystemStatus.get_status()[key]) for key in SystemStatus.get_status()]
    msg_del = await message.answer("".join(msg), reply_markup=ReplyKeyboardRemove())
    standart_delete_message(msg_del)


async def send_command_not_found(message: types.Message):
    """Return to telegram-bot system-status"""
    print(message)
    msg_del = await message.answer('Команда {} некорректна'.format(message.text), reply_markup=ReplyKeyboardRemove())
    standart_delete_message(msg_del)


async def send_changelog(message: types.Message):
    """Return all changelog"""
    changelog = functions.metadata.CHANGELOG
    msg = ('\n' + separator + '\n').join(['\n'.join(elem) for elem in changelog])
    msg_del = await message.answer(msg, reply_markup=ReplyKeyboardRemove())
    standart_delete_message(msg_del)


def create_message_for_top(header_name: str, header: List[str], data: List[Any]) -> str:
    """Create any part in top10 reply-message"""
    msg = [header_name]
    for elem in data:
        msg.append(separator)
        for i in range(len(header)):
            msg.append("{}: {}".format(header[i], elem[i]))
    return '\n'.join(msg)


async def send_top10(message: types.Message):
    """Return to telegram-bot top-10 equips and points with maximal works"""
    with Database() as base:
        _, cursor = base
        top_points = get_top_10_points(cursor)
        top_equips = get_top_10_works(cursor)
        top_workers = get_top_10_workers(cursor)

        msg_points = create_message_for_top(top_10_points_name, top_10_points, top_points)
        msg_equips = create_message_for_top(top_10_equips_name, top_10_equips, top_equips)
        msg_workers = create_message_for_top(top_10_workers_table_name, top_10_workers_table, top_workers)

        msg_del = await message.answer(msg_points, reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)
        msg_del1 = await message.answer(msg_equips, reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del1)
        msg_del2 = await message.answer(msg_workers, reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del2)