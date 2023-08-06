import os
from requests.exceptions import (
    InvalidSchema,
)
import requests
from urllib.parse import urlparse
from urllib.parse import urlencode

def getDb(dbName,port=5149,charset='UTF-8'):
    params = {"dbName": dbName, "charset": charset};
    url = f'http://localhost:{port}/query?'+urlencode(params)
    res = requests.get(url).text
    return res

class HttpQuerier:
    def __init__(self, host="localhost",isSSL=False):
        self.host=host
        self.isSSL=isSSL

    def getQueryUrl(self, mydsUrl):
        parsed_url = urlparse(mydsUrl)
        scheme = parsed_url.scheme  # 获取协议
        if scheme!="myds":
            raise InvalidSchema(f"Requires 'myds' protocol for {mydsUrl!r}")
        prot="http"
        if self.isSSL:
            prot+="s"
        port = parsed_url.port
        if port is None:
            port=5149
        netloc = parsed_url.netloc  # 获取域名和端口
        params = {"dbName": netloc};
        urlStr = f'{prot}://{self.host}:{port}/query?'+urlencode(params)
        args = parsed_url.query  # 获取查询字符串
        if args!="":
            urlStr+="&"+args
        return urlStr

    def query(self, mydsUrl):
        urlStr=self.getQueryUrl(mydsUrl);
        res = requests.get(urlStr).text
        if res.startswith("[error]"):
            raise ConnectionError(res)
        parsed_url = urlparse(mydsUrl)
        path = parsed_url.path
        if path!="":
            if res.startswith("/"):
                res=res[0:-1]
            while len(path)>=3 and path[0:3]=="/..":
                res=os.path.dirname(res)
                path=path[3:]
            res+=path
        return res