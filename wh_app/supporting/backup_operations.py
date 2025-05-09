"""This module implements database backup"""
import subprocess

from wh_app.supporting import functions
from wh_app.config_and_backup.config import path_to_dump, path_to_structure_dump, database_name, user_name

functions.info_string(__name__)


def create_dump(path_to_file: str = path_to_dump()) -> None:
    """Save to DB-dump in file"""

    try:
        print("Path: {0}".format(path_to_file))
        command_backup = "pg_dump --dbname={0} --username={1} > {2}".format(database_name(),  user_name(), path_to_file)
        print("Command1: {0}".format(command_backup))
        _ = subprocess.call(command_backup, shell=True)
        print('Дамп базы данных записан в {0}'.format(path_to_file))
        print('Path: {0}'.format(path_to_file + '.tar.gz'))
        print("Command2: {0} {1} {2}".format("tar -cvzf", path_to_file + '.tar.gz', path_to_file))
        _ = subprocess.call("tar -cvzf {0} {1}".format(
            path_to_file + '.tar.gz',
            path_to_file), shell=True)
        print("Создан сжатый архив в {0}".format(path_to_file + '.tar.gz'))
    except OSError:
        print("Невозможно создать дамп базы данных!")
    except subprocess.CalledProcessError:
        print("Невозможно создать дамп базы данных!")


def create_empty(path_to_file: str = path_to_structure_dump()) -> None:
    """Save empty database structure"""

    try:
        print("Path: {0}".format(path_to_file))
        command_backup = "pg_dump --schema-only --dbname={0} --username={1} > {2}".format(database_name(), user_name(), path_to_file)
        print(command_backup)
        _ = subprocess.call(command_backup, shell=True)
        print('Дамп структуры базы данных записан в {0}'.format(path_to_file))
        print('Path: {0}'.format(path_to_file + '.tar.gz'))
        print("Command2: {0} {1} {2}".format("tar -cvzf", path_to_file + '.tar.gz', path_to_file))
        _ = subprocess.call("tar -cvzf {0} {1}".format(
            path_to_file + '.tar.gz',
            path_to_file), shell=True)
        print("Создан сжатый архив в {0}".format(path_to_file + '.tar.gz'))
    except OSError:
        print("Невозможно создать дамп структуры базы данных!")
    except subprocess.CalledProcessError:
        print("Невозможно создать дамп структуры базы данных!")
