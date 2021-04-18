#!/usr/bin/env python
# coding: utf-8

import logging
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
from flask import render_template, request,  session, url_for, redirect, flash
from flask_login import login_required, current_user
from . import main
from ..models import * 
from ..config import *
from .forms import *

reload(sys);
sys.setdefaultencoding('utf8');

os.system('mkdir -p %s' %path_log)
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='%s/cedardeploy.log' %path_log,
                filemode='a')

@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('online.html')


@main.route("/online", methods=["GET", "POST"])
@login_required
def online():
        return render_template("online.html")


@main.route("/project_admin", methods=["GET", "POST"])
@login_required
def project_admin():
        return render_template("project_admin.html")

@main.route("/project_add", methods=["GET", "POST"])
@login_required
def project_add():
        return render_template("project_add.html")

@main.route("/online_log", methods=["GET", "POST"])
@login_required
def online_log():
        return render_template("online_log.html")


@main.route("/statistics", methods=["GET", "POST"])
@login_required
def statistics():
        return render_template("statistics.html")

@main.route("/workorderweb", methods=["GET", "POST"])
@login_required
def workorderweb():
        return render_template("workorder.html")

@main.route("/hostlisterrweb", methods=["GET", "POST"])
@login_required
def hostlisterrweb():
        return render_template("hostlisterrweb.html")

@main.route("/hostmanage", methods=["GET", "POST"])
@login_required
def hostmanage():
        return render_template("hostmanage.html")

@main.route("/assets", methods=["GET", "POST"])
@login_required
def assets():
        return render_template("assets.html")

@main.route("/useradmin", methods=["GET", "POST"])
@login_required
def useradmin():
        return render_template("useradmin.html")


@main.route("/portadmin", methods=["GET", "POST"])
@login_required
def portadmin():
        return render_template("portadmin.html")


@main.route("/del_project", methods=["POST","GET"])
@login_required
def del_project():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project = request.form.get('project', 'null')
        if project == 'null':
            raise Exception('ERROR: project null')
        DIR = getdir(project)
        ones = serverinfo.query.filter(serverinfo.project == project).all()
        if len(ones) != 0:
            raise Exception('ERROR: Please delete the host.')

        ones = projectinfo.query.filter(projectinfo.project == project).first()
        k8smanagefilepath = '%s/%s-%s.k8s' %(path_conf, ones.environment, ones.k8smanagename)
        shell_cmd = 'export KUBECONFIG=%s ;kubectl delete deployments.apps -n %s %s;kubectl delete svc -n %s %s;kubectl delete configmap -n %s %s' %(k8smanagefilepath, ones.namespace, ones.p, ones.namespace, ones.p, ones.namespace, ones.p)
        Result = shellcmd(shell_cmd)
        R['log'] = Result['log']

        serverinfo.query.filter(serverinfo.project == project).delete()
        projectinfo.query.filter(projectinfo.project == project).delete()
        os.popen('mv %s %s.%s.del' %(DIR['git'], DIR['git'], time.strftime('%Y%m%d_%H%M'))).read()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/rmpod", methods=["GET","POST"])
@login_required
def rmpod():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project = request.form.get('project', 'null')
        if project == 'null':
            raise Exception('ERROR: project null')
        ones = serverinfo.query.filter(serverinfo.project == project).all()
        if len(ones) != 0:
            raise Exception('ERROR: Please delete the host.')
        ones = projectinfo.query.filter(projectinfo.project == project).first()
        k8smanagefilepath = '%s/%s-%s.k8s' %(path_conf, ones.environment, ones.k8smanagename)
        shell_cmd = 'export KUBECONFIG=%s ;kubectl delete svc -n %s %s;kubectl delete cm -n %s %s;kubectl delete deployments.apps -n %s %s' %(k8smanagefilepath,  ones.namespace, ones.p, ones.namespace, ones.p, ones.namespace, ones.p)
        Result = shellcmd(shell_cmd)
        R['log'] = Result['log']
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/project", methods=["GET", "POST"])
@login_required
def project():

    user = request.args.get("user", "null")
    if user == "null":
        user = current_user.username
    group = request.args.get("group", "null")
    functype = request.args.get("functype", "null")

    try:
        ones = projectinfo.query.filter(projectinfo.group == group).order_by(projectinfo.project.desc()).all()
    except:
        return json.dumps({'project sql error':['error']})
    project = {}
    try:
        ones1 = userservicegroup.query.filter(userservicegroup.username == user, userservicegroup.servicegroup == group ).all()
        permissions = ones1[-1].permissions
    except:
        permissions = 'null'

    for x in ones:
        #if user not in adminuser and x.environment == 'online':
        #    if functype == 'online':
        #        if permissions != 'online':
        #            continue
        if x.environment in project:
            project[x.environment].append(x.project)
        else:
            project[x.environment] = [x.project]

    return json.dumps(project)



@main.route("/pagelist", methods=["GET", "POST"])
@login_required
def pagelist():
    user = current_user.username
    if user in adminuser:
        pagelist = adminpagelist
    else:
        pagelist = userpagelist
    return json.dumps(pagelist)



@main.route("/rmpkl", methods=["GET", "POST"])
@login_required
def rmpkl():
    project = request.args.get("project","null")
    DIR = getdir(project)
    pklFile = '%s/deploy.%s.lock' %(DIR['lock'], project)
    try:
        os.remove(pklFile)
    except:
        pass
    return json.dumps(['ok'])


@main.route("/killtask", methods=["GET", "POST"])
@login_required
def killtask():
    R = {'status':'ok', 'log':'', 'data':''}
    project = request.args.get("project","null")
    if project == "null":
       return json.dumps(['project null'])
    DIR = getdir(project)
    shell_cmd = '''ps -eaf |grep '/home/bae/deploywork/git/%s/%s'|grep -v grep |awk '{print $2}' |xargs -i -t kill -9 {} ''' % (project, project)
    Result = shellcmd(shell_cmd)
    shell_cmd = '''ps -eaf |grep deploy-k8s.py|grep -v grep |grep %s |awk '{print $2}' |xargs -i -t kill -9 {} ''' % (project)
    Result = shellcmd(shell_cmd)
    R['log'] = Result['log']
    R['status'] = Result['status']
    pklFile = '%s/deploy.%s.lock' %(DIR['lock'], project)
    try:
        os.remove(pklFile)
    except:
        pass
    return json.dumps(R)


@main.route("/clean_git_cache", methods=["GET", "POST"])
@login_required
def clean_git_cache():
    project = request.args.get("project","null")
    if project == "null":
        return json.dumps(['project null'])
    DIR = getdir(project)
    project_git_path = '%s/%s' %(DIR['git'], project)
    status = os.popen('mv -i  %s  %s.%s.clean' %(project_git_path, project_git_path,
                                                 time.strftime('%Y%m%d_%H%M'))   ).read()
    logging.info(status)

    return json.dumps([status])

