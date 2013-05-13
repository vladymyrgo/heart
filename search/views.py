# coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext #to make CSS work
from authorityengine.heart import *
import urllib

def start_page(request):
    return render_to_response('start_page.html', RequestContext(request))

def search(request):
    q = request.GET['q']
    if q:
        a = HTMLcollector(q)
        results = a.main_search_page()
        return render_to_response('results.html', {'results':results,}, RequestContext(request))
    else:
        return render_to_response('start_page.html', RequestContext(request))
