#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ministry

try:
    import json
    import codecs
    import os
    import requests
    import bs4
except Exception as e:
    raise e


def get(baseUrl, pathUrl):
    res = []
    date = ""
    req = requests.get(baseUrl + pathUrl)

    if req.ok:
        pesudo = bs4.BeautifulSoup(req.text, "lxml")
        select = pesudo.select(".block-left.clearfix h3 > a ")

        for url in select:
            url = baseUrl + url.attrs["href"]
            gpd = getPostData(url)
            res.append(gpd["data"])
            date = gpd["date"]

        dirPath = "post-data-all/"
        filePath = date[0: 10] + ".json"
        if not os.path.isdir(dirPath) :
            os.mkdir(dirPath)
        filename = os.path.join(dirPath, filePath)
        fs = codecs.open(filename, mode="wb", encoding="utf-8")
        json.dump(res, fs, ensure_ascii=False, indent=4)
        
    else:
        print ("No response. Status code: ", req.status_code)

    return date

def getPostData(url):
    res = {}
    res["url"] = url
    temp = {}
    dirPath = "post-data"
    req = requests.get(url)

    if req.ok:
        print (url)
        pesudo = bs4.BeautifulSoup(req.text, "lxml")

        title =  pesudo.select_one("h1#object_title") or pesudo.select_one("div.block-feature.block-feature-1 h1.title-2") or pesudo.select_one("div.title-2 clearfix + h1") or pesudo.select_one("html title")
        temp["title"] = title.text

        sub_tittle = pesudo.select_one("article.fck header b") or  pesudo.select_one("h2.txt-head") or pesudo.select_one("div.sp-detail-content p")
        temp["sub_tittle"] = sub_tittle.prettify()

        content = pesudo.select_one("div.fck") or pesudo.select_one("div.detailfck") or pesudo.select_one("article.fck") or pesudo.select_one("div.w980")
        temp["content"] = content.prettify()

        pub_date = pesudo.select_one("span.date") or pesudo.select_one("span.publish-date")
        temp["pub_date"] = pub_date.text

        res["data"] = temp

        # print title.text.strip()
        if not os.path.isdir(dirPath) :
            os.mkdir(dirPath)

        filename =  temp["pub_date"][6: 10]  + "-" + temp["pub_date"][3: 5] + "-" + temp["pub_date"][0: 2] + temp["pub_date"][10: 17] + url[19:-4] + ".json"
        filename = os.path.join(dirPath, filename)
        file = codecs.open(filename, encoding="utf-8", mode="wb")
        json.dump(res, file, ensure_ascii=False, indent=4)

        return {"data": res, "date": temp["pub_date"][6: 10]  + "-" + temp["pub_date"][3: 5] + "-" + temp["pub_date"][0: 2] + temp["pub_date"][10: 17]}
    else:
        print ("No response. Status code: ", req.status_code)