@main.route("/add_group", methods=["GET", "POST"])
@login_required
def add_group():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        addgroupname = request.form.get("addgroupname","null").strip().split(' ')[0]
        if addgroupname == '' or addgroupname == 'null':
            raise Exception('ERROR: add groupname null')
        u = servicegroup(servicegroup=addgroupname)
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/add_environment", methods=["GET", "POST"])
@login_required
def add_environment():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        addenvironmentname = request.form.get("addenvironmentname","null").strip().split(' ')[0]
        if addenvironmentname == '' or addenvironmentname == 'null':
            raise Exception('ERROR: add environmentname null')
        u = serviceenvironment(serviceenvironment=addenvironmentname)
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/add_codetype", methods=["GET", "POST"])
@login_required
def add_codetype():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        addcodetypename = request.form.get("addcodetypename","null").strip().split(' ')[0]
        if addcodetypename == '' or addcodetypename == 'null':
            raise Exception('ERROR: add codetypename null')
        u = servicecodetype(servicecodetype=addcodetypename)
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/add_k8scluster", methods=["GET", "POST"])
@login_required
def add_k8scluster():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        environment = request.form.get("k8smanageenvironment","null").strip()
        k8smanagename = request.form.get("k8smanagename","null").strip().split(' ')[0]
        k8smanagefilecontent = request.form.get("k8smanagefilecontent","null").strip()

        if k8smanagename == '' or k8smanagefilecontent == '':
            raise Exception('ERROR: add k8s manage file null')
        ones = k8scluster.query.filter(k8scluster.environment == environment, k8scluster.k8smanagename == k8smanagename ).all()
        if ones:
            raise Exception('ERROR: add k8scluster existence')

        k8smanagefilepath = '%s/%s-%s.k8s' %(path_conf, environment, k8smanagename)
        writefile(k8smanagefilepath, k8smanagefilecontent)

        shell_cmd = 'export KUBECONFIG=%s ;kubectl get node' %(k8smanagefilepath)
        Result = shellcmd(shell_cmd)
        R['log'] = Result['log']
        if Result['status'] != 'ok':
            raise Exception(R['log'])

        shell_cmd = '''export KUBECONFIG=%s ;kubectl get node -o wide  --no-headers |grep master |grep -v NotReady|grep Ready |awk '{print $6}' |head -n 1''' %(k8smanagefilepath)

        k8snodeip1 = shellcmd(shell_cmd)['log'].strip()

        shell_cmd = '''export KUBECONFIG=%s ;kubectl get node -o wide  --no-headers |grep master |grep -v NotReady|grep Ready |awk '{print $1}' |head -n 1''' %(k8smanagefilepath)
        k8snode1 = shellcmd(shell_cmd)['log'].strip()

        u = k8scluster(environment=environment, k8smanagename=k8smanagename, k8smanagefilecontent=k8smanagefilecontent, k8snodeip1=k8snodeip1, k8snode1=k8snode1)
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/add_templatefile", methods=["GET", "POST"])
@login_required
def add_templatefile():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        codetype = request.form.get("codetypemanage","null").strip()
        templatefilename = request.form.get("codetypemanagefilename","null").strip().split(' ')[0]
        templatefilecontent = request.form.get("codetypemanagefilecontent","null").strip()

        if codetype == '' or templatefilename == '':
            raise Exception('ERROR: add templatefile null')
        ones = templatefile.query.filter(templatefile.codetype == codetype, templatefile.templatefilename == templatefilename ).all()
        if ones:
            raise Exception('ERROR: add templatefile existence')
        u = templatefile(codetype=codetype, templatefilename=templatefilename, templatefilecontent=templatefilecontent)
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/get_projectk8sclustername", methods=["GET", "POST"])
@login_required
def get_projectk8sclustername():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project = request.args.get("project", "null")
        if project == "null":
            return json.dumps(['project null'])
        ones = projectinfo.query.filter(projectinfo.project == project).first()
        ones1 = k8scluster.query.filter(k8scluster.environment == ones.environment ).all()
        R['data'] = []
        for i in ones1:
            R['data'].append(i.k8smanagename)
        R['data'] = sorted(list(set(R['data'])))
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/update_templatefile", methods=["GET", "POST"])
@login_required
def update_templatefile():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        user = current_user.username
        if user not in adminuser:
            raise Exception('ERROR: user no permission')
        codetype = request.form.get("codetype","null").strip()
        templatefilename = request.form.get("templatefilename","null").strip().split(' ')[0]
        templatefilecontent = request.form.get("templatefilecontent","null").strip()

        templatefile.query.filter(  templatefile.codetype == codetype,
                                    templatefile.templatefilename == templatefilename
                                 ).update({
                                    "templatefilecontent" : templatefilecontent
                                 })
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/del_templatefile", methods=["GET", "POST"])
@login_required
def del_templatefile():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        user = current_user.username
        if user not in adminuser:
            raise Exception('ERROR: user no permission')
        codetype = request.form.get("codetype","null").strip()
        templatefilename = request.form.get("templatefilename","null").strip().split(' ')[0]
        templatefilecontent = request.form.get("templatefilecontent","null").strip()

        templatefile.query.filter(  templatefile.codetype == codetype,
                                    templatefile.templatefilename == templatefilename
                                 ).delete()
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/update_k8scluster", methods=["GET", "POST"])
@login_required
def update_k8scluster():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        user = current_user.username
        if user not in adminuser:
            raise Exception('ERROR: user no permission')
        environment = request.form.get("environment","null").strip()
        k8smanagename = request.form.get("k8smanagename","null").strip().split(' ')[0]
        k8smanagefilecontent = request.form.get("k8smanagefilecontent","null").strip()

        k8smanagefilepath = '%s/%s-%s.k8s' %(path_conf, environment, k8smanagename)
        writefile(k8smanagefilepath, k8smanagefilecontent)

        shell_cmd = 'export KUBECONFIG=%s ;kubectl get node' %(k8smanagefilepath)
        Result = shellcmd(shell_cmd)
        R['log'] = Result['log']
        if Result['status'] != 'ok':
            raise Exception(R['log'])

        shell_cmd = '''export KUBECONFIG=%s ;kubectl get node -o wide  --no-headers |grep master |grep -v NotReady|grep Ready |awk '{print $6}' |head -n 1''' %(k8smanagefilepath)
        k8snodeip1 = shellcmd(shell_cmd)['log'].strip()
        shell_cmd = '''export KUBECONFIG=%s ;kubectl get node -o wide  --no-headers |grep master |grep -v NotReady|grep Ready |awk '{print $1}' |head -n 1''' %(k8smanagefilepath)
        k8snode1 = shellcmd(shell_cmd)['log'].strip()

        k8scluster.query.filter(  k8scluster.environment == environment,
                                  k8scluster.k8smanagename == k8smanagename
                               ).update({
                                  "k8smanagefilecontent" : k8smanagefilecontent,
                                  "k8snodeip1"           : k8snodeip1,
                                  "k8snode1"             : k8snode1
                               })
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/del_k8scluster", methods=["GET", "POST"])
@login_required
def del_k8scluster():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        user = current_user.username
        if user not in adminuser:
            raise Exception('ERROR: user no permission')
        environment = request.form.get("environment","null").strip()
        k8smanagename = request.form.get("k8smanagename","null").strip().split(' ')[0]
        k8smanagefilecontent = request.form.get("k8smanagefilecontent","null").strip()

        k8scluster.query.filter(  k8scluster.environment == environment,
                                  k8scluster.k8smanagename == k8smanagename
                               ).delete()
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/del_group", methods=["POST"])
@login_required
def del_group():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        group = request.form.get('selectgroup', 'null')
        if group == 'null':
            raise Exception('ERROR: servicegroup null')
        ones = projectinfo.query.filter(projectinfo.group == group ).all()
        if ones != []:
            raise Exception('ERROR: Non empty group, Please delete the project in the group')
        servicegroup.query.filter(servicegroup.servicegroup == group).delete()
        userservicegroup.query.filter(userservicegroup.servicegroup == group).delete()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/del_environment", methods=["POST"])
@login_required
def del_environment():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        environment = request.form.get('selectenvironment', 'null')
        if environment == 'null':
            raise Exception('ERROR: serviceenvironment null')
        ones = projectinfo.query.filter(projectinfo.environment == environment ).all()
        if ones != []:
            raise Exception('ERROR: Non empty environment, Please delete the project in the environment')
        serviceenvironment.query.filter(serviceenvironment.serviceenvironment == environment).delete()

    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/del_codetype", methods=["POST"])
