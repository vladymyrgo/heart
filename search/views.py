# coding:utf-8
import urllib
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext #to make CSS work
from authorityengine.heart import *
from search.models import Cities, HtmlTest


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

def html_test():
    s=AuthorityAnalyzer('some')
    a='True' if s.if_unit('грв') is True else 'False'
    return a

def mytest():
    s=AuthorityAnalyzer('some')
    dic = {'владимир':2,'гр':1,'киев':5,'атом':7,'asdfdas':14,'fsdf':1}
    a = s.count_authoritative_word(dic)
    return sum(a.values())

def auth_dic():
    s=AuthorityAnalyzer('some')
    html = HtmlTest.objects.get(id=3)
    dic = s.authoritative_characteristics(html.html)
    out = html.site+'-----'
    for i in dic: out+=str(i)+':';out+=str(dic[i])+'\n'
    return out

def test(request):
    f=auth_dic()
    return HttpResponse(f)