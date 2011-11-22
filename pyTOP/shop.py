#!/usr/bin/env python
# encoding: utf-8
"""
shop.py

Created by 徐 光硕 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class ShopCat(TOP):
    '''店铺类目'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ShopCat, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['cid','parent_cid','name','is_parent']
    

class ShopCats(TOP):
    '''店铺类目'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ShopCats, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'shop_cats':ShopCat}
        self.fields = ['shop_cats',]
    
    def get(self, fields=[]):
        '''taobao.shopcats.list.get 获取前台展示的店铺类目
        
        此API获取淘宝面向买家的浏览导航类目 跟后台卖家商品管理的类目有差异'''
        request = TOPRequest('taobao.shopcats.list.get')
        if not fields:
            shopCat = ShopCat()
            fields = shopCat.fields
        request['fields'] = fields
        self.create(self.execute(request))
        return self.shop_cats
    

class ShopScore(TOP):
    '''店铺动态评分信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ShopScore, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['item_score','service_score','delivery_score']
    

class SellerCat(TOP):
    '''店铺内卖家自定义类目'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(SellerCat, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate}
        self.fields = ['type','cid','parent_cid','name','pic_url','sort_order','created','modified']
    
    def add(self, name, session, pict_url=None, parent_cid=None, sort_order=None):
        '''taobao.sellercats.list.add 添加卖家自定义类目
        
        此API添加卖家店铺内自定义类目 父类目parent_cid值等于0：表示此类目为店铺下的一级类目，值不等于0：表示此类目有父类目 注：因为缓存的关系,添加的新类目需8个小时后才可以在淘宝页面上正常显示，但是不影响在该类目下商品发布'''
        request = TOPRequest('taobao.sellercats.list.add')
        request['name'] = name
        if pict_url!=None: request['pict_url'] = pict_url
        if parent_cid!=None: request['parent_cid'] = parent_cid
        if sort_order!=None: request['sort_order'] = sort_order
        self.create(self.execute(request, session)['seller_cat'])
        return self
    
    def update(self, cid, session, name=None, pict_url=None, sort_order=None):
        '''taobao.sellercats.list.update 更新卖家自定义类目
        
        此API更新卖家店铺内自定义类目 注：因为缓存的关系，添加的新类目需8个小时后才可以在淘宝页面上正常显示，但是不影响在该类目下商品发布'''
        request = TOPRequest('taobao.sellercats.list.update')
        request['cid'] = cid
        if name!=None: request['name'] = name
        if pict_url!=None: request['pict_url'] = pict_url
        if sort_order!=None: request['sort_order'] = sort_order
        self.create(self.execute(request, session)['seller_cat'])
        return self
    

class SellerCats(TOP):
    '''店铺内卖家自定义类目'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(SellerCats, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'seller_cats':SellerCat}
        self.fields = ['seller_cats',]
    
    def get(self, nick):
        '''taobao.sellercats.list.get 获取前台展示的店铺内卖家自定义商品类目
        
        此API添加卖家店铺内自定义类目 父类目parent_cid值等于0：表示此类目为店铺下的一级类目，值不等于0：表示此类目有父类目 注：因为缓存的关系,添加的新类目需8个小时后才可以在淘宝页面上正常显示，但是不影响在该类目下商品发布'''
        request = TOPRequest('taobao.sellercats.list.get')
        request['nick'] = nick
        self.create(self.execute(request))
        return self.seller_cats
    

class Shop(TOP):
    '''店铺信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Shop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate,'shop_score':ShopScore}
        self.fields = ['sid','cid','nick','name','title','desc','bulletin','pic_path','created','modified','shop_score','remain_count','all_count','used_count']
    
    def get(self, nick, fields=[]):
        '''taobao.shop.get 获取卖家店铺的基本信息
        
        获取卖家店铺的基本信息'''
        request = TOPRequest('taobao.shop.get')
        request['nick'] = nick
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request)['shop'])
        return self
    
    def remainshowcase_get(self, session):
        '''taobao.shop.remainshowcase.get 获取卖家店铺剩余橱窗数量
        
        获取卖家店铺剩余橱窗数量，已用橱窗数量，总橱窗数量（对于B卖家，后两个参数返回-1）'''
        request = TOPRequest('taobao.shop.remainshowcase.get')
        self.create(self.execute(request, session)['shop'])
        return self
    
    def update(self, session, title=None, bulletin=None, desc=None):
        '''taobao.shop.remainshowcase.get 获取卖家店铺剩余橱窗数量
        
        目前只支持标题、公告和描述的更新'''
        request = TOPRequest('taobao.shop.remainshowcase.get')
        if title!=None: request['title'] = title
        if bulletin!=None: request['bulletin'] = bulletin
        if desc!=None: request['desc'] = desc
        self.create(self.execute(request, session)['shop'])
        return self
    