@login_required
def del_codetype():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        codetype = request.form.get('selectcodetype', 'null')
        if codetype == 'null':
            raise Exception('ERROR: servicecodetype null')
        ones = projectinfo.query.filter(projectinfo.codetype == codetype ).all()
        if ones != []:
            raise Exception('ERROR: Non empty codetype, Please delete the project in the codetype')
        servicecodetype.query.filter(servicecodetype.servicecodetype == codetype).delete()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/adduserservicegroup", methods=["GET", "POST"])
@login_required
def adduserservicegroup():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        username = request.form.get("username","null").strip().split(' ')[0]
        servicegroup = request.form.get("servicegroup","null").strip().split(' ')[0]
        permissions = request.form.get("permissions","null").strip().split(' ')[0]
        user = current_user.username
        if user not in adminuser or username == '' or username == 'null' or servicegroup == '' or servicegroup == 'null':
            raise Exception('ERROR: The current user has no rights')
        u = userservicegroup(username=username, servicegroup=servicegroup, permissions=permissions)
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/deleteuserservicegroup", methods=["POST"])
@login_required
def deleteuserservicegroup():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        user = request.form.get('user', 'null')
        servicegroup = request.form.get('servicegroup', 'null')
        if user == "null" or servicegroup == 'null':
            raise Exception('ERROR: user or servicegroup null')
        userservicegroup.query.filter(userservicegroup.username == user, userservicegroup.servicegroup == servicegroup).delete()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/group_list", methods=["GET", "POST"])
@login_required
def group_list():
    user = request.args.get("user", "null")
    if user == "null":
        user = current_user.username

    try:
        if user in adminuser:
            ones = userservicegroup.query.all()
        else:
            ones = userservicegroup.query.filter(userservicegroup.username == user ).all()
    except:
        return json.dumps(['sql error'])
    grouplist = []
    for i in ones:
        if i.servicegroup != 'null':
            grouplist.append(i.servicegroup)
    grouplist = sorted(list(set(grouplist)))
    return json.dumps(grouplist)

@main.route("/group_list_all", methods=["GET", "POST"])
@login_required
#ops.js调用次函数
def group_list_all():
    #判断当前用户
    user = current_user.username
    #如果该用户存在adminuser列表将执行以下语句
    if user in adminuser:
        try:
            #取回数据servicegroup表中所有的数据
            ones = servicegroup.query.all()
        except:
            return json.dumps(['sql error or no authority'])
    #定一个一个空的组列表，进行for循环将表组信息追加到grouplist列表中
    grouplist = []
    for i in ones:
        if i.servicegroup != 'null':
            grouplist.append(i.servicegroup)
    #将grouplist进行去重并排序重新赋值
    grouplist = sorted(list(set(grouplist)))
    #将列表数据以json的方式返回
    return json.dumps(grouplist)

@main.route("/environment_list_all", methods=["GET", "POST"])
@login_required
def environment_list_all():
    user = current_user.username
    try:
        ones = serviceenvironment.query.all()
    except:
        return json.dumps(['sql error'])

    environmentlist = []
    for i in ones:
        if i.serviceenvironment != 'null':
            environmentlist.append(i.serviceenvironment)
    environmentlist = sorted(list(set(environmentlist)))
    return json.dumps(environmentlist)

@main.route("/codetype_list_all", methods=["GET", "POST"])
@login_required
def codetype_list_all():
    user = current_user.username
    try:
        ones = servicecodetype.query.all()
    except:
        return json.dumps(['sql error'])

    codetypelist = []
    for i in ones:
        if i.servicecodetype != 'null':
            codetypelist.append(i.servicecodetype)
    codetypelist = sorted(list(set(codetypelist)))
    return json.dumps(codetypelist)

@main.route("/get_templatefile_all", methods=["GET", "POST"])
@login_required
def get_templatefile_all():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        user = current_user.username
        if user not in adminuser:
            raise Exception('ERROR: user no permission')
        ones = templatefile.query.all()
        R['data'] = []
        for template in ones:
            D = {
                'codetype':template.codetype, 
                'templatefilename':template.templatefilename, 
                'templatefilecontent':template.templatefilecontent
            }
            R['data'].append(D)
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/get_k8scluster_all", methods=["GET", "POST"])
@login_required
def get_k8scluster_all():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        user = current_user.username
        if user not in adminuser:
            raise Exception('ERROR: user no permission')
        ones = k8scluster.query.all()
        R['data'] = []
        for k8s in ones:
            D = {
                'environment':k8s.environment, 
                'k8smanagename':k8s.k8smanagename, 
                'k8smanagefilecontent':k8s.k8smanagefilecontent
            }
            R['data'].append(D)
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/get_k8sclustername", methods=["GET", "POST"])
@login_required
def get_k8sclustername():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        environment = request.args.get("environment", "null")
        ones = k8scluster.query.filter(k8scluster.environment == environment ).all()
        R['data'] = []
        for i in ones:
            R['data'].append(i.k8smanagename)
        R['data'] = sorted(list(set(R['data'])))
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)

@main.route("/group_list_user", methods=["GET", "POST"])
def group_list_user():
    user = request.args.get("user")
    try:
        if user in adminuser:
            ones = userservicegroup.query.all()
        else:
            ones = userservicegroup.query.filter(userservicegroup.username == user ).all()
    except:
        return json.dumps(['sql error'])
    grouplist = []
    for i in ones:
        if i.servicegroup != 'null':
            grouplist.append(i.servicegroup)
    grouplist = list(set(grouplist))
    return json.dumps(grouplist)


@main.route("/userservicegrouplist", methods=["GET", "POST"])
@login_required
def userservicegrouplist():
    user = request.args.get("user")
    try:
        ones = userservicegroup.query.filter(userservicegroup.username == user ).all()
    except:
        return json.dumps([['sql','error']])
    grouplist = []
    for i in ones:
        grouplist.append([i.servicegroup, i.permissions])
    return json.dumps(grouplist)



@main.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        adduser = request.form.get('adduser', 'null').strip().split(' ')[0]
        password = request.form.get('password', 'null').strip().split(' ')[0]
        user = current_user.username
        if adduser == 'null' or adduser == '' or password == 'null' or password == '':
            raise Exception('ERROR: user or password null')
        if user not in adminuser:
            raise Exception('ERROR: The current user has no rights')
        u = User(email='%s@cedar.cn' %adduser, username='%s' %adduser, password=password)
        User.query.filter(User.username == adduser).delete()
        db.session.add(u)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/delete_user", methods=["GET", "POST"])
@login_required
def delete_user():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        deleteuser = request.form.get("deleteuser","null").strip().split(' ')[0]
        user = current_user.username
        if user not in adminuser:
            raise Exception('ERROR: The current user has no rights')
        User.query.filter(User.username == deleteuser).delete()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/user_list", methods=["GET", "POST"])
@login_required
def user_list():
    try:
        user = current_user.username
        if user in adminuser:
            userlist = []
            ones = User.query.all()
            for i in ones:
                userlist.append(i.username)
        else:
            return json.dumps(['ERROR: The current user has no rights'])

        return json.dumps(userlist)
    except:
        return json.dumps(['sql error'])



