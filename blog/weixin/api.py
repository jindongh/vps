#!/usr/bin/python
#coding: utf-8
import config
import json
import urllib
import urllib2
import hashlib


BEIJING='北京'
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

def getOptions(city, loc):
    URL='http://api.dianping.com/v1/deal/find_deals'
    params={
            'city': city,
            'sort': '7',
            'latitude': str(loc['location']['lat']),
            'longitude': str(loc['location']['lng']),
            }
    return reqDianPing(URL, params)

def search(name):
    loc = getLocation(name)
    if not loc['status'] == 0:
        return 'Not Found, try another location name'
    options = getOptions(BEIJING, loc['result'])
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

def getHelp():
    return 'Please Input Location to Found items'

if __name__=='__main__':
    BAIDU='百度大厦'
    loc = getLocation(BAIDU)
    if not loc['status'] == 0:
        print 'get location failed'
    print loc
    options = getOptions(BEIJING, loc['result'])
    print options
    print search(BAIDU)


