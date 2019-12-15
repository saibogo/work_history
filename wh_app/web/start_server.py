from wh_app.supporting import functions
import wh_app.web.server

functions.info_string(__name__)

wh_app.web.server.app.run(host='0.0.0.0')
