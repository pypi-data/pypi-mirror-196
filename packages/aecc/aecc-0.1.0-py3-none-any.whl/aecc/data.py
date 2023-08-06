from . import conf
from . import util
from . import api
from .data_connector import DataConnector
from . import user
import requests

def connect(tokenfile=conf.DEFAULT_TOKENFILE_PATH):
    dconn = None
    if util.is_exist(tokenfile):
        dconn = DataConnector(tokenfile)
    else:
        util.print_error("There is no token file. ("+tokenfile+")")
    return dconn
