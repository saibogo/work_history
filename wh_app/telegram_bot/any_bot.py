from wh_app.telegram_bot.support_bot import *
from wh_app.supporting.system_status import SystemStatus

functions.info_string(__name__)


async def send_welcome(message: types.Message):
    """Create Hello-message in telegram bot"""
    msg_del = await message.reply("Привет!\nТелеграм-бот системы учета выполненных работ компании Малахит!\n" +
                                  "Список возможных команд /help")
    standart_delete_message(msg_del)


async def send_help(message: types.Message):
    """Return to telegram-bot HELP-message"""
    msg1 = ['/start -- запуск бота', '/help -- вызов данной справки', '/status -- получение статуса системы',
           '/statistic -- статистика работ', '/changelog -- просмотреть список изменений',
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