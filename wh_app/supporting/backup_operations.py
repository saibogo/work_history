"""This module implements database backup"""
import os
import re
import subprocess
from datetime import datetime

from wh_app.supporting import functions
from wh_app.config_and_backup.config import path_to_dump, path_to_structure_dump, database_name, user_name

functions.info_string(__name__)

__max_backups_count = 5


def create_dump(path_to_file: str = path_to_dump()) -> None:
    """Save to DB-dump in file"""
    current_date = datetime.now().date()
    try:
        path_to_file_new = path_to_file.format(current_date) if path_to_file == path_to_dump() else path_to_file
        print("Path: {0}".format(path_to_file_new))
        command_backup = "pg_dump  --dbname={0} > {1}".format(database_name(),  path_to_file_new)
        print("Command1: {0}".format(command_backup))
        _ = subprocess.call(command_backup, shell=True)
        print('Дамп базы данных записан в {0}'.format(path_to_file))
        print('Path: {0}'.format(path_to_file_new + '.tar.gz'))
        print("Command2: {0} {1} {2}".format("tar -cvzf", path_to_file_new + '.tar.gz', path_to_file_new))
        _ = subprocess.call("tar -cvzf {0} {1}".format(
            path_to_file_new + '.tar.gz',
            path_to_file_new), shell=True)
        print("Создан сжатый архив в {0}".format(path_to_file_new + '.tar.gz'))
    except OSError:
        print("Невозможно создать дамп базы данных!")
    except subprocess.CalledProcessError:
        print("Невозможно создать дамп базы данных!")


def create_empty(path_to_file: str = path_to_structure_dump()) -> None:
    """Save empty database structure"""
    current_date = datetime.now().date()
    try:
        path_to_file_new = path_to_file.format(current_date) if path_to_file == path_to_structure_dump() else path_to_file
        print("Path: {0}".format(path_to_file_new))
        command_backup = "pg_dump --schema-only --dbname={0}  > {1}".format(database_name() , path_to_file_new)
        print(command_backup)
        _ = subprocess.call(command_backup, shell=True)
        print('Дамп структуры базы данных записан в {0}'.format(path_to_file_new))
        print('Path: {0}'.format(path_to_file_new + '.tar.gz'))
        print("Command2: {0} {1} {2}".format("tar -cvzf", path_to_file_new + '.tar.gz', path_to_file_new))
        _ = subprocess.call("tar -cvzf {0} {1}".format(
            path_to_file_new + '.tar.gz',
            path_to_file_new), shell=True)
        print("Создан сжатый архив в {0}".format(path_to_file_new + '.tar.gz'))
    except OSError:
        print("Невозможно создать дамп структуры базы данных!")
    except subprocess.CalledProcessError:
        print("Невозможно создать дамп структуры базы данных!")


def delete_old_backups() -> None:
    """Delete all backups older 5 days"""
    path_to_files = path_to_dump()
    ind = path_to_files.find('postgress')
    path_to_dir = path_to_files[:ind]
    print('Поиск устаревших сохранений базы данных в директории {}'.format(path_to_dir))
    dates = set()
    for f in os.listdir(path_to_dir):
        matches = re.findall('\d\d\d\d-\d\d-\d\d', str(f))
        for elem in matches:
            dates.add(elem)
    if len(dates) <= __max_backups_count:
        return
    else:
        dates_ls = sorted(list(dates), key=lambda e: datetime.strptime(e, '%Y-%m-%d').date())
        dates_to_delete = dates_ls[ : len(dates_ls) - __max_backups_count]
        for dt in dates_to_delete:
            for f in os.listdir(path_to_dir):
                if str(f).find(str(dt)) > -1:
                    print('Удаляется файл {}'.format(f))
                    try:
                        os.remove(path_to_dir + str(f))
                    except Exception as e:
                        print(e)
                        print('Невозможно удалить файл {}'.format(f))
