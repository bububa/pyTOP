#!/usr/bin/env python
# encoding: utf-8
"""
sellercenter.py

Created by 徐 光硕 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class SubUserInfo(TOP):
    '''子账号基本信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(SubUserInfo, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['nick','seller_id','seller_nick','status','is_online','full_name','sub_id']
    

class SubUsers(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(SubUsers, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'subusers':SubUserInfo}
        self.fields = ['subusers',]
    
    def get(self, nick, session):
        '''taobao.sellercenter.subusers.get 查询指定账户的子账号列表
        
        根据主账号nick查询该账号下所有的子账号列表，只能查询属于自己的账号信息 (主账号以及所属子账号)'''
        request = TOPRequest('taobao.sellercenter.subusers.get')
        request['nick'] = nick
        self.create(self.execute(request, session))
        return self.subusers


