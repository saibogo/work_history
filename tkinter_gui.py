import sqlite3
import tkinter as tk
from tkinter import messagebox as mb
import threading
import requests
import psutil

import config
import insert_operations
import select_operations
import universal_windows
import functions
import web.server as webserver
from metadata import *

__author__ = "Andrey Gleykh"
__license__ = "GPL"
__email__ = "gleykh@gmail.com"
__status__ = "Prototype"

left_mouse_but = '<Button-1>'


def create_complete_works_win(curr: sqlite3.Cursor, works: list) -> None:
    """Function create new window to complete works"""

    full_works = select_operations.get_full_info_from_works_list(curr, works)
    data = [functions.full_work_to_view(elem) for elem in full_works]
    universal_windows.print_table_window(config.works_table_name, config.works_table, data)


def create_complete_equips_win(curr: sqlite3.Cursor, equips: list) -> None:
    """Function create new window to registred equips"""

    equips_full = select_operations.get_full_equips_list_info(curr, equips)
    data = [functions.full_equip_to_view(elem) for elem in equips_full]
    universal_windows.print_table_window(config.equips_table_name, config.equips_table, data)


def select_point(curr: sqlite3.Cursor) -> str:
    """Function return point_id selected point"""

    points = [str(elem[0]) + ' - ' + str(elem[1]) for elem in select_operations.get_all_points(curr)]
    point_num = universal_windows.select_window('Выберите предприятие', points)
    return point_num.split()[0]


def select_equip(curr: sqlite3.Cursor, point_num: str) -> str:
    """Function return id selected equip"""

    equips = select_operations.get_equip_in_point(curr, point_num)
    data = [" - ".join(functions.full_equip_to_view(elem)) for elem in equips]
    equip_str = universal_windows.select_window('Выберите оборудование', data)
    return equip_str.split()[0]


def point_window(conn: sqlite3.Connection, curr: sqlite3.Cursor) -> None:
    """Create window from point operations in database"""

    pw = tk.Toplevel()

    def exit_points_gui(self) -> None:
        """Function to button exit"""
        pw.destroy()

    def all_points(self) -> None:
        """Function print all points in database"""
        points = select_operations.get_all_points(curr)
        full_information_points = select_operations.get_full_information_list_points(curr, points)
        universal_windows.print_table_window(config.points_table_name, config.points_table, full_information_points)

    def commit(self) -> None:
        """Function to button commit"""

        select_operations.commit(conn)

    def create_new_point(self) -> None:
        """Function to create point button"""

        new_point_data = universal_windows.input_window(config.create_point_name, config.create_point_table)
        if len(new_point_data) != 0:
            insert_operations.create_new_point(curr, new_point_data[0], new_point_data[1])

    pw.title('Операции с предприятиями')
    but_all = tk.Button(pw, text='Просмотреть все доступные')
    but_create = tk.Button(pw, text='Создать новое')
    but_commit = tk.Button(pw, text='Применить изменения')
    but_exit = tk.Button(pw, text='Закрыть окно')

    but_all.bind(left_mouse_but, func=all_points)
    but_create.bind(left_mouse_but, func=create_new_point)
    but_commit.bind(left_mouse_but, func=commit)
    but_exit.bind(left_mouse_but, func=exit_points_gui)

    but_all.pack()
    but_create.pack()
    but_commit.pack()
    but_exit.pack()
    pw.mainloop()


def equip_window(conn: sqlite3.Connection, curr: sqlite3.Cursor) -> None:
    """Function create window to equipments operations"""

    ew = tk.Toplevel()
    ew.title('Операции с оборудованием')

    def view_equips(self)-> None:
        """Function to view button"""
        point_num = select_point(curr)
        if point_num == config.str_interrupted:
            return
        else:
            equips = select_operations.get_equip_in_point(curr, point_num)
            create_complete_equips_win(curr, equips)

    def commit(self) -> None:
        """Function to Button Commit"""

        select_operations.commit(conn)

    def close_win(self) -> None:
        """Function to exit button"""

        ew.destroy()

    def new_equip(self) -> None:
        """Function to add new equips button"""

        point_num = select_point(curr)
        if point_num == config.str_interrupted or point_num == '0':
            return
        else:
            data = universal_windows.input_window(config.create_equip_name, config.create_equip_table)
            if len(data) == 0 or len(data[0]) == 0:
                return
            else:
                name, model, serial, preid = data
                model = model if model else "not model"
                serial = serial if serial else "not number"
                preid = preid if preid else "NULL"
                insert_operations.create_new_equip(curr, point_num, name, model, serial, preid)

    def find_likes(self) -> None:
        """Function to find like button"""

        find_str = universal_windows.input_window(config.find_like_name, config.find_like_table)
        equips = select_operations.get_all_equips_list_from_like_str(curr, find_str[0])
        create_complete_equips_win(curr, equips)

    but_view = tk.Button(ew, text='Посмотреть зарегистрированное')
    but_like = tk.Button(ew, text='Поиск по имени')
    but_add = tk.Button(ew, text='Зарегистрировать новое')
    but_commit = tk.Button(ew, text='Применить изменения')
    but_exit = tk.Button(ew, text='Выход')

    but_view.bind(left_mouse_but, func=view_equips)
    but_like.bind(left_mouse_but, func=find_likes)
    but_add.bind(left_mouse_but, func=new_equip)
    but_commit.bind(left_mouse_but, func=commit)
    but_exit.bind(left_mouse_but, func=close_win)

    but_view.pack()
    but_like.pack()
    but_add.pack()
    but_commit.pack()
    but_exit.pack()


