#from .web_server import StringGeneratorWebService, load_thumbd
from .generic_web_server import FratWebServer
from .version import __version__
import json

import pkgutil

frat_gui_js = pkgutil.get_data(__name__, "resources/frat_gui.js").decode("utf-8")
frat_gui_config_seals = json.loads(pkgutil.get_data(__name__, "resources/seals_annotation_config.json").decode("utf-8"))
frat_gui_config_font = json.loads(pkgutil.get_data(__name__, "resources/font_annotation_config.json").decode("utf-8"))
frat_gui_config = json.loads(pkgutil.get_data(__name__, "resources/font_annotation_config.json").decode("utf-8"))
frat_webpage_jinja2 = pkgutil.get_data(__name__, "resources/frat_webpage.jinja2").decode("utf-8")


from .formats import rectangles_to_rgb, rectangles_to_gray, htmlrgb_to_uint8