@main.route("/hostlist", methods=["GET", "POST"])
def hostlist():
    R = {'status':'ok', 'log':'', 'data':[] }
    project = request.args.get('project','null')
    try:
        if project == 'null':
            raise Exception('ERROR: project null')
        ones = projectinfo.query.filter(projectinfo.project == project ).all()
        codetype = ones[0].codetype
        group = ones[0].group
        env = ones[0].environment

        ones1 = serverinfo.query.filter(serverinfo.project == project ).order_by(serverinfo.hostname).all()

        R['data'] = []
        for i in ones1:
            hostline = {}
            hostline['ip']           = i.ip
            hostline['hostname']     = i.hostname
            hostline['project']      = i.project
            hostline['codetype']     = codetype
            hostline['pnum']         = i.pnum
            hostline['env']          = i.env
            hostline['checkstatus']  = i.checkstatus
            hostline['checktime']    = i.checktime
            hostline['commitid']     = i.commitid
            hostline['updatestatus'] = i.updatestatus
            hostline['updatetime']   = i.updatetime
            hostline['hosttype']     = i.hosttype
            hostline['checkconsulstatus']   = i.checkconsulstatus
            hostline['checkconsultime']     = i.checkconsultime
    
            R['data'].append(hostline)
    except Exception as err:
        R['status'] = 'fail'
        R['log']    = str(err)
    return json.dumps(R)

#@main.route("/hostlist", methods=["GET", "POST"])
#def hostlist():
#    project = request.args.get("project","null")
#    if project == "null":
#        return json.dumps([['project null','error','null','null']])
#    try:
#        ones = projectinfo.query.filter(projectinfo.project == project ).all()
#        codetype = ones[0].codetype
#        group = ones[0].group
#        env = ones[0].environment
#
#        ones1 = serverinfo.query.filter(serverinfo.project == project ).order_by(serverinfo.hostname).all()
#    except:
#        return json.dumps([['sql','error','null','null']])
#    rl = []
#    for i in ones1:
#        rl.append([i.ip, i.hostname, i.project, codetype, i.pnum, i.env, i.checkstatus, i.checktime, i.commitid, i.updatestatus, i.updatetime, i.hosttype ]) 
#    return json.dumps(rl)


@main.route("/hostlistall", methods=["GET", "POST"])
def hostlistall():
    try:
        ones = serverinfo.query.all()
        rl = []
        for i in ones:
            rl.append([i.ip, i.hostname, i.project])
        return json.dumps(rl)
    except:
        return json.dumps([['sql','error','null','null']])

@main.route("/iplistall", methods=["GET", "POST"])
def iplistall():
    try:
        ones = serverinfo.query.all()
        ipl = []
        for i in ones:
            ipl.append(i.ip)

        return json.dumps(list(set(ipl)))
    except:
        return json.dumps(['sqlerror'])


@main.route("/envproject", methods=["GET", "POST"])
def envproject():
    try:
        ones  = projectinfo.query.filter(projectinfo.group == 'app', projectinfo.environment == 'online' ).all()
        pl = {}
        for p in ones:
            pl[p.project] = {'port':p.port, 'group':p.group, 'codetype':p.codetype, 'environment':p.environment, 'host':{}}
            ones1 = serverinfo.query.filter(serverinfo.project == p.project).all()
            for host in ones1:
                pl[p.project]['host'][host.ip] = {'hosttype':host.hosttype,'pnum':host.pnum,'hostname':host.hostname}
        return json.dumps(pl)
    except Exception as err:
        return json.dumps({'status':'fail', 'log':str(err)})


@main.route("/hostlisterr", methods=["GET", "POST"])
def hostlisterr():
    try:
        ones = serverinfo.query.filter(  serverinfo.checkstatus != 'RUNNING', 
                                         serverinfo.checkstatus != 'Up',
                                         serverinfo.checkstatus != 'SSHOK',
                                         serverinfo.checkstatus != 'null'
                                      ).order_by(serverinfo.project).all()
    except:
        return json.dumps([['sql','error','null','null']])
    rl = []
    Type = 'null'

    for i in ones:
        rl.append([i.ip, i.hostname, i.project, Type, i.pnum, i.checkstatus, i.checktime, 
                   i.commitid, i.updatestatus, i.updatetime])
    return json.dumps(rl)

@main.route("/port_list", methods=["GET", "POST"])
@login_required
def port_list():
    try:
        ones = projectinfo.query.order_by(projectinfo.port).all()
    except Exception as err:
        return json.dumps([['sql','error','null','null']])
    portlist = []
    for i in ones:
        portlist.append([ i.port, i.project ])
    return json.dumps(portlist)

@main.route("/project_list", methods=["GET", "POST"])
@login_required
def project_list():
    try:
        ones = projectinfo.query.order_by(projectinfo.group).all()
    except Exception as err:
        return json.dumps([['sql','error','null','null']])
    projectlist = []
    for i in ones:
        projectlist.append([i.group, i.project, i.port  ])
    return json.dumps(projectlist)

@main.route("/project_info", methods=["GET", "POST"])
@login_required
def project_info():
    project = request.args.get("project", "null")
    if project == "null":
        return json.dumps(['project null'])
    try:
        ones = projectinfo.query.filter(projectinfo.project == project).first()
    except:
        return json.dumps(['sql err'])
    rl = [ ones.project, ones.group, ones.environment,  ones.p, ones.codetype, ones.port, ones.git, ones.branch, ones.config, ones.make, ones.dockerfile, ones.k8syaml, ones.remarks, ones.makepath, ones.k8smanagename, ones.nodeport]
    return json.dumps(rl)
        

@main.route("/project_info_json", methods=["GET", "POST"])
@login_required
def project_info_json():
    R = {'status':'ok', 'log':'', 'data':{}}
    project = request.args.get("project", "null")
    if project == "null":
        return json.dumps(['project null'])
    try:
        ones = projectinfo.query.filter(projectinfo.project == project).first()
        R['data']['project']          = ones.project
        R['data']['group']            = ones.group
        R['data']['environment']      = ones.environment
        R['data']['p']                = ones.p
        R['data']['codetype']         = ones.codetype
        R['data']['port']             = ones.port
        R['data']['git']              = ones.git
        R['data']['branch']           = ones.branch
        R['data']['config']           = ones.config
        R['data']['make']             = ones.make
        R['data']['start']            = ones.start
        R['data']['remarks']          = ones.remarks
        R['data']['dockerfile']       = ones.dockerfile
        R['data']['k8syaml']          = ones.k8syaml
        R['data']['makepath']         = ones.makepath
        R['data']['k8smanagename']    = ones.k8smanagename
        R['data']['nodeport']         = ones.nodeport
        R['data']['namespace']        = ones.namespace
    except Exception as err:
        R['status'] = 'fail'
        R['log']    = str(err)
    return json.dumps(R)


@main.route("/projectinfoall", methods=["GET", "POST"])
def projectinfoall():
    try:
        ones = projectinfo.query.all()
    except:
        return json.dumps( {'environment_project null':['git', 'branch', 'type', 'port', 'group']})
    rl = {}
    for i in ones:
        rl['%s_%s' %(i.environment, i.project)] = [i.git, i.branch, i.codetype, i.port, i.group]
    return json.dumps(rl)



