"""This module contain support function to flask server.py"""

import flask
from flask import Flask, request, redirect, session, Response
from flask import send_from_directory, send_file
from typing import Callable, Any
import time

import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.supporting import functions
from wh_app.web.template import result_page


def is_integer(arg: Any) -> bool:
    """Return arg is int or not"""

    try:
        int(arg)
        return True
    except ValueError:
        return False


app = Flask(__name__, static_folder=config.static_dir(), template_folder=config.template_folder())
app.secret_key = 'gleykh secret key'
functions.info_string(__name__)

THEME_NUMBER = 'theme_number'
THEMES_MAXIMAL = 3
LOGIN_IS_CORRECT = 'access_is_allowed'
TIME_LOGIN = 'time_login'
SESSION_ROLE = 'role'


def stylesheet_number() -> str:
    """Function return string contains number decors themes"""
    if THEME_NUMBER in session:
        session[THEME_NUMBER] = session.get(THEME_NUMBER)
    else:
        session[THEME_NUMBER] = 0  # default number theme

    return session.get(THEME_NUMBER)


def get_login_from_session() -> str:
    """Return login in SESSION from web-version"""
    return session[uhtml.LOGIN]


def access_is_allowed() -> bool:
    """Function return if user input correct login and password"""
    if (LOGIN_IS_CORRECT in session) and\
            (TIME_LOGIN in session) and\
            (time.time() - session[TIME_LOGIN] < config.max_session_time()) and functions.current_session_is_valid():
        session[LOGIN_IS_CORRECT] = session.get(LOGIN_IS_CORRECT)
        session[TIME_LOGIN] = time.time()
    else:
        session[LOGIN_IS_CORRECT] = False
    session.modified = True
    return session.get(LOGIN_IS_CORRECT)


def is_role_correct(min_role: str, current_role: str) -> bool:
    """True if current_role >= min_role"""
    return functions.ROLES_IERARH.index(current_role) <= functions.ROLES_IERARH.index(min_role)


def goto_or_redirect(function: Callable, min_role=functions.ROLE_SUPERUSER) -> Any:
    if access_is_allowed():
        if is_role_correct(min_role, session[SESSION_ROLE]):
            return function()
        else:
            return redirect('/access-denied')
    else:
        return redirect('/login')


def goto_or_redirect_from_roles_list(function: Callable, roles_list=[]) ->Any:
    if access_is_allowed():
        current_role = session[SESSION_ROLE]
        if current_role in roles_list:
            return function()
        else:
            return redirect('/access-denied')
    else:
        return redirect('/login')

