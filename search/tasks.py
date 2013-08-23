# -*- coding: utf-8 -*-

import codecs
import celery
from authorityengine.heart import AuthoritativeResults

@celery.task
def create_results_file(q, max_links=2):
    s = AuthoritativeResults(q)
    res = s.get_results(max_links)
    
    with codecs.open('/media/files/documents/heart_results.html','w', "utf-8") as f:
        
        l = [
            (d['link'], d['title'], d['scores'], d['sum_terms'])
            for d in res
            ]
        
        s_s = '<html>\n<head>\n</head>\n<body>\n'
        s_m = ''
        s_f = '</body>\n</html>'
        n = 1
        for link in l:
            s_m += """<h4><a href="%(link)s">%(n)s - %(title)s</a></h4>\n
                        <p>Scores: %(scores)s</p>\n""" % {
                                                        'n': n,
                                                        'link': link[0],
                                                        'title': link[1],
                                                        'scores': link[2]
                                                        }
            n += 1
        s = s_s + s_m + s_f
        f.write(s)