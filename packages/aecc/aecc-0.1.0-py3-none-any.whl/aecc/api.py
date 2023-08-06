from . import conf
import sys
import ssl
import json
import urllib
import requests
from . import util

if (sys.version_info > (3, 0)):
    from html.parser import HTMLParser
    from urllib.parse import urlparse
    import urllib.request
else:
    from HTMLParser import HTMLParser
    import urlparse

def urljoin(arrparam):
    return urllib.parse.urljoin(conf.BACKEND, "/".join(arrparam))

def get_url(url):
    context = ssl._create_unverified_context()
    if (sys.version_info > (3, 0)):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, context=context)
        cont = response.read()
        return (cont.decode("UTF-8"))
    else:
        f = urllib.urlopen(url, context=context)
        return f.read()

def get(arrparam):
    if type(arrparam) == str:
        arrparam = [arrparam]
    return get_url(urljoin(arrparam))

def post(arrparam, fields):
    if type(arrparam) == str:
        arrparam = [arrparam]
    return post_url(urljoin(arrparam), fields)

def post_url(url, fields):
    params = urllib.parse.urlencode(fields)
    # print("params:", fields)
    print(url)
    response = requests.post(url, json=fields)
    # print(response.status_code)
    # data = urllib.request.urlopen(url, params).read()
    return response.text

def post_json_with_urljoin(arrparam, pdata):
    return json.loads(post(arrparam, pdata))


def post_multipart(host, selector, fields, files):
    import httplib
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()


def get_json_with_urljoin(arrparam):
    return json.loads(get_url(urljoin(arrparam)))

def get_json(url):
    return json.loads(get_url(url))


def check_backend():
    try:
        rst = get_json_with_urljoin (["heartbeat", util.getNow2()])
    except urllib.error.URLError:
        rst = {'check': False, "msg": "Connection Error !! - Please check a connection with "+conf.TITLE+" server!"}
    if not rst['check']:
        util.print_error(rst['msg'])
        sys.exit()
    return rst

def check_token(token, do_encode=True):
    if do_encode:
        enc_token = util.encode(token)
    else:
        enc_token = token

    try:
        rst = get_json_with_urljoin (["check_token", enc_token])
    except urllib.error.URLError:
        rst = {'check': False, "msg": "Connection Error !! - Please check a connection with "+conf.TITLE+" server!"}
    if not rst['check']:
        util.print_error (rst['msg'])
        sys.exit()

def datapost(pdata):
    url = urljoin(["data", "upload_data_post"])
    return post_url(url, pdata)