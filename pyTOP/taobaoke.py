#!/usr/bin/env python
# encoding: utf-8
"""
taobaoke.py

提供了淘宝客商品列表和淘宝客单品详情推广，店铺推广，类目和关键字推广以及淘客报表查询等功能

Created by 徐 光硕 on 2011-11-23.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate
from user import Location
from item import Item, ItemImg, Sku, Video, PropImg

class TaobaokeReportMember(TOP):
    '''淘宝客报表成员'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TaobaokeReportMember, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'pay_time':TOPDate,}
        self.fields = ['commission_rate','real_pay_fee','app_key','outer_code','trade_id','pay_time','pay_price','num_iid','item_title','item_num','category_id','category_name','shop_title','commission','iid','seller_nick']
    

class TaobaokeReport(TOP):
    '''淘宝客报表'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TaobaokeReport, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'taobaoke_report_members':TaobaokeReportMember,}
        self.fields = ['taobaoke_report_members','total_results']
    
    def get(self, date, page_no=1, page_size=40, fields=[]):
        '''taobao.taobaoke.report.get 淘宝客报表查询
        
        淘宝客报表查询'''
        request = TOPRequest('taobao.taobaoke.items.get')
        request['date'] = date
        request['page_no'] = page_no
        request['page_size'] = page_size
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request)['taobaoke_report'])
        return self
    

class TaobaokeItemDetail(TOP):
    '''淘宝客商品详情'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TaobaokeItemDetail, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'item':Item,}
        self.fields = ['item','click_url','shop_click_url','seller_credit_score']
    

class TaobaokeItem(TOP):
    '''淘宝客商品'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TaobaokeItem, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['commission_rate','iid','num_iid','title','nick','pic_url','price','click_url','commission','commission_num','commission_volume','shop_click_url','seller_credit_score','item_location','volume','taobaoke_cat_click_url','keyword_click_url']
    

class TaobaokeShop(TOP):
    '''淘宝客店铺'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TaobaokeShop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['user_id','shop_title','click_url','commission_rate','seller_credit','shop_type','total_auction','auction_count']
    

class TaobaokeShops(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TaobaokeShops, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'taobaoke_shops':TaobaokeShop}
        self.fields = ['taobaoke_shops', 'total_results']
    
    def convert(self, sids, fields=[], **kwargs):
        '''taobao.taobaoke.shops.convert 淘客店铺转换
        
        淘宝客店铺转换'''
        request = TOPRequest('taobao.taobaoke.shops.convert')
        request['num_iids'] = num_iids
        if not fields:
            taobaokeShop = TaobaokeShop()
            fields = taobaokeShop.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('nick', 'outer_code', 'pid') and v==None: continue
            request[k] = v
        self.create(self.execute(request))
        return self.taobaoke_shops
    
    def get(self, fields=[], **kwargs):
        '''taobao.taobaoke.shops.get 淘宝客店铺搜索
        
        提供对参加了淘客推广的店铺的搜索'''
        request = TOPRequest('taobao.taobaoke.shops.get')
        if not fields:
            taobaokeShop = TaobaokeShop()
            fields = taobaokeShop.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('cid', 'start_credit', 'end_credit','start_commissionrate','end_commissionrate','start_auctioncount','end_auctioncount','start_totalaction','end_totalaction','only_mall','keyword','outer_code','page_no','page_size','nick','pid') and v==None: continue
            request[k] = v
        self.create(self.execute(request))
        return self.taobaoke_shops
    

class Taobaoke(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TaobaokeShop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
    
    def caturl_get(self, **kwargs):
        '''taobao.taobaoke.caturl.get 淘宝客类目推广URL
        
        淘宝客类目推广URL'''
        request = TOPRequest('taobao.taobaoke.caturl.get')
        for k, v in kwargs.iteritems():
            if k not in ('q', 'cid', 'nick', 'outer_code', 'pid') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['taobaoke_item'], models={'taobaoke_item':TaobaokeItem})
        return self.taobaoke_item
    
    def items_convert(self, fields=[], **kwargs):
        '''taobao.taobaoke.items.convert 淘客商品转换
        
        淘宝客商品转换'''
        request = TOPRequest('taobao.taobaoke.items.convert')
        if not fields:
            taobaokeItem = TaobaokeItem()
            fields = taobaokeItem.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('nick', 'outer_code', 'num_iids', 'pid', 'is_mobile') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['taobaoke_items', 'total_results'], models={'taobaoke_items':TaobaokeItem})
        return self.taobaoke_items
    
    def items_detail_get(self, num_iids, fields=[], **kwargs):
        '''taobao.taobaoke.items.detail.get 查询淘宝客推广商品详细信息
        
        查询淘宝客推广商品详细信息'''
        request = TOPRequest('taobao.taobaoke.items.detail.get')
        request['num_iids'] = num_iids
        if not fields:
            taobaokeItem = TaobaokeItem()
            fields = taobaokeItem.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('nick', 'outer_code', 'pid') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['taobaoke_item_details', 'total_results'], models={'taobaoke_item_details':TaobaokeItemDetail})
        return self.taobaoke_item_details
    
    def items_get(self, fields=[], **kwargs):
        '''taobao.taobaoke.items.get 查询淘宝客推广商品
        
        查询淘宝客推广商品,不能通过设置cid=0来查询'''
        request = TOPRequest('taobao.taobaoke.items.get')
        if not fields:
            taobaokeItem = TaobaokeItem()
            fields = taobaokeItem.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('nick', 'pid', 'keyword', 'cid', 'start_price','end_price','auto_send','area','start_credit','end_credit','sort','guarantee','start_commissionRate','end_commissionRate','start_commissionNum','end_commissionNum','start_totalnum','end_totalnum','cash_coupon','vip_card','overseas_item','sevendays_return','real_describe','onemonth_repair','cash_ondelivery','mall_item','page_no','page_size','outer_code','is_mobile') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['taobaoke_items', 'total_results'], models={'taobaoke_items':TaobaokeItem})
        return self.taobaoke_items
    
    def listurl_get(self, q, **kwargs):
        '''taobao.taobaoke.listurl.get 淘宝客关键词搜索URL
        
        淘宝客关键词搜索URL'''
        request = TOPRequest('taobao.taobaoke.listurl.get')
        request['q'] = q
        for k, v in kwargs.iteritems():
            if k not in ('nick', 'outer_code', 'pid') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['taobaoke_item'], models={'taobaoke_item':TaobaokeItem})
        return self.taobaoke_item
    
    def tool_relation(self, pubid):
        '''taobao.taobaoke.tool.relation 工具联盟注册校验
        
        判断用户pid是否是appkey关联的注册用户'''
        request = TOPRequest('taobao.taobaoke.tool.relation')
        request['pubid'] = pubid
        self.create(self.execute(request), fields=['tools_user'])
        return self.tools_user
    
    def virtualcard_get(self, fields=[], **kwargs):
        '''taobao.taobaoke.virtualcard.get 虚拟卡查询
        
        虚拟点卡充值卡电话卡等查询'''
        request = TOPRequest('taobao.taobaoke.virtualcard.get')
        if not fields:
            taobaokeItem = TaobaokeItem()
            fields = taobaokeItem.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('nick', 'pid', 'biz_type', 'card_type', 'area','operator','price','game_name','outer_code','page_no','page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request), fields=['taobaoke_items', 'total_results'], models={'taobaoke_items':TaobaokeItem})
        return self.taobaoke_items
    
