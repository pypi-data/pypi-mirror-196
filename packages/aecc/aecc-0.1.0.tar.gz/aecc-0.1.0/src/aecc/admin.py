from . import util
from . import api
import pandas as pd

class Administration():
    def __init__(self, userinfo, sessionkey, pprint):
        self.userinfo = userinfo
        self.sessionkey = sessionkey
        self.pprint = pprint

    def init_db(self):
        util.check_admin(self.userinfo)
        rst = api.get_json_with_urljoin(['admin', 'init_db', self.sessionkey])
        print(rst)

    def add_pollutant_synonym(self, pollutant_name='', add_synonym=''):
        util.check_admin(self.userinfo)
        if pollutant_name == '' or add_synonym == '':
            util.print_error("Please add pollutant_name and add_synonym.")
        else:
            rst = api.get_json_with_urljoin(['admin', 'add_pollutant_synonym', self.sessionkey, pollutant_name, add_synonym])
            if rst['check']:
                print("The synonym("+add_synonym+") of the pollutant("+pollutant_name+") is added by admin.")

    def list_user(self, return_type="dataframe"):
        util.check_admin(self.userinfo)
        rst = api.get_json_with_urljoin(['admin','list_users', self.sessionkey])
        if return_type == "dataframe":
            return_value = pd.DataFrame.from_dict(rst)
        else:
            return_value = rst
        return return_value
    
    def print_users(self):
        util.check_admin(self.userinfo)
        userlist = self.list_user(return_type="dict")
        self.pprint.print_users(userlist)

    def add_user(self, useremail="", username="", affiliation="", userpassword="", auth_upload_rawdata=False, auth_upload_pmf=False, auth_admin=False):
        util.check_admin(self.userinfo)
        d = {}
        d['enc_email'] = util.encode(useremail)
        d['username'] = username
        d['affiliation'] = affiliation
        d['enc_userpassword'] = util.encode(userpassword)
        d['auth_upload_rawdata'] = auth_upload_rawdata
        d['auth_upload_pmf'] = auth_upload_pmf
        d['auth_admin'] = auth_admin

        rst = api.post_json_with_urljoin(['admin','add_user', self.sessionkey], d)
        if rst['check']:
            print("User("+username+") is added by admin. Also the user is confirmed.")

    def del_user(self, useremail=""):
        util.check_admin(self.userinfo)
        enc_email = util.encode(useremail)
        rst = api.get_json_with_urljoin(['admin','del_user', self.sessionkey, enc_email])
        if rst['check']:
            print("User("+useremail+") is deleted by admin.")

    def update_user(self, useremail=None, username=None, affiliation=None, userpassword=None
                    , auth_upload_rawdata=None, auth_upload_pmf=None, auth_admin=None):
        enc_email = util.encode(useremail)
        d = {}
        d['username'] = username
        d['affiliation'] = affiliation
        d['enc_userpassword'] = util.encode(userpassword) if userpassword != None else None
        d['auth_upload_rawdata'] = auth_upload_rawdata
        d['auth_upload_pmf'] = auth_upload_pmf
        d['auth_admin'] = auth_admin
        rst = api.post_json_with_urljoin(['admin','update_user', self.sessionkey, enc_email], d)
        if rst['check']:
            print("User("+useremail+") is updated by admin.")

    def confirm_user(self, useremail=None):
        util.check_admin(self.userinfo)
        enc_email = util.encode(useremail)
        rst = api.get_json_with_urljoin(['admin','confirm_user', self.sessionkey, enc_email])
        if rst['check']:
            print("User("+useremail+") is confirmed by admin. Now, the user can connect AECC DB.")

    def unconfirm_user(self, useremail=None):
        util.check_admin(self.userinfo)
        enc_email = util.encode(useremail)
        rst = api.get_json_with_urljoin(['admin','unconfirm_user', self.sessionkey, enc_email])
        if rst['check']:
            print("User("+useremail+") is unconfirmed by admin. Now, the user cannot connect AECC DB.")

    def set_admin(self, useremail=None):
        self.update_user(useremail=useremail, auth_admin=True)
    
    ##################################
    ## Region
    ##################################
    def add_region(self, pdata):
        util.check_admin(self.userinfo)
        rst = api.post_json_with_urljoin(['admin','add_region', self.sessionkey], pdata)
        if rst['check']:
            print("The region("+pdata['ename']+") is added by admin.")

    def del_region(self, code=""):
        util.check_admin(self.userinfo)
        rst = api.get_json_with_urljoin(['admin','del_region', self.sessionkey, code])
        if rst['check']:
            print("The region("+code+") is deleted by admin.")

    ##################################
    ## Pollutant
    ##################################
    def add_pollutant(self, pdata):
        util.check_admin(self.userinfo)
        rst = api.post_json_with_urljoin(['admin','add_pollutant', self.sessionkey], pdata)
        if rst['check']:
            print("The pollutant("+pdata['name']+") is added by admin.")

    def del_pollutant(self, name=""):
        util.check_admin(self.userinfo)
        rst = api.post_json_with_urljoin(['admin','del_pollutant', self.sessionkey], {'name': name})
        if rst['check']:
            print("The pollutant("+name+") is deleted by admin.")