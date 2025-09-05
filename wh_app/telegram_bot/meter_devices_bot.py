from typing import Tuple
import datetime
import os.path

from wh_app.telegram_bot.support_bot import *
from wh_app.config_and_backup import config
from wh_app.sql_operations.select_operations.select_operations import get_point, get_all_worked_meter_in_point,\
    get_last24_date_and_readings_from_device, get_full_info_from_meter_device
from wh_app.sql_operations.insert_operation.insert_operations import insert_new_reading_to_meter_device
from wh_app.sql_operations.update_operations.update_operations import update_meter_reading
from wh_app.config_and_backup.table_headers import meter_devices_table, small_readings_table, small_readings_table_name


functions.info_string(__name__)


@not_writer_decorator
async def start_view_meter_devices(message: types.Message):
    """Return message with all worked meter devices in point"""

    with Database() as base:
        _, cursor = base
        first_num = message.text.index('=')
        last_num = message.text.index(')')
        point_id = message.text[first_num + 1: last_num]
        point = get_point(cursor, point_id)
        if len(point) == 0:
            msg = ['Предприятие с таким ID не обнаружено']
        else:
            devices = get_all_worked_meter_in_point(cursor, point_id)
            if len(devices) == 0:
                msg = ['Действующих приборов учета на данном предприятии не зарегистрировано']
            else:
                msg = [point[0][1]]
                for device in devices:
                    msg.append(_device_info_message(device))
                msg.append(separator)
                msg.append('Для выбора прибора учета используйте команду /pu <device_id>, где <device_id> - id прибора')
        msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)


@not_writer_decorator
async def start_view_reading_meter_device(message: types.Message):
    """Return message with all reading to current meter device"""

    with Database() as base:
        _, cursor = base
        found_error = False
        try:
            full_command = message.text.split()
            device_id = full_command[1]
            readings = get_last24_date_and_readings_from_device(cursor, device_id)
            device_info = get_full_info_from_meter_device(cursor, device_id)
            if len(device_info) == 0:
                msg = ['Прибор учета с таким ID в базе данных не зарегистрирован']
                found_error = True
            else:
                msg = [small_readings_table_name.format(device_info[0][3] + ' ' + device_info[0][2],
                                                        device_info[0][10], device_info[0][1])]
                msg.append(separator)
                for reading in readings:
                    for i in range(len(small_readings_table)):
                        msg.append('{}: {}'.format(small_readings_table[i], reading[i]))
                    msg.append(separator)

                pp_filename = '{}power_profiles/{}_pp.pdf'.format(config.static_dir(), device_id)
                pp_exist = os.path.exists(pp_filename) and os.path.isfile(pp_filename)
                kb = [[InlineKeyboardButton(text='Внести показания (ID={})'.format(device_id))]]
                if pp_exist:
                    kb[0].append(InlineKeyboardButton(text='Профиль мощности (ID={})'.format(device_id)))
                kb[0].append(InlineKeyboardButton(text='Отмена'))
        except IndexError:
            msg = ['Неверный формат команды /pu <device_id>']
            found_error = True
        msg_del = await message.answer('\n'.join(msg), reply_markup=ReplyKeyboardRemove())
        standart_delete_message(msg_del)
        if not found_error:
            msg_del1 = await message.answer('Зарегистрировать показания на текущую дату?',
                                            reply_markup=standart_keyboard(kb))
            standart_delete_message(msg_del1)


@not_writer_decorator
async def start_create_readings_record(message: types.Message):
    """Start new message to insert new readind in meter device history"""
    with Database() as base:
        _, cursor = base
        index1 = message.text.find('ID=')
        if index1 == -1:
            msg_del = await  message.answer('Некорректный запрос на внесение показаний!',
                                            reply_markup=ReplyKeyboardRemove())
        else:
            index2 = message.text.find(')', index1 + 3)
            if index2 == -1:
                msg_del = await  message.answer('Некорректный запрос на внесение показаний!',
                                                reply_markup=ReplyKeyboardRemove())
            else:
                device_id = message.text[index1 + 3:index2]
                msg_del = await message.answer('Начинаем регистрацию показаний по прибору учета ID = {}\n'
                                               'Используйте функцию ОТВЕТ на сообщение ниже и показания будут проверены и записаны.\n'
                                               'Показания вводятся в формате только цифрами. Дробная часть отделяется точкой'.
                                               format(device_id),
                                               reply_markup=ReplyKeyboardRemove())
                msg_del1 = await message.answer('/new_reading_id_{}\nНовые показания'.format(device_id))
                standart_delete_message(msg_del1)
        standart_delete_message(msg_del)


