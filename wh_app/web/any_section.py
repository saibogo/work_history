import wh_app.web.template as web_template
import wh_app.web.universal_html as uhtml
from wh_app.config_and_backup import config
from wh_app.postgresql.database import Database
from wh_app.sql_operations import select_operations
from wh_app.supporting import functions

functions.info_string(__name__)


def main_web_menu():
    name = "Доступные действия в базе ремонтов Малахит-Екатеринбург"
    menu = [(1, 'Операции с предприятиями'),
            (2, 'Операции с оборудованием'),
            (3, 'Операции с ремонтами'),
            (4, 'Операции с сотрудниками')]
    links_list = ['/points', '/equips', '/works', '/workers']
    table = uhtml.universal_table(name, ['№', 'выполнить:'], menu, True, links_list)
    return web_template.result_page(table)


def faq_page(pre_adr: str) -> str:
    with Database() as base:
        connection, cursor = base
        page = list()
        page.append(uhtml.style_custom())
        page.append('<table><caption>Наиболее частые вопросы по системе:</caption><tr><td>')
        page.append('<ul>')
        page.append('<li>Что нужно для использования системы?'+\
                    web_template.faq_state_machine('hardware') + '</li>')
        page.append('<li>С использованием каких технологий написана система?' +\
                    web_template.faq_state_machine('tecnology') + '</li>')
        page.append('<li>Сколько пользователей поддерживает система?' +\
                    web_template.faq_state_machine('multiuser') + '</li>')
        page.append('<li>Планируется ли развитие системы?' +\
                    web_template.faq_state_machine('update') + '</li>')
        max_equip_id = select_operations.get_maximal_equip_id(cursor)
        max_point_id = select_operations.get_maximal_points_id(cursor)
        max_work_id = select_operations.get_maximal_work_id(cursor)
        page.append('<li>Сколько записей зарегистрированно на данный момент?' +\
                    uhtml.list_to_ul(['Единиц или групп оборудования: <a href="' + config.full_address + '/all-equips">' +
                                      str(max_equip_id) + '</a>',
                                      'Предприятий: <a href="' + config.full_address + '/all-points">' +
                                      str(max_point_id) + '</a>',
                                      'Произведенных работ: <a href="' + config.full_address + '/all-works">' +
                                      str(max_work_id) + '</a>']) + '</li>')
        page.append('<li>Текущий размер базы данных : ' + str(select_operations.get_size_database(cursor)) + '</li>')
        page.append('<li>Среднее количество работ на смену : ' +
                    str(select_operations.get_count_unique_works(cursor) /
                        select_operations.get_count_unique_dates_in_works(cursor)) + '</li>')
        page.append('</ul></td></tr></table>')
        return web_template.result_page('\n'.join(page), pre_adr)


def statistics_page(preview_page):
    with Database() as base:
        connection, cursor = base
        statistics = select_operations.get_statistic(cursor)
        links_list = ['/equip/' + str(elem[0]) for elem in statistics]
        result = uhtml.universal_table(config.statistics_table_name,
                                       config.statistics_table,
                                       [[elem[i] for i in range(1, len(elem))] for elem in statistics],
                                       True,
                                       links_list)
        return web_template.result_page(result, preview_page)
