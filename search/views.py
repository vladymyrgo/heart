# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from authorityengine.heart import AuthoritativeResults
from django.views.generic.base import View
import tasks

class Main(View):
    
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        k = request.GET.get('k')
        
        max_links = 4 # Limiting the number of links
        
        if k == 'wait': # Send results to browser
            s = AuthoritativeResults(q)
            res = s.get_results(max_links)
            
            l = [
                (d['link'], d['title'], d['scores'], d['sum_words'],
                d['sum_unique_words'], d['sum_terms'])
                for d in res
                ]
            
            return render_to_response('results.html', {'list_d':l})
        
        elif k == 'create': # Create file with results
            tasks.create_results_file.delay(q, max_links)
            return render_to_response('wait.html')