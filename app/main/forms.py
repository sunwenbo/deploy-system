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
from app.config import *



def check_time():
    T = time.localtime(time.time())
    WeekT = [0,1,2,3,4]
    AllT = [10,14,15,16,19]
    HalfT = [11,17]

    if int(T[6]) in WeekT:
        if int(T[3]) in AllT:
            return True
        elif int(T[3]) in HalfT:
            if int(T[4]) < 31:
                return True
        return False

def shellcmd(shell_cmd):
    s = subprocess.Popen( shell_cmd , shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE  )
    loginfo, stderr = s.communicate()
    return_status = s.returncode
    if return_status == 0:
        status = 'ok'
    else:
        loginfo = loginfo + '\n' + stderr
        status = 'fail'
    return {'status':status,'log':loginfo}


def writefile(path, content):
    f = open(path, 'w')
    f.write(content)
    f.flush()
    f.close()


def getdir(project):
    DIR = {}
    dir_path_git    = path_git.rstrip('/') + '/'    + project
    dir_path_log    = path_log.rstrip('/') + '/'    + project
    dir_path_lock   = path_lock.rstrip('/') + '/'   + project
    dir_path_conf   = path_conf.rstrip('/') + '/'   + project
    dir_path_result = path_result.rstrip('/') + '/' + project

    shell_cmd = '''mkdir -p %s %s %s %s %s ''' %(dir_path_git, dir_path_log, dir_path_lock, dir_path_conf, dir_path_result)
    Result = shellcmd(shell_cmd)

    DIR['git']     = dir_path_git
    DIR['log']     = dir_path_log
    DIR['lock']    = dir_path_lock
    DIR['conf']    = dir_path_conf
    DIR['result']  = dir_path_result

    return DIR

