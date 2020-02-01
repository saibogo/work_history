import datetime

import wh_app.config_and_backup.config as config
import threading
import requests
import psutil

import wh_app.web.server as webserver
from wh_app.supporting import functions

functions.info_string(__name__)


def start_server() -> None:
    if status_server():
        print("Веб-сервер уже запущен")
    else:
        print("Запускаем веб-сервер")
        try:
            message = open(config.path_to_messages, 'w')
            message.close()
        except FileNotFoundError:
            print("Нет доступа к файлу сообщений для пользователей")

        threading.Thread(target=webserver.start_server).start()


def stop_server() -> None:
    if not status_server():
        print("Веб-сервер не запущен")
    else:
        for process in psutil.process_iter():
            data = process.as_dict(attrs=['cmdline', 'pid'])
            for elem in data['cmdline']:
                if 'work_history' in elem:
                    print(data)
                    print("процесс найден PID=" + str(data['pid']))
                    process.kill()
                    print("Веб-сервер остановлен")


def status_server() -> bool:
    try:
        _ = requests.get("http://" + config.ip_address + ":" + config.port + '/add-work')
        for process in psutil.process_iter():
            data = process.as_dict(attrs=['cmdline', 'pid'])
            for elem in data['cmdline']:
                if 'work_history' in elem:
                    return True
    except requests.ConnectionError:
        return False
    return False


def say_stop(comment: str) -> None:
    if status_server():
        try:
            stop_time = datetime.datetime.now() + datetime.timedelta(milliseconds=(config.timeout_message) * 2)

            message = open(config.path_to_messages, 'w')
            message.write("Внимание! В {0} сервер будет остановлен для проведения работ.\n".
                          format(stop_time.strftime("%A %d %B %Y %H:%M:%S")))
            message.write("Просьба завершить работу с вашими данными.\n")
            message.write("Причина остановки: {0}\n".format(comment))
            message.close()

            message = open(config.path_to_messages, 'r')
            print("Создано сообщение для пользователей:")
            for line in message:
                print(line)
            message.close()

        except FileNotFoundError:
            print("Невозможно передать сообщение. Нет доступа к файлу {0}".format(config.path_to_messages))
    else:
        print("Сервер уже остановлен")