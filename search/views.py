# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from authorityengine.heart import AuthoritativeResults

def start(request):
    return render_to_response('base.html')

def results(request):
    q = request.GET.get('q')
    s = AuthoritativeResults(q)
    res = s.get_results(max_links=20)
    
    l = [
        (d['link'], d['scores'], d['sum_words'],
          d['sum_unique_words'], d['sum_terms'])
        for d in res
        ]
    return render_to_response('results.html', {'list_d':l})