#!/usr/bin/env python
# coding: utf-8

from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    _password = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)


class serverinfo(db.Model):
    __tablename__ = 'serverinfo'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(64) , index=True)
    hostname = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    pnum = db.Column(db.String(32))
    env = db.Column(db.String(3200))
    checkstatus = db.Column(db.String(64))
    checktime = db.Column(db.String(64))
    commitid = db.Column(db.String(64))
    updatestatus = db.Column(db.String(64))
    updatetime = db.Column(db.String(64))
    hosttype = db.Column(db.String(32))
    checkconsulstatus = db.Column(db.String(64))
    checkconsultime = db.Column(db.String(64))

    def __init__(self, project, hostname, ip, pnum, env, checkstatus, checktime, commitid, updatestatus, updatetime, hosttype, checkconsulstatus, checkconsultime):
        self.project = project
        self.hostname = hostname
        self.ip = ip
        self.pnum = pnum
        self.env = env
        self.checkstatus = checkstatus
        self.checktime = checktime
        self.commitid = commitid
        self.updatestatus = updatestatus
        self.updatetime = updatetime
        self.hosttype = hosttype
        self.checkconsulstatus = checkconsulstatus
        self.checkconsultime = checkconsultime


class userservicegroup(db.Model):
    __tablename__ = 'userservicegroup'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    servicegroup = db.Column(db.String(64))
    permissions = db.Column(db.String(64))

    def __init__(self, username, servicegroup, permissions):
        self.username = username
        self.servicegroup = servicegroup
        self.permissions = permissions

class servicegroup(db.Model):
    __tablename__ = 'servicegroup'
    id = db.Column(db.Integer, primary_key=True)
    servicegroup = db.Column(db.String(64))
    def __init__(self, servicegroup):
        self.servicegroup = servicegroup

class serviceenvironment(db.Model):
    __tablename__ = 'serviceenvironment'
    id = db.Column(db.Integer, primary_key=True)
    serviceenvironment = db.Column(db.String(64))
    def __init__(self, serviceenvironment):
        self.serviceenvironment = serviceenvironment

class servicecodetype(db.Model):
    __tablename__ = 'servicecodetype'
    id = db.Column(db.Integer, primary_key=True)
    servicecodetype = db.Column(db.String(64))
    def __init__(self, servicecodetype):
        self.servicecodetype = servicecodetype



class projectinfo(db.Model):
    __tablename__ = 'projectinfo'
    project = db.Column(db.String(64), primary_key=True)
    group = db.Column(db.String(40))
    environment = db.Column(db.String(64))
    p = db.Column(db.String(64))
    codetype = db.Column(db.String(50))
    port = db.Column(db.Integer)
    git = db.Column(db.String(1024))
    branch = db.Column(db.String(64))
    config = db.Column(db.Text)
    make = db.Column(db.Text)
    start = db.Column(db.Text)
    remarks = db.Column(db.Text)
    dockerfile = db.Column(db.Text)
    k8syaml = db.Column(db.Text)
    makepath = db.Column(db.String(1000))
    k8smanagename = db.Column(db.String(128))
    nodeport = db.Column(db.Integer)
    namespace = db.Column(db.String(32))

    def __init__(self, project, group, environment, p, codetype, port, git, branch, config, make, start, remarks, dockerfile, k8syaml, makepath, k8smanagename, nodeport, namespace):
        self.project = project
        self.group = group
        self.environment = environment
        self.p = p
        self.codetype = codetype
        self.port = port
        self.git = git
        self.branch = branch
        self.config = config
        self.make = make
        self.start = start
        self.remarks = remarks
        self.dockerfile = dockerfile
        self.k8syaml = k8syaml
        self.makepath = makepath
        self.k8smanagename = k8smanagename
        self.nodeport = nodeport
        self.namespace = namespace

class k8scluster(db.Model):
    __tablename__ = 'k8scluster'
    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String(64))
    k8smanagename = db.Column(db.String(64))
    k8smanagefilecontent = db.Column(db.Text)
    k8snodeip1 = db.Column(db.String(64))
    k8snode1 = db.Column(db.String(64))

    def __init__(self, environment, k8smanagename, k8smanagefilecontent, k8snodeip1, k8snode1):
        self.environment            = environment
        self.k8smanagename          = k8smanagename
        self.k8smanagefilecontent   = k8smanagefilecontent
        self.k8snodeip1             = k8snodeip1
        self.k8snode1               = k8snode1

class templatefile(db.Model):
    __tablename__ = 'templatefile'
    id = db.Column(db.Integer, primary_key=True)
    codetype = db.Column(db.String(64))
    templatefilename = db.Column(db.String(64))
    templatefilecontent = db.Column(db.Text)

    def __init__(self, codetype, templatefilename, templatefilecontent):
        self.codetype            = codetype
        self.templatefilename    = templatefilename
        self.templatefilecontent = templatefilecontent


class updateoperation(db.Model):
    __tablename__ = 'updateoperation'
    taskid = db.Column(db.String(64), primary_key=True, index=True)
    project = db.Column(db.String(64))
    hostlist = db.Column(db.String(2000))
    tag = db.Column(db.String(64))
    rtime = db.Column(db.String(32))
    operation = db.Column(db.String(64))
    user = db.Column(db.String(50))
    status = db.Column(db.String(20))
    commitid = db.Column(db.String(1024))
    progress = db.Column(db.Integer)
    logpath = db.Column(db.String(2000))
    dockerimage = db.Column(db.String(1024))

    def __init__(self, taskid, project, hostlist, tag, rtime, operation, user, status, commitid, progress, logpath, dockerimage):
        self.taskid = taskid
        self.project = project
        self.hostlist = hostlist
        self.tag = tag
        self.rtime = rtime
        self.operation = operation
        self.user = user
        self.status = status
        self.commitid = commitid
        self.progress = progress
        self.logpath = logpath
        self.dockerimage = dockerimage


class workorder(db.Model):
    __tablename__ = 'workorder'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(64))
    project = db.Column(db.String(64))
    applicant = db.Column(db.String(64))
    applicationtime = db.Column(db.String(64))
    status = db.Column(db.String(64))
    executor = db.Column(db.String(64))
    completiontime = db.Column(db.String(64))
    remarks = db.Column(db.Text)

    def __init__(self, group, project, applicant, applicationtime, status, executor, completiontime, remarks):
        self.group = group
        self.project = project
        self.applicant = applicant
        self.applicationtime = applicationtime
        self.status = status
        self.executor = executor
        self.completiontime = completiontime
        self.remarks = remarks


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

