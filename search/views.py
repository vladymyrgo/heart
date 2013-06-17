# coding:utf-8
import urllib
from django.shortcuts import render_to_response, HttpResponse
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
    s=AuthorityCalculation('some')
    a='True' if s.if_unit('грв') is True else 'False'
    return a

def mytest():
    s=AuthorityCalculation('some')
    dic = {'владимир':2,'гр':1,'киев':5,'атом':7,'asdfdas':14,'fsdf':1}
    a = s.count_authoritative_word(dic)
    return sum(a.values())

def auth_dic():
    s=AuthorityCalculation('some')
    html = HtmlTest.objects.get(id=3)
    dic = s.authoritative_characteristics(html.html)
    out = html.site+'-----'
    for i in dic: out+=str(i)+':';out+=str(dic[i])+'\n'
    return out

def heart(request):
    s = AuthoritativeResult('мужские черты')
    l = s.gradation_authority()
    return HttpResponse(str(l))

def results(request):
    q = request.GET.get('q')
    #s = AuthoritativeResult(q)
    #res = s.get_results()
    res = [{'sum_units': 0, 'sum_cities': 4, 'sum_terms': 19, 'sum_words': 656, 'id': 1L, 'link': u'http://www.kleo.ru/items/planetarium/kristina_orbakajte_muzhskie_ch.shtml', 'scores': 68, 'add_time': 1370962961L, 'sum_percent': 0, 'sum_names': 45, 'sum_unique_words': 470}, {'sum_units': 0, 'sum_cities': 0, 'sum_terms': 0, 'sum_words': 0, 'id': 2L, 'link': u'http://www.genon.ru/GetAnswer.aspx?qid=58c91b6e-701a-4ebb-80a6-2d9a54384d8b', 'scores': 0, 'add_time': 1371024424L, 'sum_percent': 0, 'sum_names': 0, 'sum_unique_words': 0}, {'sum_units': 0, 'sum_cities': 0, 'sum_terms': 0, 'sum_words': 0, 'id': 3L, 'link': u'http://www.ardor.ru/seducer/mood/1_07/', 'scores': 0, 'add_time': 1371024424L, 'sum_percent': 0, 'sum_names': 0, 'sum_unique_words': 0}]

    l = [(d['link'], d['scores'], d['sum_words'], d['sum_unique_words'], d['sum_terms']) for d in res]
    return render_to_response('results.html', {'list_d':l})

def start(request):
    return render_to_response('base.html')



