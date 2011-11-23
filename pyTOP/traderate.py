#!/usr/bin/env python
# encoding: utf-8
"""
traderate.py

提供了评价的添加和查询功能

Created by 徐 光硕 on 2011-11-23.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class TradeRate(TOP):
    '''评价列表'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TradeRate, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate}
        self.fields = ['valid_score','tid','oid','role','nick','result','created','rated_nick','item_title','item_price','content','reply']
    
    def add(self, tid, result, role, session, oid=None, content=None, anony=None):
        '''taobao.traderate.add 新增单个评价
        
        新增单个评价(注：在评价之前需要对订单成功的时间进行判定（end_time）,如果超过15天，不能再通过该接口进行评价)'''
        request = TOPRequest('taobao.traderate.add')
        request['tid'] = tid
        request['result'] = result
        request['role'] = role
        if oid!=None: request['oid'] = oid
        if content!=None: request['content'] = content
        if anony!=None: request['anony'] = anony
        self.create(self.execute(request, session)['trade_rate'])
        return self
    
    def list_add(self, tid, result, role, session, oid=None, content=None, anony=None):
        '''taobao.traderate.list.add 针对父子订单新增批量评价
        
        针对父子订单新增批量评价(注：在评价之前需要对订单成功的时间进行判定（end_time）,如果超过15天，不用再通过该接口进行评价)'''
        request = TOPRequest('taobao.traderate.list.add')
        request['tid'] = tid
        request['result'] = result
        request['role'] = role
        if oid!=None: request['oid'] = oid
        if content!=None: request['content'] = content
        if anony!=None: request['anony'] = anony
        self.create(self.execute(request, session)['trade_rate'])
        return self
    

class TradeRates(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TradeRates, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'trade_rates':TradeRate}
        self.fields = ['trade_rates','total_results']
    
    def get(self, rate_type, role, session, fields=[], **kwargs):
        '''taobao.traderates.get 搜索评价信息
        
        搜索评价信息，只能获取距今180天内的评价记录'''
        request = TOPRequest('taobao.traderates.get')
        request['rate_type'] = rate_type
        request['role'] = role
        if not fields:
            tradeRate = TradeRate()
            fields = tradeRate.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('result', 'page_no', 'page_size', 'start_date', 'end_date', 'tid') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.trade_rates
    
    def search(self, num_iid, seller_nick, page_no=1, page_size=20):
        '''taobao.traderates.search 商品评价查询接口
        
        通过商品id查询对应的评价信息'''
        request = TOPRequest('taobao.traderates.search')
        request['num_iid'] = num_iid
        request['seller_nick'] = seller_nick
        request['page_no'] = page_no
        reqiest['page_size'] = page_size
        self.create(self.execute(request))
        return self.trade_rates
    


