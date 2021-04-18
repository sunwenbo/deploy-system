#!/usr/bin/env python
# coding: utf-8

# 发布系统本地配置
# 管理员用户 用户名
adminuser = ['admin', 'liquanzhou', 'tianwen', 'tian', 'wangpengcheng', 'sunwenbo', 'wangjinbo', 'taodongjie', 'liyanzhe', 'xiaosha', 'wangyucheng']
# 发布系统执行编译及ssh用户
exec_user = 'work'
# 发布系统工作目录
deploywork  = '/data/deploywork/'
# git仓库目录
path_git    = deploywork + 'git/'
# 上线log目录
path_log    = deploywork + 'log/'
# 任务锁文件目录
path_lock   = deploywork + 'lock/'
# 项目配置文件目录
path_conf   = deploywork + 'conf/'
# 更新执行结果目录
path_result = deploywork + 'result/'

path_off    = deploywork + 'off/'


# ldap crowd user
Login = 'crowd'
#ldap: True    用户登陆: False
LDAP_HOST = "ldap://ldap.lc.com:389"
LDAP_BIND = "uid=admin,ou=People,dc=lc,dc=com"
LDAP_PWD  = "123"
LDAP_BASE = "ou=People,dc=lc,dc=com"
# crowd
crowd_url = 'http://192.168.10.251:8095/crowd'
crowd_user = 'confluence'
crowd_pass = 'shanjing0322'


# 远程发布目录
#remote_host_path = '/opt/'

# 使用supervisord管理的进程 项目类型
#supervisord_list = ['sh', 'go', 'golang', 'python', 'nodejs', 'java-jar']
# 远程主机supervisor配置文件目录
# [include] 
# files = supervisor_conf_dir/*.ini
#supervisor_conf_dir = '/etc/supervisord.d/'
# 远程主机supervisor存放日志目录, 没有服务无法启动
#supervisor_log_path = '/opt/logs/'


# 管理员菜单列表
adminpagelist = [['online','上线'],['project_add','添加项目'],['project_admin','项目管理'],['online_log','发布日志'],['statistics','统计'],['useradmin','用户管理'],['workorderweb','上线工单'],['hostmanage','主机管理']]
# 普通用户菜单列表
userpagelist = [['online','上线'],['project_add','添加项目'],['online_log','发布日志'],['statistics','统计'],['workorderweb','上线工单']]


# 运维钉钉通知地址
sreRobot = ''
# 业务线钉钉通知
groupRobot = ''
# 发钉钉通知的组 组名
basicGlist = ['app']

confgit = 'git@git.senses-ai.com:sre/go-test.git'
java_commons_git = 'git@git.senses-ai.com:sre/go-test.git'

imgaddr = 'image.senses-ai.com'

# 检查服务状态时,获取项目信息
#projectinfoallurl = 'http://127.0.0.1:6000/projectinfoall'
#hostlistallurl = 'http://127.0.0.1:6000/hostlistall'
# 检查服务状态时,获取主机列表
iplistallurl = 'http://192.168.88.174:5000/iplistall'
# 检查失败不报警的项目  项目名
filterList = ['online_testproject']
# 检查失败不报警的主机列表 ip
notcheckhost = ['172.10.0.172', '172.20.20.80']


# 不限制上线时间的组 组名
unlimit = ['offline', 'sre', 'op', 'web']
unlimitProject = ['test_project']

autotestURL = 'http://10.10.10.10/deploy/check'
# 需要自动测试的项目 项目名
autolist = ['online_testproject', 'online_testproject2']


