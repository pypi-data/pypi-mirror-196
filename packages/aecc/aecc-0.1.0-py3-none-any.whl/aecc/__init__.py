from ._logging import get_logger
from ._options import get_options
from .main import AECC
from .user import download_token, signup
from .data import connect

def cli():
    opt = get_options()
    opt['log'] = get_logger(silence=False, debug=False, logfile=opt['log'])
    bs = AECC(opt)
    bs.run()
