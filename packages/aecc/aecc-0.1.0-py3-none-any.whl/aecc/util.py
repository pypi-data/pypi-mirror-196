import base64
import time
import gzip
import os
import sys
from . import conf
from ._logging import get_logger
from rich.console import Console

def print_console(table):
    console = Console()
    console.print(table)

def conv_isotime_to_date(isotime_string, type="datetime"):
    isotime_string = str(isotime_string).strip()
    if type=="date":
        to_len = 10
    else:
        to_len = 19
    return_value = isotime_string[:to_len].replace("T"," ")
    return return_value

def check_file(filepath):
    if not is_exist(filepath):
        print_error("the file is not exist.")
        sys.exit()

def check_admin(userinfo):
    if not userinfo['auth_admin']:
        print_error("you don't have admin permission.")
        sys.exit()

def print_error(msg, exist=True):
    print("ERROR! " + msg)
    if exist:
        sys.exit()

def is_exist(filepath):
     return os.path.exists(filepath)

def comma(value, digit=None):
    if digit is not None:
        value = round(value, digit)
    return "{:,}".format(value)

def get_default(opt, opt_key, default_value):
    rst = None
    if opt_key in opt.keys():
        rst = opt[opt_key]
    else:
        rst = default_value
    return rst

def convert_date(tdate):
    if '-' in tdate and len(tdate) == 10:
        rdate = tdate.replace('-', '')
    elif len(tdate) == 8:
        rdate = tdate[:4] + '-' + tdate[4:6] + '-' + tdate[6:]
    return rdate

def get_dummy_log():
    return get_logger(silence=False, debug=False, logfile='')

def getlog(log):
    if log is None:
        log = get_dummy_log()
    return log

def getNow(pattern="%Y-%m-%d %I:%M:%S"):
    return time.strftime(pattern, time.localtime())

def getNow2():
    now = time.localtime()
    s = "%04d%02d%02d%02d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s

def encode(clear, key=conf.APPKEY):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        # print(clear[i], key_c, enc_c, ord(clear[i]), ord(key_c), (ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode(bytes(''.join(enc), 'latin')).decode("latin")

def decode(enc, key=conf.APPKEY):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        # dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)   ### for python2
        dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def fileSave(path, cont, opt, encoding='utf-8', gzip_flag="n"):
    path = os.path.expanduser(path)
    if gzip_flag == "gz":
        if not "b" in opt:
            opt += "b"
        f = gzip.open(path, opt)
        f.write(cont.encode())
        f.close()
    else:
        f = open(path, opt, encoding=encoding)
        f.write(cont)
        f.close

def fileOpen(path, encoding='utf-8'):
    path = os.path.expanduser(path)
    f = open(path, "r", encoding=encoding)
    return f.read()