@main.route("/add_project", methods=["POST"])
@login_required
def add_project():
    R = {'status':'ok', 'log':'', 'data':''}

    try:
        group           = request.form.get('group',           'null').strip()
        environment     = request.form.get('environment',     'null').strip()
        p               = request.form.get('p',               'null').strip().lower().replace('_','-').replace(' ','')
        codetype        = request.form.get('codetype',        'null').strip()
        port            = str(request.form.get('port',        '0')).strip()
        git             = request.form.get('git',             'null').strip()
        branch          = request.form.get('branch',          'null').strip()
        config          = request.form.get('config',          'null').strip()
        remarks         = request.form.get('remarks',         'null').strip()
        makepath        = request.form.get('makepath',        './').strip().lstrip('/')
        k8smanagename   = request.form.get('k8sclustername',  'null').strip()
        namespace       = request.form.get('namespace',       'default').strip().lower()
        if not port:
            port = '0'
        if not port.isdigit():
            raise Exception('ERROR: port Not a Number %s %s' %(port, type(port) ) )
    
        if p == "null" or environment == "null" or branch == "null" or codetype == "null" or git == "null":
            raise Exception('ERROR: parameter error')
    
        project = environment + '_' + p
        ones = projectinfo.query.filter(projectinfo.project == project ).first()
        if ones != None:
            raise Exception('ERROR: project already exists')

        make = ''
        start = ''
        dockerfile = ''
        k8syaml = ''
        ones1 = templatefile.query.filter(templatefile.codetype == codetype).all()
        for template in ones1:
            if template.templatefilename == 'make':
                make = template.templatefilecontent
            elif template.templatefilename == 'start':
                start = template.templatefilecontent
            elif template.templatefilename == 'Dockerfile':
                dockerfile = template.templatefilecontent
            elif template.templatefilename == 'podyaml':
                k8syaml = template.templatefilecontent

        try:
            nodeport = db.session.query(projectinfo).order_by(projectinfo.nodeport.desc()).limit(1)[0].nodeport + 1
        except:
            nodeport = '30000'

        newproject = projectinfo(  project        = project, 
                                   group          = group, 
                                   environment    = environment, 
                                   p              = p, 
                                   codetype       = codetype, 
                                   port           = port, 
                                   git            = git, 
                                   branch         = branch,
                                   config         = config,
                                   make           = make,
                                   start          = start,
                                   remarks        = remarks,
                                   dockerfile     = dockerfile,
                                   k8syaml        = k8syaml,
                                   makepath       = makepath,
                                   k8smanagename  = k8smanagename,
                                   nodeport       = nodeport,
                                   namespace      = namespace
                                )
        db.session.add(newproject)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/clone_project", methods=["POST"])
