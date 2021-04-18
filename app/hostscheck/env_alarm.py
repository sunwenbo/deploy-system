import subprocess
import requests
import time
import sys
import os
import json


Webhook = 'https://oapi.dingtalk.com/robot/send?access_token=f036c0bce84af52a634287f394ba01f0850f5c9b043b3832bb8a94b7ae2a83c7'

rtime = time.strftime('%Y%m%d_%H%M%S')

headers = {'Content-Type':'application/json'}

def exec_shell(shell_cmd):
    s = subprocess.Popen( shell_cmd, shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
    newlog, stderr = s.communicate()
    return_status = s.returncode
    if return_status == 0:
        return {'status':'ok', 'log':newlog}
    else:
        return {'status':'fail', 'log':newlog + stderr}

try:
    envall = requests.get('http://deploy.lc.com/envproject', timeout=2).json()
except Exception as err:
    print('ERROR: envproject URL GET fail')


for project,projectinfo in envall.items():
    for ip,ipinfo in projectinfo['host'].items():
        shell_cmd = '''ssh -o StrictHostKeyChecking=no -o ConnectTimeout=7 -p %s bae@%s "grep APP_ENV /home/bae/wwwroot/project/.env " ''' %(int(projectinfo['port']) + 20000 , ip)
        hostresult = exec_shell(shell_cmd)
        print hostresult
        if hostresult['status'] == 'fail':
            continue
        try:
            env = hostresult['log'].strip().split('=')[1].strip()
        except:
            continue
        print rtime,project,ip,projectinfo['port'],ipinfo['hostname'],env
        if env != 'true':
            AlarmInfo = '%s %s APP_ENV ERROR: %s' %(project, ip, env)
            ExpansionHost = {
                    "msgtype": "text",
                    "text": {
                        "content": AlarmInfo
                    }
                }
            try:
                requests.post(url=Webhook, headers=headers, data=json.dumps(ExpansionHost))
            except Exception as err:
                print(str(err))




