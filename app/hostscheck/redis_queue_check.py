# coding:utf-8

import time
import redis
import requests
import json

rtime = time.strftime('%Y%m%d_%H%M%S')
T = time.localtime(time.time())

rds = redis.Redis(host='r-bp10f2ddc88c4314.redis.rds.aliyuncs.com', port=6379, password='QzYUy0BwqFZaGRuZvDtS', socket_timeout=10,db=0)

if T[3] in [8,9,10,11,12]:
    fits_num = 4000
else:
    fits_num = 20

qlist = {
           'queues:hts': 5,
           'queues:fits': fits_num,
           'queues:queue1129': 20
        }

content = 'Queue blocking: '

for key,block in qlist.items():
    num = rds.llen(key)
    print rtime,key,num
    if num > block:
        content = '%s\n[%s 当前: %s]' %(content, key, num)

if content != 'Queue blocking: ':
    print rtime,content
    dingdata = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    headers = {'content-type': 'application/json'}
    Robot = 'https://oapi.dingtalk.com/robot/send?access_token=cfaf2d6eca0bfe262647725434a040dd7afea2d0a2a8c445670947d11b827118'

    try:
        r = requests.post(url=Robot, data=json.dumps(dingdata), headers=headers, timeout=2).json()
    except Exception as err:
        print 'ERROR: notice dingding api error'
        print str(err)




