@login_required
def clone_project():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        projectold  = request.form.get('project',     'null').strip()
        environment = request.form.get('environment', 'null').strip()
        p           = request.form.get('p',           'null').strip().lower().replace('_','-').replace(' ','')

        if projectold == 'null' or environment == 'null' or p == 'null':
            raise Exception('ERROR: clone project parameter null')
        project = environment + '_' + p
        if projectold == project:
            raise Exception('ERROR: clone project name error')
        currentuser = current_user.username
        logging.warning('INFO: clone_project: %s, source: %s, cloneName: %s_%s' %(
                currentuser, projectold, environment, p) )
        ones = projectinfo.query.filter(projectinfo.project == projectold ).first()
        if ones == None:
            raise Exception('ERROR: source project null')
        ones1 = projectinfo.query.filter(projectinfo.project == project ).first()
        if ones1 != None:
            raise Exception('ERROR: new project exists %s' %(ones.group))

        pold = projectold.split('_')[1]
        if pold == p:
            nodeport = ones.nodeport
        else:
            nodeport = db.session.query(projectinfo).order_by(projectinfo.nodeport.desc()).limit(1)[0].nodeport + 1

        newproject = projectinfo(  project        = project,
                                   group          = ones.group,
                                   environment    = environment,
                                   p              = p,
                                   codetype       = ones.codetype,
                                   port           = ones.port,
                                   git            = ones.git,
                                   branch         = ones.branch,
                                   config         = ones.config,
                                   make           = ones.make,
                                   start          = ones.start,
                                   remarks        = ones.remarks,
                                   dockerfile     = ones.dockerfile,
                                   k8syaml        = ones.k8syaml,
                                   makepath       = ones.makepath,
                                   k8smanagename  = ones.k8smanagename,
                                   nodeport       = nodeport,
                                   namespace      = ones.namespace
                                )
        db.session.add(newproject)
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/add_host", methods=["POST"])
@login_required
def add_host():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project      = request.form.get('project',      "null").strip()
        hostname     = request.form.get('hostname',     "null").strip()
        ip           = request.form.get('ip',           "null").strip()
        hosttype     = request.form.get('hosttype',     "null").strip()
        pnum         = request.form.get('pnum',         "1"   ).strip()
        env          = request.form.get('env',          ""    ).strip()
        if pnum == '':
            pnum = '1'
        if project == "null" or ip == "null" or project == "" or ip == "":
            raise Exception('ERROR: parameter error')

        if hostname == '' or hostname == 'null':
            Result = getHostname(ip)
            if Result['status'] == 'ok':
                hostname = Result['log'].strip().split('.')[0]
            else:
                raise Exception('ERROR: get hostname error')
    
        ones1 = serverinfo.query.filter(serverinfo.project == project, serverinfo.ip == ip).all()
        if len(ones1) != 0:
            raise Exception('ERROR: host ip exist.')
    
        ones = projectinfo.query.filter(projectinfo.project == project ).first()
        if int(ones.port) >3000:
            t = set(range(int(ones.port), int(ones.port) + int(pnum)))
            ones3 = serverinfo.query.filter(serverinfo.ip == ip).all()
            for ones3line in ones3:
                ones4 = projectinfo.query.filter(projectinfo.project == ones3line.project ).first()
                s = set(range(int(ones4.port), int(ones4.port) + int(ones3line.pnum) ))
                repeatport = s.intersection(t)
                if repeatport:
                    raise Exception('ERROR: host ip port %s %s exist conflict.' %(ip, str(list(repeatport)) ) )

        if 'docker' in ones.codetype:
            hostname = '%s-%s' %(hostname, project)
    
        newserver = serverinfo(project, hostname, ip, pnum, env, 'checkstatus', 'checktime', 'commitid', 'updatestatus', 'updatetime', hosttype, 'null', 'null')
        db.session.add(newserver)
        db.session.commit()
        ones1 = serverinfo.query.filter(serverinfo.project == project, serverinfo.ip == ip).first()

        hir = hostInit(project, ip, ones.codetype)
        if hir != 'ok':
            raise Exception(hir)
    
        dcr = deployConfig(project, ip, ones, ones1)
        if dcr != 'ok':
            raise Exception(dcr)
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/del_host", methods=["POST"])
@login_required
def del_host():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project = request.form.get('project', 'null')
        host = request.form.get('host', 'null')
        if project == 'null' or host == 'null':
            raise Exception('ERROR: host null')
        currentuser = current_user.username
        if currentuser not in adminuser and project.startswith('online_'):
            raise Exception('ERROR: No authority')

        ones  = projectinfo.query.filter(projectinfo.project == project ).first()
        ones1 = serverinfo.query.filter(serverinfo.project == project, serverinfo.ip == host).first()
        slbReg('del', ones, ones1)
        dockerDel(ones, ones1)
        logging.warning('del_host: %s, %s, %s' %(currentuser, project, host) )
        serverinfo.query.filter(serverinfo.project == project, serverinfo.ip == host).delete()
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 %s@%s "mv %s/%s.ini  %s/%s.ini.%s.bak; supervisorctl reread;supervisorctl update" ''' %( 
                           exec_user, host, supervisor_conf_dir, project, supervisor_conf_dir, project, time.strftime('%Y%m%d_%H%M%S'))
        shellcmd(shell_cmd)
        
        #Result = shellcmd(shell_cmd)
        #if Result['status'] != 'ok':
        #    raise Exception(Result['log'])
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/update_host", methods=["POST"])
@login_required
def update_host():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project      = request.form.get('project',     'null').strip()
        hostname     = request.form.get('hostname',    'null').strip()
        ip           = request.form.get('hostip',      'null').strip()
        hosttype     = request.form.get('hosttype',    'null').strip()
        pnum         = request.form.get('pnum',        '1'   ).strip()
        env          = request.form.get('env',         ''    ).strip()
        checkstatus  = request.form.get('checkstatus', 'null').strip()
        checktime    = request.form.get('checktime',   'null').strip()
        commitid     = request.form.get('commitid',    'null').strip()
        updatestatus = request.form.get('updatestatus','null').strip()
        updatetime   = request.form.get('updatetime',  'null').strip()
    
        if project == 'null' or ip == 'null':
            raise Exception('ERROR: host null')
        currentuser = current_user.username
        logging.warning('update_host: %s, %s, %s, %s' %(currentuser, project, ip, pnum) )
        ones = projectinfo.query.filter(projectinfo.project == project ).first()
        ones1old = serverinfo.query.filter(serverinfo.project == project, serverinfo.ip == ip).first()
        pnumold = int(ones1old.pnum)
        serverinfo.query.filter(  serverinfo.project == project, 
                                  serverinfo.ip == ip
                               ).update({
                                  "hostname" : hostname, 
                                  "hosttype" : hosttype, 
                                  "pnum"     : pnum, 
                                  "env"      : env
                               })
        db.session.commit()
        ones1 = serverinfo.query.filter(serverinfo.project == project, serverinfo.ip == ip).first()
        pnum = int(ones1.pnum)
        #if pnum < pnumold:
        #    if ones.consul == 'yes':
        #        portlistnew = set(range(int(ones.port), int(ones.port) + pnum))
        #        portlistold = set(range(int(ones.port), int(ones.port) + pnumold))
        #        portlistdel = list(portlistold.difference(portlistnew))
        #        for portdel in portlistdel:
        #            print('update_host del %s %s:%s' %(project, ip, portdel))
        #        #    consulReg('del', project, ip, portdel)
        dcr = deployConfig(project, ip, ones, ones1)
        if dcr != 'ok':
            raise Exception(dcr)
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/deploy", methods=["POST"])
@login_required
def deploy():
    taskid = str(time.time())
    #获取当前用户
    currentuser = current_user.username
    #操作员时间戳
    operating_time = time.strftime('%Y%m%d_%H%M%S')
    #获取当前项目名称
    project = request.form.get("project","null")
    # 获取当前操作员
    operation = request.form.get("operation","null")
    #调用getdir函数创建项目相关的目录
    DIR = getdir(project)
    tag = '%s' %(time.strftime('%Y%m%d-%H%M%S',time.localtime( int(float(taskid)) ) ) )
    #tag = '%s-%s' %(project.split('_')[0], time.strftime('%Y%m%d_%H-%M-%S',time.localtime( int(float(taskid)) ) ) )
    #判断此次操作回退，重新定义tag
    if operation == 'serviceFallback' or operation == 'serviceFastback':
        tag = request.form.get("tag","null")
    pklFile = '%s/deploy.%s.lock' %(DIR['lock'], project)
    R = {"output":"","taskid":taskid,"operation":operation,"project":project,"tag":tag,"status":"wait"}

    try:
        if tag == 'null':
            raise Exception('ERROR: tag null')
        #判断project 和operation是否为null，必须同时满足否则报错不往下执行
        if project == "null" and operation == "null":
            raise Exception('ERROR: project or operation null')
        #判断是否存在lock文件，如果存在，则不往下执行。
        if os.path.isfile(pklFile):
            raise Exception('WARNING: Repeat the update, Please wait')
        #去数据库查询当前项目名将所有数据赋值给ones
        ones = projectinfo.query.filter(projectinfo.project == project ).all()
        #获取代码类型
        codetype = ones[0].codetype
        #获取组名
        group = ones[0].group
        # 获取环境名称
        env = ones[0].environment
        #判断当前用户是否存在adminuser这个变量中。 这个变量的值为['admin', 'liquanzhou']，如果不在这个列表则去数据库查询是否有当前的用户，组是否一致
        if currentuser not in adminuser:
            ones1 = userservicegroup.query.filter(  userservicegroup.username == currentuser, 
                                                    userservicegroup.servicegroup == group 
                                                 ).all()
            #获取权限的值
            permissions = ones1[-1].permissions
            #如果没有相等，则返回用户没有部署的权限
            if env == "online" and permissions != 'online':
                raise Exception('ERROR: user not online deploy permissions')
            #if operation == 'serviceUpdate' and env == "online" and group not in unlimit and project not in unlimitProject and not check_time():
            #    raise Exception('ERROR: online deploy time: Working day  10:00-11:30.  14:00-17:30.  19:00-20:00')
        #读取pklfile文件，将内容赋值给online_update_file
        online_update_file = open(pklFile, 'wb')
        #当前用户操作员操作时间和文件内容 作为两个参数，传入dump函数，第一个参数为obj，第二个参数为file，写入文件
        cPickle.dump('%s %s %s' %(currentuser, operation, operating_time),online_update_file)
        #关闭文件
        online_update_file.close()
        #以nohup方式，执行deploy-k8s.py传入了一大堆参数。
        s = os.system(   '''(cd %s/app/main/;nohup python -u deploy-k8s.py "%s" "%s" "%s" "%s" "%s" "%s") >>%s/%s.log 2>&1    &'''  
                         %(sys.path[0], project, tag, taskid, operation, currentuser, 'reason', DIR['log'], project) )
        R['output'] = 'INFO: Please wait. %s in progress' %(operation)
        logPath = '%s/%s-%s.log' %(DIR['result'], tag, taskid)
        newupdateoperation = updateoperation(taskid,  project, 'host', tag, operating_time, operation, currentuser, R['status'], 'commitid', 0, logPath, 'dockerimage')
        db.session.add(newupdateoperation)
        db.session.commit()
    except Exception as err:
        R['output'] = str(err)
        R['status'] = 'fail'
    #生成一个json返回
    return json.dumps(R)
    

@main.route("/cmdreturns", methods=["GET", "POST"])
@login_required
def cmdreturns():
    taskid = request.args.get('taskid', 'null')
    if taskid == "null":
        return json.dumps([['taskid','null']])
    try:
        ones = updateoperation.query.filter(updateoperation.taskid == taskid ).all()
        project  = ones[0].project
        status   = ones[0].status
        progress = ones[0].progress
        logpath  = ones[0].logpath
        logfile  = file(logpath,'r')
        result   = logHandle(logfile.read())
        logfile.close()
    except:
        return json.dumps([['sql','error']])
    rl = {'taskid': taskid, 'status': status, 'project': project, 'progress': progress, 'result': result }
    logging.info(str(rl))
    return json.dumps(rl)



@main.route("/online_log_time", methods=["GET", "POST"])
@login_required
def online_log_time():
    project = request.args.get('project', 'null')
    if project == "null":
        return json.dumps([['null', 'null', 'null', 'null', 'ERROR: project null']])
    try:
        ones = updateoperation.query.filter(  updateoperation.project == project
                                           ).order_by(updateoperation.taskid.desc()).limit(200)
    except:
        return json.dumps([['null', 'null', 'null', 'null', 'ERROR: SQL not correct']])
    rl = []
    for i in ones:
        rl.append([i.operation, i.taskid, i.tag, i.project, i.status, i.user, i.commitid])
    return json.dumps(rl)


@main.route("/online_log_all", methods=["GET", "POST"])
@login_required
def online_log_all():
    try:
        #ones = updateoperation.query.filter(  updateoperation.project.like('online_%'), 
        ones = updateoperation.query.filter(  updateoperation.taskid>int(time.time())-604800, 
                                              updateoperation.operation.in_ ([ 'serviceUpdate','serviceFastback','serviceFallback','serviceRestart','serviceExpansion','serviceFastrestart']) 
                                           ).order_by(updateoperation.taskid.desc()).all()
    except:
        return json.dumps([['null', 'null', 'null', 'null', 'ERROR: SQL not correct']])
    rl = []
    for i in ones:
        rl.append([i.operation, i.taskid, i.tag, i.project, i.status, i.user, i.commitid])
    return json.dumps(rl)


@main.route("/online_tag", methods=["GET", "POST"])
@login_required
def online_tag():
    project = request.args.get('project', 'null')
    if project == "null":
        return json.dumps(['ERROR: project null'])

    try:
        ones = updateoperation.query.filter(  updateoperation.project == project, 
                                              updateoperation.operation.in_ ([ 'serviceUpdate']),
                                              updateoperation.status == 'ok'
                                           ).order_by(updateoperation.taskid.desc()).limit(15)
    except:
        return json.dumps(['ERROR: SQL not correct'])
    rl = []
    for i in ones:
        if 'intest' in i.tag:
            continue
        if 'demo' in i.tag:
            continue
        rl.append(i.tag)
    return json.dumps( sorted(list(set(rl)), reverse=True))


@main.route("/current_tag", methods=["GET", "POST"])
def current_tag():
    project = request.args.get('project', 'null')
    if project == "null":
        return json.dumps(['ERROR: project null'])
    try:
        ones = updateoperation.query.filter(  updateoperation.project == project, 
                                              updateoperation.operation.in_ ([ 'serviceUpdate','serviceFallback','serviceFastback']), 
                                              updateoperation.status == 'ok' 
                                           ).order_by(updateoperation.taskid.desc()).limit(2)
        rl = [ones[0].tag]
    except:
        return json.dumps(['null update'])
    logging.info('tag: %s' %rl[0])
    return json.dumps(rl)



@main.route("/lastlog", methods=["GET", "POST"])
@login_required
def lastlog():
    project = request.args.get('project', 'null')
    if project == "null":
        return json.dumps([['project','null']])
    try:
        ones = updateoperation.query.filter( updateoperation.project == project, 
                                             updateoperation.status != 'wait',
                                           ).order_by(updateoperation.taskid.desc()).limit(1)
        taskid   = ones[0].taskid
        project  = ones[0].project
        status   = ones[0].status
        progress = ones[0].progress
        logpath  = ones[0].logpath
        logfile  = file(logpath,'r')
        result   = logHandle(logfile.read())
        logfile.close()
    except:
        return json.dumps([['sql','error']])
    rl = {'taskid': taskid, 'status': status, 'project': project, 'progress': progress, 'result': result }
    return json.dumps(rl)



@main.route("/update_project", methods=["POST"])
@login_required
def update_project():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        project        = request.form.get('project',        'null').strip()
        group          = request.form.get('group',          'null').strip()
        environment    = request.form.get('environment',    'null').strip()
        p              = request.form.get('p',              'null').strip()
        codetype       = request.form.get('codetype',       'null').strip()
        port           = request.form.get('port',           '0'   ).strip()
        git            = request.form.get('git',            'null').strip()
        branch         = request.form.get('branch',         'null').strip()
        config         = request.form.get('config',         'null').strip()
        make           = request.form.get('make',           'null').strip()
        start          = request.form.get('start',          'null').strip()
        remarks        = request.form.get('remarks',        'null').strip()
        dockerfile     = request.form.get('dockerfile',     'null').strip()
        k8syaml        = request.form.get('k8syaml',        'null').strip()
        makepath       = request.form.get('makepath',       './').strip().lstrip('/')
        k8smanagename  = request.form.get('k8smanagename',  'null').strip()
        nodeport       = request.form.get('nodeport',       '0').strip()
        namespace      = request.form.get('namespace',      'default').strip()
        if project == 'null' or group == 'null' or environment == 'null' or p == 'null' or branch == 'null' or codetype == 'null':
            raise Exception('ERROR: parameter error')
        project1 = environment + '_' + p
        if project != project1:
            raise Exception('ERROR: project name error')
        currentuser = current_user.username
        #if currentuser not in adminuser and environment == 'online':
        #    raise Exception('ERROR: update_project no authority')
        if not namespace:
            namespace = 'default'
        logging.warning('INFO: update_project: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' %(
                currentuser, project, group, environment, p, codetype, port, git, branch, config, make, start, remarks, dockerfile, k8syaml, makepath, k8smanagename, nodeport) )

        projectinfo.query.filter(projectinfo.project == project).update({
                             "group"          : group,
                             "codetype"       : codetype,
                             "port"           : port,
                             "git"            : git,
                             "branch"         : branch,
                             "config"         : config,
                             "make"           : make,
                             "start"          : start,
                             "remarks"        : remarks,
                             "dockerfile"     : dockerfile,
                             "k8syaml"        : k8syaml,
                             "makepath"       : makepath,
                             "k8smanagename"  : k8smanagename,
                             "nodeport"       : nodeport,
                             "namespace"      : namespace
                             })
        db.session.commit()
        ones = projectinfo.query.filter(projectinfo.project == project ).first()
        ones1all = serverinfo.query.filter(serverinfo.project == project).all()
        for ones1 in ones1all:
            dcr = deployConfig(project, ones1.ip, ones, ones1)
        #if int(port) != int(portold):
        #    print('Registration services new port')
        #    print('Stop old port flow')
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)


@main.route("/get_svcadd", methods=["GET", "POST"])
@login_required
def get_svcadd():
    R = {'status':'ok', 'log':'', 'data':{}}
    try:
        project = request.args.get("project", "null")
        ones = projectinfo.query.filter(projectinfo.project == project ).first()
        ones1 = k8scluster.query.filter(k8scluster.environment == ones.environment, k8scluster.k8smanagename == ones.k8smanagename ).first()

        ones2 = updateoperation.query.filter(  updateoperation.project == project,
                                              updateoperation.operation.in_ ([ 'serviceUpdate']),
                                              updateoperation.status == 'ok'
                                           ).order_by(updateoperation.taskid.desc()).limit(1)

        try:
            R['data']['url'] = '%s:%s' %(ones1.k8snodeip1, ones.nodeport)
        except:
            R['data']['url'] = 'ip:%s' %(ones.nodeport)
        R['data']['svc'] = '%s:%s' %(ones.p, ones.port)
        R['data']['svc_ns'] = '%s.%s.svc.cluster.local:%s' %(ones.p, ones.namespace, ones.port)
        try:
            R['data']['img'] = ones2[0].dockerimage
            R['data']['img_latest'] = '%s:latest' % ones2[0].dockerimage.split(':')[0]
        except:
            R['data']['img'] = 'null'
            R['data']['img_latest'] = 'null'
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/online_statistics", methods=["GET", "POST"])
@login_required
def online_statistics():
    try:
        monday=datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        monday_timestamp=time.mktime(time.strptime(monday.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))

        online_total=updateoperation.query.filter(updateoperation.project.like('online_%'),updateoperation.status.notlike('error'),updateoperation.taskid<monday_timestamp, updateoperation.taskid>monday_timestamp-2419200).all()

        statistical_result = {}

        for i in online_total:
            if i.project not in statistical_result:
                statistical_result[i.project] = [0,0,0,0,0,0,0,0,0,0,0,0]

            timestamp = int( float(i.taskid) )
            if timestamp < monday_timestamp and timestamp > monday_timestamp-604800:
                if i.operation == 'serviceUpdate':
                    statistical_result[i.project][0] = statistical_result[i.project][0] + 1
                elif i.operation == 'serviceRestart':
                    statistical_result[i.project][1] = statistical_result[i.project][1] + 1
                elif i.operation == 'serviceFallback':
                    statistical_result[i.project][2] = statistical_result[i.project][2] + 1
            elif timestamp < monday_timestamp and timestamp > monday_timestamp-1209600:
                if i.operation == 'serviceUpdate':
                    statistical_result[i.project][3] = statistical_result[i.project][3] + 1
                elif i.operation == 'serviceRestart':
                    statistical_result[i.project][4] = statistical_result[i.project][4] + 1
                elif i.operation == 'serviceFallback':
                    statistical_result[i.project][5] = statistical_result[i.project][5] + 1
            elif timestamp < monday_timestamp and timestamp > monday_timestamp-1814400:
                if i.operation == 'serviceUpdate':
                    statistical_result[i.project][6] = statistical_result[i.project][6] + 1
                elif i.operation == 'serviceRestart':
                    statistical_result[i.project][7] = statistical_result[i.project][7] + 1
                elif i.operation == 'serviceFallback':
                    statistical_result[i.project][8] = statistical_result[i.project][8] + 1
            elif timestamp < monday_timestamp and timestamp > monday_timestamp-2419200:
                if i.operation == 'serviceUpdate':
                    statistical_result[i.project][9] = statistical_result[i.project][9] + 1
                elif i.operation == 'serviceRestart':
                    statistical_result[i.project][10] = statistical_result[i.project][10] + 1
                elif i.operation == 'serviceFallback':
                    statistical_result[i.project][11] = statistical_result[i.project][11] + 1
        return json.dumps(statistical_result)
    except:
        return json.dumps({'status':["sql error"]})



@main.route("/lock_check", methods=["GET", "POST"])
def lock_check():
    R = {'status':'ok', 'log':'', 'data':'', 'user':''}
    try:
        project = request.args.get('project', "null")
        DIR = getdir(project)
        pklFile = '%s/deploy.%s.lock' %(DIR['lock'], project)
    
        if os.path.isfile(pklFile):
            lock_file = open(pklFile,'rb')
            lock_user = cPickle.load(lock_file)
            lock_file.close()
            R['user'] = lock_user
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)
    

@main.route("/add_workorder", methods=["POST"])
@login_required
def add_workorder():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        group = str(request.form.get('group', 'null')).strip()
        project = str(request.form.get('project', 'null')).strip()
        remarks = str(request.form.get('remarks', 'null')).strip()
    
        if project == 'null':
            raise Exception('ERROR: project null')
    
        user = current_user.username
        applicationtime = str(time.time())
        status = 'wait'
        executor = ''
        completiontime = ''
    
        newworkorder = workorder( group, project, user, applicationtime, status, executor, completiontime, remarks)
        db.session.add(newworkorder)
        db.session.commit()
    
        data = {
                "msgtype": "text",
                "text": {
                    "content": "%s\n%s 提交工单" %(project, user)
                }
            }
    
        headers = {'content-type': 'application/json'}
        r = requests.post(url=sreRobot, data=json.dumps(data), headers=headers, timeout=2).json()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)



@main.route("/update_workorder", methods=["POST"])
@login_required
def update_workorder():
    R = {'status':'ok', 'log':'', 'data':''}
    try:
        applicationtime = str(request.form.get('applicationtime', 'null')).strip()
        if project == 'null':
            raise Exception('ERROR: project null')
        oldworkorder = workorder.query.filter(workorder.applicationtime == applicationtime).one()
        oldworkorder.status = 'done'
        oldworkorder.executor = current_user.username
        oldworkorder.completiontime = str(time.time())
        db.session.flush()
        db.session.commit()
    except Exception as err:
        R['log'] = str(err)
        R['status'] = 'fail'
    return json.dumps(R)




@main.route("/wait_workorder", methods=["GET", "POST"])
@login_required
def wait_workorder():
    user = current_user.username
    try:
        if user in adminuser:
            ones = workorder.query.filter(workorder.status == 'wait' ).all()
        else:
            ones = workorder.query.filter(workorder.status == 'wait', workorder.applicant == user ).all()
    except Exception as err:
        logging.error(str(err))
        return json.dumps([['status','select workorder sql error!!!']])

    workorderlist = []
    for i in ones:
        workorderlist.append([i.group, i.project, i.applicant, i.applicationtime, i.status, i.executor, i.completiontime, i.remarks])

    return json.dumps(workorderlist)


@main.route("/done_workorder", methods=["GET", "POST"])
@login_required
def done_workorder():

    user = current_user.username

    try:
        if user in adminuser:
            ones = workorder.query.filter(workorder.status == 'done' ).order_by(workorder.applicationtime.desc()).limit(200)
        else:
            ones = workorder.query.filter(workorder.status == 'done', workorder.applicant == user ).order_by(workorder.applicationtime.desc()).limit(100)
    except Exception as err:
        logging.error(str(err))
        return json.dumps([['status','select workorder sql error!!!']])

    workorderlist = []
    for i in ones:
        workorderlist.append([i.group, i.project, i.applicant, i.applicationtime, i.status, i.executor, i.completiontime, i.remarks])

    return json.dumps(workorderlist)


@main.route("/get_area", methods=["GET", "POST"])
def get_area():
    biggroup = request.args.get("biggroup", "null")
    if biggroup == 'pp-online':
        area={'shal-d':'阿里云上海-D区','shal-f':'阿里云上海-F区','shal-e':'阿里云上海-E区','bjaws-d':'aws北京-D区'}
    elif biggroup == 'pp-test':
        area={'shal-d':'阿里云上海-D区'}
    elif biggroup == 'zy-online':
        area={'shal-d':'阿里云上海-D区','shal-f':'阿里云上海-F区','bjal-d':'阿里云北京-D区'}
    elif biggroup == 'zy-test':
        area={'shal-d':'阿里云上海-D区','shal-f':'阿里云上海-F区'}
    elif biggroup == 'hanabi-online':
        area={'shal-f':'阿里云上海-F区'}
    elif biggroup == 'hanabi-test':
        area={'shal-d':'阿里云上海-D区'}
    else:
        area={'error':'无可用区'}
    return json.dumps(area)


@main.route("/get_configuration", methods=["GET", "POST"])
def get_configuration():
    area = request.args.get("area", "null")
    if area == 'shal-d':
        configuration={'shal-4c8g':'4c8g计算网络增强型','shal-4c8g':'4c8g高主频型','shal-8c16g':'8c16g计算网络增强型','shal-8c32g':'8c32g内存型',}
    elif area == 'shal-f':
        configuration={'shal-4c8g':'4c8g计算型','shal-8c16g':'8c16g计算型','shal-8c32g':'8c32g内存型',}
    elif area == 'shal-e':
        configuration={'shal-4c8g':'4c8g计算型'}
    elif area == 'bjaws-d':
        configuration={'bjaws-4c8g':'4c8g共享型','bjaws-8c16g':'8c16g'}
    else:
        configuration={'error':'无可用配置'}
    return json.dumps(configuration)


@main.route("/create_hosts", methods=["GET", "POST"])
@login_required
def create_hosts():
    biggroup = request.form.get("biggroup", "null")
    area = request.form.get("area", "null")
    configuration = request.form.get("configuration", "null")
    image = request.form.get("image", "null")
    hostnames = request.form.get("hostnames", "null")

    create_hosts_taskid = 'ceshi-id-xx'
    log = '%s\n%s\n%s\n%s\n%s' %(biggroup,area,configuration,image,hostnames)
    r = {'status':'ok','hostnames':hostnames,'create_hosts_taskid':create_hosts_taskid,'log':log}
    return json.dumps(r)

@main.route("/get_create_hosts_result", methods=["GET", "POST"])
@login_required
def get_create_hosts_result():
    taskid = request.args.get("taskid", "null")
    log = '执行完成\n初始化完成\nok'
    r = {'status':'ok','taskid':taskid,'log':log}
    return json.dumps(r)



