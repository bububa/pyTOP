#!/usr/bin/env python
# encoding: utf-8
"""
test_crawler.py

Created by 徐 光硕 on 2011-11-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from pyTOP.crawler import Crawler
from pyTOP.user import User
from pyTOP.insight import TopLevelCats, WordsBase, WordsAnalysis
from pyTOP.item import Items
from pprint import pprint
import requests
import urllib, re
from BeautifulSoup import BeautifulSoup

top_session = '4020831d426896a5328c50f8117b920fb78579dYCThsHyd6517981601'

def extract_form_fields(soup):
    fields = {}
    for input in soup.findAll('input'):
        # ignore submit/image with no name attribute
        if input['type'] in ('submit', 'image') and not input.has_key('name'):
            continue
        
        # single element nome/value fields
        if input['type'] in ('text', 'hidden', 'password', 'submit', 'image'):
            value = ''
            if input.has_key('value'):
                value = input['value']
            fields[input['name']] = value
            continue
        
        # checkboxes and radios
        if input['type'] in ('checkbox', 'radio'):
            value = ''
            if input.has_key('checked'):
                if input.has_key('value'):
                    value = input['value']
                else:
                    value = 'on'
            if 'name' in input and fields.has_key(input['name']) and value:
                fields[input['name']] = value
            
            if 'name' in input and not fields.has_key(input['name']):
                fields[input['name']] = value
            
            continue
        
        assert False, 'input type %s not supported' % input['type']
    
    # textareas
    for textarea in soup.findAll('textarea'):
        fields[textarea['name']] = textarea.string or ''
    
    # select fields
    for select in soup.findAll('select'):
        value = ''
        options = select.findAll('option')
        is_multiple = select.has_key('multiple')
        selected_options = [
            option for option in options
            if option.has_key('selected')
        ]
        
        # If no select options, go with the first one
        if not selected_options and options:
            selected_options = [options[0]]
        
        if not is_multiple:
            assert(len(selected_options) < 2)
            if len(selected_options) == 1:
                value = selected_options[0]['value']
        else:
            value = [option['value'] for option in selected_options]
        
        fields[select['name']] = value
    
    return fields

def get_cats():
    crawler = Crawler()
    cats = crawler.get_cats()
    crawler.save_cats(cats)

def get_top_keywords():
    crawler = Crawler()
    crawler.get_top_keywords()

def get_sug():
    crawler = Crawler()
    crawler.sug('儿童卫衣 男')

def get_user():
    user = User()
    print user.get('北京喜宝')
    items = Items()
    print items.onsale_get(top_session)
    return
    tlc = TopLevelCats()
    print tlc.get(top_session)

def adwords_login():
    s = requests.session()
    login_url = 'https://login.taobao.com/member/login.jhtml'
    r = s.get(login_url)
    soup = BeautifulSoup(r.content)
    #pprint(r.cookies)
    forms = extract_form_fields(soup.find('form', id='J_StaticForm'))
    forms['TPL_username'] = u'喜宝_03'.encode('gbk')
    forms['TPL_password'] = 'uwUe3tlToXtZgO6Y'
    #forms['_tb_token_'] = 'L3T8QONzL1/PqT8QON0M1/mga8QON4M1/Niw9QONCQ1/YM3AQONJQ1/9fZWUON8f3/QFbWUONAf3/qyfWUONEf3'
    #forms['umto'] = 'T7f5c7eb9e08c689752f741e81dcbe2c5,'
    #forms['gvfdcre'] = '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F67696E2E6A68746D6C'
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Content-Type':'application/x-www-form-urlencoded',
    'Origin':'https://login.taobao.com',
    'Referer':'https://login.taobao.com/member/login.jhtml',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.53.11 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'}
    r = s.post(login_url, data=forms, headers=headers)
    print r.status_code
    pprint(r.request.data)
    pprint(r.headers)
    pprint(r.cookies)
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-cn',
    'Origin':'https://login.taobao.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.53.11 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'}
    if 'location' in r.headers:
        r = s.get(r.headers['location'], headers=headers)
        pprint(r.headers)
    else:
        m = re.findall(r'window\.location = "([^^]*?)";', r.text)
        if m:
            r = s.get(m[0], headers=headers)
            print r.url
            
    r = s.get('http://subway.simba.taobao.com/login.htm?outSideKey=taobao', headers=headers)
    print r.content
    #print r.status_code
    #print r.cookies
    
def main():
    #get_cats()
    #get_top_keywords()
    #get_sug()
    #get_user()
    adwords_login()


if __name__ == '__main__':
    main()

