"""This module contain metadata for all project"""

__author__ = "Andrey Gleykh"
__license__ = "GPL v.2.0"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"
__version__ = "0.44.1"

CHANGELOG = [
    ("0.8.2", "Изменена навигация по страницам с большим количеством записей"),
    ("0.8.3", "Внедрен просмотр реализованных изменений в программе"),
    ("0.8.4", "Добавлена возможность редактирования сведений об оборудовании"),
    ("0.9.1", "Реализована возможность перемещения оборудования между предприятиями"),
    ("0.9.5", "Добавлен просмотр перемещений оборудования между предприятиями"),
    ("0.10.2", "Начат перевод GUI с tkinter на PyQt5"),
    ("0.10.9", "Начата реализация ограничения доступа к системе"),
    ("0.10.12", "Введено ограничение по максимальной длительности сессии без активности (6 часов)"),
    ("0.10.14", "Удалены все зависимости от tkinter"),
    ('0.10.20', 'Начата реализация возможности сохранения выборки в документы PDF'),
    ('0.10.24', 'В раздел READMI добавлена информация о полной структуре всех таблиц и представлений'),
    ('0.11.1', 'Добавлена возможность редактирования содержимого выполненных работ'),
    ('0.12.1', 'Добавлено отображение технических параметров предприятия'),
    ('0.13.0', 'Добавлено отображение схем вводных устройств электроснабжения'),
    ('0.13.3', 'Добавлена возможность изменения времени окончания в отчете о произведенной работе'),
    ('0.13.29', 'Большая часть создания HTML переведена на автоматическую генерацию из шаблонов'),
    ('0.14.0', 'Начата интеграция с мессенджером Telegram'),
    ('0.15.0', 'Реализованы просмотр, добавление оборудования и работ через Telegram-бот'),
    ('0.16.0', 'Реализован необходимый минимум для работы через Telegram-бот'),
    ('0.16.6', 'Реализован механизм загрузки данных конфигурации системы "на лету"'),
    ('0.16.16', 'Начат перевод WEB-интерфейса на технологию FlexBox и CSS Grid'),
    ('0.17.0', 'Полностью удалены таблицы в веб-секции приложения'),
    ('0.18.1', 'Начата переработка и дополнение интерфейса'),
    ('0.18.20', 'Начата замена части функций приложения на функции базы данных'),
    ('0.19.0', 'Удаление лишних таблиц в базе данных'),
    ('0.19.8', 'В багтрекер добавлены дата регистрации и дата закрытия проблемы'),
    ('0.20.0', 'Начата работа по удалению десктопного приложения из системы'),
    ('0.20.16', 'Переработан вывод больших сообщений при использовании /find в telegram-боте'),
    ('0.21.00', 'Добавлена возможность принимать сотрудников в web-интерфейсе'),
    ('0.21.20', 'Работа WEB-версии приложения переведена на протокол HTTPS'),
    ('0.21.25', 'Все данные о телеграмм-контактах перенесены в базу данных'),
    ('0.23.0', 'полностью удалена десктопная версия приложения'),
    ('0.24.1', 'Введены статусы предприятий: Работает, Закрыто, Реконструкция'),
    ('0.24.8', 'Модифицирована статистика по оборудованию. Теперь не учитываются списки в неработающих предприятиях и списанное оборудование'),
    ('0.24.12', 'Реализовано сохранение структуры базы без данных'),
    ('0.24.15', 'Реализован постраничный вывод изменений в системе'),
    ('0.25.2', 'В веб-версию добавлено подменю с допсервисами. Добавлено получение информации о планируемых отключениях'),
    ('0.26.2', 'Начата реализация отображения текущего графика сотрудников'),
    ('0.26.13', 'Основная часть команд телеграмм бота отныне нечувствительна к регистру символов'),
    ('0.26.16', 'Реализован просмотр планируемых отключений электроэнергии посредством телеграмм-бота'),
    ('0.27.7', 'Релизовано хранение сведений о приборах учета энергоресурсов, показаниях ПУ и привязки ПУ к предприятиям'),
    ('0.28.0', 'Добавлена возможность просмотра приборов учета в телеграмм-боте, а также добавление показаний через него'),
    ('0.28.12', 'Переработана система предоставления прав к просмотрам и созданию записей'),
    ('0.29.0', 'Добавлено оповещение через телеграмм бот о новых заявках'),
    ('0.29.17', 'Функции расчета аналитики для приборов учета перенесены в базу данных'),
    ('0.29.25', 'Все SELECT операции с базой данных разнесены по разделам, соответствующим назначению запросов'),
    ('0.30.6', 'Переработана система авторизации'),
    ('0.40.2', 'Реализована система хранения деталировок а также их отдача через веб-интерфейс и через телеграм-бот'),
    ('0.40.27', 'Все SQL-запросы разделены по файловой структуре соотвествующей тематике запросов'),
    ('0.40.36', 'Начата работа по удалению привязок сотрудников к предприятиям'),
    ('0.40.43', 'Реализована иерархия предприятий и методика их отображения'),
    ('0.44.1', 'Реализовано хранение и отдача действующих профилей мощности приборов учета')
]
