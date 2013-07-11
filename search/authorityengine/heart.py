# -*- coding: utf-8 -*-

import urllib
import time
from bs4 import BeautifulSoup
from ..models import Terms, Names, Cities, Units, Links

class LinksCollector(object):
    
    def __init__(self, user_request):
        self.user_request = user_request
        
    def search_html(self, page):
        '''html of bing.com with results
            
            Attribute:
                page - Number of results page
            
            return html string
        '''
        bing = 'http://www.bing.com/search?'
        request = 'q=' + self.user_request
        first = '&first=' + str(((page-1)*10)+1)
        
        search_url = bing + request + first
        search_page = urllib.urlopen(search_url.encode('utf-8')).read()
        return search_page
    
    def links_scanner(self, html):
        '''Colects links from search html
            
            Attribute:
                html - Html of search
            
            return list of links from html
        '''
        soup = BeautifulSoup(html)
        links = [a.a['href'] for a in soup.find_all('h3')]
        return links
    
    def is_next_button(self, html):
        '''Checking for the "next" button
            
            Attribute:
                html - Html of search
            
            return True if there is a button in html and False if there isn't
        '''
        soup = BeautifulSoup(html)
        return True if soup.select(".sb_pagN") else False
    
    def get_links(self, max_search_page=50, max_links=50):
        '''Solo function to get links
            
            Attribute (not required):
                max_links - limiting the number of returned links
                max_search_page - limiting
                                the number of search pages to be scanned
            
            return list of links
        '''
        all_links = []
        for p in range(1, max_search_page+1): # Leafs through search pages
            html = self.search_html(page=p) # Gets html
            
            # If there is the "next" button
            # and page/numbers of links are in permissible range
            if (self.is_next_button(html=html) and p < max_search_page
                                        and len(all_links) < max_links):
                all_links.extend(self.links_scanner(html))
            else:
                all_links.extend(self.links_scanner(html))
                return all_links[:max_links]


class HTMLcollector(LinksCollector):
    
    def no_links_in_db(self,links):
        '''Links which are not in the database
            
            Attribute:
                links - links to check in db
            
            return list of links which are not in the database
        '''
        no_links = []
        for link in links:
            try: Links.objects.get(link=link)
            except Links.DoesNotExist: no_links.append(link)
        return no_links
    
    def links_html_dict(self, all_links):
        '''Links with html
            
            Attribute:
                all_links - links to check in db and
                                            if there isn't link
                                            get its html
            return dictionary like this {'link':'html',...}
        '''
        links = self.no_links_in_db(all_links)
        l = [[link, urllib.urlopen(link).read()] for link in links]
        l = dict(l)
        return l


