import wh_app.config_and_backup.config as config
import threading
import requests
import psutil

import wh_app.web.server as webserver
from wh_app.supporting import functions

functions.info_string(__name__)


def start_server():
    try:
        _ = requests.get("http://" + config.ip_address + ":" + config.port + '/add-work')
        print("Веб-сервер уже запущен")
    except:
        print("Запускаем веб-сервер")
        threading.Thread(target=webserver.start_server).start()


def stop_server():
    try:
        _ = requests.get("http://" + config.ip_address + ":" + config.port + '/add-work')
        for process in psutil.process_iter():
            data = process.as_dict(attrs=['cmdline', 'pid'])
            for elem in data['cmdline']:
                if 'work_history' in elem:
                    print(data)
                    print("процесс найден PID=" + str(data['pid']))
                    process.kill()
                    print("Веб-сервер остановлен")
    except:
        print("Веб-сервер не запущен")


def status_server() -> bool:
    try:
        _ = requests.get("http://" + config.ip_address + ":" + config.port + '/add-work')
        for process in psutil.process_iter():
            data = process.as_dict(attrs=['cmdline', 'pid'])
            for elem in data['cmdline']:
                if 'work_history' in elem:
                    print("Веб сервер работает")
                    return True
    except:
        print("Веб-сервер не работает")
        return False