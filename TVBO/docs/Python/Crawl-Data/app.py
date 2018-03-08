#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ministry

try:
    import json
    import os
    from flask import Flask
    from flask import render_template
    baseUrl = "https://tuoitre.vn"
    pathUrl = "/tin-moi-nhat.htm"
    import tuoitre
    tuoitre.get(baseUrl, pathUrl)
except Exception as e:
    raise e


app = Flask(__name__)

@app.route('/')
def main():
    pathName = "post-data-all/"
    try:
        import glob
        import codecs
        # import tuoitre
        # tuoitre.get(baseUrl, pathUrl)
        filename = glob.glob(pathName  + "*.json").pop()        
        fs = codecs.open(filename, encoding="utf-8")
    except Exception as e:
        raise e
    finally:
        return render_template("index.html", data=json.load(fs))


@app.route('/post/<posturl>')
def postDetails(posturl):
    pathName = "post-data/"
    try:
        import glob
        import codecs
        filename = glob.glob(pathName  + "*" +  posturl[0:-4] + ".json").pop()
        fs = codecs.open(filename, encoding="utf-8")
        res = json.load(fs)
    except Exception as e:
        raise e
    finally:
        return render_template("post.html", data=res)

app.run(host='0.0.0.0')