#!/usr/bin/env python
# encoding: utf-8
"""
item.py

Created by 徐 光硕 on 2011-11-15.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate
from user import Location

class Item(TOP):
    '''Item(商品)结构'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Item, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'skus':Sku,'location':Location,'item_imgs':ItemImg,'prop_imgs':PropImg,'videos':Video}
        self.fields = ['detail_url','num_iid','title','nick','type','desc','skus','props_name','created','promoted_service','is_lightning_consignment','is_fenxiao','auction_point','property_alias','volume','template_id','after_sale_id','is_xinpin','sub_stock','cid','seller_cids','props','input_pids','input_str','pic_url','num','valid_thru','list_time','delist_time','stuff_status','location','price','post_fee','express_fee','ems_fee','has_discount','freight_payer','has_invoice','has_warranty','has_showcase','modified','increment','approve_status','postage_id','product_id','item_imgs','prop_imgs','outer_id','is_virtual','is_taobao','is_ex','is_timing','videos','is_3D','score','one_station','second_kill','auto_fill','violation','is_prepay','ww_status','wap_desc','wap_detail_url','cod_postage_id','sell_promise']
    
    def add(self, num, price, aType, stuff_status, title, desc, location_state, location_city, cid, session, **kwargs):
        '''taobao.item.add 添加一个商品
        
        此接口用于新增一个商品 商品所属的卖家是当前会话的用户 商品的属性和sku的属性有包含的关系，商品的价格要位于sku的价格区间之中（例如，sku价格有5元、10元两种，那么商品的价格就需要大于等于5元，小于等于10元，否则新增商品会失败） 商品的类目和商品的价格、sku的价格都有一定的相关性（具体的关系要通过类目属性查询接口获得） 商品的运费承担方式和邮费设置有相关性，卖家承担运费不用设置邮费，买家承担运费需要设置邮费 当关键属性值选择了“其他”的时候，需要输入input_pids和input_str商品才能添加成功。'''
        request = TOPRequest('taobao.item.add')
        request['num'] = num
        request['price'] = price
        request['type'] = aType
        request['stuff_status'] = stuff_status
        request['title'] = title
        request['desc'] = desc
        request['location.state'] = location_state
        request['location.city'] = location_city
        request['cid'] = cid
        for k, v in kwargs.iteritems():
            if k not in ('props', 'approve_status', 'freight_payer', 'valid_thru', 'has_invoice', 'has_warranty', 'has_showcase', 'seller_cids', 'has_discount', 'post_fee', 'express_fee', 'ems_fee', 'list_time', 'increment', 'image', 'postage_id', 'auction_point', 'property_alias', 'input_pids', 'sku_properties', 'sku_prices', 'sku_outer_ids', 'lang', 'outer_id', 'product_id', 'pic_path', 'auto_fill', 'input_str', 'is_taobao', 'is_ex', 'is_3D', 'sell_promise', 'after_sale_id', 'cod_postage_id', 'is_lightning_consignment', 'weight', 'is_xinpin', 'sub_stock') and v==None: continue
            request[k] = v
        
        self.create(self.execute(request, session)['item'])
        return self
    
    def update(self, num_iid, session, **kwargs):
        '''taobao.item.update 更新商品信息
        
        根据传入的num_iid更新对应的商品的数据 传入的num_iid所对应的商品必须属于当前会话的用户 商品的属性和sku的属性有包含的关系，商品的价格要位于sku的价格区间之中（例如，sku价格有5元、10元两种，那么商品的价格就需要大于等于5元，小于等于10元，否则更新商品会失败） 商品的类目和商品的价格、sku的价格都有一定的相关性（具体的关系要通过类目属性查询接口获得） 当关键属性值更新为“其他”的时候，需要输入input_pids和input_str商品才能更新成功。'''
        request = TOPRequest('taobao.item.update')
        request['num_iid'] = num_iid
        for k, v in kwargs.iteritems():
            if k not in ('cid', 'props', 'num', 'price', 'title', 'desc', 'location_state', 'location_city', 'post_fee', 'express_fee', 'ems_fee', 'list_time', 'increment', 'image', 'stuff_status', 'auction_point', 'property_alias', 'input_pids', 'sku_quantities', 'sku_prices', 'sku_properties', 'seller_cids', 'postage_id', 'outer_id', 'product_id', 'pic_path', 'auto_fill', 'sku_outer_ids', 'is_taobao', 'is_ex', 'is_3D', 'is_replace_sku', 'input_str', 'lang', 'has_discount', 'has_showcase', 'approve_status', 'freight_payer', 'valid_thru', 'has_invoice', 'has_warranty', 'after_sale_id', 'sell_promise', 'cod_postage_id', 'is_lightning_consignment', 'weight', 'is_xinpin', 'sub_stock') and v==None: continue
            if k == 'location_state': k = 'location.state'
            if k == 'location_city': k = 'location.city'
            request[k] = v
        
        self.create(self.execute(request, session)['item'])
        return self
    
    def delete(self, num_iid, session):
        '''taobao.item.delete 删除单条商品
        
        删除单条商品'''
        request = TOPRequest('taobao.item.delete')
        request['num_iid'] = num_iid
        self.create(self.execute(request, session)['item'])
        return self
    
    def update_delisting(self, num_iid, session):
        '''taobao.item.update.delisting 商品下架
        
        单个商品下架 
        输入的num_iid必须属于当前会话用户'''
        request = TOPRequest('taobao.item.update.delisting')
        request['num_iid'] = num_iid
        self.create(self.execute(request, session)['item'])
        return self
    
    def update_listing(self, num_iid, num, session):
        '''taobao.item.update.listing 一口价商品上架
        
        单个商品上架 
        输入的num_iid必须属于当前会话用户'''
        request = TOPRequest('taobao.item.update.listing')
        request['num_iid'] = num_iid
        request['num'] = num
        self.create(self.execute(request, session)['item'])
        return self
    
    def get(self, num_iid, fields=[], session=None):
        '''taobao.item.get 得到单个商品信息
        
        获取单个商品的详细信息 卖家未登录时只能获得这个商品的公开数据，卖家登录后可以获取商品的所有数据'''
        request = TOPRequest('taobao.item.get')
        request['num_iid'] = num_iid
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request, session)['item'])
        return self
    
    def price_update(self, num_iid, session, **kwargs):
        '''taobao.item.price.update 更新商品价格
        
        更新商品价格'''
        request = TOPRequest('taobao.item.price.update')
        request['num_iid'] = num_iid
        for k, v in kwargs.iteritems():
            if k not in ('cid', 'props', 'num', 'price', 'title', 'desc', 'location_state', 'location_city', 'post_fee', 'express_fee', 'ems_fee', 'list_time', 'increment', 'image', 'stuff_status', 'auction_point', 'property_alias', 'input_pids', 'sku_quantities', 'sku_prices', 'sku_properties', 'seller_cids', 'postage_id', 'outer_id', 'product_id', 'pic_path', 'auto_fill', 'sku_outer_ids', 'is_taobao', 'is_ex', 'is_3D', 'is_replace_sku', 'input_str', 'lang', 'has_discount', 'has_showcase', 'approve_status', 'freight_payer', 'valid_thru', 'has_invoice', 'has_warranty', 'after_sale_id', 'sell_promise', 'cod_postage_id', 'is_lightning_consignment', 'weight', 'is_xinpin') and v==None: continue
            if k == 'location_state': k = 'location.state'
            if k == 'location_city': k = 'location.city'
            request[k] = v
        
        self.create(self.execute(request, session)['item'])
        return self
    
    def quantity_update(self, num_iid, quantity, session, sku_id=None, outer_id=None, aType=None):
        '''taobao.item.quantity.update 宝贝/SKU库存修改
        
        提供按照全量或增量形式修改宝贝/SKU库存的功能'''
        request = TOPRequest('taobao.item.quantity.update')
        request['num_iid'] = num_iid
        request['quantity'] = quantity
        if sku_id!=None:
            request['sku_id'] = sku_id
        if outer_id!=None:
            request['outer_id'] = outer_id
        if aType!=None:
            request['type'] = aType
        self.create(self.execute(request, session)['item'])
        return self
    
    def recommend_add(self, num_iid, session):
        '''taobao.item.recommend.add 橱窗推荐一个商品
        
        将当前用户指定商品设置为橱窗推荐状态 橱窗推荐需要用户有剩余橱窗位才可以顺利执行 这个Item所属卖家从传入的session中获取，需要session绑定 需要判断橱窗推荐是否已满，橱窗推荐已满停止调用橱窗推荐接口，2010年1月底开放查询剩余橱窗推荐数后可以按数量橱窗推荐商品'''
        request = TOPRequest('taobao.item.recommend.add')
        request['num_iid'] = num_iid
        self.create(self.execute(request, session)['item'])
        return self
    
    def recommend_delete(self, num_iid, session):
        '''taobao.item.recommend.delete 取消橱窗推荐一个商品
        
        取消当前用户指定商品的橱窗推荐状态 这个Item所属卖家从传入的session中获取，需要session绑定'''
        request = TOPRequest('taobao.item.recommend.delete')
        request['num_iid'] = num_iid
        self.create(self.execute(request, session)['item'])
        return self
    

class Items(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Items, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'items':Item, 'item_search':ItemSearch}
        self.fields = ['items', 'total_results', 'item_search']
    
    def custom_get(self, outer_id, session, fields=[]):
        '''taobao.items.custom.get 根据外部ID取商品
        
        跟据卖家设定的商品外部id获取商品 这个商品对应卖家从传入的session中获取，需要session绑定'''
        request = TOPRequest('taobao.items.custom.get')
        request['outer_id'] = outer_id
        if not fields:
            item = Item()
            fields = item.fields
        request['fields'] = fields
        self.create(self.execute(request, session))
        return self.items
    
    def get(self, session, fields=[], **kwargs):
        '''taobao.items.get 搜索商品信息
        
        根据传入的搜索条件，获取商品列表（类似于淘宝页面上的商品搜索功能，但是只有搜索到的商品列表，不包含商品的ItemCategory列表） 只能获得商品的部分信息，商品的详细信息请通过taobao.item.get获取 如果只输入fields其他条件都不输入，系统会因为搜索条件不足而报错。 不能通过设置cid=0来查询。'''
        request = TOPRequest('taobao.items.get')
        if not fields:
            item = Item()
            fields = item.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('q', 'nicks', 'cid', 'props', 'product_id', 'page_no', 'order_by', 'ww_status', 'post_free', 'location_state', 'location_city', 'is_3D', 'start_score', 'end_score', 'start_volume', 'end_volume', 'one_station', 'is_cod', 'is_mall', 'is_prepay', 'genuine_security', 'stuff_status', 'start_price', 'end_price', 'page_size', 'promoted_service', 'is_xinpin') and v==None: continue
            if k == 'location_state': k = 'location.state'
            if k == 'location_city': k = 'location.city'
            request[k] = v
        
        self.create(self.execute(request, session))
        return self.items
    
    def inventory_get(self, session, fields=[], **kwargs):
        '''taobao.items.inventory.get 得到当前会话用户库存中的商品列表
        
        获取当前用户作为卖家的仓库中的商品列表，并能根据传入的搜索条件对仓库中的商品列表进行过滤 只能获得商品的部分信息，商品的详细信息请通过taobao.item.get获取'''
        request = TOPRequest('taobao.items.inventory.get')
        if not fields:
            item = Item()
            fields = item.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('q', 'banner', 'cid', 'seller_cids', 'page_no', 'page_size', 'has_discount', 'order_by', 'is_taobao', 'is_ex', 'start_modified', 'end_modified') and v==None: continue
            request[k] = v
        
        self.create(self.execute(request, session))
        return self.items
    
    def list_get(self, num_iids, fields=[], session=None):
        '''taobao.items.list.get 批量获取商品信息
        
        查看非公开属性时需要用户登录'''
        request = TOPRequest('taobao.items.list.get')
        request['num_iids'] = num_iids
        if not fields:
            item = Item()
            fields = item.fields
        request['fields'] = fields
        self.create(self.execute(request, session))
        return self.items
    
    def onsale_get(self, session, fields=[], **kwargs):
        '''taobao.items.onsale.get 获取当前会话用户出售中的商品列表
        
        获取当前用户作为卖家的出售中的商品列表，并能根据传入的搜索条件对出售中的商品列表进行过滤 只能获得商品的部分信息，商品的详细信息请通过taobao.item.get获取'''
        request = TOPRequest('taobao.items.onsale.get')
        if not fields:
            item = Item()
            fields = item.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('q', 'banner', 'cid', 'seller_cids', 'page_no', 'has_discount', 'has_showcase', 'order_by', 'is_taobao', 'is_ex', 'page_size', 'start_modified', 'end_modified') and v==None: continue
            request[k] = v
        
        self.create(self.execute(request, session))
        return self.items
    
    def search(self, fields=[], **kwargs):
        '''taobao.items.search 搜索商品信息
        
        - 根据传入的搜索条件，获取商品列表和商品类目信息ItemCategory列表（类似于淘宝页面上的商品搜索功能，与 taobao.items.get的区别在于：这个方法得到的结果既有商品列表，又有类目信息列表） 
        - 商品列表里只能获得商品的部分信息，商品的详细信息请通过taobao.item.get获取 
        - 商品类目信息列表里只包含类目id和该类目下商品的数量 
        - 不能通过设置cid=0来查询'''
        request = TOPRequest('taobao.items.search')
        if not fields:
            item = Item()
            fields = item.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('q', 'nicks', 'cid', 'props', 'product_id', 'order_by', 'ww_status', 'post_free', 'location_state', 'location_city', 'is_3D', 'start_score', 'end_score', 'start_volume', 'end_volume', 'one_station', 'is_cod', 'is_mall', 'is_prepay', 'genuine_security', 'promoted_service', 'stuff_status', 'start_price', 'end_price', 'page_no', 'page_size', 'auction_flag', 'auto_post', 'has_discount', 'is_xinpin') and v==None: continue
            if k == 'location_state': k = 'location.state'
            if k == 'location_city': k = 'location.city'
            request[k] = v
        
        self.create(self.execute(request))
        return self.item_search
    

class Sku(TOP):
    '''Sku结构'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Sku, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate}
        self.fields = ['sku_id','num_iid','properties','quantity','price','outer_id','created','modified','status']
    
    def add(self, num_iid, properties, quantity, price, session, outer_id=None, item_price=None, lang=None):
        '''taobao.item.sku.add 添加SKU
        
        新增一个sku到num_iid指定的商品中 传入的iid所对应的商品必须属于当前会话的用户'''
        request = TOPRequest('taobao.item.sku.add')
        request['num_iid'] = num_iid
        request['properties'] = properties
        request['quantity'] = quantity
        request['price'] = price
        if outer_id!=None:
            request['outer_id'] = outer_id
        if item_price!=None:
            request['item_price'] = item_price
        if lang!=None:
            request['lang'] = lang
        self.create(self.execute(request, session)['sku'])
        return self
    
    def delete(self, num_iid, properties, session, item_price=None, item_num=None, lang=None):
        '''taobao.item.sku.delete 删除SKU
        
        删除一个sku的数据 需要删除的sku通过属性properties进行匹配查找'''
        request = TOPRequest('taobao.item.sku.delete')
        request['num_iid'] = num_iid
        request['properties'] = properties
        if item_num!=None:
            request['item_num'] = item_num
        if item_price!=None:
            request['item_price'] = item_price
        if lang!=None:
            request['lang'] = lang
        self.create(self.execute(request, session)['sku'])
        return self
    
    def get(self, sku_id, fields=[], num_iid=None, nick=None):
        '''taobao.item.sku.get 获取SKU
        
        获取sku_id所对应的sku数据 sku_id对应的sku要属于传入的nick对应的卖家'''
        request = TOPRequest('taobao.item.sku.get')
        request['sku_id'] = sku_id
        if num_iid!=None:
            request['num_iid'] = num_iid
        if nick!=None:
            request['nick'] = nick
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request)['sku'])
        return self
    
    def price_update(self, num_iid, properties, session, quantity=None, price=None, outer_id=None, item_price=None, lang=None):
        '''taobao.item.sku.price.update 更新商品SKU的价格
        
        更新商品SKU的价格'''
        request = TOPRequest('taobao.item.sku.price.update')
        request['num_iid'] = num_iid
        request['properties'] = properties
        if quantity!=None:
            request['quantity'] = quantity
        if price!=None:
            request['price'] = price
        if outer_id!=None:
            request['outer_id'] = outer_id
        if item_price!=None:
            request['item_price'] = item_price
        if lang!=None:
            request['lang'] = lang
        self.create(self.execute(request, session)['sku'])
        return self
    
    def update(self, num_iid, properties, session, quantity=None, price=None, outer_id=None, item_price=None, lang=None):
        '''taobao.item.sku.update 更新SKU信息
        
        - 更新一个sku的数据 
        - 需要更新的sku通过属性properties进行匹配查找 
        - 商品的数量和价格必须大于等于0 
        - sku记录会更新到指定的num_iid对应的商品中 
        - num_iid对应的商品必须属于当前的会话用户'''
        request = TOPRequest('taobao.item.sku.update')
        request['num_iid'] = num_iid
        request['properties'] = properties
        if quantity!=None:
            request['quantity'] = quantity
        if price!=None:
            request['price'] = price
        if outer_id!=None:
            request['outer_id'] = outer_id
        if item_price!=None:
            request['item_price'] = item_price
        if lang!=None:
            request['lang'] = lang
        self.create(self.execute(request, session)['sku'])
        return self
    

class Skus(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Users, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'skus':Sku}
        self.fields = ['skus']
    
    def get(self, num_iids, fields=[]):
        '''taobao.item.sku.get 获取SKU
        
        获取sku_id所对应的sku数据 sku_id对应的sku要属于传入的nick对应的卖家'''
        request = TOPRequest('taobao.item.sku.get')
        request['num_iids'] = num_iids
        if not fields:
            sku = Sku()
            fields = sku.fields
        request['fields'] = fields
        self.create(self.execute(request))
        return self.skus
    
    def custom_get(self, outer_id, session, fields=[]):
        '''taobao.skus.custom.get 根据外部ID取商品SKU
        
        跟据卖家设定的Sku的外部id获取商品，如果一个outer_id对应多个Sku会返回所有符合条件的sku 这个Sku所属卖家从传入的session中获取，需要session绑定(注：iid标签里是num_iid的值，可以用作num_iid使用)'''
        request = TOPRequest('taobao.skus.custom.get')
        request['outer_id'] = outer_id
        if not fields:
            item = Item()
            fields = item.fields
        request['fields'] = fields
        self.create(self.execute(request, session))
        return self.skus
    

class ItemImg(TOP):
    '''ItemImg结构'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemImg, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate}
        self.fields = ['id','url','position','created']
    
    def delete(self, id, num_iid, session):
        '''taobao.item.img.delete 删除商品图片
        
        删除itemimg_id 所指定的商品图片 传入的num_iid所对应的商品必须属于当前会话的用户 itemimg_id对应的图片需要属于num_iid对应的商品'''
        request = TOPRequest('taobao.item.img.delete')
        request['id'] = id
        request['num_iid'] = num_iid
        self.create(self.execute(request, session)['item_img'])
        return self
    
    def upload(self, num_iid, session, id=None, position=None, image=None, is_major=None):
        '''taobao.item.img.upload 添加商品图片
        
        添加一张商品图片到num_iid指定的商品中 传入的num_iid所对应的商品必须属于当前会话的用户 如果更新图片需要设置itemimg_id，且该itemimg_id的图片记录需要属于传入的num_iid对应的商品。如果新增图片则不用设置 商品图片有数量和大小上的限制，根据卖家享有的服务（如：卖家订购了多图服务等），商品图片数量限制不同。'''
        request = TOPRequest('taobao.item.img.upload')
        request['num_iid'] = num_iid
        if id!=None:
            request['id'] = id
        if position!=None:
            request['position'] = position
        if image!=None:
            request['image'] = image
        if is_major!=None:
            request['is_major'] = is_major
        self.create(self.execute(request, session)['item_img'])
        return self
    
    def joint_img(self, num_iid, pic_path, session, id=None, position=None, is_major=None):
        '''taobao.item.joint.img 商品关联子图
        
        - 关联一张商品图片到num_iid指定的商品中 
        - 传入的num_iid所对应的商品必须属于当前会话的用户 
        - 商品图片关联在卖家身份和图片来源上的限制，卖家要是B卖家或订购了多图服务才能关联图片，并且图片要来自于卖家自己的图片空间才行 
        - 商品图片数量有限制。不管是上传的图片还是关联的图片，他们的总数不能超过一定限额'''
        request = TOPRequest('taobao.item.joint.img')
        request['num_iid'] = num_iid
        request['pic_path'] = pic_path
        if id!=None:
            request['id'] = id
        if position!=None:
            request['position'] = position
        if is_major!=None:
            request['is_major'] = is_major
        self.create(self.execute(request, session)['item_img'])
        return self
    

class PropImg(TOP):
    '''商品属性图片结构'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemImg, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate}
        self.fields = ['id','url','properties','position','created']
    
    def joint_prop(self, properties, pic_path, num_iid, session, id=None, position=None):
        '''taobao.item.joint.propimg 商品关联属性图
        
        - 关联一张商品属性图片到num_iid指定的商品中 
        - 传入的num_iid所对应的商品必须属于当前会话的用户 
        - 图片的属性必须要是颜色的属性，这个在前台显示的时候需要和sku进行关联的 
        - 商品图片关联在卖家身份和图片来源上的限制，卖家要是B卖家或订购了多图服务才能关联图片，并且图片要来自于卖家自己的图片空间才行 
        - 商品图片数量有限制。不管是上传的图片还是关联的图片，他们的总数不能超过一定限额，最多不能超过24张（每个颜色属性都有一张）'''
        request = TOPRequest('taobao.item.joint.prop')
        request['num_iid'] = num_iid
        request['pic_path'] = pic_path
        request['properties'] = properties
        if id!=None:
            request['id'] = id
        if position!=None:
            request['position'] = position
        self.create(self.execute(request, session)['prop_img'])
        return self
    
    def delete(self, id, num_iid, session):
        '''taobao.item.propimg.delete 删除属性图片
        
        删除propimg_id 所指定的商品属性图片 传入的num_iid所对应的商品必须属于当前会话的用户 propimg_id对应的属性图片需要属于num_iid对应的商品'''
        request = TOPRequest('taobao.item.propimg.delete')
        request['id'] = id
        request['num_iid'] = num_iid
        self.create(self.execute(request, session)['prop_img'])
        return self
    
    def upload(self, num_iid, properties, session, id=None, image=None, position=None):
        '''taobao.item.propimg.upload 添加或修改属性图片
        
        添加一张商品属性图片到num_iid指定的商品中 传入的num_iid所对应的商品必须属于当前会话的用户 图片的属性必须要是颜色的属性，这个在前台显示的时候需要和sku进行关联的 商品属性图片只有享有服务的卖家（如：淘宝大卖家、订购了淘宝多图服务的卖家）才能上传 商品属性图片有数量和大小上的限制，最多不能超过24张（每个颜色属性都有一张）。'''
        request = TOPRequest('taobao.item.propimg.upload')
        request['num_iid'] = num_iid
        request['properties'] = properties
        if id!=None:
            request['id'] = id
        if position!=None:
            request['position'] = position
        if image!=None:
            request['image'] = image
        self.create(self.execute(request, session)['prop_img'])
        return self
    

class Video(TOP):
    '''商品视频关联记录'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Video, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate}
        self.fields = ['id','video_id','url','created','modified','iid','num_iid']
    

class ItemCategory(TOP):
    '''商品查询分类结果'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemCategory, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['category_id','count']
    

class ProductPropImg(TOP):
    '''产品属性图片'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ProductPropImg, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate}
        self.fields = ['id','product_id','props','url','position','created','modified']
    
    def delete(self, id, product_id, session):
        '''taobao.product.propimg.delete 删除产品属性图
        
        1.传入属性图片ID 2.传入产品ID 删除一个产品的属性图片'''
        request = TOPRequest('taobao.product.propimg.delete')
        request['id'] = id
        request['product_id'] = product_id
        self.create(self.execute(request, session)['product_prop_img'])
        return self
    
    def upload(self, product_id, props, image, session, id=None, position=None):
        '''taobao.product.propimg.upload 上传单张产品属性图片，如果需要传多张，可调多次
        
        传入产品ID 传入props,目前仅支持颜色属性.调用taobao.itemprops.get.v2取得颜色属性pid, 再用taobao.itempropvalues.get取得vid;格式:pid:vid,只能传入一个颜色pid:vid串; 传入图片内容 注意：图片最大为2M,只支持JPG,GIF,如果需要传多张，可调多次'''
        request = TOPRequest('taobao.product.propimg.upload')
        request['product_id'] = product_id
        request['props'] = props
        request['image'] = image
        if id!=None: request['id'] = id
        if position!=None: request['position'] = position
        self.create(self.execute(request, session)['product_prop_img'])
        return self
    

class ProductImg(TOP):
    '''产品图片'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ProductPropImg, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate}
        self.fields = ['id','product_id','url','position','created','modified']
    
    def delete(self, id, product_id, session):
        '''taobao.product.img.delete 删除产品非主图
        
        1.传入非主图ID 2.传入产品ID 删除产品非主图'''
        request = TOPRequest('taobao.product.img.delete')
        request['id'] = id
        request['product_id'] = product_id
        self.create(self.execute(request, session)['product_img'])
        return self
    
    def upload(self, product_id, image, session, id=None, position=None, is_major=None):
        '''taobao.product.img.upload 上传单张产品非主图，如果需要传多张，可调多次
        
        1.传入产品ID 2.传入图片内容 注意：图片最大为500K,只支持JPG,GIF格式,如果需要传多张，可调多次'''
        request = TOPRequest('taobao.product.img.upload')
        request['product_id'] = product_id
        request['image'] = image
        if id!=None: request['id'] = id
        if position!=None: request['position'] = position
        if is_major!=None: request['is_major'] = is_major
        self.create(self.execute(request, session)['product_img'])
        return self
    

class AfterSale(TOP):
    '''卖家设置售后服务对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(AfterSale, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'after_sales':AfterSale}
        self.fields = ['after_sales', 'after_sale_id','after_sale_name','after_sale_path']
    
    def get(self, session):
        '''taobao.aftersale.get 查询用户售后服务模板
        
        查询用户设置的售后服务模板，仅返回标题和id'''
        request = TOPRequest('taobao.aftersale.get')
        self.create(self.execute(request, session))
        return self.after_sales
    

class ItemTemplate(TOP):
    '''宝贝详情页面信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemTemplate, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['template_id','template_name','shop_type']
    

class ItemTemplates(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemTemplate, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'item_template_list':ItemTemplate}
        self.fields = ['item_template_list']
    
    def get(self, session):
        '''taobao.item.templates.get 获取用户宝贝详情页模板名称
        
        查询当前登录用户的店铺的宝贝详情页的模板名称'''
        request = TOPRequest('taobao.item.templates.get')
        self.create(self.execute(request, session))
        return self
    

class ItemSearch(TOP):
    '''商品搜索'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ItemSearch, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'items':Item,'item_categories':ItemCategory}
        self.fields = ['items','item_categories']
    

class Product(TOP):
    '''产品结构'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Product, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate, 'product_imgs':ProductImg,'product_prop_imgs':ProductPropImg}
        self.fields = ['product_id','outer_id','created','tsc','cid','cat_name','props','props_str','binds_str','sale_props_str','collect_num','name','binds','sale_props','price','desc','pic_url','modified','product_imgs','product_prop_imgs','status','level','pic_path','vertical_market','customer_props','property_alias']
    
    def add(self, cid, price, image, name, desc, major, market_time, property_alias, session, **kwargs):
        '''taobao.product.add 上传一个产品，不包括产品非主图和属性图片
        
        获取类目ID，必需是叶子类目ID；调用taobao.itemcats.get.v2获取 传入关键属性,结构:pid:vid;pid:vid.调用taobao.itemprops.get.v2获取pid, 调用taobao.itempropvalues.get获取vid;如果碰到用户自定义属性,请用customer_props.'''
        request = TOPRequest('taobao.product.add')
        request['cid'] = cid
        request['price'] = price
        request['image'] = image
        request['name'] = name
        request['desc'] = desc
        request['major'] = major
        request['market_time'] = market_time
        request['property_alias'] = property_alias
        for k, v in kwargs.iteritems():
            if k not in ('outer_id', 'props', 'binds', 'sale_props', 'customer_props', 'order_by', 'ww_status', 'post_free', 'location_state', 'location_city', 'is_3D', 'start_score', 'end_score', 'start_volume', 'end_volume', 'one_station', 'is_cod', 'is_mall', 'is_prepay', 'genuine_security', 'promoted_service', 'stuff_status', 'start_price', 'end_price', 'page_no', 'page_size', 'auction_flag', 'auto_post', 'has_discount', 'is_xinpin') and v==None: continue
            if k == 'location_state': k = 'location.state'
            if k == 'location_city': k = 'location.city'
            request[k] = v
        self.create(self.execute(request, session)['product'])
        return self
    
    def get(self, fields=[], product_id=None, cid=None, props=None):
        '''taobao.product.get 获取一个产品的信息
        
        两种方式查看一个产品详细信息: 传入product_id来查询 传入cid和props来查询'''
        request = TOPRequest('taobao.product.get')
        if not fields:
            fields = self.fields
        request['fields'] = fields
        if product_id!=None: request['product_id'] = product_id
        if cid!=None: request['cid'] = cid
        if props!=None: request['props'] = props
        self.create(self.execute(request)['product'])
        return self
    
    def update(self, product_id, session, **kwargs):
        '''taobao.product.update 修改一个产品，可以修改主图，不能修改子图片
        
        传入产品ID 可修改字段：outer_id,binds,sale_props,name,price,desc,image 注意：1.可以修改主图,不能修改子图片,主图最大500K,目前仅支持GIF,JPG 2.商城卖家产品发布24小时后不能作删除或修改操作'''
        request = TOPRequest('taobao.product.update')
        request['product_id'] = product_id
        for k, v in kwargs.iteritems():
            if k not in ('outer_id', 'binds', 'sale_props', 'price', 'desc', 'image', 'name', 'major', 'native_unkeyprops') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session)['product'])
        return self
    

class Products(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Products, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'products':Product}
        self.fields = ['products', 'total_results']
    
    def get(self, nick, fields=[], props=None, page_no=None, page_size=None):
        '''taobao.products.get 获取产品列表
        
        根据淘宝会员帐号搜索所有产品信息 注意：支持分页，每页最多返回100条,默认值为40,页码从1开始，默认为第一页'''
        request = TOPRequest('taobao.products.get')
        request['nick'] = nick
        if not fields:
            product = Product()
            fields = product.fields
        request['fields'] = fields
        if props!=None: request['props'] = props
        if page_no!=None: request['page_no'] = page_no
        if page_size!=None: request['page_size'] = page_size
        self.create(self.execute(request))
        return self.products
    
    def search(self, fields=[], **kwargs):
        '''taobao.products.search 搜索产品信息
        
        两种方式搜索所有产品信息(二种至少传一种): 传入关键字q搜索 传入cid和props搜索 返回值支持:product_id,name,pic_path,cid,props,price,tsc 当用户指定了cid并且cid为垂直市场（3C电器城、鞋城）的类目id时，默认只返回小二确认的产品。如果用户没有指定cid，或cid为普通的类目，默认返回商家确认或小二确认的产品。如果用户自定了status字段，以指定的status类型为准'''
        request = TOPRequest('taobao.products.search')
        if not fields:
            product = Product()
            fields = product.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('q', 'cid', 'props', 'status', 'page_no', 'page_size', 'vertical_market') and v==None: continue
            request[k] = v
        self.create(self.execute(request))
        return self.products


