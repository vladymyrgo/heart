# coding:utf-8
import urllib
from bs4 import BeautifulSoup

class HTMLcollector(object):
    def __init__(self, user_request):
        self.user_request = user_request
        
    def search_html(self, page):
        '''
        Принимает номер страницы для поиска и возвращает html поиска.
        '''
        bing='http://www.bing.com/search?'
        request = ''.join(['q=', self.user_request])
        first = ''.join(['&first=', str(((page-1)*10)+1)])
        search_url = ''.join([bing, request, first])
        search_page = urllib.urlopen(search_url).read()
        return search_page
    
    def links_scanner(self, html):
        '''
        Принимает html поиска и возвращает список ссылок с этой страницы.
        '''
        soup = BeautifulSoup(html)
        links = [a.a['href'] for a in soup.find_all('h3')]
        return links
    
    def is_next_button(self, html):
        '''
        Принимает html поиска и возвращает "True" если есть кнопка "Next".
        Это нужно для определения последней страницы результатов поиска.
        '''
        soup = BeautifulSoup(html)
        return True if soup.select(".sb_pagN") else False
    
    def get_links(self, max_search_page, max_links):
        '''
        Возвращает список ссылок поиска на сайты.
        Может принимать ограничение 'max_page' по количеству сканируемых страниц поиска и
        ограничение max_links по количеству возвращаемых ссылок.
        '''
        all_links=[]
        for p in range(1, max_search_page+1): # листаем станицы поиска
            # открываем html поиска функцией search_html()
            html = self.search_html(page=p)
            #Если есть кнопка 'Next', и не срабатывают ограничители
            #то собираем ссылки и идем на след. стр.
            if self.is_next_button(html=html) and p < max_search_page and len(all_links) < max_links:
                all_links.extend(self.links_scanner(html))
            else: #нет "next" или сработал ограничитель
                #собираем ссылки и возвращаем результаты
                all_links.extend(self.links_scanner(html))
                return all_links[0:max_links]
    
    def links_html_dict(self, max_html=50, max_search_page=5):
        '''
        Возвращает словарь из ссылок и их html-ей
        Может принимать ограничение количества возвращаемых html-ей и
        ограничение количества сканируемых страниц в поиске.
        '''
        links = self.get_links(max_search_page=max_search_page, max_links=max_html)
        l = [[link, urllib.urlopen(link).read()] for link in links]
        l=dict(l)
        return l
    
class AuthorityAnalyzer(HTMLcollector):
    def extract_text(self, html):
        '''
        Принимает html и возвращает текст страницы
        '''
        soup = BeautifulSoup(html)
        #удаляем теги "style" и "script" и их содержимое
        for_del = soup("style")
        for_del.extend(soup("script"))
        [tag.decompose() for tag in for_del]
        #извлекаем текст из html
        text = soup.get_text()
        return text
    
    def number_of_words(self, voc):
        '''
        Возвращает количество слов в статье
        '''
        n = sum(voc.values())
        return n
    
    def vocabulary(self, text):
        '''
        Принимает текст и возвращает словарь из слов и количества их повторений 
        '''
        words = {}
        garb = '\t\n\x0b\x0c\r !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~0123456789"\''
        for word in text.lower().split():
            word = word.strip(garb)
            if len(word) > 2:
                words[word] = words.get(word, 0) + 1
        
        return words
    
    def terms(self, voc):
        '''
        Возвращает количество терминов в статье
        или сами термины (это лучше)
        '''
        pass
    
    def names(self, voc):
        '''
        Возвращает количество имен в статье
        '''
        pass
    
    def ranks(self, voc):
        '''
        Возвращает количество званий/рангов в статье
        '''
        pass
    
    def places(self, voc):
        '''
        Возвращает количество мест в статье
        '''
        pass
    
    def time(self, voc):
        '''
        Возвращает количество упоминаний времени в статье
        '''
        pass
    
    def statistics(self, text):
        '''
        Возвращает количество символов "%" в статье
        '''
        perc = text.count('%')
        return perc

if __name__ == '__main__':
    def create_file_html():
        a=HTMLcollector('храм')
        f=open('/Users/vladymyr/Desktop/htmlsites.txt','w')
        for i in a.links_html_dict(max_html=3):
            f.write(i)
        f.close()
        print 'done'
    create_file_html()