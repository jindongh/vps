#!/bin/env python
#encoding: utf-8
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from store.models import App
import os

# Create your views here.

def index(req):
    apps = App.objects.order_by('name')
    return render_to_response('store.html', {"apps":apps})

def version(req):
    app=get_app_or_404(req)
    app.version='1.1'
    info='''<?xml version="1.0" encoding="utf-8"?>  
<info>  
    <version>%s</version>  
    <url>http://hankjohn.net/store/download?package=%s</url>  
    <description>%s</description>
</info>  
    ''' % (app.version, app.package, app.description)
    return HttpResponse(info,mimetype='application/xml')

def download(req):
    app=get_app_or_404(req)
    f = open(app.apk.path)
    data = f.read()
    f.close()
    response = HttpResponse(data, mimetype='application/octer-stream')
    response['Content-Length'] = len(data)
    response['Content-Disposition']='attachment; filename=%s' % os.path.basename(app.apk.name)
    return response

def get_app_or_404(req):
    package = req.GET['package']
    apps = App.objects.filter(package=package)
    if 0 == len(apps):
        raise Http404
    return apps[0]

