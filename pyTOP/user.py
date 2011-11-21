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

class Location(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Location, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['zip','address','city','state','country','district']
    

class UserCredit(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(UserCredit, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['level','score','total_num','good_num']
    

class User(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(User, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'buyer_credit':UserCredit, 'seller_credit':UserCredit, 'location':Location, 'created':TOPDate, 'last_visit':TOPDate, 'birthday':TOPDate}
        self.fields = ['user_id','uid','nick','sex','buyer_credit','seller_credit','location','created','last_visit','birthday','type','has_more_pic','item_img_num','item_img_size','prop_img_num','prop_img_size','auto_repost','promoted_type','status','alipay_bind','consumer_protection','alipay_account','alipay_no','avatar','liangpin','sign_food_seller_promise','has_shop','is_lightning_consignment','has_sub_stock','vip_info','email','magazine_subscribe','vertical_market','online_gaming']
        
    def get(self, nick='', fields=[], session=None):
        '''taobao.user.get 获取单个用户信息
        *在传入session的情况下,可以不传nick，表示取当前用户信息；否则nick必须传.
        自用型应用不需要传入nick'''
        request = TOPRequest('taobao.user.get')
        request['nick'] = nick
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request, session)['user'])
        return self
    
    def login(self, app_user_nick=None, target=None):
        systime = SysTime()
        params = {
            'app_key' : self.API_KEY,
            'timestamp'  : systime.get(),
            'sign_method' : self.SIGN_METHOD,
        }
        if app_user_nick!=None: params['app_user_nick'] = app_user_nick
        if target!=None: params['target'] = target
        src = self.APP_SECRET + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())])
        params['sign'] = md5(src).hexdigest()
        form_data = urllib.urlencode(params)
        rsp = requests.get('%s?%s'%(self.LOGIN_URL, form_data))
        print rsp.url
    
    def validate_session(self, session_ts):
        now = time()
        ts = session_ts / 1000;
        if ts > ( now + 60 * 10 ) or now > ( ts + 60 * 30 ):
            return False
        return True
        
    def refresh_session(self, sessionkey, refresh_token=None):
        if not refresh_token:
            refresh_token = sessionkey
        params = {
            'appkey' : self.API_KEY,
            'sessionkey'  : sessionkey,
            'refresh_token': refresh_token
        }
        src = ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())]) + self.PRODUCT_APP_SECRET
        params['sign'] = md5(src).hexdigest().upper()
        form_data = urllib.urlencode(params)
        rsp = requests.get('%s?%s'%(self.REFRESH_TOKEN_URL, form_data))
        rsp = json.loads(rsp.content)
        if 'error' in rsp:
            raise TOPException(rsp['error'], rsp['error_description'])
            return None
        rsp['re_expires_in'] = int(rsp['re_expires_in'])
        rsp['expires_in'] = int(rsp['expires_in'])
        return rsp
    

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
    
