#!/usr/bin/env python
# coding: utf-8
import json
import time
import sys
import os
import subprocess
import datetime
import requests
import socket
import commands
import random
import cPickle
import MySQLdb as mysql

reload(sys);
sys.setdefaultencoding('utf8');

sys.path.append("..")
from configdb import *
from config import *


mdb = mysql.connect(user=user, passwd=passwd, host=host, port=port, db=dbname, charset=charset)
mdb.autocommit(True)
c = mdb.cursor()

#mdb = mysql.connect(user='opsdeploy', passwd='yclkAee2m', host='rm-uf6fku193l3ynx2p733150.mysql.rds.aliyuncs.com', port=3306, db='ops_deploy', charset='utf8')
#mdb.autocommit(True)
#c = mdb.cursor()


def exec_shell(shell_cmd):
    s = subprocess.Popen( shell_cmd, shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE  )
    newlog, stderr = s.communicate()
    return_status = s.returncode
    logs = '%s\n%s' % (newlog.strip(), stderr.strip())
    if return_status != 0:
        print shell_cmd
        #print(logs)


def project_info():
    sql = "SELECT * FROM `projectinfo` WHERE checkhttp = 'yes';"
    c.execute(sql)
    ones = c.fetchall()
    return ones


def gethostname(project):
    sql = "SELECT `ip`,`hostname`,`pnum` FROM `serverinfo` WHERE project = '%s';" % (project)
    c.execute(sql)
    ones = c.fetchall()
    hostnameinfo = {}
    for i in ones:
        if i[2] == '' or i[2] == 'null':
           pnum = 1
        else:
           pnum = int(i[2])
        hostnameinfo[i[0]] = [i[1], pnum]
    return hostnameinfo


def checkConsul(project, host, port, consulserver):
    consulurl = 'http://%s/v1/health/service/%s' %(consulserver, project)
    ServiceID = "%s-%s-%d" %(project, host, port)
    try:
        result = requests.get(consulurl,timeout=2).json()
        for node in result:
            if node['Checks'][1]['ServiceID'] == ServiceID:
                output = str(node['Checks'][1]['Output'])
                #if '200 OK Output' in output:
                if output.split()[3] in '200':
                    return {'status':'ok', 'output': output}
                else:
                    return {'status':'fail', 'output': output}
        output = 'consul No registration'
    except Exception as err:
        output = str(err)
    return {'status':'fail', 'output':output}

def update_consul_status(checkconsulstatus, checkconsultime, project, host):
    sql = "update serverinfo set checkconsulstatus='%s',checkconsultime='%s' WHERE project= '%s' and ip = '%s';" %(checkconsulstatus, checkconsultime, project, host)
    c.execute(sql)
    ones = c.fetchall()
    return ones


pinfos = project_info()

for pinfo in pinfos:
    project = pinfo[0]
    group = pinfo[1]
    environment = pinfo[2]
    p =  pinfo[3]
    codetype = pinfo[4]
    port = int(pinfo[5])
    git = pinfo[6]
    checkhttp = pinfo[9]

    hostnameinfo = gethostname(project)

    consulserver = 'consul.lc.com'

    for host in hostnameinfo:

        result = checkConsul(project, host, port, consulserver)
        #print result
        if result['status'] != 'ok':
            print project, host, port, result['status'],result['output']
        checkconsultime = time.strftime('%m%d_%H:%M')
        update_consul_status(result['status'], checkconsultime, project, host)
        print checkconsultime, p, host, port, result['status']
















