import pandas as pd


class ExcelFile():
    filepath = ""
    sheet_names = []
    num_sheet = 0
    unc_sheetname = ""
    unc_sheetnames = []
    conc_sheetname = ""
    conc_sheetnames = []

    def __init__(self, file=""):
        self.filepath = file
        self.load_file()

    def load_file(self):
        xl = pd.ExcelFile(self.filepath)
        self.sheet_names = xl.sheet_names
        self.num_sheet = len(self.sheet_names)
        for sheetname in self.sheet_names:
            if "unc_" in sheetname.lower() or "_unc" in sheetname.lower():
                self.unc_sheetnames.append(sheetname)
                self.check_sheet(sheetname)
            if "conc_" in sheetname.lower() or "_conc" in sheetname.lower():
                self.conc_sheetnames.append(sheetname)
                self.check_sheet(sheetname)
        # self.check_pollutants(self.unc_sheetnames)
        # self.check_pollutants(self.conc_sheetnames)

    def check_sheet(self, sheetname=""):
        df = pd.read_excel(self.filepath, sheet_name=sheetname)
        


    # TODO: ExcelFile > print_sheet_infos
    def print_sheet_infos(self):
        print("File Path: " + self.filepath)
        print("Number of sheets: " + str(self.num_sheet))
        print("conc sheets: " + ", ".join(self.conc_sheetnames))
        print("unc sheets: " + ", ".join(self.unc_sheetnames))
        
        # df = pd.read_excel(file, sheet_name=unc_sheetname)
        # print(df)
        # df = pd.read_excel(file, sheet_name=conc_sheetname)
        # print(df)