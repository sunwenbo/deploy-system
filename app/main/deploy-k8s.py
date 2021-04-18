#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
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
import yaml
import MySQLdb as mysql

print('%s' % sys.path[0])

sys.path.append("..")
from configdb import *
from config import *



reload(sys);
sys.setdefaultencoding('utf8');


mdb = mysql.connect(user=user, passwd=passwd, host=host, port=port, db=dbname, charset=charset)
mdb.autocommit(True)
c = mdb.cursor()


def project_info(project):
    print(project)
    #查询项目信息赋值给ones。并返回ones下标为0的数据
    sql = "SELECT * FROM `projectinfo` WHERE project = '%s';" % (project)
    #执行sql语句
    c.execute(sql)
    #fetchall()返回多个元组，即返回多个记录(rows), 如果没有结果则返回()，ones为元组
    ones = c.fetchall()
    return ones[0]

def k8scluster_info(environment, k8smanagename):
    print(environment,k8smanagename)
    sql = "SELECT k8smanagefilecontent,k8snodeip1,k8snode1 FROM `k8scluster` WHERE environment = '%s' and k8smanagename = '%s';" % (environment, k8smanagename)
    c.execute(sql)
    ones = c.fetchall()
    return ones[0]

class Deploy:
    def __init__(self, project, tag, taskid, operation, currentuser, reason):

        self.project     = project
        self.tag         = tag
        self.taskid      = taskid
        self.operation   = operation
        self.currentuser = currentuser
        self.reason      = reason
        #查询当前项目信息赋值给pinfo
        pinfo  = project_info(project)
        print(pinfo)
        #赋值给变量
        self.group            = pinfo[1]
        self.environment      = pinfo[2]
        self.p                = pinfo[3]
        self.codetype         = pinfo[4]
        self.port             = int(pinfo[5])
        self.git              = pinfo[6]
        self.branch           = pinfo[7]

        self.config           = pinfo[8]
        self.make             = pinfo[9].strip()
        self.start            = pinfo[10]
        self.remarks          = pinfo[11]
        self.dockerfile       = pinfo[12]
        self.k8syaml          = pinfo[13]
        self.makepath         = pinfo[14]
        self.k8smanagename    = pinfo[15]
        self.nodeport         = int(pinfo[16])
        self.namespace        = pinfo[17]
        if self.namespace == '' or self.namespace == 'null':
            self.namespace = 'default'

        try:
            k8scluster = k8scluster_info(self.environment, self.k8smanagename)
            self.k8smanagefilecontent = k8scluster[0]
            self.k8snodeip1           = k8scluster[1]
            self.k8snode1             = k8scluster[2]
        except:
            self.k8smanagefilecontent = 'null'
            self.k8snodeip1           = '{{ k8snodeip1 }}'
            self.k8snode1             = '{{ k8snode1 }}'

        self.host             = 'Deploy'
        self.hostName         = 'Deploy'
        self.status           = 'ok'
        self.progress         = 0
        self.commitid         = ''
        self.configfilename   = '%s.conf' %self.p

        self.execUser         = exec_user
        self.basicGlist       = basicGlist
        self.groupRobot       = groupRobot
        self.sreRobot         = sreRobot
        self.autotestURL      = autotestURL
        self.autolist         = autolist
        self.confgit          = confgit
        self.java_commons_git = java_commons_git
        self.imgaddr          = imgaddr
        self.dockerurl        = '%s/%s/%s' %(self.imgaddr, self.group, self.project)
        self.dockertag        = 'latest'

        print(self.autolist)

        #定义了一大堆目录,之后会在服务器创建这些目录
        self.dir_path_git    = path_git.rstrip('/') + '/'    + self.project
        self.dir_path_log    = path_log.rstrip('/') + '/'    + self.project
        self.dir_path_lock   = path_lock.rstrip('/') + '/'   + self.project
        self.dir_path_conf   = path_conf.rstrip('/') + '/'   + self.project
        self.dir_path_result = path_result.rstrip('/') + '/' + self.project
        self.dir_path_off    = path_off.rstrip('/') + '/'    + self.group
        #赋值操作
        self.path    = '%s/%s' %(self.dir_path_git, self.project)
        self.commons = '%s/%s' %(self.dir_path_git, self.codetype)
        self.pklFile = '%s/deploy.%s.lock' %(self.dir_path_lock, self.project)
        self.logPath = file('%s/%s-%s.log' % (self.dir_path_result, self.tag, self.taskid), 'a+')
        self.k8smanagefilepath = '%s/%s-%s.k8s' %(path_conf, self.environment, self.k8smanagename)
        self.k8syamlfilepath = '%s/%s_pod.yaml' %(self.dir_path_conf, self.project)
        self.configfilepath = '%s/%s.conf.toml' %(self.dir_path_conf, self.project)

        self.makepath   = self.vsub(self.makepath)
        self.make       = self.vsub(self.make)
        self.start      = self.vsub(self.start)
        self.dockerfile = self.vsub(self.dockerfile)
        self.k8syaml    = self.vsub(self.k8syaml)

        self.writefile(self.configfilepath, self.config)
        self.writefile(self.k8smanagefilepath, self.k8smanagefilecontent)

        #定义一个字典，控制服务的状态
        self.makeFun      = {   
                                #更新操作
                                "serviceUpdate":       self.makeUpdate,
                                #回滚操作
                                "serviceFallback":     self.makeFallback
                            }

    def vsub(self, content):
        variable = {
            '$project$':             self.project,
            '$p$':                   self.p,
            '$group$':               self.group,
            '$environment$':         self.environment,
            '$codetype$':            self.codetype,
            '$branch$':              self.branch,
            '$path$':                self.path,
            '$makepath$':            self.makepath,
            '$port$':                str(self.port),
            '$nodeport$':            str(self.nodeport),
            '$k8snodeip1$':          self.k8snodeip1,
            '$k8snode1$':            self.k8snode1
        }
        for n, v in variable.items():
            content = content.replace(n, v)
        return content


    def makeOperation(self):
        rtime = time.strftime('%Y%m%d_%H%M%S')
        self.addlog('user: %s\noperation: %s\nproject: %s\ntaskid: %s\nbranch: %s\n' %(
                    self.currentuser, self.operation, self.project, self.taskid, self.branch) )
        self.addlog('Deploy System Compile Start Time: %s\n' % rtime)
        if self.git == 'null' or self.git == '':
            self.addlog('git addr : null')
        else:
            #根据operation的值对服务进行重启或者更新回退等操作。
            self.makeFun[self.operation]()
        rtime = time.strftime('%Y%m%d_%H%M%S')
        self.addlog('\nCompile Done Time: %s\n' % rtime)
        #更新数据库字段的值，记录更新信息
        self.updateProgress()

    def dockerBuild(self):
        if self.operation == 'serviceUpdate':
            if self.dockerfile:
                #定义dockerfile的地址  git仓库/项目名称作为dockerfile
                dockerfile_path = '%s/%s/%s/Dockerfile' %(self.dir_path_git, self.project, self.makepath)
                #执行writefile函数将self.dockerfile的值写到文件中。self.dockerfile值是从数据库获取
                self.writefile(dockerfile_path, self.dockerfile)
                #定义build镜像脚本路径
                start_path = '%s/%s/%s/start.sh' %(self.dir_path_git, self.project, self.makepath)
                #将新的项目名称写入start.sh脚本中
                self.writefile(start_path, self.start.replace('$project$', self.project))
                #镜像名格式 image.senses-ai.com/组名/项目名称/分支/commitid/时间戳
                self.dockertag = '%s_%s' %(self.commitid, self.tag)
                #self.dockertag = '%s_%s' %(self.commitid, time.strftime('%y%m%d%H%M%S'))
                #build镜像的命令
                shell_cmd = 'cd %s/%s/%s;docker build --build-arg branch=%s  --build-arg project=%s  -t %s:latest .' %(self.dir_path_git, self.project, self.makepath, self.branch, self.project, self.dockerurl)
                self.addlog(shell_cmd)
                #执行build镜像的命令
                self.exec_shell(shell_cmd)

                shell_cmd = 'docker tag %s:latest %s:%s' %(self.dockerurl, self.dockerurl, self.dockertag)
                self.exec_shell(shell_cmd)
                #push镜像
                shell_cmd = 'docker push  %s:latest' %(self.dockerurl)
                self.exec_shell(shell_cmd)
                shell_cmd = 'docker push  %s:%s' %(self.dockerurl, self.dockertag)
                self.exec_shell(shell_cmd)
        elif self.operation == 'serviceFallback':
            self.getdockerimage()
        #更新数据库
        self.updateProgress()


    def k8sOperation(self):

        if self.environment in ['online', 'poc']:
            self.offDeploy()
        else:
            if self.k8syaml:

                self.k8syaml = self.k8syaml.replace('$dockerurl$', self.dockerurl+':'+self.dockertag)
                self.writefile(self.k8syamlfilepath, self.k8syaml)
                self.addlog('\nYaml File: \n---\n%s\n---\n\n'  % self.k8syaml.replace(' ', '&#8194;'))

                shell_cmd = '''export KUBECONFIG=%s;kubectl get ns  %s --no-headers''' %(self.k8smanagefilepath, self.namespace )
                nsstatus = os.system(shell_cmd)
                self.addlog('\nNamespace status: %s\n' %nsstatus)
                if nsstatus != 0:
                    self.addlog('\nCreate Namespace: \n')
                    shell_cmd = '''export KUBECONFIG=%s;kubectl create ns %s''' %(self.k8smanagefilepath, self.namespace )
                    self.exec_shell(shell_cmd)

                self.get_configfilename()
                self.addlog('\nConfig Filename: %s\n' %(self.configfilename))
                self.addlog('\nK8s ConfigMap Create:\n')
                shell_cmd = 'export KUBECONFIG=%s;kubectl create configmap %s --from-file=%s=%s  --dry-run=client -o yaml | kubectl apply -n %s -f - ' %(self.k8smanagefilepath, self.p, self.configfilename, self.configfilepath, self.namespace)
                self.exec_shell(shell_cmd)

                self.addlog('\nK8s Cluster Deploy: %s' %  self.k8smanagename)
                shell_cmd = 'export KUBECONFIG=%s; \
                             kubectl apply -n %s -f %s; \
                             sleep 10; \
                             kubectl get pod -n %s -l app=%s  --no-headers; \
                            ' %(self.k8smanagefilepath, self.namespace, self.k8syamlfilepath, self.namespace, self.p)
                self.exec_shell(shell_cmd)

                self.addlog('\nINFO: check k8s pod status: %s' % self.p)
                self.check_pod_status()

                self.addlog('\nINFO: Pod Name: %s' % self.p)
                self.addlog('\nINFO: Pod Service Address: http://%s:%s' % (self.k8snodeip1, self.nodeport))
            self.addlog('\nINFO: Docker URL: %s:latest' %(self.dockerurl))
            self.addlog('\nINFO: Docker URL: %s:%s' %(self.dockerurl, self.dockertag))
            rtime = time.strftime('%Y%m%d_%H%M%S')
            self.addlog('\n\nINFO: Deploy Done Time: %s' % (rtime))
        self.updateProgress()


    def offDeploy(self):

        shell_cmd = 'mkdir -p %s/images %s/config %s/deployment %s/del' %(self.dir_path_off, self.dir_path_off, self.dir_path_off, self.dir_path_off)
        self.exec_shell(shell_cmd)
        
        if self.dockerfile:
            shell_cmd = 'docker save %s:%s | gzip > %s/images/%s.tar.gz' %(self.dockerurl, self.dockertag, self.dir_path_off, self.p)
            self.exec_shell(shell_cmd)
        
        if self.k8syaml:
        
            self.k8syaml = self.k8syaml.replace('$dockerurl$', self.dockerurl+':'+self.dockertag)
            offk8syaml = '%s/deployment/%s.yaml' %(self.dir_path_off, self.p)
            self.writefile(offk8syaml, self.k8syaml)
        
            self.get_configfilename()
            self.addlog('\nConfig Filename: %s\n' %(self.configfilename))
            shell_cmd = 'kubectl create configmap %s --from-file=%s=%s  --dry-run=client -o yaml > %s/config/%s.cfg.yaml' %(self.p, self.configfilename, self.configfilepath, self.dir_path_off, self.p)
            self.exec_shell(shell_cmd)
        self.addlog('\nINFO: off install dir: 192.168.10.66:%s' %(self.dir_path_off))



    def get_configfilename(self):
        try:
            for yamlfile in self.k8syaml.split('---'):
                yfile = yaml.full_load(yamlfile)
                if yfile['kind'] == 'Deployment':
                    containers = yfile['spec']['template']['spec']['containers']
                    break
            for container in containers:
                if container['name'] == self.p:
                    vms = container['volumeMounts']
                    break
            for vm in vms:
                if vm['name'] == self.p:
                    self.configfilename = vm['subPath']
                    break
        except:
            pass



    def addlog(self, newlog):
        self.logPath.write('\n%s' %newlog)
        self.logPath.flush()



    def updateTaskStatus(self):
        sql = "update `updateoperation` set `status`='%s',`tag`='%s',`commitid`='%s',`dockerimage`='%s:%s' \
                       where project='%s' and taskid='%s';  " % (
                       self.status, self.tag, self.commitid, self.dockerurl, self.dockertag, self.project, self.taskid)
        try:
            c.execute(sql)
        except Exception as err:
            print('ERROR: updateTaskStatus execute SQL fail')
            print(str(err))

    def updateProgress(self):
        self.progress = self.progress + 1
        #修改progress的值每执行一次就加一
        sql = "update `updateoperation` set `progress`=%d where project='%s' and taskid='%s';" % (self.progress, self.project, self.taskid)
        print(sql)
        try:
            c.execute(sql)
        except Exception as err:
            print('ERROR: updateProgress execute SQL fail')
            print(str(err))

    def notice(self):
        if self.environment != 'online':
            return ''

        content = ''
        headers = {'content-type': 'application/json'}

        if self.group in self.basicGlist:
            self.dingding(self.groupRobot, content)


    def getdockerimage(self):
        sql = "SELECT `dockerimage` FROM `updateoperation`  \
                      WHERE project = '%s' and tag = '%s' and operation = 'serviceUpdate' and status = 'ok' \
                      order by taskid desc limit 1;" % (self.project, self.tag)
        c.execute(sql)
        ones = c.fetchall()
        if ones:
            dockerimage = ones[0][0]
            self.dockertag = dockerimage.split(':')[1]
        else:
            self.faildone('tag %s dockerimage null' %(self.tag))

    #获取tag，和commitid
    #def getlastokstatus(self):
    #    sql = "SELECT `tag`,`commitid` FROM `updateoperation`  \
    #                  WHERE project = '%s' and operation = 'serviceUpdate' and status = 'ok' \
    #                  order by taskid desc limit 1;" % (self.project)
    #    c.execute(sql)
    #    ones = c.fetchall()
    #    if ones:
    #        tag      = ones[0][0]
    #        commitid = ones[0][1]
    #    else:
    #        tag = ''
    #        commitid = ''
    #    return {'tag': tag, 'commitid': commitid}


    def exec_shell(self, shell_cmd):
        print(shell_cmd)
        s = subprocess.Popen( shell_cmd, shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE  )
        newlog, stderr = s.communicate()
        return_status = s.returncode
        logs = '%s\n%s' % (newlog.strip(), stderr.strip())
        logs = logs.replace('\010','').replace('\b','')
        if return_status == 0:
            if logs.strip() != '':
                self.addlog(logs.strip())
            return {'status':'ok', 'log':newlog}
        else:
            self.faildone(logs)

    def ssh_shell(self, remoteCmd, sshport=22):
        shell_cmd = '''ssh -p %s -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "%s"
                    ''' %(sshport, self.execUser, self.host, remoteCmd)
        sshout = self.exec_shell(shell_cmd)
        return sshout

    def ssh_rsync(self, localPath, remotePath, sshport=22, excludes=''):
        excludelist = ''
        if excludes != '':
            for exclude in excludes.split(','):
                excludelist = ' %s --exclude=%s ' %(excludelist, exclude)
        self.addlog(excludelist)
        localPath  = localPath.rstrip('/')
        remotePath = remotePath.rstrip('/')
        shell_cmd = '''rsync -az %s --delete -e "ssh -p %s -o StrictHostKeyChecking=no -o ConnectTimeout=2" %s/ %s@%s:%s/  > /dev/null
                    ''' %(excludelist, sshport, localPath, self.execUser, self.host, remotePath)
        self.addlog(shell_cmd)
        self.exec_shell(shell_cmd)


    def writefile(self, path, content):
        f = open(path, 'w')
        f.write(str(content))
        f.flush()
        f.close()


    def dingding(self, Robot, content):
        headers = {'content-type': 'application/json'}
        data = {
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }
        try:
            r = requests.post(url=Robot, data=json.dumps(data), headers=headers, timeout=2).json()
        except Exception as err:
            print('ERROR: notice dingding api error. %s' %(str(err)))

    def done(self):
        #更新状态至数据库
        self.updateTaskStatus()
        #当前环境不登陆online返回''
        self.notice()
        try:
            #删除lock文件
            os.remove(self.pklFile)
        except:
            pass
        self.logPath.close()
        #判断状态如果为ok则退出返回0，否者为1
        if self.status == 'ok':
            sys.exit(0)
        else:
            sys.exit(1)
    #错误日志写入
    def faildone(self, log=''):
        self.addlog('ERROR: %s' %(log))
        self.status = 'fail'
        self.done()

    def notexec(self, port = None):
        pass

    def makeUpdate(self):
        self.addlog('\nCode Update:')
        self.code_update()
        #添加更新日志到日志文件
        self.addlog('\nConfig Update:')
        self.conf_update()
        self.addlog('\nCode Compile:')
        #开始进行编译会根据不同的语言调用不同的sh脚本
        self.make_operation()
        self.addlog('INFO:  commitid: %s' %(self.commitid))

    def makeFallback(self):
        pass

    #判断gitlab文件是否拉取到本地，如果存在删除
    def code_update(self):
        if self.git == 'null':
            self.addlog('git addr : null')
            return True
        newmake = ''
        if os.path.isdir('%s/%s' %(self.dir_path_git, self.project) ):
            #获取gitlab地址，
            shell_cmd = "cd %s/%s && git remote -v |grep fetch |awk '{print $2}'" %(self.dir_path_git, self.project)
            #self.addlog(shell_cmd)
            Result = self.exec_shell(shell_cmd)
            localGit = Result['log'].strip()
            #判断系统执行shell命令的git仓库是否等于数据库的git仓库，如果等于则pass。否则删除服务器上的gitlab仓库目录，之后重新clone一个新的gitlab仓库
            if localGit == self.git:
                pass
            else:
                shell_cmd = 'rm -rf %s/%s' %(self.dir_path_git, self.project)
                self.addlog(shell_cmd)
                self.exec_shell(shell_cmd)
                shell_cmd = 'git clone  %s %s/%s' %(self.git, self.dir_path_git, self.project)
                self.addlog(shell_cmd)
                self.exec_shell(shell_cmd)
        else:
            #clone新的代码仓库
            shell_cmd = 'git clone  %s %s/%s' %(self.git, self.dir_path_git, self.project)
            self.addlog(shell_cmd)
            self.exec_shell(shell_cmd)
            #将serviceUpdate给operation记录更新记录
            if self.operation == 'serviceUpdate':
                newmake = 'force'
            

        #  git submodule init && git submodule update
        #  --no-guess
        #获取gitlab分支代码仓库
        shell_cmd = ''' cd %s/%s && git reset --hard && git gc 2>/dev/null && git remote prune origin \
                              && git fetch && git checkout %s -- && git reset --hard origin/%s \
                              && git log -n 1 --stat
                    '''  %(self.dir_path_git, self.project, self.branch, self.branch)
        self.exec_shell(shell_cmd)

        shell_cmd = "cd %s/%s && git rev-parse HEAD" %(self.dir_path_git, self.project)
        Result = self.exec_shell(shell_cmd)
        self.commitid = Result['log'].strip()[0:8]
        if newmake == 'force':
            self.addlog('force')
            self.commitid = '%s-%s' % (self.commitid, newmake)


    def conf_update(self):
        pass


    def make_operation(self):
        make_start_time = time.strftime('%Y-%m-%d %H:%M:%S')
        #shell_cmd = '''/bin/bash -c "\nset -e;\ncd %s/%s/%s;\n. $HOME/.bashrc;export KUBECONFIG=%s;\n%s\n"\n''' %(
        #                 self.dir_path_git, self.project, self.makepath, self.k8smanagefilepath, self.make)
        #self.addlog(shell_cmd)
        #self.exec_shell(shell_cmd)

        shell_file = '''#!/bin/bash\nset -e;\ncd %s/%s/%s;\n. $HOME/.bashrc;\nexport KUBECONFIG=%s;\n%s\n\n''' %(
                         self.dir_path_git, self.project, self.makepath, self.k8smanagefilepath, self.make)
        makefilepath = '%s/%s/%s/deploy_make.sh' %(self.dir_path_git, self.project, self.makepath)
        self.writefile(makefilepath, shell_file)

        self.addlog(shell_file)
        self.exec_shell('bash %s' %makefilepath)

        make_done_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.addlog('make_start_time: %s' %(make_start_time))
        self.addlog('make_done_time: %s' %(make_done_time))


    def check_pod_status(self):
        i = 0
        results = 'ok'
        while i < 80:
            try:
                shell_cmd = 'export KUBECONFIG=%s; \
                         kubectl get pod -n %s -l app=%s  --no-headers|grep -v "Running"| grep -v "Terminating"| wc -l; \
                        ' %(self.k8smanagefilepath, self.namespace, self.p)
                R = self.exec_shell(shell_cmd)
                if R['status'] == 'ok':
                    line = int(R['log'].strip())
                    if line == 0:
                        shell_cmd = 'export KUBECONFIG=%s; \
                                 kubectl get pod -n %s -l app=%s  --no-headers|grep "Running" | wc -l; \
                                ' %(self.k8smanagefilepath, self.namespace, self.p)
                        R = self.exec_shell(shell_cmd)
                        if R['status'] == 'ok':
                            runline = int(R['log'].strip())
                            if runline > 0:
                                results = 'ok'
                                break
                    else:
                        shell_cmd = 'export KUBECONFIG=%s; \
                                 kubectl get pod -n %s -l app=%s  --no-headers|grep -v "Running"| grep -v "Terminating"; \
                                ' %(self.k8smanagefilepath, self.namespace, self.p)
                        self.exec_shell(shell_cmd)
                        if i > 6:
                            shell_cmd = 'export KUBECONFIG=%s; \
                                     kubectl get pod -n %s -l app=%s  --no-headers|grep -E "Error|BackOff"|wc -l; \
                                    ' %(self.k8smanagefilepath, self.namespace, self.p)
                            line1 = int(self.exec_shell(shell_cmd)['log'].strip())
                            if line1 != 0:
                                results = 'fail'
                                break
            except Exception as err:
                err = str(err)
            results = 'fail'
            i = i + 1
            time.sleep(3)
        if results == 'ok':
            self.addlog('\nINFO: check k8s pod Running: %s\n' %(self.p))
            shell_cmd = 'export KUBECONFIG=%s; \
                     kubectl get pod -n %s -l app=%s  --no-headers |grep -v Terminating; \
                    ' %(self.k8smanagefilepath, self.namespace, self.p)
            self.exec_shell(shell_cmd)
        else:
            self.faildone('check k8s pod Fail: %s' %(self.p))
            shell_cmd = '''export KUBECONFIG=%s; \
                            kubectl get pod -n %s -l app=%s  --no-headers|grep -v "Running"| grep -v "Terminating"| head -n 1|awk '{print $1}'; \
                        ''' %(self.k8smanagefilepath, self.namespace, self.p)
            podE = self.exec_shell(shell_cmd)['log'].strip()

            self.addlog('\nINFO: kubectl describe pod %s\n' %(podE))
            shell_cmd = '''export KUBECONFIG=%s; \
                            kubectl describe pod -n %s %s |tail -n 15; \
                        ''' %(self.k8smanagefilepath, self.namespace, podE)
            self.exec_shell(shell_cmd)
            self.addlog('\nINFO: kubectl logs %s\n' %(podE))
            shell_cmd = '''export KUBECONFIG=%s; \
                            kubectl logs -n %s %s |tail -n 20; \
                        ''' %(self.k8smanagefilepath, self.namespace, podE)
            self.exec_shell(shell_cmd)


    def autotest(self, port = None):
        if port is None:
            port = self.port
        if self.environment != 'online':
            self.addlog('INFO: not auto test\n')
            return 'not auto test'
        if self.operation == 'serviceFallback':
            self.addlog('INFO: serviceFallback not auto test\n')
            return 'INFO: serviceFallback not auto test'
        if self.project in self.autolist:
            data = {'biz':self.project, 'host': self.host, 'port': self.port, 'way':1}
            try:
                r = requests.post(self.autotestURL, data=json.dumps(data)).json()
                self.addlog(r['data'])
                if r['data'] == 'pass':
                    self.addlog('INFO: auto test OK\n')
                    return 'ok'
                else:
                    self.faildone('auto test Fail.\nError details: %s' %(r['url_list']) )
            except Exception as err:
                self.faildone('auto test Fail. QA api Fail \n%s' % str(err))




if __name__ == "__main__":

    project = sys.argv[1]
    tag = sys.argv[2]
    taskid = sys.argv[3]
    operation = sys.argv[4]
    currentuser = sys.argv[5]
    reason = sys.argv[6]


    dp=Deploy(project, tag, taskid, operation, currentuser, reason)
    #拉取gitlab代码仓库，更新，回滚操作

    try:
        dp.makeOperation()
        dp.dockerBuild()
      
        dp.k8sOperation()
        dp.done()
    except Exception as err:
        dp.faildone(str(err))




