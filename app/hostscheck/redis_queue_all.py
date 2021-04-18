import re
import sys
import redis

rds = redis.StrictRedis(host='r-bp10f2ddc88c4314.redis.rds.aliyuncs.com', port=6379, db=0, password='QzYUy0BwqFZaGRuZvDtS')




for key in rds.scan_iter(match='*', count=1000):
    try:
        if 'queues:' in key:
            num = rds.llen(key)
            print '%s : %s' %(key, num)
    except Exception,err:
        pass
        #Linenum = sys._getframe().f_lineno
        #print 'Linenum: %s log: %s' %(Linenum, str(err))


#print rds.delete('aa')

