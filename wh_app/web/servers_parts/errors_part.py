"""This module contain all error handlers to Flask server.py"""

from wh_app.web.servers_parts.support_part import *


@app.errorhandler(404)
def page_not_found(error: Any) -> Response:
    """Return network error handling page 404"""
    print(error)
    return goto_or_redirect(lambda: web_template.result_page(uhtml.html_page_not_found(),
                                                             '/',
                                                             stylesheet_number()))


@app.errorhandler(405)
def method_not_allowed(error: Any) -> Response:
    """Return network error handling page 405"""
    print(error)
    return goto_or_redirect(lambda: web_template.result_page(uhtml.html_page_not_found(),
                                                             '/',
                                                             stylesheet_number()))


@app.errorhandler(500)
def page_internal_server_error(error: Any) -> Response:
    """Return network error handling page 500"""
    print(error)
    return goto_or_redirect(lambda: web_template.result_page(uhtml.html_internal_server_error(),
                                                             '/',
                                                             stylesheet_number()))


@app.route('/not_found')
def not_found():
    """See page_not_found()"""
    return 'Oops!', 404