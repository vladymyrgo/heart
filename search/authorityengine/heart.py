# coding:utf-8
import urllib
import time
from bs4 import BeautifulSoup
from ..models import Terms, Names, Cities, Units, Links

class LinksCollector(object):
    
    def __init__(self, user_request):
        self.user_request = user_request
        
    def search_html(self, page):
        '''
        Принимает номер страницы для поиска и возвращает html поиска.
        '''
        bing='http://www.bing.com/search?'
        request = 'q=' + self.user_request
        first = '&first=' + str(((page-1)*10)+1)
        search_url = bing + request + first
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
    
    def get_links(self, max_search_page=50, max_links=50):
        '''
        Возвращает список ссылок поиска на сайты.
        Может принимать ограничение 'max_page' по количеству сканируемых
        страниц поиска и ограничение max_links по количеству возвращаемых
        ссылок.
        '''
        all_links=[]
        for p in range(1, max_search_page+1): # листаем станицы поиска
            # открываем html поиска функцией search_html()
            html = self.search_html(page=p)
            #Если есть кнопка 'Next', и не срабатывают ограничители
            #то собираем ссылки и идем на след. стр.
            if (self.is_next_button(html=html) and p < max_search_page
                and len(all_links) < max_links):
                all_links.extend(self.links_scanner(html))
            else: #нет "next" или сработал ограничитель
                #собираем ссылки и возвращаем результаты
                all_links.extend(self.links_scanner(html))
                return all_links[:max_links]


class HTMLcollector(LinksCollector):
    
    
    def no_links_in_db(self,links):
        '''
        Принимает список ссылок и проверяет их наличие в БД.
        Возвращает список ссылок которых нет в БД.
        '''
        no_links=[]
        for link in links:
            try: Links.objects.get(link=link)
            except Links.DoesNotExist: no_links.append(link)
        return no_links
    
    def links_html_dict(self, max_html=50, max_search_page=50):
        '''
        Возвращает словарь из ссылок(которых нет в БД) и их html-ей.
        Может принимать ограничение количества возвращаемых html-ей и
        ограничение количества сканируемых страниц в поиске.
        '''
        all_links = self.get_links(max_search_page=max_search_page,
                               max_links=max_html)
        links = no_links_in_db(all_links)
        l = [[link, urllib.urlopen(link).read()] for link in links]
        l = dict(l)
        return l


class AuthorityAnalyzer(HTMLcollector):
    
    def extract_text(self, html):
        '''
        Принимает html и возвращает текст страницы.
        '''
        soup = BeautifulSoup(html)
        for_del = soup("style")
        for_del.extend(soup("script"))
        [tag.decompose() for tag in for_del]
        text = soup.get_text()
        return text
    
    def vocabulary(self, text):
        '''
        Принимает текст.
        Возвращает словарь из слов и количества их повторений.
        '''
        words={}
        garb = '\t\n\x0b\x0c\r !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~0123456789"\''
        for word in text.lower().split():
            word = word.strip(garb)
            #if len(word) > 2:
            words[word] = words.get(word, 0) + 1
        return words
    
    def percent(self, text):
        '''
        Принимает текст.
        Возвращает словарь "percent":количество символов "%" в тексте.
        '''
        p = text.count('%')
        perc = {'sum_percent':p}
        return perc
    
    def sum_of_words(self, dic):
        '''
        Принимает словарь из слов и количества их повторений.
        Возвращает словарь из "number_of_words": количество слов в статье.
        '''
        n = {'sum_of_words':sum(dic.values())}
        return n
    
    def if_term(self, word):
        '''
        Принимает слово.
        Возвращает 'True' если слово найдено в словаре терминов.
        '''
        try:
            Terms.objects.get(term=word)
            return True
        except Terms.MultipleObjectsReturned: return True
        except Terms.DoesNotExist: return False
    
    def if_name(self, word):
        '''
        Принимает слово.
        Возвращает 'True' если слово найдено в словаре имен.
        '''
        try:
            Names.objects.get(name=word)
            return True
        except Names.MultipleObjectsReturned: return True
        except Names.DoesNotExist: return False
    
    def if_city(self, word):
        '''
        Принимает слово.
        Возвращает 'True' если слово найдено в словаре городов.
        '''
        try:
            Cities.objects.get(city=word)
            return True
        except Cities.MultipleObjectsReturned: return True
        except Cities.DoesNotExist: return False
    
    def if_unit(self, word):
        '''
        Принимает слово.
        Возвращает 'True' если слово найдено в словаре величин.
        '''
        try:
            Units.objects.get(unit=word)
            return True
        except Units.MultipleObjectsReturned: return True
        except Units.DoesNotExist: return False
    
    def count_authoritative_words(self, dic):
        '''
        Принимает словарь из слов и количества их повторений.
        Возвращает словарь с количеством терминов, имен, городов, величин.
        '''
        terms =0
        names =0
        cities=0
        units =0
        for word in dic:
            if self.if_term(word) is True: terms += dic[word]
            elif self.if_name(word) is True: names += dic[word]
            elif self.if_city(word) is True: cities += dic[word]
            elif self.if_unit(word) is True: units += dic[word]
        auth_words = {'sum_terms':terms, 'sum_names':names, 'sum_cities':cities, 'sum_units':units}
        return auth_words
    
    def authoritative_characteristics(self, html):
        '''
        Получает html сайта.
        Возвращает словарь:характеристика, ее количество.
        '''
        charact={}
        text = self.extract_text(html)
        voc = self.vocabulary(text)
        charact.update(self.count_authoritative_words(voc)) # Авторитетные слова
        charact.update(self.percent(text))# Проценты
        charact.update(self.sum_of_words(voc)) # Количество слов
        charact.update({'sum_unique_words':len(voc)}) # Количество уникальных слов
        return charact
    
    def save_characteristics_to_db(self, link, dic):
        '''
        Принимает ссылку и словарь с ее характеристиками.
        Записывает принятые данные в БД
        '''
        sum_words =        dic['sum_words']
        sum_unique_words = dic['sum_unique_words']
        sum_terms =        dic['sum_terms']
        sum_names =        dic['sum_names']
        sum_units =        dic['sum_units']
        sum_cities =       dic['sum_cities']
        sum_percent =      dic['sum_percent']
        p = Links(
            link=link,
            sum_words=sum_words,
            sum_unique_words=sum_unique_words,
            sum_terms=sum_terms,
            sum_names=sum_names,
            sum_units=sum_units,
            sum_cities=sum_cities,
            sum_percent=sum_percent,
            add_time = int(time.time())
            #Еще нужно записывать время записи в БД
        )
        p.save()
        pass
    
    
    
     #Листает словарь ссылка-html.
     #Получает характеристики сайта функцией authoritative_characteristics()
    
    #def листать найденные html и передавать их для вычисления авторитета
    #def вычисление баллов сайта
    #def запись характеристик сайта в БД с датой их занесения
    #def проверка сайта в БД, чтоб не парсить одни и теже сайты
    
if __name__ == '__main__':
    pass