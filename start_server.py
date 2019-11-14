import web.server
import functions

functions.info_string(__name__)

web.server.app.run(host='0.0.0.0')
