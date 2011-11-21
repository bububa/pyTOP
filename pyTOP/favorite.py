#!/usr/bin/env python
# encoding: utf-8
"""
favorite.py

Created by 徐 光硕 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class CollectItem(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''商品或店铺的信息'''
        super(CollectItem, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['item_owner_nick','item_numid','title']
    

class Favorite(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Favorite, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'search_list':CollectItem}
        self.fields = ['result','total_results', 'search_list']
    
    def add(self, item_numid, collect_type, shared, session):
        '''taobao.favorite.add 添加收藏夹
        ===================================
        根据用户昵称和收藏目标的数字id以及收藏目标的类型，实现收藏行为'''
        request = TOPRequest('taobao.favorite.add')
        request['item_numid'] = item_numid
        request['collect_type'] = collect_type
        request['shared'] = shared
        self.create(self.execute(request, session))
        return self.result
    
    def search(self, user_nick, collect_type, page_no, session=None):
        '''taobao.favorite.search 查询
        ===================================
        查询淘宝用户收藏的商品或店铺信息.(收藏有公开和未公开两种，不入参sessionkey的只能获得公开的收藏，而入参了sessionkey的能获得未公开的收藏。)'''
        request = TOPRequest('taobao.favorite.search')
        request['user_nick'] = user_nick
        request['collect_type'] = collect_type
        request['page_no'] = page_no
        self.create(self.execute(request, session))
        return self.result
    