class CollectionCharacteristics(HTMLcollector):
    
    def extract_title(self, html):
        """Title
            
            Attribute:
                html - html of the page
            
            return string with title
        """
        try:
            soup = BeautifulSoup(html)
            title = soup.html.head.title.string
        except: title="Error"
        return title
    
    def extract_text(self, html):
        '''Get text from html
            
            Attribute:
                html - html of the page
            
            return text from html
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
        '''Words and the number of repeats
            
            Attribute:
                text - the text to be scanned
            
            return dictionary like this {'someword1':12,'someword2':3}
        '''
        words = {}
        garb = '\t\n\x0b\x0c\r !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~0123456789"\''
        
        for word in text.lower().split():
            word = word.strip(garb)
            #if len(word) > 2:
            words[word] = words.get(word, 0) + 1
        return words
    
    def percent(self, text):
        '''Count percent in text
            
            Attribute:
                text - the text to be scanned
            
            return dictionary like this {'percent':number}
        '''
        p = text.count('%')
        perc = {'sum_percent':p}
        return perc
    
    def sum_of_words(self, dic):
        '''The number of words
            
            Attribute:
                dic - the dictionary of words and their repeats
                        example: {'word1':12, 'word2':3}
                
            return dictionary like this {'number_of_words':number}
        '''
        n = {'sum_words':sum(dic.values())}
        return n
    
    def if_term(self, word):
        '''If the word is term
            
            Attribute:
                word - the word to check
            
            return True if word is term else False
        '''
        try:
            Terms.objects.get(term=word)
            return True
        except Terms.MultipleObjectsReturned: return True
        except Terms.DoesNotExist: return False
    
    def if_name(self, word):
        '''If the word is name
            
            Attribute:
                word - the word to check
            
            return True if word is name else False
        '''
        try:
            Names.objects.get(name=word)
            return True
        except Names.MultipleObjectsReturned: return True
        except Names.DoesNotExist: return False
    
    def if_city(self, word):
        '''If the word is city name
            
            Attribute:
                word - the word to check
            
            return True if word is city name else False
        '''
        try:
            Cities.objects.get(city=word)
            return True
        except Cities.MultipleObjectsReturned: return True
        except Cities.DoesNotExist: return False
    
    def if_unit(self, word):
        '''If the word is unit
            
            Attribute:
                word - the word to check
            
            return True if word is unit else False
        '''
        try:
            Units.objects.get(unit=word)
            return True
        except Units.MultipleObjectsReturned: return True
        except Units.DoesNotExist: return False
    
    def count_authoritative_words(self, dic):
        '''
            Attribute:
                dic - the dictionary of words and their repeats
                        example: {'someword1':12, 'someword2':3}
            
            return dictionary {
                    'sum_terms':number,
                    'sum_names':number,
                    'sum_cities':number,
                    'sum_units':number
                    }
        '''
        terms = 0
        names = 0
        units = 0
        cities = 0
        
        for word in dic:
            if self.if_term(word): terms += dic[word]
            elif self.if_name(word): names += dic[word]
            elif self.if_city(word): cities += dic[word]
            elif self.if_unit(word): units += dic[word]
        
        auth_words = {
                    'sum_terms':terms,
                    'sum_names':names,
                    'sum_cities':cities,
                    'sum_units':units
                    }
        return auth_words
    
    def authoritative_characteristics(self, html):
        '''
            Attribute:
                html - html of the page
            
            return dictionary {
                                'sum_terms':number,
                                'sum_names':number,
                                'sum_cities':number,
                                'sum_units':number,
                                'number_of_words':number
                                'sum_unique_words':number
                                'percent':number
                                'add_time':number
                                }
        '''
        text = self.extract_text(html)
        voc = self.vocabulary(text)
        
        charact = {}
        charact.update(self.count_authoritative_words(voc))
        charact.update(self.percent(text))
        charact.update(self.sum_of_words(voc))
        charact.update({'sum_unique_words':len(voc)})
        charact.update({'add_time':int(time.time())})
        #charact.update({'title':self.extract_title(html)})
        return charact
    
    def save_characteristics_to_db(self, link, dic):
        '''Function saves the link and its characteristics to db
            
            Attribute:
                link - the link to save in db
                dic - dictionary with characteristics of the link
        '''
        p = Links(
            link = link,
            add_time = dic['add_time'],
            sum_words = dic['sum_words'],
            sum_terms = dic['sum_terms'],
            sum_names = dic['sum_names'],
            sum_units = dic['sum_units'],
            sum_cities = dic['sum_cities'],
            sum_percent = dic['sum_percent'],
            sum_unique_words = dic['sum_unique_words'],
            )
        p.save()
    
    def get_characteristics_from_db(self, link):
        '''
            Attribute:
                link - the link to get its characteristics from db
            
            return dictionary of characteristics from db
        '''
        return Links.objects.values().get(link=link)


class AuthorityCalculation(CollectionCharacteristics):
    
    def scores_imp_char(self, dic):
        '''Scores for important characteristics
            
            Attribute:
                dic - the dictionary with characteristics
                    required data in dictionary:
                    "sum_terms, sum_names, sum_units, sum_cities, sum_percent"
            
            return integer of scores
        '''
        sum_terms = dic['sum_terms']
        sum_names = dic['sum_names']
        sum_units = dic['sum_units']
        sum_cities = dic['sum_cities']
        sum_percent = dic['sum_percent']
        
        scores = sum_terms + sum_names + sum_units + sum_cities + sum_percent
        return scores
    
    def scores_average_char(self,dic):
        '''Scores for average characteristics
            
            Attribute:
                dic - the dictionary with characteristics
                    required data in dictionary: "sum_words, sum_unique_words"
            
            return integer of scores
        '''
        sum_words = dic['sum_words']
        sum_unique_words = dic['sum_unique_words']
        concentration = float(sum_words) / float(sum_unique_words)
        
        scores = concentration
        return scores
    
    def total_authority_scores(self, dic):
        '''Total sum of scores
            
            Attribute:
                dic - the dictionary with characteristics
                    required data in dictionary:
                        "sum_terms, sum_names, sum_units, sum_cities,
                        sum_percent, sum_words, sum_unique_words"
            
            return integer of scores
        '''
        imp_scores = self.scores_imp_char(dic)
        #avr_scores = self.scores_avr_char(dic)
        
        total_scores = imp_scores #+ avr_scores
        return total_scores


class AuthoritativeResults(AuthorityCalculation):
    
    def set_place(self, dic):
        '''
            Attribute:
                dic - the dictionary like this {link:(scores, characteristics)}
            
            return list like this [(link,(scores,{characteristics})), (...]
                            where the first element has the highest scores
                                                        and then descending
        '''
        return sorted(dic.items(), key=lambda x:x[1][0], reverse=True)
    
    def get_results(self, max_links=50):
        '''Solo function to get links with data which sorted by scores
            
            Attribute (not required):
                max_links - limiting the number of returned links
            
            return list like this
                    [
                    {'link':, 'sum_units':, 'sum_cities':, 'sum_terms':,
                    'sum_words':, 'id':, 'scores':, 'add_time':,
                    'sum_percent':, 'sum_names':, 'sum_unique_words':},
                    {...
                    ]
                    where the first element has the highest scores
                                                        and then descending
        '''
        # Collect all links on request
        all_links = self.get_links(max_links=max_links)
        
        # Get a dictionary of references and html that are not in the database
        links_html_dic = self.links_html_dict(all_links)
        
        for link in links_html_dic:
            # Get characteristics
            char_dic = self.authoritative_characteristics(links_html_dic[link])
            
            # Save characteristics to database
            self.save_characteristics_to_db(link=link, dic=char_dic)
        
        # Get all links with characteristics from database
        link_score = {}
        
        for link in all_links:
            char_dic = self.get_characteristics_from_db(link)
            
            # Gives scores by characteristics
            scores = self.total_authority_scores(char_dic)
            
            # Adds 'scores' to the dictionary of characteristics
            char_dic.update({'scores':scores})
            link_score.update({link:(scores, char_dic)})
        
        # Gets the list sorted by scores
        scores_list = self.set_place(link_score)
        
        # Generates the list of dictionaries with characteristics
        scores_dic_list = [d[1][1] for d in scores_list]
        return scores_dic_list