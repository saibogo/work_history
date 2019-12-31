from tkinter import GROOVE


path_to_project = '/home/saibogo/PycharmProjects/work_history/'
database_name = 'workhistory'
user_name = 'saibogo'
user_password = 'begemot100'
database_host = '127.0.0.1'
database_port = '5432'
static_dir = path_to_project + 'wh_app/web/static/'
str_interrupted = 'Interrupted'
max_size_column = 40
rows_pxls = 25
max_pxls_in_canvas = 600
relief = GROOVE
ip_address = '192.168.6.242'
port = '5000'
full_address = "http://" + ip_address + ":" + port
pass_hash = 52380570359700838927303160461451880435941242634047643826816963312413378430196
max_records_in_page = 10

points_table = ['Название предприятия', 'Адрес предприятия', 'Текущий статус']
points_table_name = 'Зарегистрированные предприятия'

create_point_table = ['Введите название предприятия', 'Введите адрес предприятия']
create_point_name = 'Регистрация нового предприятия'

equips_table = ['Предприятие', 'Наименование', 'Модель', 'Серийник', 'ID ранее']
equips_table_name = 'Зарегистрированнное оборудование'

create_equip_table = ['Введите наименование оборудования', 'Введите марку оборудования(если есть)',
                      'Введите серийный номер(если есть)', 'Предыдущий ID(если есть)']
create_equip_name = 'Регистрация нового оборудования'

works_table = ['ID', 'Предприятие', 'Наименование', 'Модель', 'Номер', 'Дата', 'Заявка', 'Произведено', 'Исполнители']
works_table_name = 'Произведенные работы'

create_work_table_name = 'Регистрация нового ремонта'
create_work_table = ['Введите причину', 'Введите описание работ']

all_workers_table_name = 'Все зарегистрированные сотрудники'
workers_table = ['ID', 'Фамилия', 'Имя', 'Телефон', 'Статус', 'Должность']

find_like_name = 'Поиск по совпадениям'
find_like_table = ['Введите часть наименования оборудования']
find_like_table_points = ['Введите часть наименования предприятия']

statistics_table_name = 'Сборная статистика по предприятиям'
statistics_table = ['Предприятие', 'Единиц оборудования', 'Выполнено работ', 'Дата последних работ']

works_days_table_name = 'Распределение сотрудников по предприятиям'
works_days_table = ['Предприятие', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

alter_works_days_table_name = 'Дополнительные привязки'
alter_works_days_table = ['Предприятие', 'Дополнительные сотрудники']

max_width_for_date = 7
max_height_for_date = 6
