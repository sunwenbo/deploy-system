import requests
import json
import sys
import socket

def regconsul(name, ip, port, service_id, hostname, httpurl):
    tag = []
    if 'stg-' in hostname:
        tag.append('weight_1')

    payload = {
            'ID' : service_id,
            'Name' : name,
            'Port' : port,
            'Address' : ip,
            'Tags' : tag,
            'Check' : {
                'http' : "http://%s:%d%s" %(ip, port, httpurl),
                'Interval' : '2s',
                'Timeout' : '2s'
            }
    }

    headers = {'content-type': 'application/json'}
    regurl = 'http://127.0.0.1:8500/v1/agent/service/register'
    print(payload)

    try:
        r = requests.put(regurl,  data=json.dumps(payload), headers=headers)
        status = r.status_code
        if status == 200:
            print('INFO: reg consul %s http status: %s' %(name, status))
        else:
            print('ERROR: reg consul %s http status: %s' %(name, status))
            sys.exit(3)

    except Exception as err:
        print(str(err))
        sys.exit(2)


def delconsul(name, ip, port, service_id, hostname, httpurl):
    delurl = 'http://127.0.0.1:8500/v1/agent/service/deregister/%s' % service_id
    try:
        r = requests.put(delurl)
        status = r.status_code
        if status == 200:
            print('INFO: del consul %s http status: %s' %(name, status))
        else:
            print('ERROR: del consul %s http status: %s' %(name, status))
            sys.exit(3)
    except Exception as err:
        print(str(err))
        sys.exit(2)


operation = sys.argv[1]
name = sys.argv[2]
ip = sys.argv[3]
port = int(sys.argv[4])
try:
    httpurl = sys.argv[5]
except:
    httpurl = '/slbhb'

hostname = socket.gethostname()

service_id = "%s-%s-%d" %(name,ip, port)
print(service_id)

if operation == 'reg':
    regconsul(name, ip, port, service_id, hostname, httpurl)
elif operation == 'del':
    delconsul(name, ip, port, service_id, hostname, httpurl)




