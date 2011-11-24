#!/usr/bin/env python
# encoding: utf-8
"""
systime.py

Created by 徐 光硕 on 2011-11-19.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest

class SysTime(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(SysTime, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['time']
    
    def get(self):
        '''taobao.time.get 获取前台展示的店铺类目
        
        获取淘宝系统当前时间'''
        request = TOPRequest('taobao.time.get')
        self.create(self.execute(request))
        return self.time
    


