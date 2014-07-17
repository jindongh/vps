#!/usr/bin/python
#coding: utf-8
import config
import json
import urllib
import urllib2
import hashlib
import filedb
import time


BEIJING=u'\u5317\u4eac'.encode('utf-8')
#MeiShi
EAT=u'\u7f8e\u98df'.encode('utf-8')
def reqJson(url, params):
    try:
        paramData=urllib.urlencode(params)
        full_url='%s?%s' % (url, paramData)
        raw=urllib2.urlopen(full_url).read()
        obj=json.loads(raw)
        return obj
    except Exception, e:
        return {'status':-1, 'result': e}

def reqDianPing(url, params):
    tmpParam=''
    for param in sorted(params.keys()):
        tmpParam+=param+params[param]
    tmpParam=config.DIANPING_KEY + tmpParam + config.DIANPING_SECRET
    sign=hashlib.sha1(tmpParam).hexdigest().upper()
    params['appkey'] = config.DIANPING_KEY
    params['sign'] = sign
    return reqJson(url, params)

def getLocation(addr):
    URL='http://api.map.baidu.com/geocoder/v2/'
    params={'address':addr,
            'output':'json',
            'ak':config.BIDU_KEY
            }
    return reqJson(URL, params)

def getOptionsDianPing(city, loc, category):
    URL='http://api.dianping.com/v1/deal/find_deals'
    params={
            'city': city,
            'sort': '7',
            'category': category,
            'latitude': str(loc['location']['lat']),
            'longitude': str(loc['location']['lng']),
            }
    return reqDianPing(URL, params)

def getOptionsBIDU(city, loc, category):
    URL='http://api.map.baidu.com/place/v2/eventsearch'
    params={
            'query': category,
            'event':'groupon',
            'region':city,
            'location':'%f,%f' % (loc['location']['lat'], loc['location']['lng']),
            'output':'json',
            'ak':config.BIDU_KEY,
            }
    return reqJson(URL, params)

def searchDianPing(name, category):
    loc = getLocation(name)
    if not loc['status'] == 0:
        return 'Not Found, try another location name'
    options = getOptionsDianPing(BEIJING, loc['result'], category)
    result=[]
    for option in options['deals']:
        result.append('%s %dM %dRMB %s' % (
            option['title'],
            option['distance'],
            int(option['current_price']),
            option['deal_h5_url']
            )
            )
    return '\n'.join(result)

def searchBIDU(name, category):
    loc = getLocation(name)
    if not loc['status'] == 0:
        return 'Not Found, try another location name'
    options = getOptionsBIDU(BEIJING, loc['result'], category)
    result=[]
    for option in options['results']:
        result.append('%s %sM %sRMB %s' % (
            option['name'],
            option['distance'],
            option['events'][0]['groupon_price'],
            option['events'][0]['groupon_webapp_url'],
            )
            )
    return '\n'.join(result)

def search(name, category=EAT):
    db=filedb.FileDB()

    #try db first
    dbitem=db.getItem(db.GROUPON, name)
    if not None==dbitem:
        now=int(time.time())
        #check timeout
        if now - dbitem[0] < 300:
            return dbitem[1]

    #access api
    if False:
        result=searchBIDU(name, category)
    else:
        result=searchDianPing(name, category)
    
    #save cache
    db.setItem(db.GROUPON, name, result)
    return result

def translate(query):
    URL='http://openapi.baidu.com/public/2.0/bmt/translate'
    params={
            "q":query,
            'client_id': config.BIDU_KEY,
            'from':'auto',
            'to':'auto',
            }
    res=reqJson(URL, params)
    result=[]
    for item in res['trans_result']:
        result.append(item['dst'])
    return '\n'.join(result)

def isEnglish(query):
    for x in query:
        if ord(x)>127:
            return False
    return True

if __name__=='__main__':
    #for debug
    #BaiDu in chinese
    BAIDU=u'\u767e\u5ea6\u5927\u53a6'.encode('utf-8')
    '''
    loc = getLocation(BAIDU)
    if not loc['status'] == 0:
        print 'get location failed'
    print loc
    options = getOptions(BEIJING, loc['result'])
    print options
    '''

    result=search(BAIDU)
    print result.decode('utf-8').encode('gb2312')
    print translate('hello'.encode('utf-8')).encode('gb2312')
    print translate(u'\u4f60\u597d'.encode('utf-8'))


