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

mdb = mysql.connect(user='deploy', passwd='Deploy123', host='127.0.0.1', port=3306, db='cedardeploy', charset='utf8')
mdb.autocommit(True)
c = mdb.cursor()


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
    sql = "SELECT `ip`,`hostname` FROM `serverinfo` WHERE project = '%s';" % (project)
    c.execute(sql)
    ones = c.fetchall()
    hostnameinfo = {}
    for i in ones:
        pnum = 1
        hostnameinfo[i[0]] = [i[1], pnum]
    return hostnameinfo

pinfos = project_info()

for pinfo in pinfos:
    project = pinfo[0]

    port = int(pinfo[5])
    httpurl = pinfo[10]
    print httpurl

    hostnameinfo = gethostname(project)
    
    for host in hostnameinfo:
        print project, host, port

        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 bae@%s "python /opt/consul-agent/consul_reg.py reg %s %s %s '%s'" ''' %(host, project, host, port, httpurl)
        exec_shell(shell_cmd)















