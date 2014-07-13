#!/usr/bin/python
#coding: utf-8
#description: change img src from 163 etc to local

import MySQLdb
import os
import re

conn=MySQLdb.connect(host="localhost",user="blogu",passwd="blogp",db="blog",charset="utf8")  
cursor = conn.cursor() 
n = cursor.execute("select id,content from zinnia_entry")    
rows = cursor.fetchall()
for row in rows:
    rid=row[0]
    rdata=row[1]
    update=False
    for ip in ['126','163']:
        for net in ['com', 'net']:
            for pic in ['jpg', 'png', 'bmp', 'gif']:
                ret = re.findall('"(http://[^"]*%s.%s/[^"]*.%s)"' % (ip, net, pic), rdata)
                for item in ret:
                    rdata=rdata.replace(item, '/static/163/%s' % os.path.basename(item))
                    update=True
    if update:
        sql = "update zinnia_entry set content=%s where id=%s"   
        param = (rdata, int(rid))
        n = cursor.execute(sql, param)    
        print 'update %s ret=%d' % (rid,n)
conn.commit()
