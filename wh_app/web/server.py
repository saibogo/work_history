"""This module contain all rules WEB-section"""

import ssl

from wh_app.web.servers_parts.errors_part import *
from wh_app.web.servers_parts.urers_actions_part import *
from wh_app.web.servers_parts.points_part import *
from wh_app.web.servers_parts.equips_part import *
from wh_app.web.servers_parts.works_part import *
from wh_app.web.servers_parts.bugs_part import *
from wh_app.web.servers_parts.workers_part import *
from wh_app.web.servers_parts.find_part import *
from wh_app.web.servers_parts.any_part import *
from wh_app.web.servers_parts.orders_part import *


context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(config.path_to_certificate(), config.path_to_private_key())


def start_server():
    """Start development server"""
    app.run(host=config.ip_address(), ssl_context=context)


if __name__ == "__main__":
    start_server()