def works_windows(conn: sqlite3.Connection, curr: sqlite3.Cursor) -> None:
    """Function create new window for works in database operations"""

    ww = tk.Toplevel()
    ww.title('Выполненные работы')

    def complete_works(self) -> None:
        """Function to all complete works button"""
        point_num = select_point(curr)
        if point_num == config.str_interrupted:
            return
        else:
            equip_id = select_equip(curr, point_num)
            if equip_id == config.str_interrupted:
                return
            else:
                works = select_operations.get_works_from_point_and_equip(curr, point_num, equip_id)
                create_complete_works_win(curr, works)

    def close_works(self) -> None:
        """Function to exit button"""

        ww.quit()
        ww.destroy()

    def commit_works(self) -> None:
        """Function to commit button"""

        select_operations.commit(conn)

    def new_work(self) -> None:
        """Function to create new work button"""

        point_num = select_point(curr)
        if point_num == config.str_interrupted:
            return
        else:
            equip_id = select_equip(curr, point_num)
            if equip_id == config.str_interrupted or equip_id == '0':
                return
            else:
                data_work = universal_windows.input_window(config.create_work_table_name, config.create_work_table)
                date = universal_windows.select_date_and_time()
                insert_operations.create_new_work(curr, equip_id, date, data_work[0], data_work[1])

    def find_equips_to_point_likes(self) -> None:
        """Function to button find likes points name"""

        find_str = universal_windows.input_window(config.find_like_name, config.find_like_table_points)
        points = select_operations.get_all_points_list_from_like_str(curr, find_str[0])
        equips = []
        for point in points:
            equips = equips + (select_operations.get_equip_in_point(curr, point[0]))
        works = select_operations.get_works_list_from_equips_list(curr, equips)
        create_complete_works_win(curr, works)

    but_complete = tk.Button(ww, text='Все выполненные')
    but_find_like_point = tk.Button(ww, text='Поиск по предприятию')
    but_add = tk.Button(ww, text='Зарегистрировать новую')
    but_commit = tk.Button(ww, text='Применить изменения')
    but_close = tk.Button(ww, text='Выход')

    but_complete.bind(left_mouse_but, func=complete_works)
    but_find_like_point.bind(left_mouse_but, func=find_equips_to_point_likes)
    but_add.bind(left_mouse_but, func=new_work)
    but_commit.bind(left_mouse_but, func=commit_works)
    but_close.bind(left_mouse_but, func=close_works)

    but_complete.pack()
    but_find_like_point.pack()
    but_add.pack()
    but_commit.pack()
    but_close.pack()

    ww.mainloop()


def main_window() -> None:
    """Create new window-gui from database operations"""

    conn = select_operations.open_database()
    curr = select_operations.create_cursor(conn)

    def exit_gui(self) -> None:
        """Function to Button Exit"""

        answer = mb.askyesno('Сохранение', 'Применить изменения?')
        select_operations.close_database(conn, answer)
        root.destroy()

    def create_poin_gui(self) -> None:
        """Function to Button 'Points'"""

        point_window(conn, curr)

    def create_equip_window(self) -> None:
        """Function to Button Equip"""

        equip_window(conn, curr)

    def create_works_window(self) -> None:
        """Function to Works Button"""

        works_windows(conn, curr)

    def start_web_server(self) -> None:
        """Function start web-server to connect database"""

        try:
            response = requests.get("http://" + config.ip_address + ":" + config.port + '/add-work')
            print("Веб-сервер уже запущен")
        except:
            print("Запускаем веб-сервер")
            threading.Thread(target=webserver.start_server).start()

    def stop_web_server(self) -> None:
        """Function stop web-server to connect database"""

        try:
            response = requests.get("http://" + config.ip_address + ":" + config.port + '/add-work')
            for proc in psutil.process_iter():
                data = proc.as_dict(attrs=['cmdline', 'pid'])
                for elem in data['cmdline']:
                    if 'work_history' in elem:
                        print(data)
                        print("процесс найден PID=" + str(data['pid']))
                        proc.kill()
                        print("Веб-сервер остановлен")
        except:
            print("Веб-сервер не запущен")


    root = tk.Tk()
    root.title('База ремонтов')
    but_points = tk.Button(root, text='Операции с предприятиями')
    but_equip = tk.Button(root, text='Операции с оборудованием')
    but_work = tk.Button(root, text='Операции с ремонтами')
    but_start_server = tk.Button(root, text='Запустить веб-сервис')
    but_stop_server = tk.Button(root, text='Остановить сервер')
    but_exit = tk.Button(root, text='Выход')

    but_points.bind(left_mouse_but, func=create_poin_gui)
    but_equip.bind(left_mouse_but, func=create_equip_window)
    but_work.bind(left_mouse_but, func=create_works_window)
    but_start_server.bind(left_mouse_but, func=start_web_server)
    but_stop_server.bind(left_mouse_but, func=stop_web_server)
    but_exit.bind(left_mouse_but, func=exit_gui)

    but_points.pack()
    but_equip.pack()
    but_work.pack()
    but_start_server.pack()
    but_stop_server.pack()
    but_exit.pack()
    root.mainloop()
