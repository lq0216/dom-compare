import os
import json
import urllib2
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

def byteify(obj):
    if isinstance(obj, dict):
        res = {}
        for key, value in obj.iteritems():
            res = dict(res, **{byteify(key): byteify(value)})
        return res
    elif isinstance(obj, list):
        res = []
        for i in obj:
            res.append(byteify(i))
        return res
    elif isinstance(obj, unicode):
        return obj.encode('utf-8')
    else:
        return obj

def compare_func(req):
    html_list = []
    for url in req['urls']:
        print url
        resp = urllib2.urlopen(url)
        doc = resp.read()
        print doc
        html_list.append(doc)
    print len(html_list)
    with open("test1.txt",'w') as fp1:
        fp1.write(html_list[0])
    with open("test2.txt",'w') as fp2:
        fp2.write(html_list[1])
    for i in range(len(html_list) - 1):
        if not (html_list[i] == html_list[i + 1]):
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    key_word = 'not '
    req = request.data
    req = json.loads(req)
    req = byteify(req)
    print req
    if len(req['urls']) < 1:
        return json.dumps({'code': 400, 'msg': 'please send more than one url!'})
    result = compare_func(req)
    print result
    if result:
        key_word = ''
    msg = 'These {0} dom are {1}the same!'.format(len(req['urls']), key_word)
    return json.dumps({'code': 200, 'msg': msg})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12346)
