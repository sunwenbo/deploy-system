# coding:utf-8
# Created Time : Tue 31 Jul 2018 02:33:04 PM CST
# File Name: check_es.py

import requests
import json
import sys
import time


headers = {'content-type': 'application/json'}

data = {
    "query": {
        "bool": {
            "must": [
                {
                    "range": {
                        "@timestamp": {
                            "gt": "now-5m",
                            "lt": "now"
                        }
                    }
                },
                {
                    "range": {
                        "status": {
                            "gte": "500",
                            "lt": "600"
                        }
                    }
                }
            ]
        }
    }
}

url = 'http://10.112.164.4:9200/logstash-nginxaccess-*/_count'

url1000 = 'http://10.112.164.4:9200/logstash-nginxaccess-*/_search?size=10000'

Robot = 'https://oapi.dingtalk.com/robot/send?access_token=fdb9222b70740eb96ad6fe98bff8e0ba4cea94ee696d586c8a13977b133e4f91'

try:
    num = requests.post(url, data=json.dumps(data), headers=headers).json()['count']
except Exception as err:
    print str(err)
    sys.exit(1)


print num
if num > 10:
    try:
        jdata = requests.post(url1000, data=json.dumps(data), headers=headers).json()['hits']['hits']
    except Exception as err:
        print str(err)
        sys.exit(1)

    errlog = {}
    for mline in jdata:
        hostname = mline['_source']['beat']['hostname']
        api = mline['_source']['api']
        if hostname in errlog:
            if api in errlog[hostname]:
                errlog[hostname][api] += 1
            else:
                errlog[hostname][api] = 1
        else:
            errlog[hostname] = {api:1}

    content = '[ Nginx 5min 5XX Error Total: %s ]' %(num)
    for h,n in errlog.items():
        content = '%s\n%s' %(content, h) 
        for api,num in n.items():
            content = '%s\n  %s : %s' %(content, api, num ) 

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






