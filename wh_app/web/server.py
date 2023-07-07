"""This module contain all rules WEB-section"""

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


def start_server():
    """Start development server"""
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    start_server()
