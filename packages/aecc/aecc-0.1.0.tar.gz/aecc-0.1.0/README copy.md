# AECC

AECC is the air quality database maintained by SNU APCC.
<!--Read the full documentation at [https://aecc.readthedocs.io](https://aecc.readthedocs.io) -->

## Installation

To install `aecc`, 

```
pip install https://github.com/danielmsk/snuair/dist/aecc-0.0.1-py3-none-any.whl
pip install aecc
```

### Prerequisite
* pandas ([https://pandas.pydata.org/](https://pandas.pydata.org/))

## Getting Started
```
>>> import aecc
>>> aecc.download_key(file="~/user.key")
email: user@email.com
password: userpassword
>>> conn = aecc.connector(keyfile='~/user.key')
>>> conn.all_regions
['','', '', '', '', ...
>>> conn.all_pollutants
['CO', '']
>>> conn.count_pollutants
{'CO': 323, 'NO': 25}
>>> r = conn.request(region="", from="2007-08-12", to="2020-09-15")
>>> r.download_to_file(path="data/raw.tsv", type="tsv")
>>> r.all_pollutants
['CO', '']
>>> r.count_pollutants
{'CO': 323, 'NO': 25}
>>> list1 = r.to_list()
>>> list1
[ 
	{datetime:"2007-08-12", region="CN", CO2=25.3, },
	{datetime:"2007-08-13", region="CN", CO2=25.3, },
]
>>> s1 = r.to_series()
>>> df1 = r.to_dataframe()

### upload data
>>> cnx.dataupload(file="data/update.tsv", type="tsv")
>>> cnx.close()
```

**CLI(Command-line interface)** 

```
# Download userkey
$ aecc -download_key
email: user@email.com
password: userpassword

# 
$ aecc -download region -key ~/user.key
$ aecc -download polutant -key ~/user.key
$ aecc -download user -key ~/user.key

$ aecc -print region -key ~/user.key


```


## Sing-up and sign-in

### Sign-up
```
>>> import aecc
>>> aecc.signup()
user email: user@email.com
user name: Tom
orgcode: snu
password: userpassword
```

### Download userkey
```
>>> aecc.download_key(file="~/user.key")
email: user@email.com
password: userpassword

####### CLI #######
$ aecc -download_key
email: user@email.com
password: userpassword
```

## Request Data



## List Data


### listing regions

```
>>> conn.all_regions
['','', '', '', '', ...
```

### listing pollutants

```
>>> conn.all_regions
['','', '', '', '', ...
```

### listing pmf results

```
>>> conn.list_pmf
['','', '', '', '', ...
```


## Print statistics

```
>>> conn.stat
>>> conn.stat_regions
>>> r.stat
```


## Download Data

```
>>> r.download_to_file(path="data/raw.csv", type="csv")
>>> r.download_to_file(path="data/raw.xlsx", type="xlsx")
```


## Upload Data

This uploading data function is for the users that have permission to upload data. If you don't have permission to upload data, please contact the admin.  


### from file

```
>>> conn.upload_from_file(path="data/raw.csv", type="raw")
>>> conn.upload_from_file(path="data/raw.xlsx", type="raw")
>>> conn.upload_from_file(path="data/test_Constrained.xls", type="pmf", title="2019_Seoul")
```




## Adminitstration

### User management for admin
```
>>> cnx = aecc.connector(keyfile='~/user.key')
>>> cnx.userlist()
[{''}]
```



## CLI(Command-line interface) usage

### CLI Options

```
optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
  -download_key  download key file
  -signup        signup user
  -download      download
  -log LOG       log file
```

### Sign-up and sign-in with userkey
```
> aecc -signup
email : user@email.com
username: Tom
orgcode: snu
password: userpassword
password(confirm): userpassword
```

### Download key file
```
> aecc -download_key
email : user@email.com
password : userpassword
```



### Data upload

```
aecc -dataupload 
```



## Administration Options
These options are for the adminstrator. 

### User management
```
```

### 


## Version History
### 0.1.0 (2023.03.06)
* 
