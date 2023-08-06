import aecc


# def test_answer():
#     assert inc(3) == 5

def test_signup():
    aecc.signup()

def test_download_token():
    aecc.download_token()

def test_connect(tokenfile=""):
    if tokenfile != "":
        conn = aecc.connect(tokenfile)
    else:
        conn = aecc.connect()
    print(conn.sessionkey)
    return conn

def test_ex():
    cnx = aecc.connect()
    print(cnx.all_regions)
    print(cnx.all_pollutants)
    print(cnx.count_pollutants)
    
    print(cnx.userlist()) ## for admin
    cnx.close()
    
    cnx.dataupload(file="test/data/PL.tsv", filetype="tsv", region="PL")

def test_listing(conn):
    print(conn.all_regions)
    print(conn.all_region_infos)
    print(conn.list_region())
    print(conn.list_region_codes())
    print(conn.all_pollutants)
    print(conn.all_pollutant_infos)

def test_raw_data_upload(conn):
    # print(conn.all_regions)
    conn.print_region()
    conn.upload_from_file(file="test/data/(211026)GJ_input_unc.tsv", filetype="raw", datatype="unc", region="GJ", na_string=['-999'])
    # conn.upload_from_file(file="test/data/(211026)GJ_input_unc.tsv", filetype="raw", datatype="unc", region="GJ", update_force=True)
    # conn.upload_from_file(file="test/data/(211026)GJ_input_conc.tsv", filetype="raw", datatype="conc", region="GJ", na_string=['-999'])

    # conn.upload_from_file(file="test/data/(220411)Gwangju_input_file_unc.tsv", filetype="raw", datatype="unc", region="GJ", na_string=['-999'])
    # conn.upload_from_file(file="test/data/(220411)Gwangju_input_file_conc.tsv", filetype="raw", datatype="conc", region="GJ", na_string=['-999'])
    
    # conn.upload_from_file(file="test/data/(211026)JN_input_unc.tsv", filetype="raw", datatype="unc", region="JN", na_string=['-999'])
    # conn.upload_from_file(file="test/data/(211026)JN_input_conc.tsv", filetype="raw", datatype="conc", region="JN", na_string=['-999'])
    # conn.upload_from_file(file="test/data/(220411)Incheon_input_file_unc.tsv", filetype="raw", datatype="unc", region="IC", na_string=['-999'])
    # conn.upload_from_file(file="test/data/(220411)Incheon_input_file_conc.tsv", filetype="raw", datatype="conc", region="IC", na_string=['-999'])
    # conn.upload_from_file(file="test/data/(220421)Jeju_input_file_nss_unc.tsv", filetype="raw", datatype="unc", region="JJ", na_string=['-999'])
    # conn.upload_from_file(file="test/data/(220421)Jeju_input_file_nss_conc.tsv", filetype="raw", datatype="conc", region="JJ", na_string=['-999'])
    
    # conn.upload_from_file(file="test/data/대기환경연구소_서울대_백령도_conc.tsv", filetype="raw", datatype="conc", region="BN", dateformat="%Y/%m/%d %h:%M",  granularity="hour")
    # conn.upload_from_file(file="test/data/대기환경연구소_서울대_수도권_conc.tsv", filetype="raw", datatype="conc", region="CP", dateformat="%Y/%m/%d %h:%M",  granularity="hour")
    # conn.upload_from_file(file="test/data/대기환경연구소_서울대_중부권_conc.tsv", filetype="raw", datatype="conc", region="JB", dateformat="%Y/%m/%d %h:%M",  granularity="hour")

    # conn.upload_from_file(file="test/data/(2ndKC1)china_rawdata_CRAES_conc.tsv", filetype="raw", datatype="conc", region="CR", dateformat="%Y/%m/%d",  granularity="date")

    # conn.upload_from_file(file="test/data/(211026)GJ_input.xlsx", filetype="raw")
    # conn.upload_from_file(file="test/data/GJ_input.xlsx", type="raw")


def test_pmf_upload(conn):
    conn.upload_from_file(file="test/data/(2ndKC1)china_rawdata_CRAES_conc.tsv", filetype="pmf", datatype="conc", region="CR", dateformat="%Y/%m/%d",  granularity="date")

def test_request(conn):
    # print(conn.list_rawdataset())
    conn.print_rawdataset()
    # conn.print_region()
    # conn.print_pollutant()
    # conn.print_pl()
    # req = conn.request()
    # req = conn.request(region=["JN","IC"])
    req = conn.request(region=["CR","BN"])
    # req = conn.request(datatype="conc", region=["JN","IC"])
    # req = conn.request(datatype="conc", region=["JN","IC"], date_from="2020-10-01")
    # req = conn.request(datatype="conc", region=["JN","IC"], date_from="2020-10-01", date_to="2020-12-31")
    # req = conn.request(datatype="conc", region=["JN","IC"], date_from="2020-10-01", date_to="2020-12-31", pl=["Ti","Cr"])
    df = req.to_dataframe()
    print(df)
    # print(df.info())

def test_save_data(conn):
    req = conn.request(datatype="conc", region=["JN","IC"], date_from="2020-10-01", date_to="2020-12-31")
    req.save(out="test/out_test.tsv", filetype="tsv", na_string="-999")
    req.save(out="test/out_test.csv", filetype="csv", na_string="NA")
    req.save(out="test/out_test.xlsx", filetype="xlsx")
    req.save(out="test/out_test.json", filetype="json")

# ADMINISTRATION
def test_admin_init_db(conn):
    conn.init_db()

def test_admin_user_list(conn):
    print(conn.list_user())
    conn.print_users()

def test_admin_user(conn):
    conn.add_user(useremail="demo@demo.com", username="홍길동", affiliation="데모컴퍼니", userpassword="demo1234", auth_upload_rawdata=True)
    conn.print_users()
    conn.update_user(useremail="demo@demo.com", auth_upload_pmf=True)
    conn.print_users()
    conn.set_admin(useremail="demo@demo.com")
    conn.print_users()
    conn.unconfirm_user(useremail="demo@demo.com")
    conn.print_users()
    conn.confirm_user(useremail="demo@demo.com")
    conn.del_user(useremail="demo@demo.com")
    conn.print_users()


def test_admin_add_pollutant_synonym(conn):
    print(conn.all_pollutant_infos)
    conn.add_pollutant_synonym(pollutant_name='SO42-', add_synonym='SO4-')

def test_admin_region(conn):
    region = {'code':'GA', 'ename':'Gwanak', 'kname':'관악'}
    conn.add_region(region)
    conn.print_region()
    conn.del_region('GA')
    conn.print_region()

def test_admin_pollutant(conn):
    pollutant = {'name':'TEST+', 'synonym':['TEST1', 'TEST2', 'TEST3']}
    conn.add_pollutant(pollutant)
    conn.print_pollutant()
    conn.del_pollutant('TEST+')
    conn.print_pollutant()

if __name__=="__main__":
    # test_signup()
    # test_download_token()
    # conn = test_connect("./demo_user.aecctoken")
    conn = test_connect("./demo_admin.aecctoken")

    ##### ADMINISTRATION
    test_admin_init_db(conn)
    # test_admin_add_pollutant_synonym(conn)
    # test_admin_user_list(conn)
    # test_admin_user(conn)
    # test_admin_region(conn)
    # test_admin_pollutant(conn)

    ##### GENERAL USER
    # test_listing(conn)
    # test_raw_data_upload(conn)
    # test_pmf_upload(conn)
    # test_request(conn)
    # test_save_data(conn)
    # test_ex()

    
    
    