@not_writer_decorator
async def get_profile_file_start(message: types.Message):
    """If profile exist then get file to user"""
    index1 = message.text.find('ID=')
    if index1 == -1:
        msg_del = await  message.answer('Некорректный запрос профиля мощности!',
                                        reply_markup=ReplyKeyboardRemove())
    else:
        index2 = message.text.find(')', index1 + 3)
        if index2 == -1:
            msg_del = await  message.answer('Некорректный запрос профиля мощности!',
                                            reply_markup=ReplyKeyboardRemove())
        else:
            device_id = message.text[index1 + 3:index2]
            try:
                doc = open('{}wh_app/web/static/power_profiles/{}_pp.pdf'.format(path_to_project(), device_id), 'rb')
                msg_del = await message.reply_document(doc)
                standart_delete_message(msg_del)
            except FileNotFoundError:
                msg_del = await message.answer(
                    'Действующий профиль мощности для прибора учета с  ID = {} не найден'.format(device_id),
                    reply_markup=ReplyKeyboardRemove())
                standart_delete_message(msg_del)
    standart_delete_message(msg_del)


@not_writer_decorator
async def new_reading_repler(message: types.Message):
    """Handler to reply message /new_reading_id"""
    incorrect_data_found = False
    index1 = message.reply_to_message.text.find('id_')
    if index1 == -1:
        incorrect_data_found = True
    else:
        index2 = message.reply_to_message.text.find('\n', index1 + 3)
        if index2 == -1:
            incorrect_data_found = True
        else:
            device_id_raw = message.reply_to_message.text[index1 + 3: index2]
            try:
                device_id = int(device_id_raw)
                with Database() as base:
                    connection, cursor = base
                    current_data = datetime.datetime.today().strftime('%Y-%m-%d')
                    device_info = get_full_info_from_meter_device(cursor, device_id)
                    if len(device_info) == 0:
                        incorrect_data_found = True
                    else:
                        try:
                            new_reading = float(message.text)
                            readings = get_last24_date_and_readings_from_device(cursor, device_id)
                            if len(readings) > 0:
                                last_reading = readings[-1]
                                if last_reading[2] > new_reading:
                                    msg_del = await  message.answer('Показания не могут быть меньше предыдущих!',
                                                                    reply_markup=ReplyKeyboardRemove())
                                else:
                                    #проверяем что дата последних показаний отличается от текущей
                                    if current_data == str(last_reading[1]):
                                        update_meter_reading(cursor, device_id, current_data, new_reading)
                                        connection.commit()
                                        msg_del = await message.answer('Показания на текущую дату перезаписаны',
                                                                       reply_markup=ReplyKeyboardRemove() )
                                    else:
                                        insert_new_reading_to_meter_device(cursor, device_id, current_data, new_reading)
                                        connection.commit()
                                        msg_del = await message.answer('Показания добавлены')
                            else:
                                insert_new_reading_to_meter_device(cursor, device_id, current_data, new_reading)
                                connection.commit()
                                msg_del = await message.answer('Внесены первичные показания!')

                        except:
                            incorrect_data_found = True

            except:
                incorrect_data_found = True

    if incorrect_data_found:
        msg_del = await  message.answer('Некорректный запрос на внесение показаний!',
                                            reply_markup=ReplyKeyboardRemove())
    standart_delete_message(msg_del)


def _device_info_message(device: Tuple) -> str:
    """Function get full info from meter device and return message to chat"""
    result = [separator]
    for i in range(len(meter_devices_table)):
        result.append('{}: {}'.format(meter_devices_table[i], device[i]))
    return "\n".join(result)
