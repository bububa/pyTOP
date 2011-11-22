#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by 徐 光硕 on 2011-11-14.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

try :  
    import json  
except ImportError :  
    import simplejson as json  
import urllib
import requests
from hashlib import md5
import base64
from api import TOP, TOPRequest, TOPDate
from systime import SysTime
import time
from BeautifulSoup import BeautifulSoup

class Location(TOP):
    '''用户地址'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Location, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['zip','address','city','state','country','district']
    

class UserCredit(TOP):
    '''用户信用'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(UserCredit, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['level','score','total_num','good_num']
    

class User(TOP):
    '''用户'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(User, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'buyer_credit':UserCredit, 'seller_credit':UserCredit, 'location':Location, 'created':TOPDate, 'last_visit':TOPDate, 'birthday':TOPDate}
        self.fields = ['user_id','uid','nick','sex','buyer_credit','seller_credit','location','created','last_visit','birthday','type','has_more_pic','item_img_num','item_img_size','prop_img_num','prop_img_size','auto_repost','promoted_type','status','alipay_bind','consumer_protection','alipay_account','alipay_no','avatar','liangpin','sign_food_seller_promise','has_shop','is_lightning_consignment','has_sub_stock','vip_info','email','magazine_subscribe','vertical_market','online_gaming']
        
    def get(self, nick='', fields=[], session=None):
        '''taobao.user.get 获取单个用户信息;
        
        在传入session的情况下,可以不传nick，表示取当前用户信息；否则nick必须传.
        自用型应用不需要传入nick'''
        request = TOPRequest('taobao.user.get')
        request['nick'] = nick
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request, session)['user'])
        return self
    
    def logout(self):
        systime = SysTime()
        params = {
            'app_key' : self.API_KEY,
            'timestamp'  : systime.get(),
            'sign_method' : self.SIGN_METHOD,
        }
        src = self.APP_SECRET + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())]) + self.APP_SECRET
        params['sign'] = md5(src).hexdigest().upper()
        form_data = urllib.urlencode(params)
        rsp = requests.get('%s?%s'%(self.LOGOUT_URL, form_data))
        if 'login.taobao.com' in rsp.url: return True
        return False
        
    def login(self, username='', passwd='', app_user_nick=None, target=None, use_taobaoid=False):
        if use_taobaoid:
            systime = SysTime()
            params = {
                'app_key' : self.API_KEY,
                'timestamp'  : systime.get(),
                'sign_method' : self.SIGN_METHOD,
            }
            if app_user_nick!=None: params['app_user_nick'] = app_user_nick
            if target!=None: params['target'] = target
            src = self.APP_SECRET + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())]) + self.APP_SECRET
            params['sign'] = md5(src).hexdigest().upper()
            form_data = urllib.urlencode(params)
            rsp = requests.get('%s?%s'%(self.TaobaoID_URL, form_data))
            print rsp.content
        else:
            rsp = requests.get('%s%s'%(self.LOGIN_URL, self.API_KEY))
            soup = BeautifulSoup(rsp.content)
            iframe_src = soup.find('iframe')['src']
            rsp = requests.get(iframe_src)
            print rsp.url
            #s = requests.session()
            login_url = 'https://login.taobao.com/member/login.jhtml'
            soup = BeautifulSoup(rsp.content)
            login_url = soup.find('form')['action']
            #inputs = soup.findAll('input')
            forms = self.extract_form_fields(soup)
            forms['TPL_username'] = username
            forms['TPL_password'] = passwd
            rsp = requests.post(login_url, data=forms)
            print rsp.url
            print rsp.content
    
    def validate_session(self, session_ts):
        '''
        检查Session是否过期, 验证Session可用性
        '''
        now = time()
        ts = session_ts / 1000;
        if ts > ( now + 60 * 10 ) or now > ( ts + 60 * 30 ):
            return False
        return True
        
    def refresh_session(self, sessionkey, refresh_token=None):
        '''
        Refresh Session Token
        '''
        if not refresh_token:
            refresh_token = sessionkey
        params = {
            'appkey' : self.API_KEY,
            'sessionkey'  : sessionkey,
            'refresh_token': refresh_token
        }
        src = ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())]) + self.APP_SECRET
        params['sign'] = md5(src).hexdigest().upper()
        form_data = urllib.urlencode(params)
        rsp = requests.get('%s?%s'%(self.REFRESH_TOKEN_URL, form_data))
        rsp = json.loads(rsp.content)
        if 'error' in rsp:
            raise TOPException(rsp['error'], rsp['error_description'])
            return None
        rsp['re_expires_in'] = int(rsp['re_expires_in'])
        rsp['expires_in'] = int(rsp['expires_in'])
        rsp['session'] = rsp['top_session']
        del rsp['top_session']
        return rsp
    
    def extract_form_fields(self, soup):
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
    

class Users(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Users, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'users':User}
        self.fields = ['users']
    
    def get(self, nicks=[], fields=[]):
        '''taobao.users.get 获取多个用户信息'''
        request = TOPRequest('taobao.users.get')
        request['nicks'] = ','.join(nicks)
        if not fields:
            user = User()
            fields = user.fields
        request['fields'] = ','.join(fields)
        self.create(self.execute(request))
        return self.users
    
