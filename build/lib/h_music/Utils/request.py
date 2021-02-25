import requests
from hyper.contrib import HTTP20Adapter

def net_get(url, data=None, headers=None):
    if headers is None:
        headers = {}
    if data is None:
        data = {}
    return requests.get(url,params=data,headers=headers)

def net_post(url, data=None, headers=None):
    if headers is None:
        headers = {}
    if data is None:
        data = {}
    return requests.post(url,data=data,headers=headers)

def net2_session(index_url_list):
    session = requests.session()
    for index_url in index_url_list:
        session.mount(index_url, HTTP20Adapter())
    return session