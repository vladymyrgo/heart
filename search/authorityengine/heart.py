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
    
    def get_links(self, max_search_page=50, max_links=3):
        '''
            Самостоятельная функция.
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
    
    def links_html_dict(self, all_links):
        '''
            Принимает список ссылок.
            Возвращает словарь из ссылок(которых нет в БД) и их html-ей.
        '''
        links = self.no_links_in_db(all_links)
        l = [[link, urllib.urlopen(link).read()] for link in links]
        l = dict(l)
        return l


class CollectionCharacteristics(HTMLcollector):
    
    def extract_text(self, html):
        '''
            Принимает html и возвращает текст страницы.
        '''
        try:
            soup = BeautifulSoup(html)
            for_del = soup("style")
            for_del.extend(soup("script"))
            [tag.decompose() for tag in for_del]
            text = soup.get_text()
        except: text=''
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
        n = {'sum_words':sum(dic.values())}
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
        terms=0
        names=0
        cities=0
        units=0
        for word in dic:
            if self.if_term(word) is True: terms += dic[word]
            elif self.if_name(word) is True: names += dic[word]
            elif self.if_city(word) is True: cities += dic[word]
            elif self.if_unit(word) is True: units += dic[word]
        auth_words = {
                    'sum_terms':terms, 'sum_names':names,
                    'sum_cities':cities, 'sum_units':units
                    }
        return auth_words
    
    def authoritative_characteristics(self, html):
        '''
            Принимает html сайта.
            Возвращает словарь:характеристика, ее количество.
        '''
        charact={}
        text = self.extract_text(html)
        voc = self.vocabulary(text)
        charact.update(self.count_authoritative_words(voc)) # Авторитетные слова
        charact.update(self.percent(text))# Проценты
        charact.update(self.sum_of_words(voc)) # Количество слов
        charact.update({'sum_unique_words':len(voc)}) # Количество уникальных слов
        charact.update({'add_time':int(time.time())}) # Время добавления в словарь (в БД)
        return charact
    
    def save_characteristics_to_db(self, link, dic):
        '''
            Принимает ссылку и словарь с ее характеристиками.
            Записывает принятые данные в БД
        '''
        add_time = dic['add_time']
        sum_words = dic['sum_words']
        sum_terms = dic['sum_terms']
        sum_names = dic['sum_names']
        sum_units = dic['sum_units']
        sum_cities = dic['sum_cities']
        sum_percent = dic['sum_percent']
        sum_unique_words = dic['sum_unique_words']
        p = Links(
            link=link,
            sum_words=sum_words,
            sum_unique_words=sum_unique_words,
            sum_terms=sum_terms,
            sum_names=sum_names,
            sum_units=sum_units,
            sum_cities=sum_cities,
            sum_percent=sum_percent,
            add_time=add_time
        )
        p.save()
    
    def get_characteristics_from_db(self, link):
        '''
            Принимает ссылку.
            Возвращает словарь характеристик ссылки из БД.
        '''
        return Links.objects.values().get(link=link)


class AuthorityCalculation(CollectionCharacteristics):
    
    def scores_imp_char(self, dic):
        '''
            Принимает словарь характеристик.
            Данные необходимые в словаре:
            "sum_terms, sum_names, sum_units, sum_cities, sum_percent".
            Начисляет баллы за важные характеристики сайта.
            Возвращает число набранных баллов.
        '''
        sum_terms = dic['sum_terms']
        sum_names = dic['sum_names']
        sum_units = dic['sum_units']
        sum_cities = dic['sum_cities']
        sum_percent = dic['sum_percent']
        scores = sum_terms + sum_names + sum_units + sum_cities + sum_percent
        return scores
    
    def scores_average_char(self,dic):
        '''
            Принимает словарь характеристик.
            Данные необходимые в словаре:
            "sum_words, sum_unique_words"
            Начисляет баллы за "средние" показатели.
            Возвращает число набранных баллов.
        '''
        sum_words = dic['sum_words']
        sum_unique_words = dic['sum_unique_words']
        concentration = float(sum_words) / float(sum_unique_words)
        scores = concentration # + надо подумать...
        return scores
    
    def total_authority_scores(self, dic):
        '''
            Принимает словарь с характеристиками сайта.
            Обьединяет все функции по вычислению баллов авторитета.
            Данные необходимые в словаре:
                "sum_terms, sum_names, sum_units, sum_cities, sum_percent,
                sum_words, sum_unique_words"
            Возвращает число баллов.
        '''
        imp_scores = self.scores_imp_char(dic)
        #avr_scores = self.scores_avr_char(dic)
        total_scores = imp_scores
        return total_scores


class AuthoritativeResult(AuthorityCalculation):
    
    def set_place(self, dic):
        '''
        Принимает словарь ссылка:баллы авторитетности
        Возвращает отсортированный список вида [('link',(scores,{характеристики})), (...],
        где первый элемент имеет найбольшее количество баллов и далее по убыванию.
        '''
        return sorted(dic.items(), key=lambda x:x[1][0], reverse=True)
    
    def gradation_authority(self,):
        '''
        Самостоятельная функция.
        Возвращает отсортированный списоквида [('link',(scores,{характеристики})), (...],
        где первый элемент имеет найбольшее количество баллов и далее по убыванию.
        '''
        all_links = self.get_links() # Собирает все ссылки по запросу
        links_html_dic = self.links_html_dict(all_links) # Получает cловарь ссылок и html которых нет в БД
        for link in links_html_dic:
            char_dic = self.authoritative_characteristics(links_html_dic[link])
            self.save_characteristics_to_db(link=link, dic=char_dic) # Сохраняет характеристики ссылок в БД
        # Собирает из БД все ссылки с характеристиками
        link_score={}
        for link in all_links:
            char_dic = self.get_characteristics_from_db(link)
            scores = self.total_authority_scores(char_dic) # Вычисляет по характеристикам авторитетность
            link_score.update({link:(scores, char_dic)})
        scores_list = self.set_place(link_score) # Получает отсортированный по баллам список
        return scores_list