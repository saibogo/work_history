"""This module starting development server"""

import wh_app.web.server
from wh_app.supporting import functions

functions.info_string(__name__)

wh_app.web.server.app.run(host='0.0.0.0')
