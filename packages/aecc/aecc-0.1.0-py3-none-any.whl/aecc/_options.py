
import argparse
import sys
from . import conf
from . import util
import textwrap

NOPRINTOPTLIST = []

def loading_config(opt):
    for line in open(opt['conf']):
        line = line.strip()
        if len(line) > 0 and line[0] != "#":
            arr = line.split("=")
            k1 = arr[0].strip().lower()
            v1 = arr[1].strip()
            if len(k1) > 0:
                opt[k1] = v1
    return opt


def check_out_path(opt):
    if ('out' in opt.keys() and opt['out'] == ''):
        opt['out'] = './bamsnap_' + util.getNow2()
    if 'out' in opt.keys() and opt['out'] != None:
        util.check_dir(opt['out'])



def convert_valuetype(typestr):
    rsttype = None
    if typestr is not None:
        if typestr == "int":
            rsttype = int
        if typestr == "float":
            rsttype = float
    return rsttype


def has_subparser(opts):
    flag = False
    for a1 in opts:
        if a1['type'] == "subparser":
            flag = True
            break
    return flag


def get_options():
    global OPT
    # OPT = util.load_json(util.getDataPath('conf.json'))

    parser = argparse.ArgumentParser(usage='%(prog)s <sub-command> [options]',
                                    description='%(prog)s version ' + OPT['VERSION'] + " (" + OPT['VERSION_DATE'] + ")" )
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ver' + OPT['VERSION'] + " (" + OPT['VERSION_DATE'] + ")")

    if has_subparser(OPT['options']):
        subparsers = parser.add_subparsers(title="sub-commands", dest="subcommand",metavar='', prog=OPT['PROG'])
        for a1 in OPT['options']:
            if a1['type'] == "subparser":
                p1 = subparsers.add_parser(a1['param'], help=a1['help'], description=textwrap.dedent(a1['desc']), formatter_class=argparse.RawDescriptionHelpFormatter)
            else:
                valuetype = a1['type']
                if a1['action'] is not None:
                    if 'param_a' in a1.keys():
                        p1.add_argument('-' + a1['param_a'], '--' + a1['param'], default=a1['default'], help=a1['help'], action=a1['action'])
                    else:
                        p1.add_argument('-' + a1['param'], default=a1['default'], help=a1['help'], action=a1['action'])
                else:
                    if 'param_a' in a1.keys():
                        p1.add_argument('-' + a1['param_a'], '--' + a1['param'], default=a1['default'], help=textwrap.dedent(a1['help']), nargs=a1['nargs'], type=valuetype)
                    else:
                        p1.add_argument('-' + a1['param'], default=a1['default'], help=textwrap.dedent(a1['help']), nargs=a1['nargs'], type=valuetype)
    else:
        for a1 in OPT['options']:
            valuetype = a1['type']
            if a1['action'] is not None:
                if 'param_a' in a1.keys():
                    parser.add_argument('-' + a1['param_a'], '--' + a1['param'], default=a1['default'], help=a1['help'], action=a1['action'])
                else:
                    parser.add_argument('-' + a1['param'], default=a1['default'], help=a1['help'], action=a1['action'])
            else:
                if 'param_a' in a1.keys():
                    parser.add_argument('-' + a1['param_a'], '--' + a1['param'], default=a1['default'], help=textwrap.dedent(a1['help']), nargs=a1['nargs'], type=valuetype)
                else:
                    parser.add_argument('-' + a1['param'], default=a1['default'], help=textwrap.dedent(a1['help']), nargs=a1['nargs'], type=valuetype)
    


    # if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1][0] != '-'):
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    opt = vars(parser.parse_args())

    if 'conf' in opt.keys() and opt['conf'] is not None and util.is_exist(opt['conf']):
        opt = loading_config(opt)

    opt['cmd'] = " ".join(sys.argv)
    check_out_path(opt)
    return opt


### OPTION ####
OPT = {
  "TITLE": "aecc",
  "VERSION": conf.VERSION,
  "VERSION_DATE": conf.VERSION_DATE,
  "PROG": "aecc",
  "options": [
    { "param": "download_key", "default": False, "nargs": None, "action": "store_true", "choices": None, "type": None, "help": "download key file" },
    { "param": "signup", "default": False, "nargs": None, "action": "store_true", "choices": None, "type": None, "help": "signup user" },
    { "param": "download", "default": "", "nargs": None, "action": None, "choices": ["region", "polutant", "user"], "type": None, "help": "download" },
    { "param": "key", "default": "", "nargs": None, "action": None, "choices": None, "type": None, "help": "userkey file" },
    { "param": "print", "default": "", "nargs": None, "action": None, "choices": None, "type": None, "help": "userkey file" },
    { "param": "log", "default": '', "nargs": None, "action": None, "choices": None, "type": None, "help": "log file" },
  ]
}
