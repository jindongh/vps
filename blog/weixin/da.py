#!/usr/bin/python
#coding: utf-8
import api
from django.shortcuts import render_to_response

#http://www.hankjohn.net/weixin/web
def helpMsg():
    return render_to_response('weixin.html')
    return u'''
menu/help/\u5e2e\u52a9: \u6253\u5370\u5e2e\u52a9\u83dc\u5355
1. \u670d\u52a1
<\u897f\u4e8c\u65d7>: \u4e2d\u6587\u5730\u540d\uff0c\u81ea\u52a8\u5bfb\u627e\u9644\u8fd1\u7f8e\u98df
<\u4f4f\u5bbf> <\u897f\u4e8c\u65d7>\uff1a\u670d\u52a1\u7c7b\u578b+\u7a7a\u683c+\u5730\u540d\uff1a\u5bfb\u627e\u9644\u8fd1\u670d\u52a1
2. \u5de5\u5177
<english sentenses>: \u82f1\u6587\u53e5\u5b50\u6216\u5355\u8bcd\u81ea\u52a8\u7ffb\u8bd1
\u751f\u65e5:\u67e5\u770b\u751f\u65e5\u8bb0\u5f55
\u751f\u65e5 \u59d3\u540d \u65f6\u95f4:\u67e5\u770b\u751f\u65e5\u8bb0\u5f55
\u7ffb\u8bd1 <\u4e2d\u6587\u53e5\u5b50>\uff1a\u7ffb\u8bd1\u4e2d\u6587\u5230\u82f1\u6587
    '''.encode('utf-8')
def birthList():
    return [
            'Hankjin: 1985-10-17',
            'Father: 1950-10-11',
            ]
def birthOP(query):
    return 'TODO: %s' % query

SERVICES={
        #movie
        u'\u7535\u5f71'.encode('utf-8'): u'\u9662\u7ebf\u5f71\u9662'.encode('utf-8'),
        #eat
        u'\u7f8e\u98df'.encode('utf-8'): u'\u7f8e\u98df'.encode('utf-8'),
        #shopping
        u'\u8d2d\u7269'.encode('utf-8'): u'\u8d2d\u7269'.encode('utf-8'),
        #entertainment
        u'\u5a31\u4e50'.encode('utf-8'): u'\u4f11\u95f2\u5a31\u4e50'.encode('utf-8'),
        u'\u4f11\u95f2'.encode('utf-8'): u'\u4f11\u95f2\u5a31\u4e50'.encode('utf-8'),
        #hotel
        u'\u9152\u5e97'.encode('utf-8'): u'\u9152\u5e97'.encode('utf-8'),
        u'\u65c5\u5e97'.encode('utf-8'): u'\u9152\u5e97'.encode('utf-8'),
        #travel
        u'\u65c5\u884c'.encode('utf-8'): u'\u65c5\u884c'.encode('utf-8'),
        #daily
        u'\u751f\u6d3b'.encode('utf-8'): u'\u751f\u6d3b\u670d\u52a1'.encode('utf-8'),
        }
def analyze(query):
    #1.help/BangZhu
    if query in ['help', 'menu', u'\u5e2e\u52a9'.encode('utf-8')]:
        return helpMsg()
    #2.birthday
    if query == u'\u751f\u65e5'.encode('utf-8'):
        return '\n'.join(birthList())
    if query.startswith(u'\u751f\u65e5 '.encode('utf-8')):
        return birthOP(query)
    #3. services
    ensubquery=query.split()
    chsubquery=query.split(u'\u3000'.encode('utf-8'))
    subquery=query
    sublen=0
    if len(ensubquery)>1: #there is subquery in english
        subquery=ensubquery[0]
        sublen=1
    if len(chsubquery)>1 and len(chsubquery[0]) < len(subquery):#there is subquery in chinese and shorter
        subquery=chsubquery[0]
        sublen=3
    if not subquery==query:
        #1.translate
        if subquery in ('translate', u'\u7ffb\u8bd1'.encode('utf-8')):
            return api.translate(query[len(subquery)+1:])
        #2. movie, eatting, shopping, entertain, hotel, travel
        if subquery in SERVICES:
            print SERVICES[subquery].decode('utf-8').encode('gbk')
            return api.search(query[len(subquery)+sublen:], SERVICES[subquery])
    #4 default
    return api.translate(query)

if __name__=='__main__':
    #1. help
    print '1.helo'
    print analyze('help').decode('utf-8').encode('gb2312')
    print '2.birth'
    print analyze(u'\u751f\u65e5'.encode('utf-8'))
    print '3. trans'
    print analyze(u'\u7ffb\u8bd1 hello'.encode('utf-8'))
    print '4.search'
    print analyze(u'\u5a31\u4e50 \u5929\u5b89\u95e8'.encode('utf-8')).decode('utf8').encode('gbk')
    print '5.trans'
    print analyze('hello world'.encode('utf-8')).encode('gbk')
