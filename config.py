from tkinter import GROOVE, FLAT, RAISED, SUNKEN, RIDGE

database_name = '/home/saibogo/PycharmProjects/work_history/malachite_works.db'
str_interrupted = 'Interrupted'
max_size_column = 40
rows_pxls = 25
max_pxls_in_canvas = 600
relief = GROOVE
ip_address = '192.168.6.242'
port = '5000'
full_address = "http://" + ip_address + ":" + port
pass_hash = 52380570359700838927303160461451880435941242634047643826816963312413378430196

points_table = ['Название предприятия', 'Адрес предприятия']
points_table_name = 'Зарегистрированные предприятия'

create_point_table = ['Введите название предприятия', 'Введите адрес предприятия']
create_point_name = 'Регистрация нового предприятия'

equips_table = ['Предприятие', 'Наименование', 'Модель', 'Серийник', 'ID ранее']
equips_table_name = 'Зарегистрированнное оборудование'

create_equip_table = ['Введите наименование оборудования', 'Введите марку оборудования(если есть)',
                      'Введите серийный номер(если есть)', 'Предыдущий ID(если есть)']
create_equip_name = 'Регистрация нового оборудования'

works_table = ['Предприятие', 'Наименование', 'Модель', 'Номер', 'Дата', 'Заявка', 'Произведено']
works_table_name = 'Произведенные работы'

create_work_table_name = 'Регистрация нового ремонта'
create_work_table = ['Введите причину', 'Введите описание работ']

find_like_name = 'Поиск по совпадениям'
find_like_table = ['Введите часть наименования оборудования']
find_like_table_points = ['Введите часть наименования предприятия']

max_width_for_date = 7
max_height_for_date = 6
