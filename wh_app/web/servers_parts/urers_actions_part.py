"""This module contain all action like login. logout. new theme and e.t.c. for Flask server.py"""

from wh_app.web.servers_parts.support_part import *
from wh_app.web.universal_html import LOGIN, PASSWORD, access_denided, access_allowed, logout_user
from wh_app.web.any_section import login_input_page, new_theme_page


@app.route('/login')
def login_page() -> str:
    """Redirect to LOGIN-form"""
    session[LOGIN_IS_CORRECT] = False
    session.modified = True
    return login_input_page()


@app.route('/logout')
def logout_page() -> str:
    """Function call logout-function for user and redirect to LOGOUT-page"""

    user_name = session[LOGIN]
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print('Пользователь {} покинул систему'.format(user_name))
    functions.add_record_in_logout_log(user_name, user_ip)
    session[LOGIN_IS_CORRECT] = False
    functions.close_session()
    session.modified = True
    return result_page(logout_user(), '/login', stylesheet_number())


@app.route('/login-verification',  methods=['POST'])
def login_verification() -> str:
    """Function compare pair login-password with data in system and redirect to new page"""
    user_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    if functions.is_login_and_password_correct(request.form[LOGIN], request.form[PASSWORD]):
        user_name = request.form[LOGIN]
        print("Успешная верификация пользователя ", user_name)
        user_role = functions.get_user_role(user_name)
        if functions.is_login_and_password_correct( user_name, request.form[PASSWORD]) \
                and user_role == functions.ROLE_SUPERUSER:
            session[SESSION_ROLE] = functions.ROLE_SUPERUSER
            session[LOGIN] = user_name
        elif user_role == functions.ROLE_WORKER:
            session[SESSION_ROLE] = functions.ROLE_WORKER
            session[LOGIN] = user_name
        else:
            session[LOGIN] = user_name
            session[SESSION_ROLE] = functions.NO_ROLE
        session[LOGIN_IS_CORRECT] = True
        session[TIME_LOGIN] = time.time()
        session.modified = True
        functions.add_new_session_in_db()
        result = access_allowed(request.form[LOGIN])
        print('Для пользователя установлена роль: ', functions.get_role_description(session[SESSION_ROLE]))
        functions.add_record_in_login_log(user_name, session[SESSION_ROLE], user_ip)
    elif functions.is_valid_customer(request.form[LOGIN], request.form[PASSWORD]):
        print("Успешная верификация пользователя ", request.form[LOGIN])
        session[SESSION_ROLE] = functions.ROLE_CUSTOMER
        session[LOGIN] = request.form[LOGIN]
        session[LOGIN_IS_CORRECT] = True
        session[TIME_LOGIN] = time.time()
        session.modified = True
        functions.add_new_session_in_db()
        result = access_allowed(request.form[LOGIN])
        print('Для пользователя установлена роль: ', functions.get_role_description(session[SESSION_ROLE]))
        functions.add_record_in_login_log(request.form[LOGIN], session[SESSION_ROLE], user_ip)
    else:
        print("Неудачная попытка входа пользователя ", request.form[LOGIN])
        result = access_denided(request.form[LOGIN])
    return result_page(result, '/')


@app.route('/favicon.ico')
def favicon() -> Any:
    """Return static favicon-logo to web-page"""
    return send_from_directory(config.static_dir(), 'favicon.ico')


@app.route('/style<number>.css')
def styles(number: int) -> Response:
    """Return selected CSS-page from static folder"""
    if is_integer(number):
        page = send_from_directory(config.static_dir(), 'style{0}.css'.format(number))
    else:
        page = ""
    return page


@app.route('/<folder>/style<number>.css')
def styles_table(folder: str, number: int) -> Response:
    """Return selected CSS-page from static folder"""
    if is_integer(number):
        page = send_from_directory(config.static_dir(), '{0}/style{1}.css'.format(folder, number))
    else:
        page = ""
    return page


@app.route('/image/background<number>.jpg')
def get_background_image(number: int) -> Response:
    """Return selected background from static folder"""
    if is_integer(number):
        page = send_from_directory(config.static_dir(), 'image/background{0}.jpg'.format(number))
    else:
        page = ""
    return page


@app.route('/image/background<number>.gif')
def get_background_image_gif(number: int) -> Response:
    """Return selected background from static folder"""
    if is_integer(number):
        page = send_from_directory(config.static_dir(), 'image/background{0}.gif'.format(number))
    else:
        page = ""
    return page


@app.route('/next-themes')
def next_themes() -> str:
    """redirect to new themes methods"""
    if THEME_NUMBER in session:
        session[THEME_NUMBER] = session.get(THEME_NUMBER) + 1
    else:
        session[THEME_NUMBER] = 0  # default number theme
    session[THEME_NUMBER] %= THEMES_MAXIMAL
    session.modified = True
    return new_theme_page(session[THEME_NUMBER])


@app.route('/server-ready-to-shutdown')
def server_ready_to_shutdown() -> str:
    """Return message from admin"""
    message = ""
    try:
        message_file = open(config.path_to_messages(), 'r')
        for line in message_file:
            message += line
    except FileNotFoundError:
        pass
    return message
