#!/usr/bin/env python
# encoding: utf-8
"""
vas.py

提供用户应用订购关系相关查询

Created by 徐 光硕 on 2011-11-23.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class ArticleUserSubscribe(TOP):
    '''用户订购信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ArticleUserSubscribe, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'deadline':TOPDate}
        self.fields = ['item_code','deadline']
    

class ArticleBizOrder(TOP):
    '''应用订单信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ArticleBizOrder, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create':TOPDate,'order_cycle_start':TOPDate,'order_cycle_end':TOPDate}
        self.fields = ['biz_order_id','order_id','nick','article_name','article_code','item_name','item_code','create','order_cycle','order_cycle_start','order_cycle_end','biz_type','fee','prom_fee','refund_fee','total_pay_fee']
    

class ArticleSub(TOP):
    '''应用订购信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ArticleSub, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'deadline':TOPDate}
        self.fields = ['nick','article_name','article_code','item_name','item_code','deadline','status','autosub','expire_notice']
    

class Vas(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Vas, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
    
    def order_search(self, article_code, **kwargs):
        '''taobao.vas.order.search 订单记录导出
        
        用于ISV查询自己名下的应用及收费项目的订单记录。目前所有应用调用此接口的频率限制为200次/分钟，即每分钟内，所有应用调用此接口的次数加起来最多为200次。'''
        request = TOPRequest('taobao.vas.order.search')
        request['article_code'] = article_code
        for k, v in kwargs.iteritems():
            if k not in ('item_code', 'nick', 'start_created', 'end_created', 'biz_type', 'biz_order_id', 'order_id', 'page_size','page_no') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['article_biz_orders','total_item'], models={'article_biz_orders':ArticleBizOrder})
        return self.article_biz_orders
    
    def subsc_search(self, article_code, **kwargs):
        '''taobao.vas.subsc.search 订购记录导出
        
        用于ISV查询自己名下的应用及收费项目的订购记录'''
        request = TOPRequest('taobao.vas.subsc.search')
        request['article_code'] = article_code
        for k, v in kwargs.iteritems():
            if k not in ('item_code', 'nick', 'start_deadline', 'end_deadline', 'status', 'autosub', 'expire_notice', 'page_size','page_no') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['article_subs','total_item'], models={'article_subs':ArticleSub})
        return self.article_subs
    
    def subscribe_get(self, nick, article_code):
        '''taobao.vas.subscribe.get 订购关系查询
        
        用于ISV根据登录进来的淘宝会员名查询该为该会员开通哪些收费项目，ISV只能查询自己名下的应用及收费项目的订购情况'''
        request = TOPRequest('taobao.vas.subscribe.get')
        request['nick'] = nick
        request['article_code'] = article_code
        self.create(self.execute(request), fields=['article_user_subscribes',], models={'article_user_subscribes':ArticleUserSubscribe})
        return self.article_user_subscribes
    