def getHostname(host):
    shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "hostname" ''' %(exec_user, host)
    Result = shellcmd(shell_cmd)
    return Result


def hostInit(project, host, Type):
    if Type == 'java':
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "cp -a %s/tomcat8_install_template %s/%s " ''' %(
                       exec_user, host, remote_host_path, remote_host_path, project)
    else:
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "mkdir -p %s %s" ''' %(
                       exec_user, host, supervisor_log_path, remote_host_path)
    Result = shellcmd(shell_cmd)
    if Result['status'] != 'ok':
        return Result['log']
    else:
        return Result['status']


def deployConfig(project, host, ones, ones1):
    try:
        DIR = getdir(project)

        supervisor_conf = ones.supervisor
        crond_conf = ones.crond

        variable = {
            '$USER$':                exec_user,
            '$HOST_PATH$':           remote_host_path,
            '$supervisor_log_path$': supervisor_log_path,
            '$environment$':         ones.environment,
            '$project$':             ones.project,
            '$ip$':                  host,
            '$pnum$':                ones1.pnum,
            '$env$':                 ones1.env,
            '$port$':                str(ones.port),
            '$ajpport$':             str(int(ones.port)-105),
            '$shutdownport$':        str(int(ones.port)-75)
        }
        for n, v in variable.items():
            supervisor_conf = supervisor_conf.replace(n, v)
            crond_conf = crond_conf.replace(n, v)
        supervisor_conf_path = '%s/%s_%s_supervisor.ini' %(DIR['conf'], project, host)
        writefile(supervisor_conf_path, supervisor_conf)

        crond_conf_path = '%s/%s_%s.crond' %(DIR['conf'], project, host)
        writefile(crond_conf_path, crond_conf)

        return 'ok'
    except Exception as err:
        return str(err)


#def logHandle(logtext):
#    variable = {
#                '<':                    '&#60;',
#                '>':                    '&#62;',
#                'ERROR:':               '<span style="color: red">ERROR:</span>',
#                'INFO:':                '<span style="color: green">INFO:</span>',
#                'WARN:':                '<span style="color: yellow">WARN:</span>',
#                'Git Code update:':     '<span style="color: blue">Git Code update:</span>',
#                'Code Compile:':        '<span style="color: blue">Code Compile:</span>',
#                'Version Backup:':      '<span style="color: blue">Version Backup:</span>',
#                'Update Config:':       '<span style="color: blue">Update Config:</span>',
#                'Del Service Start:':   '<span style="color: blue">Del Service Start:</span>',
#                'Rsync Code:':          '<span style="color: blue">Rsync Code:</span>',
#                'Pre Start Operation:': '<span style="color: blue">Pre Start Operation:</span>',
#                'Restart Service:':     '<span style="color: blue">Restart Service:</span>',
#                'Check Start:':         '<span style="color: blue">Check Start:</span>',
#                'Autotest Start:':      '<span style="color: blue">Autotest Start:</span>',
#                'Reg Service Start:':   '<span style="color: blue">Reg Service Start:</span>',
#                'branch:':              '<span style="color: green">git Branch:</span>',
#                'Author:':              '<span style="color: green"><br>git Author:</span>',
#                'Date:':                '<span style="color: green">git Date:</span>',
#                'Merge branch':         '<span style="color: green">Merge branch: </span>',
#                'newCommitId:':         '<span style="color: green">newCommitId:</span>',
#                '\t':                   '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;',
#                '\n':                   '<br>'
#    }
#    for n, v in variable.items():
#        result = logtext.replace(n, v)
#    result = '<font size="4" face="arial" >%s</font>' % (result)
#    #return result
#    return logtext

def logHandle(logtext):
    result   = logtext.replace(
                    '<', '&#60;').replace(
                    '>', '&#62;').replace(
                    'ERROR:', '<span style="color: red">ERROR:</span>').replace(
                    'INFO:', '<span style="color: green">INFO:</span>').replace(
                    'WARN:', '<span style="color: yellow">WARN:</span>').replace(
                    'Git Code update:', '<span style="color: blue">Git Code update:</span>').replace(
                    'Code Compile:', '<span style="color: blue">Code Compile:</span>').replace(
                    'Version Backup:', '<span style="color: blue">Version Backup:</span>').replace(
                    'Update Config:', '<span style="color: blue">Update Config:</span>').replace(
                    'Del Service Start:', '<span style="color: blue">Del Service Start:</span>').replace(
                    'Rsync Code:', '<span style="color: blue">Rsync Code:</span>').replace(
                    'Pre Start Operation:', '<span style="color: blue">Pre Start Operation:</span>').replace(
                    'Restart Service:', '<span style="color: blue">Restart Service:</span>').replace(
                    'Check Start:', '<span style="color: blue">Check Start:</span>').replace(
                    'Autotest Start:', '<span style="color: blue">Autotest Start:</span>').replace(
                    'Reg Service Start:', '<span style="color: blue">Reg Service Start:</span>').replace(
                    'branch:', '<span style="color: green">git Branch:</span>').replace(
                    'Author:', '<span style="color: green"><br>git Author:</span>').replace(
                    'Date:', '<span style="color: green">git Date:</span>').replace(
                    'Merge branch', '<span style="color: green">Merge branch: </span>').replace(
                    'newCommitId:', '<span style="color: green">newCommitId:</span>').replace(
                    'Code Update:', '<span style="color: blue">Code Update:</span>').replace(
                    'Config Update:', '<span style="color: blue">Config Update:</span>').replace(
                    'Docker URL:', '<span style="color: blue">Docker URL:</span>').replace(
                    'Yaml File:', '<span style="color: blue">Yaml File:</span>').replace(
                    'Config Filename:', '<span style="color: blue">Config Filename:</span>').replace(
                    'Pod Name:', '<span style="color: blue">Pod Name:</span>').replace(
                    'K8s ConfigMap Create:', '<span style="color: blue">K8s ConfigMap Create:</span>').replace(
                    'Pod Service Address:', '<span style="color: blue">Pod Service Address:</span>').replace(
                    'K8s Cluster Deploy:', '<span style="color: blue">K8s Cluster Deploy:</span>').replace(
                    '\t', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;').replace(
                    '\n', '<br>'
                )
    result = '<font size="4" face="arial" >%s</font>' % (result)

    return result


def slbReg(operation, pones, hones):
    pass

def dockerDel(pones, hones):
    if 'docker' in pones.codetype:
        project   = pones.project
        portstart = pones.port
        pnum      = hones.pnum
        host      = hones.ip

def slbReg(operation, pones, hones):
    pass

def dockerDel(pones, hones):
    if 'docker' in pones.codetype:
        project   = pones.project
        portstart = pones.port
        pnum      = hones.pnum
        host      = hones.ip
        for port in range(portstart, int(portstart) + int(pnum)):
            dockerName = '%s-%s' %(project, port)
            shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "docker rm -f %s" ''' %(
                           exec_user, host, dockerName)
            Result = shellcmd(shell_cmd)
            if Result['status'] != 'ok':
                return Result['log']


