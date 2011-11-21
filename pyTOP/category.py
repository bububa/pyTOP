#!/usr/bin/env python
# encoding: utf-8
"""
category.py

Created by 徐 光硕 on 2011-11-15.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest

class PropValue(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(PropValue, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['cid','pid','prop_name','vid','name','name_alias','is_parent','status','sort_order']
    

class SellerAuthorize(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(SellerAuthorize, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'item_cats':ItemCat, 'brands':Brand}
        self.fields = ['item_cats','brands']
    

class ItemCat(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemCat, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['cid','parent_cid','name','is_parent','status','sort_order']
    
class Brand(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Brand, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['vid','name','pid','prop_name']
   

class ItemProp(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemProp, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'prop_values':PropValue}
        self.fields = ['is_input_prop','pid','parent_pid','parent_vid','name','is_key_prop','is_sale_prop','is_color_prop','is_enum_prop','is_item_prop','must','multi','prop_values','status','sort_order','child_template','is_allow_alias']

class ItemCats(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemCats, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'item_cats':SellerAuthorize, 'item_cats':ItemCat}
        self.fields = ['last_modified','item_cats', 'seller_authorize']
        
    def authorize_get(self, session, fields=[]):
        '''taobao.itemcats.authorize.get 查询B商家被授权品牌列表和类目列表'''
        sellerAuthorize = SellerAuthorize()
        request = TOPRequest('taobao.authorize.get')
        if not fields:
            fields = sellerAuthorize.fields
        request['fields'] = ','.join(fields)
        self.create(self.execute(request, session))
        return self.seller_authorize
    
    def get(self, parent_cid=None, cids=[], fields=[]):
        '''taobao.itemcats.get 获取后台供卖家发布商品的标准商品类目'''
        request = TOPRequest('taobao.itemcats.get')
        if not fields:
            itemCat = ItemCat()
            fields = itemCat.fields
        request['fields'] = fields
        if parent_cid!=None:
            request['parent_cid'] = parent_cid
        if cids:
            request['cids'] = ','.join([str(cid) for cid in cids])
        self.create(self.execute(request))
        return self.item_cats


class ItemProps(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemProps, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'item_props':ItemProp}
        self.fields = ['last_modified','item_props']
    
    def get(self, cid, fields=[], **kwargs):
        '''taobao.itemprops.get 获取标准商品类目属性
        ===============================
        Q：能否通过图形化界面获取特定类目下面的属性及属性值? 
        A：请点击属性工具，通过图形化界面直接获取上述数据 
        Q：关键属性，非关键属性，销售属性有什么区别？ A：产品的关键属性是必填的，关键属性＋类目id确定一个产品，非关键属性，是分类上除了关键属性和销售属性以外的属性。销售属性是只有一件实物的商品才能确定的一个属性，如：N73　红色，黑色。没有实物不能确定。 
        Q：销售属性与SKU之间有何关联？ 
        A：销售属性是组成SKU的特殊属性，它会影响买家的购买和卖家的库存管理，如服装的"颜色"、"套餐"和"尺码"。 
        SKU 即我们常说的销售属性，最小购买单位或最小库存单位。它是销售属性的一个组合。比如"红色的诺基亚N95"就是一个SKU。'''
        request = TOPRequest('taobao.itemprops.get')
        if not fields:
            itemProp = ItemProp()
            fields = itemProp.fields
        request['fields'] = fields
        request['cid'] = cid
        for k, v in kwargs.iteritems():
            if k not in ('pid', 'parent_pid', 'is_key_prop', 'is_sale_prop', 'is_color_prop', 'is_enum_prop', 'is_input_prop', 'is_item_prop', 'child_path') and v==None: continue
            request[k] = v
        self.create(self.execute(request))
        return self.item_props
    

class ItemPropValues(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemPropValues, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'prop_values':PropValue}
        self.fields = ['last_modified','prop_values']
    
    def get(self, cid, pvs=None, fields=[]):
        '''taobao.itempropvalues.get 获取标准类目属性值
        ===============================
        传入类目ID,必需是叶子类目，通过taobao.itemcats.get获取类目ID 返回字段目前支持有：cid,pid,prop_name,vid,name,name_alias,status,sort_order 作用:获取标准类目属性值'''
        request = TOPRequest('taobao.itempropvalues.get')
        if not fields:
            propValue = PropValue()
            fields = propValue.fields
        request['fields'] = fields
        if pvs!=None:
            request['pvs'] = pvs
        request['cid'] = cid
        self.create(self.execute(request))
        return self.prop_values
