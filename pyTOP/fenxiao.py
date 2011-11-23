#!/usr/bin/env python
# encoding: utf-8
"""
fenxiao.py

提供了分销商信息和采购单信息的查询以及分销产品的添加和更新等功能

Created by 徐 光硕 on 2011-11-23.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class Discount(TOP):
    '''折扣信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Discount, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'details':DiscountDetail, 'created':TOPDate, 'modified':TOPDate}
        self.fields = ['discount_id','name','details','created','modified']
    
    def add(self, discount_name, target_types, target_ids, discount_types, discount_values, session):
        '''taobao.fenxiao.discount.add 新增等级折扣
        
        新增等级折扣'''
        request = TOPRequest('taobao.fenxiao.discount.add')
        request['discount_name'] = discount_name
        request['target_types'] = target_types
        request['target_ids'] = target_ids
        request['discount_types'] = discount_types
        request['discount_values'] = discount_values
        self.create(self.execute(request, session), fields=['discount_id'])
        return self.discount_id
    
    def update(self, session, **kwargs):
        '''taobao.fenxiao.discount.update 修改等级折扣
        
        修改等级折扣'''
        request = TOPRequest('taobao.fenxiao.discount.update')
        for k, v in kwargs.iteritems():
            if k not in ('discount_id', 'discount_name', 'discount_status', 'detail_ids', 'target_types', 'target_ids', 'discount_types', 'discount_values', 'detail_statuss') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), fields=['is_success',])
        return self.is_success
    

class Discounts(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Discounts, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'discounts':Discount}
        self.fields = ['discounts','total_results']
    
    def get(self, session, discount_id=None, ext_fields=None):
        '''taobao.fenxiao.discounts.get 获取折扣信息
        
        查询折扣信息'''
        request = TOPRequest('taobao.fenxiao.discounts.get')
        if discount_id!=None: request['discount_id'] = discount_id
        if ext_fields!=None: request['ext_fields'] = ext_fields
        self.create(self.execute(request, session))
        return self.discounts
    

class DiscountDetail(TOP):
    '''折扣详情信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(DiscountDetail, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate}
        self.fields = ['discount_id','target_type','target_id','target_name','discount_type','discount_value','created','modified']
    

class FenxiaoSku(TOP):
    '''分销产品SKU'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(FenxiaoSku, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['standard_price','id','quantity','properties','cost_price','dealer_cost_price','name','outer_id']
    

class FenxiaoItemRecord(TOP):
    '''分销商品下载记录'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(FenxiaoItemRecord, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate}
        self.fields = ['distributor_id','item_id','product_id','trade_type','created','modified']
    

class Cooperation(TOP):
    '''合作分销关系'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Cooperation, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'start_date':TOPDate, 'end_date':TOPDate}
        self.fields = ['cooperate_id','distributor_id','distributor_nick','product_line','grade_id','trade_type','auth_payway','supplier_id','supplier_nick','start_date','end_date','status']
    
    def get(self, session, **kwargs):
        '''taobao.fenxiao.cooperation.get 获取供应商的合作关系信息
        
        获取供应商的合作关系信息'''
        request = TOPRequest('taobao.fenxiao.cooperation.get')
        for k, v in kwargs.iteritems():
            if k not in ('status', 'start_date', 'end_date', 'trade_type', 'page_no', 'page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), fields=['total_results','cooperations'], models={'cooperations':Cooperation})
        return self.cooperations
    
    def update(self, distributor_id, grade_id, session, trade_type=None):
        '''taobao.fenxiao.cooperation.update 更新合作关系等级
        
        供应商更新合作的分销商等级'''
        request = TOPRequest('taobao.fenxiao.cooperation.update')
        request['distributor_id'] = distributor_id
        request['grade_id'] = grade_id
        if trade_type!=None: request['trade_type'] = trade_type
        self.create(self.execute(request, session), fields=['is_success'])
        return self.is_success
    

class FenxiaoGrade(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(FenxiaoGrade, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'modified':TOPDate}
        self.fields = ['grade_id','name','created','modified']
    

class FenxiaoGrades(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(FenxiaoGrades, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'fenxiao_grades':FenxiaoGrade}
        self.fields = ['total_results','fenxiao_grades']
    
    def get(self, session):
        '''taobao.fenxiao.grades.get 分销商等级查询
        
        根据供应商ID，查询他的分销商等级信息'''
        request = TOPRequest('taobao.fenxiao.grades.get')
        self.create(self.execute(request, session))
        return self.fenxiao_grades
    

class Receiver(TOP):
    '''收货人详细信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Receiver, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['name','phone','mobile_phone','address','district','city','zip','state']
    

class LoginUser(TOP):
    '''登录分销用户信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(LoginUser, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate}
        self.fields = ['user_id','nick','user_type','create_time']
    
    def get(self, session):
        '''taobao.fenxiao.login.user.get 获取分销用户登录信息
        
        获取用户登录信息'''
        request = TOPRequest('taobao.fenxiao.login.user.get')
        self.create(self.execute(request, session)['login_user'])
        return self
    

class Distributor(TOP):
    '''分销API返回数据结构'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Distributor, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'starts':TOPDate, 'created':TOPDate}
        self.fields = ['distributor_id','full_name','category_id','level','appraise','starts','user_id','created','alipay_account','contact_person','distributor_name','email','mobile_phone','phone','shop_web_link']
    
    def items_get(self, session, **kwargs):
        '''taobao.fenxiao.distributor.items.get 查询商品下载记录
        
        供应商查询分销商商品下载记录。'''
        request = TOPRequest('taobao.fenxiao.distributor.items.get')
        for k, v in kwargs.iteritems():
            if k not in ('distributor_id', 'start_modified', 'end_modified', 'page_no', 'page_size', 'product_id') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), fields=['total_results','records'], models={'records':FenxiaoItemRecord})
        return self.records
    

class Distributors(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Distributors, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'distributors':Distributor}
        self.fields = ['distributors',]
    
    def get(self, nicks, session):
        '''taobao.fenxiao.distributors.get 获取分销商信息
        
        查询和当前登录供应商有合作关系的分销商的信息'''
        request = TOPRequest('taobao.fenxiao.distributors.get')
        request['nicks'] = nicks
        self.create(self.execute(request, session))
        return self.distributors
    

class PurchaseOrder(TOP):
    '''采购单及子采购单信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(PurchaseOrder, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'receiver':Receiver, 'created':TOPDate, 'pay_time':TOPDate, 'consign_time':TOPDate, 'modified':TOPDate, 'sub_purchase_orders':SubPurchaseOrder}
        self.fields = ['supplier_memo','fenxiao_id','pay_type','trade_type','distributor_from','id','status','buyer_nick','memo','tc_order_id','receiver','shipping','logistics_company_name','logistics_id','supplier_from','supplier_username','distributor_username','created','alipay_no','total_fee','post_fee','distributor_payment','snapshot_url','pay_time','consign_time','modified','sub_purchase_orders']
    

class FenxiaoProduct(TOP):
    '''分销产品'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(FenxiaoProduct, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'upshelf_time':TOPDate, 'created':TOPDate, 'modified':TOPDate, 'skus':FenxiaoSku}
        self.fields = ['discount_id','trade_type','standard_price','upshelf_time','is_authz','category_id','properties','property_alias','input_properties','description','dealer_cost_price','pid','name','productcat_id','cost_price','retail_price_low','retail_price_high','outer_id','quantity','alarm_number','pictures','desc_path','prov','city','postage_type','postage_id','postage_ordinary','postage_fast','postage_ems','have_invoice','have_guarantee','status','items_count','orders_count','created','modified','skus']
    
    def add(self, name, productcat_id, standard_price, retail_price_low, retail_price_high, category_id, quantity, alarm_number, desc, prov, city, postage_type, have_invoice, have_guarantee, session, **kwargs):
        '''taobao.fenxiao.product.add 添加产品
        
        添加分销平台产品数据。业务逻辑与分销系统前台页面一致
        
        - 产品图片默认为空 
        - 产品发布后默认为下架状态'''
        request = TOPRequest('taobao.fenxiao.product.add')
        request['name'] = name
        request['productcat_id'] = productcat_id
        request['standard_price'] = standard_price
        request['retail_price_low'] = retail_price_low
        request['retail_price_high'] = retail_price_high
        request['category_id'] = category_id
        request['quantity'] = quantity
        request['alarm_number'] = alarm_number
        request['desc'] = desc
        request['prov'] = prov
        request['city'] = city
        request['postage_type'] = postage_type
        request['have_invoice'] = have_invoice
        request['have_guarantee'] = have_guarantee
        for k, v in kwargs.iteritems():
            if k not in ('cost_price', 'outer_id', 'postage_id', 'postage_ordinary', 'postage_fast', 'postage_ems', 'discount_id', 'trade_type','is_authz','pic_path','image','properties','property_alias','input_properties','sku_standard_prices','sku_cost_prices','sku_outer_ids','sku_quantitys','sku_properties','dealer_cost_price','sku_dealer_cost_prices') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), fields=['pid','created'], models={'created':TOPDate})
        return self
    
    def image_delete(self, product_id, position, session):
        '''taobao.fenxiao.product.image.delete 产品图片删除
        
        产品图片删除，只删除图片信息，不真正删除图片'''
        request = TOPRequest('taobao.fenxiao.product.image.delete')
        request['product_id'] = product_id
        request['position'] = position
        self.create(self.execute(request, session), fields=['result','created'], models={'created':TOPDate})
        return self
    
    def image_upload(self, product_id, position, session, pic_path=None, image=None):
        '''taobao.fenxiao.product.image.upload 产品图片上传
        
        产品主图图片空间相对路径或绝对路径添加或更新，或者是图片上传。如果指定位置的图片已存在，则覆盖原有信息，如果位置为1,自动设为主图。'''
        request = TOPRequest('taobao.fenxiao.product.image.upload')
        request['product_id'] = product_id
        request['position'] = position
        if pic_path!=None: request['pic_path'] = pic_path
        if image!=None: request['image'] = image
        self.create(self.execute(request, session), fields=['result','created'], models={'created':TOPDate})
        return self
    
    def sku_add(self, product_id, standard_price, properties, session, **kwargs):
        '''taobao.fenxiao.product.sku.add 产品sku添加接口
        
        添加产品SKU信息'''
        request = TOPRequest('taobao.fenxiao.product.sku.add')
        request['product_id'] = product_id
        request['standard_price'] = standard_price
        request['properties'] = properties
        for k, v in kwargs.iteritems():
            if k not in ('quantity', 'agent_cost_price', 'sku_number', 'dealer_cost_price') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), fields=['result','created'], models={'created':TOPDate})
        return self
    
    def sku_delete(self, product_id, properties, session):
        '''taobao.fenxiao.product.sku.delete 产品SKU删除接口
        
        根据sku properties删除sku数据'''
        request = TOPRequest('taobao.fenxiao.product.sku.delete')
        request['product_id'] = product_id
        request['properties'] = properties
        self.create(self.execute(request, session), fields=['result','created'], models={'created':TOPDate})
        return self
    
    def sku_update(self, product_id, properties, session, **kwargs):
        '''taobao.fenxiao.product.sku.update 产品sku编辑接口
        
        产品SKU信息更新'''
        request = TOPRequest('taobao.fenxiao.product.sku.update')
        request['product_id'] = product_id
        request['properties'] = properties
        for k, v in kwargs.iteritems():
            if k not in ('quantity', 'standard_price', 'agent_cost_price', 'sku_number', 'dealer_cost_price') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), fields=['result','created'], models={'created':TOPDate})
        return self
    
    def skus_get(self, product_id, session):
        '''taobao.fenxiao.product.skus.get SKU查询接口
        
        产品sku查询'''
        request = TOPRequest('taobao.fenxiao.product.skus.get')
        request['product_id'] = product_id
        self.create(self.execute(request, session), fields=['skus','total_results'], models={'skus':FenxiaoSku})
        return self.skus
    
    def update(self, pid, session, **kwargs):
        '''taobao.fenxiao.product.update 更新产品
        
        - 更新分销平台产品数据，不传更新数据返回失败
        - 对sku进行增、删操作时，原有的sku_ids字段会被忽略，请使用sku_properties和sku_properties_del。'''
        request = TOPRequest('taobao.fenxiao.product.update')
        request['pid'] = pid
        for k, v in kwargs.iteritems():
            if k not in ('name', 'standard_price', 'cost_price', 'retail_price_low', 'retail_price_high', 'outer_id', 'quantity', 'alarm_number','desc','prov','city','postage_type','postage_id','postage_ordinary','postage_fast','postage_ems','status','sku_ids','sku_cost_prices','sku_quantitys','sku_outer_ids','have_invoice','have_guarantee','discount_id','sku_standard_prices','sku_properties','sku_properties_del','is_authz','pic_path','image','properties','property_alias','input_properties','dealer_cost_price','sku_dealer_cost_prices','category_id') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), fields=['pid','modified'], models={'modified':TOPDate})
        return self
    

class FenxiaoProducts(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(FenxiaoProducts, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'products':FenxiaoProduct}
        self.fields = ['total_results','products']
    
    def get(self, session, **kwargs):
        '''taobao.fenxiao.products.get 查询产品列表
        
        查询供应商的产品数据
        - 入参传入pids将优先查询，即只按这个条件查询。 
        - 入参传入sku_number将优先查询(没有传入pids)，即只按这个条件查询(最多显示50条) 
        - 入参fields传skus将查询sku的数据，不传该参数默认不查询，返回产品的其它信息。 
        - 入参fields传入images将查询多图数据，不传只返回主图数据。 
        - 入参fields仅对传入pids生效（只有按ID查询时，才能查询额外的数据） 
        - 查询结果按照产品发布时间倒序，即时间近的数据在前。'''
        request = TOPRequest('taobao.fenxiao.products.get')
        for k, v in kwargs.iteritems():
            if k not in ('outer_id', 'productcat_id', 'status', 'pids', 'fields', 'start_modified', 'end_modified', 'page_no','page_size','sku_number','is_authz') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.products
    

class SubPurchaseOrder(TOP):
    '''子采购单详细信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(SubPurchaseOrder, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'pay_time':TOPDate, 'consign_time':TOPDate, 'modified':TOPDate, 'sub_purchase_orders':SubPurchaseOrder}
        self.fields = ['status','refund_fee','id','fenxiao_id','sub_tc_order_id','tc_order_id','sku_id','old_sku_properties','item_id','item_outer_id','sku_outer_id','sku_properties','num','title','price','snapshot_url','created','total_fee','distributor_payment','buyer_payment']
    

class ProductCat(TOP):
    '''产品线'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ProductCat, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['id','retail_low_percent','retail_high_percent','name','product_num']
    

class ProductCats(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ProductCats, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'productcats':ProductCat}
        self.fields = ['total_results','productcats']
    
    def get(self, session, fields=None):
        '''taobao.fenxiao.productcats.get 查询产品线列表
        
        查询供应商的所有产品线数据。根据登陆用户来查询，不需要其他入参'''
        request = TOPRequest('taobao.fenxiao.productcats.get')
        if fields: request['fields'] = fields
        self.create(self.execute(request, session))
        return self.productcats
    

class FenxiaoOrder(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(FenxiaoOrder, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['is_success',]
    
    def confirm_paid(self, purchase_order_id, session, confirm_remark=None):
        '''taobao.fenxiao.order.confirm.paid 确认收款
        
        供应商确认收款（非支付宝交易）。'''
        request = TOPRequest('taobao.fenxiao.order.confirm.paid')
        request['purchase_order_id'] = purchase_order_id
        if confirm_remark!=None: request['confirm_remark'] = confirm_remark
        self.create(self.execute(request, session))
        return self.is_success
    

class FenxiaoOrders(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(FenxiaoOrders, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'purchase_orders':PurchaseOrder}
        self.fields = ['total_results','purchase_orders']
    
    def get(self, session, **kwargs):
        '''taobao.fenxiao.orders.get 查询采购单信息
        
        分销商或供应商均可用此接口查询采购单信息. (发货处理请调用物流API中的发货接口)'''
        request = TOPRequest('taobao.fenxiao.orders.get')
        for k, v in kwargs.iteritems():
            if k not in ('status', 'start_created', 'end_created', 'time_type', 'page_no', 'page_size', 'purchase_order_id') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.purchase_orders
    
