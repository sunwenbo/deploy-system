# deploy service check
#* * * * * cd /app/opsdeploy/app/hostscheck/;python service_alarm.py >> /data/log/service_alarm.log 2>&1
import sys, os, re
import MySQLdb as mysql
import json
import time
import cPickle
import requests

try:
    reload(sys)  # Python 2
    sys.setdefaultencoding('utf8')
except NameError:
    pass         # Python 3

sys.path.append("..")
from configdb import *
from config import *



mdb = mysql.connect(user=user, passwd=passwd, host=host, port=port, db=dbname, charset=charset)
mdb.autocommit(True)
c = mdb.cursor()


timestamp = int(time.time())


pkl = '/tmp/host_check_alarm.pkl'
try:
    pklFile = open(pkl, 'rb')
    pd = cPickle.load(pklFile)
    pklFile.close()
except:
    pd = {}


AlarmInfo = 'ServiceDown:'
RecoveryInfo = 'ServiceUP:'

try:
    sql = """select `project`,`hostname`,`ip`,`checkstatus`,`checktime` from `serverinfo`
                   where checkstatus != 'RUNNING' and checkstatus != 'Up' and checkstatus != 'SSHOK' and checkstatus != 'null'
                         and project not like 'qa_%' and project not like 'test_%'; """
    c.execute(sql)
    failData = c.fetchall()
except:
    failData = []
    AlarmInfo = 'ServiceDown: AlarmInfo SQL ERROR'

for s in pd.values():
    try:
        sql = """select `checkstatus`,`checktime`,`hostname` from `serverinfo`
                       where project = '%s' and ip = '%s';""" %(s['project'], s['ip'])
        c.execute(sql)
        ones = c.fetchall()
        if not ones:
            del pd["%s : %s" %(s['project'], s['ip'])]
            continue
        if ones[0][0] == 'RUNNING' or ones[0][0] == 'Up' or ones[0][0] == 'SSHOK':
            RecoveryInfo = '%s\n%s : %s %s %s %s' %(RecoveryInfo, s['project'], s['ip'], ones[0][2], ones[0][0], ones[0][1] )
            del pd["%s : %s" %(s['project'], s['ip'])]
    except:
        RecoveryInfo = 'ServiceUP: RecoveryInfo ERROR'


for i in failData:

    try:
        if i[2] in notcheckhost:
            continue
        if i[0] in filterList:
            continue
        pklFile = '/%s/%s/deploy.%s.lock' %(path_lock, i[0], i[0])
        if os.path.isfile(pklFile):
            continue

        k = "%s : %s" %(i[0], i[2])
        if k in pd:
            if timestamp - pd[k]['timestamp'] < 1200:
                print('warning: %s Non repeating alarm.' % (k))
                continue
        pd[k] = {'project':i[0], 'ip':i[2], 'status':i[3], 'timestamp':timestamp, 'hostname':i[1], 'atime':i[4] }
        AlarmInfo = '%s\n%s %s %s %s' %(AlarmInfo, k, i[1], i[3], i[4])
    except:
        AlarmInfo = 'ServiceDown: AlarmInfo ERROR'


pklFile = open(pkl, 'wb')
cPickle.dump(pd, pklFile)
pklFile.close()


checklogfile = '/data/log/service_check.log'
logtime = 60*5
try:
    ct = os.path.getmtime(checklogfile)
    intervaltime = timestamp - int(ct)
    if intervaltime > logtime:
        AlarmInfo = 'ERROR: Deploy service check log stop. time: %ss' %(intervaltime)
except:
    AlarmInfo = 'ERROR: Deploy service check stop'


headers = {'Content-Type':'application/json'}

if AlarmInfo != 'ServiceDown:':
    print(AlarmInfo)
    ExpansionHost = {
            "msgtype": "text",
            "text": {
                "content": AlarmInfo
            }
        }
    try:
        requests.post(url=sreRobot, headers=headers, data=json.dumps(ExpansionHost))
    except Exception as err:
        print(str(err))

if RecoveryInfo != 'ServiceUP:':
    print(RecoveryInfo)
    ExpansionHost = {
            "msgtype": "text",
            "text": {
                "content": RecoveryInfo
            }
        }
    try:
        requests.post(url=sreRobot, headers=headers, data=json.dumps(ExpansionHost))
    except Exception as err:
        print(str(err))
