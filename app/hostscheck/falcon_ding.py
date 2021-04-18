#!/usr/bin/python
# -*- coding: UTF-8 -*-
# * * * * * /usr/bin/python /home/bae/deploy/app/hostscheck/falcon_ding.py >>/home/bae/logs/falcon_ding.log 2>&1

import MySQLdb
import datetime
import urllib2
import json
import sys
import requests
from datetime import timedelta

reload(sys)
sys.setdefaultencoding('utf-8')


time = repr(str((datetime.datetime.now()-datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M")))


def send_dingding_message(content):
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=9f6b41e660f0b4968977ef6c90d98e6eaf3ebdcfccb407df62fa5902fafa19fa'
    #webhook = 'https://oapi.dingtalk.com/robot/send?access_token=b7f016498afa18627af203140731c17eb2619115622d7f60b418fd406b8a8676'
    data = {'msgtype': 'markdown', 'markdown': {'title': 'falcon报警', 'text': content}}
    #print(data)
    #ret = http_post(webhook, data)
    headers = {'Content-Type':'application/json'}
    try:
        requests.post(url=webhook, headers=headers, data=json.dumps(data))
    except Exception as err:
        print(str(err))



DBHOST = '127.0.0.1'
DBUSER = 'root'
DBPASSWD = ''
DBNAME = 'alarms'


db = MySQLdb.connect(host=DBHOST,user=DBUSER,passwd=DBPASSWD,db=DBNAME,charset='utf8')
db.autocommit(True)
cursor = db.cursor()


# online sql
#sql = "select distinct endpoint,note from event_cases where note not like '%%磁盘IO%%' and note not like '%%长期满载%%' and status != 'OK';" 
sql = "select distinct endpoint,note from event_cases where timestamp >= %s and note not like '%%磁盘IO%%' and note not like '%%长期满载%%' and status != 'OK';" % time
#sql = "select distinct endpoint,note from event_cases where timestamp >= %s and endpoint like '%%-lite-%%' and note not like '%%磁盘IO%%' and note not like '%%系统负载%%' and note not like '%%长期满载%%' and note not like '%%CPU使用率超过%%' and status != 'OK';" % time

try:
    cursor.execute(sql)

    for content in cursor.fetchall():
        #print(content)
        send_dingding_message(content)
except:
    db.rollback()

db.close()
