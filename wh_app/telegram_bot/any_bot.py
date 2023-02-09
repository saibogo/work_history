from wh_app.telegram_bot.support_bot import *
from wh_app.supporting.system_status import SystemStatus

functions.info_string(__name__)


async def send_welcome(message: types.Message):
    """Create Hello-message in telegram bot"""
    msg_del = await message.reply("Привет!\nТелеграм-бот системы учета выполненных работ компании Малахит!\n" +
                                  "Список возможных команд /help")
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


async def send_help(message: types.Message):
    """Return to telegram-bot HELP-message"""
    msg = ['/start -- запуск бота', '/help -- вызов данной справки', '/status -- получение статуса системы',
           '/statistic -- статистика работ', '/points -- все зарегистрированные предприятия',
           '/bugs -- Известные проблемы с системой',
           'Внимание! Следующие команды требуют Разрешения на чтение.',
           '<Параметр> обозначает число и вводится через пробел',
           '/point <point ID> -- перейти к предприятию с данным ID',
           '/svu <point ID> -- Получить схему вводного устройства предприятия, если она имеется в базе',
           '/equip <equip_id> f -- перейти к нужной единице оборудования и показать ВСЕ произведенные работы',
           '/equip <equip_id> -- перейти к нужной единице оборудования и показать только последние 20 действий',
           'Регистрация новых работ возможна только, если вы имеете разрешение на запись данных',
           'Внимание! Сообщения бота автоматически удаляются из чата через 2 часа после публикации.']
    msg_del = await message.answer("\n".join(msg))
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


async def send_status(message: types.Message):
    """Return to telegram-bot system-status"""
    msg = ['{0}: {1}\n'.format(key, SystemStatus.get_status()[key]) for key in SystemStatus.get_status()]
    msg_del = await message.answer("".join(msg))
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))


async def send_command_not_found(message: types.Message):
    """Return to telegram-bot system-status"""
    print(message)
    msg_del = await message.answer('Команда {} некорректна'.format(message['text']))
    asyncio.create_task(delete_message(msg_del, telegram_delete_message_pause))