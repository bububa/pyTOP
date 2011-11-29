#!/usr/bin/env python
# encoding: utf-8
"""
crawler.py

Created by 徐 光硕 on 2011-11-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import requests
from requests import Response, RequestException
import random
import re
import time
try :  
    import json  
except ImportError:  
    import simplejson as json
from BeautifulSoup import BeautifulSoup
#from pprint import pprint
from urlparse import urlparse
from utils import ThreadPool

class SearchResults:
    '''Search Results Object'''
    def __init__(self, q, total, lists, malls, ads, cats, keywords):
        self.q = q
        self.total = total
        self.lists = lists
        self.malls = malls
        self.ads = ads
        self.cats = cats
        self.keywords = keywords
    
    def __str__(self):
        return "<%s: q=%s, total=%d, lists=%d, malls=%s, ads=%d, cats=%d, keywords=%d>" %(self.__class__.__name__, self.q, self.total, len(self.lists), len(self.malls), len(self.ads), len(self.cats), len(self.keywords))
    
    __repr__ = __str__

class Cat:
    '''The category object in search results'''
    def __init__(self, id, url, title, amount):
        self.id = id
        self.url = url
        self.title = title
        self.amount = amount
    
    def __str__(self):
        return "<%s: id=%d, title=%s, amount=%d>" %(self.__class__.__name__, self.id, self.title, self.amount)
    
    __repr__ = __str__

class Item:
    '''The item object in search results'''
    def __init__(self, id, summary, photo, attrs, legends=None):
        self.id = id
        self.photo = photo
        self.summary = summary
        self.attrs = attrs
        self.legends = legends
    
    def __str__(self):
        if self.legends:
            lgs = ','.join(self.legends)
        lgs = None
        return "<%s: id=%d, summary=%s, img=%s, attrs=%s, legends=%s>" %(self.__class__.__name__, self.id, self.summary, self.photo, self.attrs, lgs)
    
    __repr__ = __str__

class ItemAttr:
    '''The item's attributs object in search results'''
    def __init__(self, price, transaction, shipment_fee=None, location=None, seller=None, seller_id=None):
        self.price = price
        self.transaction = transaction
        self.shipment_fee = shipment_fee
        self.seller = seller
        self.seller_id = seller_id
        self.location = location
    
    def __str__(self):
        return "<%s: price=%.2f, transaction=%d, shipment_fee=%.2f, location=%s, seller=%s, seller_id=%d>" %(self.__class__.__name__, self.price, self.transaction, self.shipment_fee, self.location, self.seller, self.seller_id)
    
    __repr__ = __str__

class Ad:
    '''The advertisement object in search results'''
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            k = k.lower().encode('utf-8')
            v = v.encode('utf-8') if type(v) == unicode else v
            if k in ('resourceid', 'sell', 'grade', ):
                v = int(v)
            elif k in ('isglobal', 'ishk', 'ismall', 'isprepay'):
                v = True if v=='1' else False
            elif not v:
                v = None
            setattr(self, k, v)
    
    def __str__(self):
        return "<%s: id=%d, title=%s, price=%s, wangwangid=%s>"%(self.__class__.__name__, self.resourceid, self.title, self.goodsprice, self.wangwangid)
    
    __repr__ = __str__

class Crawler:
    '''General Crawler for Taobao Site.'''
    def __init__(self, proxies=[]):
        self.proxies = proxies
        self.search_url = 'http://s.taobao.com/search'
    
    def search(self, keyword):
        '''Get search results for a specific keyword'''
        if type(keyword) != unicode: q = keyword.decode('utf-8')
        req = self.fetch(self.search_url, {'q':q.encode('gbk')})
        if not req: return None
        html = req.content.decode('gbk').encode('utf-8')
        soup = BeautifulSoup(html)
        cats = self.cats_parser(soup)
        keywords = self.keywords_parser(soup)
        mall_items = self.mall_items_parser(soup)
        total = int(soup.find('div', attrs={'class':'user-easy'}).find('a').string)
        lists = self.lists_parser(soup)
        ads = self.ads_parser(soup)
        return SearchResults(keyword, total, lists, mall_items, ads, cats, keywords)
    
    def cats_parser(self, soup):
        return [Cat(int(re.findall('cat\=(\d+)', dd.a['href'])[0]), dd.a['href'], dd.a['title'].encode('utf-8'), int(dd.contents[1][1:-1])) for dd in soup.find('div', id='J_AllCates').findAll('dd')]
    
    def keywords_parser(self, soup):
        return [a.string.encode('utf-8') for a in soup.find('dl', attrs={'class':'related-search'}).findAll('a')]
    
    def mall_items_parser(self, soup):
        items = []
        for li in soup.find('div', id='J_mall').findAll('li', attrs={'class':'list-item'}):
            items.append(self.list_item_parser(li))
        return items
    
    def lists_parser(self, soup):
        items = []
        for li in soup.find('ul', attrs={'class':'list-view-enlarge-4pic with-shipment lazy-list-view'}).findAll('li', attrs={'class':'list-item'}):
            items.append(self.list_item_parser(li))
        return items
    
    def ads_parser(self, soup):
        items = []
        url = 'http:%s%d'%(re.findall(r'\'(//tmatch.simba.taobao.com/[^^]*?)\'', soup.find('div', 'col-main').script.string)[0], int(time.time()))
        req = self.fetch(url)
        items = [Ad(**item) for item in json.loads(re.findall(r'__p4p_sidebar__ \=(\[[^^]*?\])\n', req.content)[0])]
        return items
        
        print soup.findAll('ul', attrs={'class':'p4p-list'})
        for ul in soup.findAll('ul', attrs={'class':'p4p-list'}):
            for li in ul.findAll('li', attrs={'class':'item'}):
                items.append(self.item_parser(li))
        return items
    
    def item_parser(self, li):
        itemAttr = ItemAttr( float(li.find('div', attrs={'class':'price'}).strong.string), self.parse_float(li.find('div', attrs={'class':'transaction'}).string) )
        url = li.find('div', attrs={'class':'title'}).a['href']
        req = self.fetch(url)
        if req:
            item_id = (re.findall(r'id\=(\d+)', req.url)[0])
        else:
            item_id = None
        item = Item(item_id, li.find('div', attrs={'class':'title'}).a['title'], li.find('div', attrs={'class':'pic'}).img['src'], itemAttr)
        return item
        
    def list_item_parser(self, li):
        # parse attributes
        attrs = li.find('ul', attrs={'class':'attribute'})
        attr_price = attrs.find('li', attrs={'class':'price'})
        attr_shipment = attrs.find('li', attrs={'class':'shipment'})
        attr_seller = attrs.find('li', attrs={'class':'seller'})
        item_attr = ItemAttr( float(attr_price.em.string), int(re.findall('\d+', attr_price.span.string)[0]), self.parse_float(attr_shipment.find('span', attrs={'class':'fee'}).string), attr_shipment.find('span', attrs={'class':'loc'}).string.strip().encode('utf-8'), attr_seller.a.string.encode('utf-8'), int(re.findall('user_number_id\=(\d+)', attr_seller.a['href'])[0]) )
        # parse legends
        legends = li.find('div', attrs={'class':'legend2'})
        lgs = []
        for a in legends.findAll('a'):
            if 'class' in a and a['class'] == 'mall-icon': lgs.append('商城')
            elif a.string: lgs.append(a.string.encode('utf-8'))
        # parse summary
        desc_a = li.find('h3', attrs={'class':'summary'}).a
        try:
            desc_img = li.find('div', attrs={'class':re.compile(r".*\bphoto\b.*")}).find('img')['src'].encode('utf-8')
        except KeyError:
            desc_img = li.find('div', attrs={'class':re.compile(r".*\bphoto\b.*")}).find('img')['data-ks-lazyload'].encode('utf-8')
        item = Item(int(re.findall('id\=(\d+)', desc_a['href'])[0]), desc_a['title'].encode('utf-8'), desc_img, item_attr, lgs)
        return item
    
    def get_top_keywords(self, cats=None, parent=None, up=True):
        '''Get top keywords for all the categories'''
        if not cats: cats = self.get_cats()
        if not cats: return []
        threadPool = ThreadPool(len(cats) if len(cats)<=5 else 5)
        for cat in cats:
            threadPool.run(self.cat_top_keywords_thread, callback=None, cat=cat, parent=parent, up=up)
        cats = threadPool.killAllWorkers(None)
        return cats
    
    def cat_top_keywords_thread(self, cat, parent, up):
        if 'children' in cat and cat['children']:
            cat['children'] = self.get_top_keywords(cat['children'], cat['id'], up)
        if 'level' in cat:
            if cat['level'] == 2:
                cat['keywords'] = self.cat_top_keywords(cat['id'], '', up)
            elif cat['level'] == 3 and parent:
                cat['keywords'] = self.cat_top_keywords(parent, cat['level'], up)
        return cat
    
    def cat_top_keywords(self, cat, level3='', up=True,  offset=0, offsets=[]):
        '''Get top keywords in a specific category'''
        #print 'CAT:%s, level:%s'%(str(cat), str(level3))
        #print 'OFFSET: %d'%offset
        response = []
        if not offsets or offset==0: 
            url = 'http://top.taobao.com/level3.php?cat=%s&level3=%s&show=focus&up=%s&offset=%d'%(str(cat), str(level3), 'true' if up else '', offset)
            rs = self.fetch(url)
            if not rs: return response
            soup = BeautifulSoup(rs.content)
            response = self.parse_cat_top_keywords(soup, offset)
        if offset==0:
            offsets = self.get_cat_top_keywords_pages(soup, offset)
            #print 'OFFSETS: %s'%offsets
        if offsets:
            rs = []
            threadPool = ThreadPool(len(offsets) if len(offsets)<=5 else 5)
            for idx, page_offset in enumerate(offsets):
                page_url = 'http://top.taobao.com/level3.php?cat=%s&level3=%s&show=focus&up=%s&offset=%d'%(str(cat), str(level3), 'true' if up else '', page_offset)
                next_page = 'True' if idx == (len(offsets)-1) else 'False'
                threadPool.run(self.fetch, callback=None, url=page_url, config=dict(get_next=next_page, offset=page_offset))
            pages = threadPool.killAllWorkers(None)
            #print 'RESPONSES: %s'%pages
            for p in pages:
                if not p: continue
                soup2 = BeautifulSoup(p.content)
                offset2 = int(p.config['offset'])
                response += self.parse_cat_top_keywords(soup2, offset2)
                #print 'GOT: %d'%offset2
                if p.config['get_next'] != 'True': continue
                offsets = self.get_cat_top_keywords_pages(soup2, offset2)
                #print offsets
                if not offsets: continue
                response += self.cat_top_keywords(cat, level3, up, offset2, offsets)
        #return sorted(response, key=itemgetter('pos')) if response else []
        #print "RETURN:%d"%offset
        return response
    
    def get_cat_top_keywords_pages(self, soup, offset):
        aa = soup.find('div', attrs={'class':'pagination'}).findAll('a')
        if not aa: return []
        return [30*(int(a.string)-1) for idx, a in enumerate(aa) if a.string and 30*(int(a.string)-1)>offset]
            
    def parse_cat_top_keywords(self, soup, offset=0):
        if not soup: return []
        if type(soup) == Response: 
            soup = BeautifulSoup(soup.content)
            offset = soup.config['page_offset']
        ks = []
        for idx, tr in enumerate(soup.find('table', attrs={'class':'textlist'}).find('tbody').findAll('tr')):
            name = tr.td.find('span', attrs={'class':'title'}).a.string.encode('utf-8')
            focus = int(tr.td.find('span', attrs={'class':'focus'}).em.string)
            grows = tr.td.findAll('span', attrs={'class':'grow'})
            multi = -1 if 'down' in grows[0].i['class'] else 1
            grow_percent = int(grows[0].em.string[:-1]) * multi
            multi = -1 if 'down' in grows[1].i['class'] else 1
            grow_pos = int(re.findall('\d+', grows[1].em.string)[0]) * multi
            ks.append({'pos':idx+offset+1, 'name':name, 'focus':focus, 'grow_percent':grow_percent, 'grow_pos':grow_pos})
        return ks
    
    def get_cats(self):
        '''Get top keywords categories'''
        start_url = 'http://top.taobao.com/index.php?from=tbsy'
        rs = self.fetch(start_url)
        if not rs: return None
        soup = BeautifulSoup(rs.content)
        cats = [{'id':'TR_%s'%li['id'].encode('utf-8').upper(), 'title':li.a.text.encode('utf-8')} for li in soup.find('div', id='nav').findAll('li') if li['id']!='index']
        threadPool = ThreadPool(len(cats) if len(cats)<=5 else 5)
        for cat in cats:
            threadPool.run(self.get_cats_thread, callback=None, cat=cat)
        cats = threadPool.killAllWorkers(None)
        print 'got cats'
        return cats
    
    def get_cats_thread(self, cat):
        subcats = self.get_sub_cats('http://top.taobao.com/level2.php?cat=%s'%cat['id'], 'cat', 2)
        if len(subcats) == 1:
            cat['children'] = self.get_sub_cats_thread(subcats[0])
            return cat
        threadPool = ThreadPool(len(subcats) if len(subcats)<=5 else 5)
        for sc in subcats:
            threadPool.run(self.get_sub_cats_thread, callback=None, sc=sc)
        cat['children'] = threadPool.killAllWorkers(None)
        return cat
        
    def get_sub_cats_thread(self, sc):
        return {'id':sc['id'], 'title':sc['title'], 'children':self.get_sub_cats('http://top.taobao.com/level3.php?cat=%s'%sc['id'], 'level3', 3), 'level':sc['level']}
        
    def get_sub_cats(self, url, param, level):
        #print 'get_sub_cats:%s'%url
        rs = self.fetch(url)
        if not rs: return None
        cats = []
        soup = BeautifulSoup(rs.content)
        div = soup.find('div', id='categories')
        if not div: return None
        for dd in div.findAll('dd'):
            lc = dict([q.split('=') for q in urlparse(dd.a['href']).query.split('&')])[param]
            try:
                lc = int(lc)
            except ValueError:
                lc = lc.encode('utf-8')
            cats.append({'id':lc, 'title':dd.a.string.encode('utf-8'), 'level':level})
        return cats
    
    def fetch(self, url, params=None, method='get', config={}):
        proxy = None
        if self.proxies:
            proxy = {'http':random.choice(self.proxies)}
            retry = 5
        else:
            retry = 0
        while retry>=0:
            try:
                if method=='get':
                    req = requests.get(url, params=params, proxies = proxy, config=config)
                else:
                    req = requests.post(url, data=params, proxies=proxy, config=config)
                return req
            except RequestException:
                retry -= 1
                continue
        return None
        
    def parse_float(self, string):
        return float(re.findall(r'[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', string)[0])
    
