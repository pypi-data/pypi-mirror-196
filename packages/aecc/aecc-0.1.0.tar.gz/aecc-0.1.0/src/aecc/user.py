import getpass
from . import conf
from . import util
from . import api


def download_token(tokenfile=""):
    api.check_backend()
    if tokenfile == "":
        tokenfile = conf.DEFAULT_TOKENFILE_PATH
    
    useremail = input('email : ')
    userpw = getpass.getpass('password : ')

    enc_email = util.encode(useremail)
    enc_pw = util.encode(userpw)

    rst = api.get_json_with_urljoin(["get_token", enc_email, enc_pw])
    if not rst["check"]:
        util.print_error(rst["msg"])
    else:
        util.fileSave(tokenfile, rst['token'], 'w')
        print("Saved token file. " + tokenfile)


def input_mandatory(query, errormsg):
    userinput = ""
    while True:
        userinput = input(query)
        userinput = userinput.strip()
        if userinput != "":
            break
        else:
            print(errormsg)
    return userinput


def signup():
    useremail = input_mandatory('User email : ', 'Please enter your email!')
    username = input_mandatory('User name : ', 'Please enter your name!')
    affiliation = input_mandatory('Affiliation : ', 'Please enter your affiliation!')

    while True:
        userpw = getpass.getpass('password : ')
        userpw2 = getpass.getpass('password(confirm) : ')
        if userpw == userpw2:
            break
        else:
            print("Passwords are not matched. Please input password correctly!")

    enc_email = util.encode(useremail)
    enc_pw = util.encode(userpw)

    pdata = {}
    pdata['enc_email'] = enc_email
    pdata['username'] = username
    pdata['affiliation'] = affiliation
    pdata['enc_pw'] = enc_pw

    rst = api.post_json_with_urljoin(["signup"], pdata)
    if not rst["check"]:
        print("Signup Error!: " + rst["msg"])
    else:
        # download_token()
        print("Signup Successfully! After the administrator confirms, you can signin with your email, password, and this token file.")
        print("Please keep this your token file. This token is required when you connect AECC DB.")
        print("If you miss the token file, you can download it with 'aecc.download_token()'.")


def get_userinfo_from_userkey(userkey):
    api.get(['userinfo',userkey])