def dockerCrond(pones, hones):
    if pones.codetype == 'jobs':
        project   = pones.project
        port      = pones.port
        host      = hones.ip

        crond_conf_path = '%s/%s_%s.crond' %(DIR['conf'], project, host)
        remote_crond_conf_path = '%s/jobs/%s' %(remote_host_path, project)
        shell_cmd = 'rm -f %s' %(crond_conf_path)
        shellcmd(shell_cmd)

        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "true > %s " ''' %(
                       exec_user, host, remote_crond_conf_path)
        Result = shellcmd(shell_cmd)
        if Result['status'] != 'ok':
            return Result['log']



# chown $USER$:$USER$ /etc/cron.d
crontab_conf = '''#01 01 * * * $USER$ bash $HOST_PATH$$project$/job_start.sh >> $supervisor_log_path$$project$.log  2>&1 
'''


config_list = '''
#config list
'''


supervisor_python36_conf = '''[program:$project$]
environment=HOME=/home/$USER$,PROJECT_ENV="$environment$",PROJECT=$project$,PROJECT_PORT=$port$,PROJECT_PATH="$HOST_PATH$$project$/",PRODUCT_ENV="",$env$
directory=$HOST_PATH$$project$/
command=/usr/bin/python3.6  $HOST_PATH$$project$/main.py --port=%(process_num)02d
process_name=%(process_num)d
user=$USER$
startretries=5
stopsignal=TERM
autorestart=true
stopasgroup=true
redirect_stderr=true
stdout_logfile=$supervisor_log_path$/%(program_name)s-%(process_num)d.log
stdout_logfile_maxbytes=500MB
stdout_logfile_backups=10
loglevel=info
numprocs = $pnum$
numprocs_start=$port$
'''


catalina_sh = '''

#export JAVA_HOME="/opt/jdk1.8.0_45"

JAVA_OPTS="-server -Xms4000m -Xmx4000m -Xmn400m -XX:PermSize=256M -XX:MaxPermSize=256M -XX:+UseConcMarkSweepGC -XX:MaxTenuringThreshold=3 -XX:CMSInitiatingOccupancyFraction=70 -XX:CMSFullGCsBeforeCompaction=0 -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=$CATALINA_HOME/logs/dump.log.`date +%Y-%m-%d-%H-%M` -Xloggc:$CATALINA_HOME/logs/gc.log.`date +%Y-%m-%d-%H-%M`"

CATALINA_PID="$CATALINA_HOME"/temp/pid.tmp
'''

golang_dockerfile = '''FROM centos:centos7
ARG project
MAINTAINER www.senses-ai.com

RUN echo "Asia/Shanghai" >> /etc/timezone && rm -rf  /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN rpm -ivh https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm 

RUN mkdir -p /opt/project/config; 

WORKDIR /opt/project
COPY  ./$project  .

COPY  ./start.sh  .
'''

java8_dockerfile = '''FROM image.senses-ai.com/centos7-jdk1.8
ARG project
MAINTAINER www.senses-ai.com

RUN echo "Asia/Shanghai" >> /etc/timezone && rm -rf  /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN yum update -y && DEBIAN_FRONTEND=noninteractive yum install -y krb5-workstation krb5-libs wget
RUN mkdir /config
COPY startdir   /startdir
COPY optdir/*   /opt/

WORKDIR /startdir

'''


