import pandas as pd
from datetime import datetime
from . import util
from . import conf
from . import api
from .excelfile import ExcelFile
from .data_uploader import RawDataUploader, PMFUploader
from .data_request import RawDataRequest
from .data_print import PrintData
from .admin import Administration
from rich.table import Table



class DataConnector():
    sessionkey = ""
    userinfo = {}
    all_regions = []
    all_region_codes = []
    all_pollutants = []
    all_pollutant_names = []
    count_pollutants = {}

    def __init__(self, tokenfile=conf.DEFAULT_TOKENFILE_PATH, token=None):
        self.pprint = PrintData()
        if token == None:
            token = util.fileOpen(tokenfile).strip()
        enc_token = util.encode(token)
        api.check_token(enc_token, do_encode=False)
        s1 = api.get_json_with_urljoin(['create_sessionkey', enc_token])
        self.sessionkey = s1['sessionkey']
        self.userinfo = s1['userinfo']
        del self.userinfo['password']
        del self.userinfo['token']

        self.admin = Administration(self.userinfo, self.sessionkey, self.pprint)
        self.load_metainfo()


    # TODO: add pollutants
    def load_metainfo(self):
        self.all_region_infos = api.get_json_with_urljoin(['list_regions', self.sessionkey])
        self.all_regions = self.get_region_codes()
        self.all_pollutant_infos = api.get_json_with_urljoin(['list_pollutants', self.sessionkey])
        self.all_pollutants = self.get_pollutant_names()
        # self.count_pollutants = api.get(['count_pollutants', self.sessionkey])


    ##################################
    ## ADMINISTRATION
    ##################################    
    ## CALL: init_db()
    def init_db(self):
        self.admin.init_db()

    ## CALL: add_pollutant_synonym()
    def add_pollutant_synonym(self, pollutant_name='', add_synonym=''):
        self.admin.add_pollutant_synonym(pollutant_name, add_synonym)

    ## CALL: list_users()
    def list_users(self,return_type="dataframe"):
        return self.list_user(return_type)

    ## CALL: list_users()
    def list_user(self, return_type="dataframe"):
        return self.admin.list_user(return_type)
    
    ## CALL: print_user()
    def print_user(self):
        self.print_users()

    ## CALL: print_users()
    def print_users(self):
        self.admin.print_users()

    ## CALL: add_user()
    def add_user(self, useremail="", username="", affiliation="", userpassword=""
                 , auth_upload_rawdata=False, auth_upload_pmf=False, auth_admin=False):
        self.admin.add_user(useremail,username, affiliation, userpassword, 
                            auth_upload_rawdata,auth_upload_pmf,auth_admin)

    ## CALL: unconfirm_user()
    def del_user(self, useremail=None):
        self.admin.del_user(useremail)

    ## CALL: update_user()
    def update_user(self, useremail=None, username=None, affiliation=None, userpassword=None
                    , auth_upload_rawdata=None, auth_upload_pmf=None, auth_admin=None):
        self.admin.update_user(useremail,username, affiliation, userpassword, 
                            auth_upload_rawdata,auth_upload_pmf,auth_admin)

    ## CALL: confirm_user()
    def confirm_user(self, useremail=None):
        self.admin.confirm_user(useremail)

    ## CALL: unconfirm_user()
    def unconfirm_user(self, useremail=None):
        self.admin.unconfirm_user(useremail)

    ## CALL: set_admin()
    def set_admin(self, useremail=None):
        self.admin.set_admin(useremail)
    
    ## CALL: add_region()
    def add_region(self, region=None):
        self.admin.add_region(region) 

    ## CALL: del_region()
    def del_region(self, code=None):
        self.admin.del_region(code)
    
    ## CALL: add_pollutant()
    def add_pollutant(self, pollutant=None):
        self.admin.add_pollutant(pollutant) 

    ## CALL: del_pollutant()
    def del_pollutant(self, name=None):
        self.admin.del_pollutant(name)

    ##################################
    ## LISTING & PRINTING
    ##################################

    ## CALL: list_regions()
    def list_region(self, return_type="dataframe"):
        rst = api.get_json_with_urljoin(['list_regions', self.sessionkey])
        if return_type == "dataframe":
            return_value = pd.DataFrame.from_dict(rst)
        else:
            return_value = rst
        return return_value
    
    ## CALL: print_region()
    def print_region(self):
        regionlist = self.list_region(return_type="dict")
        self.pprint.print_region(regionlist)
    
    ## CALL: list_pollutant()
    def list_pollutant(self, return_type="dataframe"):
        rst = api.get_json_with_urljoin(['list_pollutants', self.sessionkey])
        if return_type == "dataframe":
            return_value = pd.DataFrame.from_dict(rst)
        else:
            return_value = rst
        return return_value
    
    ## CALL: print_pollutant()
    def print_pollutant(self):
        plist = self.list_pollutant(return_type="dict")
        self.pprint.print_pollutant(plist)

    ## CALL: list_pl()
    def list_pl(self, return_type="dataframe"):
        return self.list_pollutant(return_type)
    
    ## CALL: print_pl()
    def print_pl(self):
        self.print_pollutant()

    ## CALL: list_region_codes()
    def list_region_codes(self):
        rst = []
        regions =  api.get_json_with_urljoin(['list_regions', self.sessionkey])
        for r1 in regions:
            rst.append(r1['code'])
        return rst
    
    ## CALL: list_rawdataset()
    def list_rawdataset(self, return_type="dataframe"):
        rst = []
        regions = api.get_json_with_urljoin(['list_rawdataset', self.sessionkey])
        for r1 in regions:
            r1['upload_date'] = util.conv_isotime_to_date(r1['upload_date'], type="datetime")
            if r1['granularity'] == "date":
                r1['start_date'] = util.conv_isotime_to_date(r1['start_date'], type="date")
                r1['end_date'] = util.conv_isotime_to_date(r1['end_date'], type="date")
            else:
                r1['start_date'] = util.conv_isotime_to_date(r1['start_date'], type="datetime")
                r1['end_date'] = util.conv_isotime_to_date(r1['end_date'], type="datetime")
            del r1['uploader_id']
            del r1['sessionkey']
            rst.append(r1)

        if return_type == "dataframe":
            return_value = pd.DataFrame.from_dict(rst)
        else:
            return_value = rst
        return return_value
    
    ## CALL: print_rawdataset()
    def print_rawdataset(self):
        rlist = self.list_rawdataset(return_type="dict")
        self.pprint.print_rawdataset(rlist)

    ##################################
    ## REQUEST
    ##################################
    ## CALL: request()
    def request(self, datatype=None, region=None, pl=None, pollutant=None, date_from=None, date_to=None, year_from=None, year_to=None):
        return self.request_rawdata(datatype=datatype, region=region, pl=pl, pollutant=pollutant, date_from=date_from, date_to=date_to, year_from=year_from, year_to=year_to)

    ## CALL: request_rawdata()
    def request_rawdata(self, datatype=None, region=None, pl=None, pollutant=None, date_from=None, date_to=None, year_from=None, year_to=None):
        if pl != None:
            pollutant = pl
        # if datatype == None:
        #     util.print_error("Please define datatype.", exit=True)
        request = RawDataRequest(self.sessionkey, datatype=datatype, region=region, pollutant=pollutant, date_from=date_from, date_to=date_to, year_from=year_from, year_to=year_to)
        return request

    ##################################
    ## CALL: get_region_codes()
    ##################################
    def get_region_codes(self):
        rst = []
        for r1 in self.all_region_infos:
            rst.append(r1['code'])
        return rst

    ##################################
    ## CALL: get_pollutant_names()
    ##################################
    def get_pollutant_names(self):
        rst = []
        for r1 in self.all_pollutant_infos:
            rst.append(r1['name'])
        return rst
    
    ##################################
    ## CALL: upload_fron_file()
    ##################################
    def upload_from_file(self, file="", filetype="raw", datatype="", region="", update_force=False, na_string=['-999'], dateformat="%Y/%m/%d", granularity="date"):
        util.check_file(file)
        self.check_region(region)

        if granularity == "hour" and dateformat=="%Y/%m/%d":
            dateformat="%Y/%m/%d %H:%M"

        if filetype == "raw":
            ruploader = RawDataUploader(file, region, datatype, self.all_pollutant_infos, update_force, na_string, dateformat, granularity)
            ruploader.upload(self.sessionkey, self.userinfo)
        elif filetype == "pmf":
            puploader = PMFUploader(file, region, datatype)
        else:
            util.print_error("Wrong filetype!! Please select 'raw' or 'pmf' for filetype.")

    # DONE
    def check_region(self, region=""):
        if region not in self.all_regions:
            util.print_error("Wrong region code. Please select proper region code.")

    def close(self):
        api.get(['delete_sessionkey',self.sessionkey])

    