# coding:utf-8
import requests
import re
import json
import sys
from datetime import datetime

rootUrl = "http://msdn.itellyou.cn"

reload(sys)
sys.setdefaultencoding('utf-8')

def GetIndexList():
    r = requests.get(rootUrl)
    indexArr = re.findall(r'data-menuid="([^"]*)"[^>]*>([^<]*)', r.text)
    indexList = {}
    for item in indexArr:
        indexId = item[0]
        indexName = item[1]
        indexList[indexName] = indexId
    return indexList

def GetIndex(indexId):
    url = rootUrl + "/Category/Index"
    headers = {
        "Referer": rootUrl,
    }
    payload = {"id": indexId}
    r = requests.post(url, headers=headers, params=payload, timeout=30)
    return json.loads(r.content)

def GetLang(langId):
    url = rootUrl + "/Category/GetLang"
    headers = {
        "Referer": rootUrl,
    }
    payload = {"id": langId}
    r = requests.post(url, headers=headers, params=payload, timeout=30)
    return json.loads(r.content)

def GetList(langId, lang):
    url = rootUrl + "/Category/GetList"
    headers = {
        "Referer": rootUrl,
    }
    payload = {
        "id": langId,
        "lang": lang,
        "filter": "false",
    }
    r = requests.post(url, headers=headers, params=payload, timeout=30)
    return json.loads(r.content)

def GetProduct(productId):
    url = rootUrl + "/Category/GetProduct"
    headers = {
        "Referer": rootUrl,
    }
    payload = {"id": productId}
    r = requests.post(url, headers=headers, params=payload, timeout=30)
    #print(productId, r.content)
    return json.loads(r.content)

#indexId = "36d3766e-0efb-491e-961b-d1a419e06c68"
#data = GetIndex(indexId)
#print(data)

#productId = "838edc07-437f-43a4-8ae6-4771b04dbc2f"
#GetProduct(productId)

def Run():
    indexList = GetIndexList()
    for indexName, indexId in indexList.items():
        indexData = GetIndex(indexId)
        for item in indexData:
            langId = item["id"]
            submenuName = item["name"]
            langData = GetLang(langId)
            if langData["status"]:
                for li in langData["result"]:
                    sublangId = li["id"]
                    lang = li["lang"]
                    productListData = GetList(langId, sublangId)
                    if productListData["status"]:
                        for i in productListData["result"]:
                            subname = i["name"].replace('"', '""')
                            productId = i["id"]
                            try:
                                product = GetProduct(productId)
                                if product["status"]:
                                    download = product["result"]["DownLoad"]
                                    time = product["result"]["PostDateString"]
                                    sha1 = product["result"]["SHA1"]
                                    size = product["result"]["size"]
                                    print(u'"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}"'. format(indexName, submenuName, lang, subname, time, download, sha1, size))
                            except:
                                download = i["url"] or ""
                                tmp = re.findall("\d+", i["post"])
                                ts = int(tmp[0])/1000
                                time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
                                sha1 = "未知"
                                size = "未知"
                                print(u'"{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}"'. format(indexName, submenuName, lang, subname, time, download, sha1, size))
Run()

