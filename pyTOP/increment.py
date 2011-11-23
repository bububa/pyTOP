#!/usr/bin/env python
# encoding: utf-8
"""
increment.py

配合主动通知业务，提供商品，交易，退款和评价等数据或状态变更的查询功能

Created by 徐 光硕 on 2011-11-23.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class NotifyRefund(TOP):
    '''退款通知消息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(NotifyRefund, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'modified':TOPDate}
        self.fields = ['rid','tid','oid','seller_nick','buyer_nick','refund_fee','status','modified']
    

class NotifyItem(TOP):
    '''商品通知消息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(NotifyItem, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'modified':TOPDate}
        self.fields = ['sku_id','sku_num','status','increment','iid','num_iid','title','nick','num','changed_fields','price','modified']
    

class NotifyTrade(TOP):
    '''交易通知消息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(NotifyTrade, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'modified':TOPDate}
        self.fields = ['oid','tid','seller_nick','buyer_nick','payment','trade_mark','type','status','modified']
    

class AppCustomer(TOP):
    '''开通增量消息服务的应用用户'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(AppCustomer, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate}
        self.fields = ['nick','created','status']
    

class Increment(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Increment, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
    
    def customer_permit(self, session):
        '''taobao.increment.customer.permit 开通增量消息服务
        
        提供app为自己的用户开通增量消息服务功能'''
        request = TOPRequest('taobao.increment.customer.permit')
        self.create(self.execute(request, session), fields=['app_customer',], models={'app_customer':AppCustomer})
        return self.app_customer
    
    def customer_stop(self, nick, session):
        '''taobao.increment.customer.stop 关闭用户的增量消息服务
        
        供应用关闭其用户的增量消息服务功能，这样可以节省ISV的流量。'''
        request = TOPRequest('taobao.increment.customer.stop')
        request['nick'] = nick
        self.create(self.execute(request, session), fields=['is_success',])
        return self.is_success
    
    def customers_get(self, session, page_no=1, page_size=10, nicks=None):
        '''taobao.increment.customers.get 查询应用为用户开通的增量消息服务
        
        提供查询应用为自身用户所开通的增量消息服务信息。'''
        request = TOPRequest('taobao.increment.customers.get')
        request['page_no'] = page_no
        request['page_size'] = page_size
        if nicks!=None: request['nicks'] = nicks
        self.create(self.execute(request, session), fields=['app_customers', 'total_results'], models={'app_customers':AppCustomer})
        return self.app_customers
    
    def items_get(self, **kwargs):
        '''taobao.increment.items.get 获取商品变更通知信息
        
        开通主动通知业务的APP可以通过该接口获取商品变更通知信息 建议获取增量消息的时间间隔是：半个小时'''
        request = TOPRequest('taobao.increment.items.get')
        for k, v in kwargs.iteritems():
            if k not in ('status', 'nick', 'start_modified', 'end_modified', 'page_no', 'page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['notify_items', 'total_results'], models={'notify_items':NotifyItem})
        return self.notify_items
    
    def refunds_get(self, **kwargs):
        '''taobao.increment.refunds.get 获取退款变更通知信息
        
        开通主动通知业务的APP可以通过该接口获取用户的退款变更通知信息 建议在获取增量消息的时间间隔是：半个小时'''
        request = TOPRequest('taobao.increment.refunds.get')
        for k, v in kwargs.iteritems():
            if k not in ('status', 'nick', 'start_modified', 'end_modified', 'page_no', 'page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['notify_refunds', 'total_results'], models={'notify_refunds':NotifyRefund})
        return self.notify_refunds
    
    def trades_get(self, **kwargs):
        '''taobao.increment.trades.get 获取交易和评价变更通知信息
        
        开通主动通知业务的APP可以通过该接口获取用户的交易和评价变更通知信息 建议在获取增量消息的时间间隔是：半个小时'''
        request = TOPRequest('taobao.increment.trades.get')
        for k, v in kwargs.iteritems():
            if k not in ('status', 'nick', 'type', 'start_modified', 'end_modified', 'page_no', 'page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['notify_trades', 'total_results'], models={'notify_trades':NotifyTrade})
        return self.notify_trades
    
