"""This module implement operations from any users"""

import getpass

from wh_app.supporting import functions

functions.info_string(__name__)


def user_exist(username: str) -> bool:
    """Return exist or not exist user"""

    return username in functions.read_all_users()


def update_password(username: str) -> None:
    """Update hash password if user exist"""

    if user_exist(username):
        users = functions.read_all_users()
        password = getpass.getpass("Требуется пароль администратора системы:")
        if functions.is_superuser_password(password):
            password = getpass.getpass("Ввведите новый пароль для пользователя {0} :"
                                       .format(username))
            password1 = getpass.getpass("Повторите новый пароль для пользователя {0} :"
                                        .format(username))
            if password == password1:
                users[username] = functions.create_hash(password)
                full_users = {}
                for user in users.keys():
                    full_users[user] = [users[user], functions.get_user_role(user)]
                functions.save_all_users(full_users)
                print("Пароль для пользователя {0} успешно обновлен".format(username))
        else:
            print("Неверный пароль суперпользователя! В доступе отказано!")
    else:
        print("Пользователь {0} не создан".format(username))


def create_new_user() -> None:
    """Create new user if user not exist"""

    username = input("Введите псевдоним для нового пользователя: ")
    if user_exist(username):
        print("Пользователь {0} уже существует")
    else:
        password = getpass.getpass("Требуется пароль администратора системы:")
        if functions.is_superuser_password(password):
            users = functions.read_all_users()
            users[username] = functions.create_hash(username)
            full_users = {}
            for user in users.keys():
                full_users[user] = [users[user], functions.get_user_role(user)]
            functions.save_all_users(full_users)
            print(("Создан пользователь {0} с паролем по умолчанию {0}." +
                   " Обязательно измените пароль!").format(username))
        else:
            print("Неверный пароль суперпользователя! В доступе отказано!")
