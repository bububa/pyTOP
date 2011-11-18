#!/usr/bin/env python
# encoding: utf-8
"""
user.py

Created by 徐 光硕 on 2011-11-14.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class Location(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(Location, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['zip','address','city','state','country','district']
    

class UserCredit(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(UserCredit, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['level','score','total_num','good_num']
    

class User(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
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
    

class Users(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
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
    
