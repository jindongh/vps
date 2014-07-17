#!/usr/bin/python
#coding: utf-8
import config
import json
import urllib
import urllib2
import hashlib
import filedb
import time


BEIJING='北京'
EAT='美食'
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

def getOptionsDianPing(city, loc):
    URL='http://api.dianping.com/v1/deal/find_deals'
    params={
            'city': city,
            'sort': '7',
            'latitude': str(loc['location']['lat']),
            'longitude': str(loc['location']['lng']),
            }
    return reqDianPing(URL, params)

def getOptionsBIDU(city, loc):
    URL='http://api.map.baidu.com/place/v2/eventsearch'
    params={
            'query':EAT,
            'event':'groupon',
            'region':city,
            'location':'%f,%f' % (loc['location']['lat'], loc['location']['lng']),
            'output':'json',
            'ak':config.BIDU_KEY,
            }
    return reqJson(URL, params)

def searchDianPing(name):
    loc = getLocation(name)
    if not loc['status'] == 0:
        return 'Not Found, try another location name'
    options = getOptionsDianPing(BEIJING, loc['result'])
    result=[]
    for option in options['deals']:
        result.append('%s(%s)%dM %fRMB %s' % (
            option['title'],
            option['description'],
            option['distance'],
            option['current_price'],
            option['deal_h5_url']
            )
            )
    return '\n'.join(result)

def searchBIDU(name):
    loc = getLocation(name)
    if not loc['status'] == 0:
        return 'Not Found, try another location name'
    options = getOptionsBIDU(BEIJING, loc['result'])
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

def search(name):
    db=filedb.FileDB()

    #try db first
    dbitem=db.getItem(db.GROUPON, name)
    if not None==dbitem:
        now=int(time.time())
        #check timeout
        if now - dbitem[0] < 300:
            return dbitem[1]

    #access api
    if True:
        result=searchBIDU(name)
    else:
        result=searchDianPing(name)

    #save cache
    db.setItem(db.GROUPON, name, result)
    return result

def getHelp():
    return 'Please Input Location to Found items'

if __name__=='__main__':
    #for debug
    BAIDU='百度大厦'
    '''
    loc = getLocation(BAIDU)
    if not loc['status'] == 0:
        print 'get location failed'
    print loc
    options = getOptions(BEIJING, loc['result'])
    print options
    '''
    print search(BAIDU)


