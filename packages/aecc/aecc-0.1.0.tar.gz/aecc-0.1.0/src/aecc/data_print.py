from rich.table import Table
from . import util


class PrintData():

    def __init__(self):
        pass

    def print_users(self, userlist):
        table = Table(show_header=True)
        # ks = list(userlist[0].keys())
        # for k1 in ks:
            # table.add_column(k1, justify="right", no_wrap=False)
        table.add_column("email", justify="right", no_wrap=False)
        table.add_column("username", justify="right", no_wrap=False)
        table.add_column("affiliation", justify="right", no_wrap=False)
        table.add_column("signup_date", justify="right", no_wrap=False)
        table.add_column("last_connect_date", justify="right", no_wrap=False)
        table.add_column("last_connect_ip", justify="right", no_wrap=False)
        table.add_column("admin_confirmed", justify="right", no_wrap=False)
        table.add_column("admin_confirmed_date", justify="right", no_wrap=False)
        table.add_column("auth_upload_rawdata", justify="right", no_wrap=False)
        table.add_column("auth_upload_pmf", justify="right", no_wrap=False)
        table.add_column("auth_admin", justify="right", no_wrap=False)
        for r1 in userlist:
            table.add_row(r1['email'],r1['username'],r1['affiliation'],
                          util.conv_isotime_to_date(r1['signup_date']), util.conv_isotime_to_date(r1['last_connect_date'])
                          ,r1['last_connect_ip'], str(r1['admin_confirmed']),util.conv_isotime_to_date(r1['admin_confirmed_date'])
                          ,str(r1['auth_upload_rawdata']),str(r1['auth_upload_pmf']),str(r1['auth_admin']))
        util.print_console(table)

    def print_region(self, regionlist):
        table = Table(show_header=True)
        table.add_column("code", justify="right", no_wrap=False)
        table.add_column("ename", justify="right", no_wrap=False)
        table.add_column("kname", justify="right", no_wrap=False)
        table.add_column("num_date_field", justify="right", no_wrap=False)
        table.add_column("num_hour_field", justify="right", no_wrap=False)
        for r1 in regionlist:
            table.add_row(r1['code'],r1['ename'],r1['kname'],str(r1['num_date_field']),str(r1['num_hour_field']))
        util.print_console(table)

    def print_pollutant(self, plist):
        table = Table(show_header=True)
        table.add_column("name", justify="right", no_wrap=False)
        table.add_column("synonym", justify="right", no_wrap=False)
        # table.add_column("num_date_field", justify="right", no_wrap=False)
        # table.add_column("num_hour_field", justify="right", no_wrap=False)
        for r1 in plist:
            table.add_row(r1['name'], "; ".join(r1['synonym']) )
        util.print_console(table)

    def print_rawdataset(self, rlist):
        table = Table(show_header=True)
        table.add_column("region", justify="right", no_wrap=False)
        table.add_column("datatype", justify="right", no_wrap=False)
        table.add_column("granularity", justify="right", no_wrap=False)
        table.add_column("filepath", justify="left", no_wrap=False)
        table.add_column("start_date", justify="right", no_wrap=False)
        table.add_column("end_date", justify="right", no_wrap=False)
        table.add_column("uploader", justify="right", no_wrap=False)
        table.add_column("num_field", justify="right", no_wrap=False)
        table.add_column("num_pollutants", justify="right", no_wrap=False)
        table.add_column("upload_date", justify="right", no_wrap=False)
        for d1 in rlist:
            table.add_row(d1['region'], d1['datatype'], d1['granularity'],d1['filepath'], d1['start_date'], d1['end_date'], 
                          d1['uploader']['username']+"("+d1['uploader']['email']+")", str(d1['num_field']), str(d1['num_pollutants']), d1['upload_date'])
        util.print_console(table)