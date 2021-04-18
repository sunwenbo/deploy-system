# coding:utf-8
# Created Time : Tue 31 Jul 2018 02:33:04 PM CST
# File Name: check_es.py

import requests
import json
import sys
import time


headers = {'content-type': 'application/json'}

data = {
    "query":{
        "bool":{
            "filter":{
                "range":{
                    "@timestamp": {
                       "gt": "now-5m",
                       "lt": "now"
                    }
                }
            },
            "must":{
                "match":{
                    "message":"exception"
                }
            },
            "must_not":{
                "match":{
                    "message":"INFO"
                }
            }
        }
    }
}


url = 'http://10.112.164.4:9200/laravel-*/_count'

url1000 = 'http://10.112.164.4:9200/laravel-*/_search?size=10000'

Robot = 'https://oapi.dingtalk.com/robot/send?access_token=fdb9222b70740eb96ad6fe98bff8e0ba4cea94ee696d586c8a13977b133e4f91'

try:
    num = requests.post(url, data=json.dumps(data), headers=headers).json()['count']
except Exception as err:
    print str(err)
    sys.exit(1)

if num > 50:
    try:
        jdata = requests.post(url1000, data=json.dumps(data), headers=headers).json()['hits']['hits']
    except Exception as err:
        print str(err)
        sys.exit(1)

    errlog = {}
    for mline in jdata:
        hostname = mline['_source']['beat']['hostname']
        if hostname in errlog:
            errlog[hostname] += 1
        else:
            errlog[hostname] = 1

    content = '[Laravel 5min Exception Error Total: %s ]' %(num)
    for h,n in errlog.items():
        content = '%s\n%s : %s' %(content, h, n) 
    print content
    dingdata = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    try:
        r = requests.post(url=Robot, verify=False, data=json.dumps(dingdata), headers=headers, timeout=2).json()
    except Exception as err:
        print 'ERROR: notice dingding api error'
        print str(err)






