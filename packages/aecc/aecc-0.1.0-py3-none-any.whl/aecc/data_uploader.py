import pandas as pd
import json
from . import api
from . import util

class RawDataUploader():
    filepath = ""
    region = ""
    datatype = ""
    dataframe = None
    datatable = None
    all_pollutant_infos = []

    def __init__(self, file="", region="", datatype="", all_pollutant_infos=[], update_force=False, na_string=['-999'], dateformat="%Y/%m/%d", granularity="date"):
        self.filepath = file
        self.region = region
        self.datatype = datatype
        self.all_pollutant_infos = all_pollutant_infos
        self.update_force = update_force
        self.na_string = na_string
        self.dateformat = dateformat
        self.granularity = granularity

        # if file.lower().endswith(".xlsx") or file.lower().endswith(".xls"):
        #     pass
        #     # f1 = ExcelFile(file)
        #     # f1.print_sheet_infos()
        if file.lower().endswith(".tsv"):
            self.datatable = RawDataTable(pd.read_table(file))
            self.datatable.check_pollutants(self.all_pollutant_infos)

    def upload(self, sessionkey, userinfo):
        print("Uploading...")
        pdata = {}
        pdata['filepath'] = self.filepath
        pdata['region'] = self.region
        pdata['datatype'] = self.datatype
        pdata['granularity'] = self.granularity
        pdata['dateformat'] = self.dateformat
        pdata['sessionkey'] = sessionkey
        pdata['uploader_id'] = userinfo['_id']
        pdata['update_force'] = self.update_force
        pdata['na_string'] = self.na_string
        pdata['pollutants'] = self.datatable.pollutants
        pdata['data'] = json.loads(self.datatable.df.to_json(orient='records'))
        # rst = api.post(['data','fileupload', sessionkey], pdata)
        rst = api.post_json_with_urljoin(['data','dataupload', sessionkey], pdata)
        if rst['check']:
            print("Successfully uploaded.")
            print(rst['stat'])
        

class RawDataTable():
    columns = []
    pollutants = []

    def __init__(self, df):
        self.df = df
        self.columns = list(self.df.keys())
        self.pollutants = self.columns[1:]

    def check_pollutants(self, all_pollutant_infos=[]):
        pollutant_name_map = {}
        for pinfo in all_pollutant_infos:
            pollutant_name_map[pinfo['name'].lower()] = pinfo['name']
            for s1 in pinfo['synonym']:
                pollutant_name_map[s1.lower()] = pinfo['name']

        # TODO: pollutatant list에 없을때 오류 메시지 처리...
        for i in range(len(self.pollutants)):
            p1 = self.pollutants[i]
            try:
                p2 = pollutant_name_map[p1.strip().lower()]
                if p1 != p2:
                    self.pollutants[i] = p2
                    self.df.columns = self.df.columns.str.replace(p1, p2)
                    self.columns = list(self.df.keys())
                    
            except KeyError:
                util.print_error(p1 + " is not available pollutant name. Please contact a site admin.")
        

class PMFUploader():
    filepath = ""
    region = ""
    datatype = ""

    def __init__(self, file="", region="", datatype=""):
        self.filepath = file
        self.region = region
        self.datatype = datatype


