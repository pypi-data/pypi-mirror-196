from . import api
from . import util
import pandas as pd
import numpy as np



class RawDataRequest():
    sessionkey = ""
    dataframe = None

    def __init__(self, sessionkey=None, datatype=None,  region=None, pollutant=None, date_from=None, date_to=None, year_from=None, year_to=None):
        self.sessionkey = sessionkey
        if type(region) == str:
            self.region = [region]
        else:
            self.region = region
        if type(pollutant) == str:
            self.pollutant = [pollutant]
        else:
            self.pollutant = pollutant
        self.datatype = datatype
        self.date_from = date_from
        self.date_to = date_to
        self.year_from = year_from
        self.year_to = year_to

        self.datasearch()


    def datasearch(self):
        pdata = {}
        pdata['region'] = self.region
        pdata['pollutant'] = self.pollutant
        pdata['datatype'] = self.datatype
        pdata['date_from'] = self.date_from
        pdata['date_to'] = self.date_to
        pdata['year_from'] = self.year_from
        pdata['year_to'] = self.year_to

        print ("Requesting...")
        regions =  api.post_json_with_urljoin(['data','search_rawdata', self.sessionkey], pdata)
        self.dataframe = pd.DataFrame.from_dict(regions['row'])
        if self.dataframe.size > 0:
            self.dataframe['date'] = pd.to_datetime(self.dataframe['date'], infer_datetime_format=True)
            self.dataframe = self.dataframe.replace(-999, np.nan)
    
    def to_dataframe(self):
        return self.dataframe

    def save(self, out="", filetype="tsv", na_string=""):
        if out == "":
            util.print_error("Please add a filename in 'out' param.")
        if filetype=="tsv":
            self.dataframe.to_csv(out, sep='\t', index=False, na_rep=na_string)
            print("Saved " + out)
        if filetype=="csv":
            self.dataframe.to_csv(out, index=False, na_rep=na_string)
            print("Saved " + out)
        if filetype=="xlsx":
            self.dataframe.to_excel(out, index=False, na_rep=na_string)
            print("Saved " + out)
        if filetype=="json":
            self.dataframe.to_json(out, orient="records")
            print("Saved " + out)


    def count(self):
        pass