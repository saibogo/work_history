import subprocess


def create_dump(path_to_file: str) -> None:
    """Save to DB-dump in file"""
    try:
        print("Path: {0}".format(path_to_file))
        print("Command1: pg_dump workhistory > {0}".format(path_to_file))
        proc = subprocess.call("pg_dump workhistory > {0}".format(path_to_file), shell=True)
        print('Дамп базы данных записан в {0}'.format(path_to_file))
        print('Path: {0}'.format(path_to_file + '.tar.gz'))
        print("Command2: {0} {1} {2}".format("tar -cvzf", path_to_file + '.tar.gz', path_to_file))
        proc = subprocess.call("tar -cvzf {0} {1}".format(
            path_to_file + '.tar.gz',
            path_to_file), shell=True)
        print("Создан сжатый архив в {0}".format(path_to_file + '.tar.gz'))
    except:
        print("Невозможно создать дамп базы данных!")