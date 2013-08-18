# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from authorityengine.heart import AuthoritativeResults
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Main(View):
    
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        s = AuthoritativeResults(q)
        res = s.get_results(max_links=2)
        
        l = [
            (d['link'], d['scores'], d['sum_words'],
            d['sum_unique_words'], d['sum_terms'])
            for d in res
            ]
        
        return render_to_response('results.html', {'list_d':l})