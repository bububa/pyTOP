#!/usr/bin/env python
# encoding: utf-8
"""
 logistics.py

Created by 徐 光硕 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate
from user import Location
from trade import Task, Subtask

class TransitStepInfo(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''物流跟踪信息的一条'''
        super(TransitStepInfo, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'status_time':TOPDate}
        self.fields = ['status_time','status_desc']
    

class Area(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''地址区域结构'''
        super(Area, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['id','type', 'name', 'parent_id', 'zip']
    

class Areas(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''地址区域结构'''
        super(Areas, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'areas':Area}
        self.fields = ['areas',]
    
    def get(self, fields=[]):
        '''taobao.areas.get 查询地址区域
        ===================================
        查询标准地址区域代码信息 参考：http://www.stats.gov.cn/tjbz/xzqhdm/t20100623_402652267.htm'''
        request = TOPRequest('taobao.areas.get')
        if not fields:
            area = Area()
            fields = area.fields
        request['fields'] = fields
        self.create(self.execute(request))
        return self.areas
    

class DeliveryTemplate(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''运费模板对象'''
        super(DeliveryTemplate, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'fee_list':TopFee}
        self.fields = ['template_id','name', 'assumer', 'valuation', 'fee_list', 'supports', 'created', 'modified']
    
    def add(self, name, assumer, valuation, template_types, template_dests, template_start_standards, template_start_fees, template_add_standards, template_add_fees, session):
        '''taobao.delivery.template.add 新增运费模板
        ===================================
        新增运费模板'''
        request = TOPRequest('taobao.delivery.template.add')
        request['name'] = name
        request['assumer'] = assumer
        request['valuation'] = valuation
        request['template_types'] = template_types
        request['template_dests'] = template_dests
        request['template_start_standards'] = template_start_standards
        request['template_start_fees'] = template_start_fees
        request['template_add_standards'] = template_add_standards
        request['template_add_fees'] = template_add_fees
        self.create(self.execute(request, session)['delivery_template'])
        return self
    
    def delete(self, template_id, session):
        '''taobao.delivery.template.delete 删除运费模板
        ===================================
        根据用户指定的模板ID删除指定的模板'''
        request = TOPRequest('taobao.delivery.template.delete')
        request['template_id'] = template_id
        self.create(self.execute(request, session), fields=['complete', ])
        return self.complete
    
    def get(self, template_ids, session, fields=[]):
        '''taobao.delivery.template.get 获取用户指定运费模板信息
        ===================================
        获取用户指定运费模板信息'''
        request = TOPRequest('taobao.delivery.template.get')
        request['template_ids'] = template_ids
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request, session), fields=['delivery_templates', 'total_results'], models={'delivery_templates':DeliveryTemplate})
        return self.delivery_templates
    
    def update(self, template_id, assumer, template_types, template_dests, template_start_standards, template_start_fees, template_add_standards, template_add_fees, session, name=None):
        '''taobao.delivery.template.update 修改运费模板
        ===================================
        修改运费模板'''
        request = TOPRequest('taobao.delivery.template.update')
        if name!=None: request['name'] = name
        request['assumer'] = assumer
        request['template_id'] = template_id
        request['template_types'] = template_types
        request['template_dests'] = template_dests
        request['template_start_standards'] = template_start_standards
        request['template_start_fees'] = template_start_fees
        request['template_add_standards'] = template_add_standards
        request['template_add_fees'] = template_add_fees
        self.create(self.execute(request, session), fields=['complete', ])
        return self.complete
    

class DeliveryTemplates(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''运费模板对象'''
        super(DeliveryTemplates, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'delivery_templates':DeliveryTemplate}
        self.fields = ['delivery_templates','total_results']
    
    def get(self, session):
        '''taobao.delivery.templates.get 获取用户下所有模板
        ===================================
        根据用户ID获取用户下所有模板'''
        request = TOPRequest('taobao.delivery.templates.get')
        self.create(self.execute(request, session))
        return self.delivery_templates
    

class PartnerDetail(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''物流公司详细信息'''
        super(PartnerDetail, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['account_no','company_code', 'company_id', 'full_name', 'company_name', 'wangwang_id', 'reg_mail_no']
    

class LogisticsCompany(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''物流公司基础数据结构'''
        super(LogisticsCompany, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['id','code', 'name', 'reg_mail_no']
    

class LogisticsCompanies(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(LogisticsCompanies, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'logistics_companies':LogisticsCompany}
        self.fields = ['logistics_companies',]

    def get(self, session, is_recommended=None, order_mode=None, fields=[]):
        '''taobao.logistics.companies.get 查询物流公司信息
        ===================================
        查询淘宝网合作的物流公司信息，用于发货接口。'''
        request = TOPRequest('taobao.logistics.companies.get')
        if not fields:
            lc = LogisticsCompany()
            fields = lc.fields
        request['fields'] = fields
        if is_recommended!=None: request['is_recommended'] = is_recommended
        if order_mode!=None: request['order_mode'] = order_mode
        self.create(self.execute(request, session))
        return self.logistics_companies
    

class PostageMode(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''运费方式模板收费方式'''
        super(PostageMode, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['postage_id','id', 'type', 'dests', 'price', 'increase']
    

class Shipping(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''物流数据结构'''
        super(Shipping, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models ={'delivery_start':TOPDate, 'delivery_end':TOPDate, 'location':Location, 'created':TOPDate, 'modified':TOPDate}
        self.fields = ['tid','order_code', 'seller_nick', 'buyer_nick', 'delivery_start', 'delivery_end', 'out_sid', 'item_title', 'receiver_name', 'receiver_phone', 'receiver_mobile', 'location', 'status', 'type', 'freight_payer', 'seller_confirm', 'company_name', 'is_success', 'created', 'modified']
    

class TopFee(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''运费模板中运费信息对象'''
        super(TopFee, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['service_type','destination', 'start_standard', 'start_fee', 'add_standard', 'add_fee']
    

class Postage(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''运费模板结构'''
        super(Postage, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models ={'postage_modes':PostageMode, 'created':TOPDate, 'modified':TOPDate}
        self.fields = ['postage_id','name', 'memo', 'created', 'modified', 'post_price', 'post_increase', 'express_price', 'express_increase', 'ems_price', 'ems_increase', 'postage_modes']
    
    def add(self, name, session, **kwargs):
        '''taobao.postage.add 添加邮费模板
        ===================================
        添加邮费模板 
        新增的邮费模板属于当前会话用户 
        postage_mode_types、postage_mode_dests、postage_mode_prices、 postage_mode_increases四个字段组合起来表示邮费的子模板列表。每个邮费子模板都包含了type（邮费类型，有post、 express、ems可以选择）、dest（邮费模板应用地区，每个模板可以使用于多个地区，每个地区填入他的代码，地区与地区之间用半角逗号分隔）、 price（邮费基价）、increment（邮费增价）四个部分。如果有多个子模板，则将他们的4个部分分别组合，之间用半角分号隔开（注意每个模板的每个部分的位置要一样。即，子模板1号的type、dest、price、increment都要排在这四个参数的第一位；子模板2号要排在第二位……以此类推）'''
        request = TOPRequest('taobao.postage.add')
        request['name'] = name
        for k, v in kwargs.iteritems():
            if k not in ('post_price', 'post_increase', 'express_price', 'express_increase', 'ems_price', 'ems_increase', 'memo', 'postage_mode_types', 'postage_mode_dests', 'postage_mode_prices', 'postage_mode_increases') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session)['postage'])
        return self
    
    def delete(self, postage_id, session):
        '''taobao.postage.delete 删除单个运费模板
        ===================================
        删除单个邮费模板 postage_id对应的邮费模板要属于当前会话用户'''
        request = TOPRequest('taobao.postage.delete')
        request['postage_id'] = postage_id
        self.create(self.execute(request, session)['postage'])
        return self
    
    def get(self, postage_id, nick, fields=[]):
        '''taobao.postage.get 获取单个运费模板
        ===================================
        获取单个邮费模板 
        postage_id对应的邮费模板要属于nick所对应的用户 
        Q：是否必须是模板所有者才能够使用这个接口? 
        A： 不是的,只要给出了邮费模板id和创建者的昵称就可以使用'''
        request = TOPRequest('taobao.postage.get')
        request['postage_id'] = postage_id
        request['nick'] = nick
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request)['postage'])
        return self
    
    def update(self, postage_id, session, **kwargs):
        '''taobao.postage.update 修改邮费模板
        ===================================
        修改邮费模板 
        修改的邮费模板属于当前会话用户 
        修改的邮费子模板要传入子模板id，否则作为添加子模板处理。postage_mode_types、 postage_mode_dests、postage_mode_prices、postage_mode_increases四个字段的处理逻辑见 taobao.postage.add中的描述'''
        request = TOPRequest('taobao.postage.update')
        request['postage_id'] = postage_id
        for k, v in kwargs.iteritems():
            if k not in ('post_price', 'post_increase', 'express_price', 'express_increase', 'ems_price', 'ems_increase', 'name', 'memo', 'postage_mode_ids', 'postage_mode_types', 'postage_mode_dests', 'postage_mode_prices', 'postage_mode_increases', 'postage_mode_optTypes', 'remove_post', 'remove_express', 'remove_ems') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session)['postage'])
        return self
    

class Postages(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''运费模板结构'''
        super(Postages, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models ={'postages':Postage}
        self.fields = ['postages','total_results']
    
    def get(self, session, fields=[]):
        '''taobao.postages.get 获取卖家的运费模板
        ===================================
        获得当前会话用户的所有邮费模板'''
        request = TOPRequest('taobao.postages.get')
        if not fields:
            postage = Postage()
            fields = postage.fields
        request['fields'] = fields
        self.create(self.execute(request, session))
        return self.postages
    

class AddressResult(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''地址库返回数据信息'''
        super(AddressResult, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models ={'modify_date':TOPDate}
        self.fields = ['postage_id','contact_name', 'province', 'city', 'country', 'addr', 'zip_code', 'phone', 'mobile_phone', 'seller_company', 'memo', 'area_id', 'send_def', 'get_def', 'cancel_def', 'modify_date']
    

class LogisticsPartner(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''查询揽送范围之内的物流公司信息'''
        super(LogisticsPartner, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models ={'partner':ParnterDetail}
        self.fields = ['cover_remark','uncover_remark', 'partner']
    

class LogisticsPartners(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''查询揽送范围之内的物流公司信息'''
        super(LogisticsPartners, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models ={'logistics_partners':LogisticsPartner}
        self.fields = ['logistics_partners',]
    
    def get(self, service_type, source_id=None, target_id=None, goods_value=None):
        '''taobao.logistics.partners.get 查询支持起始地到目的地范围的物流公司
        ===================================
        查询物流公司信息（可以查询目的地可不可达情况）'''
        request = TOPRequest('taobao.logistics.partners.get')
        request['service_type'] = service_type
        if source_id!=None: request['source_id'] = source_id
        if target_id!=None: request['target_id'] = target_id
        if goods_value!=None: request['goods_value'] = goods_value
        self.create(self.execute(request))
        return self.logistics_partners
    

class LogisticsAddress(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(LogisticsAddress, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'address_result':AddressResult}
        self.fields = ['address_result',]
    
    def add(self, contact_name, province, city, addr, session, **kwargs):
        '''taobao.logistics.address.add 卖家地址库新增接口
        ===================================
        通过此接口新增卖家地址库,卖家最多可添加5条地址库,新增第一条卖家地址，将会自动设为默认地址库'''
        request = TOPRequest('taobao.logistics.address.add')
        request['contact_name'] = contact_name
        request['province'] = province
        request['city'] = city
        request['addr'] = addr
        for k, v in kwargs.iteritems():
            if k not in ('country', 'zip_code', 'phone', 'mobile_phone', 'seller_company', 'memo', 'get_def', 'cancel_def') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.address_result
    
    def modify(self, contact_id, contact_name, province, city, addr, session, **kwargs):
        '''taobao.logistics.address.modify 卖家地址库修改
        ===================================
        卖家地址库修改'''
        request = TOPRequest('taobao.logistics.address.modify')
        request['contact_id'] = contact_id
        request['contact_name'] = contact_name
        request['province'] = province
        request['city'] = city
        request['addr'] = addr
        for k, v in kwargs.iteritems():
            if k not in ('country', 'zip_code', 'phone', 'mobile_phone', 'seller_company', 'memo', 'get_def', 'cancel_def') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.address_result
    
    def remove(self, contact_id, session):
        '''taobao.logistics.address.remove 删除卖家地址库
        ===================================
        用此接口删除卖家地址库'''
        request = TOPRequest('taobao.logistics.address.remove')
        request['contact_id'] = contact_id
        self.create(self.execute(request, session))
        return self.address_result
    
    def search(self, session, rdef=None):
        '''taobao.logistics.address.search 查询卖家地址库
        ===================================
        通过此接口查询卖家地址库，'''
        request = TOPRequest('taobao.logistics.address.search')
        if rdef!=None: request['rdef'] = rdef
        self.create(self.execute(request, session), fields=['addresses', ], models={'addresses':AddressResult})
        return self.addresses
    

class LogisticsDummy(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(LogisticsDummy, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'shipping':Shipping}
        self.fields = ['shipping',]
    
    def send(self, tid, session, feature=None):
        '''taobao.logistics.dummy.send 无需物流（虚拟）发货处理
        ===================================
        用户调用该接口可实现无需物流（虚拟）发货,使用该接口发货，交易订单状态会直接变成卖家已发货'''
        request = TOPRequest('taobao.logistics.dummy.send')
        request['tid'] = tid
        if feature!=None: request['feature'] = feature
        self.create(self.execute(request, session))
        return self.shipping
    

class LogisticsOffline(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(LogisticsOffline, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'shipping':Shipping}
        self.fields = ['shipping',]
    
    def send(self, tid, out_sid, company_code, session, sender_id=None, cancel_id=None, feature=None):
        '''taobao.logistics.offline.send 自己联系物流（线下物流）发货
        ===================================
        用户调用该接口可实现自己联系发货（线下物流），使用该接口发货，交易订单状态会直接变成卖家已发货。不支持货到付款、在线下单类型的订单。'''
        request = TOPRequest('taobao.logistics.offline.send')
        request['tid'] = tid
        request['out_sid'] = out_sid
        request['company_code'] = company_code
        if feature!=None: request['feature'] = feature
        if sender_id!=None: request['sender_id'] = sender_id
        if cancel_id!=None: request['cancel_id'] = cancel_id
        self.create(self.execute(request, session))
        return self.shipping
    

class LogisticsOnline(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(LogisticsOnline, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
    
    def cancel(self, tid, session):
        '''taobao.logistics.online.cancel 取消物流订单接口
        ===================================
        调此接口取消发货的订单，重新选择物流公司发货。前提是物流公司未揽收货物。对未发货和已经被物流公司揽收的物流订单，是不能取消的。'''
        request = TOPRequest('taobao.logistics.online.cancel')
        request['tid'] = tid
        self.create(self.execute(request, session), fields = ['is_success','modify_time','recreated_order_id'], models = {'modify_time':TOPDate})
        return self
    
    def confirm(self, tid, out_sid, session):
        '''taobao.logistics.online.confirm 确认发货通知接口
        ===================================
        确认发货的目的是让交易流程继承走下去，确认发货后交易状态会由【买家已付款】变为【卖家已发货】，然后买家才可以确认收货，货款打入卖家账号。货到付款的订单除外'''
        request = TOPRequest('taobao.logistics.online.confirm')
        request['tid'] = tid
        request['out_sid'] = out_sid
        self.create(self.execute(request, session), fields = ['shipping',], models = {'shipping':Shipping})
        return self.shipping
    
    def send(self, tid, company_code, session, **kwargs):
        '''taobao.logistics.online.send 在线订单发货处理（支持货到付款）
        ===================================
        用户调用该接口可实现在线订单发货（支持货到付款） 
        调用该接口实现在线下单发货，有两种情况：
        如果不输入运单号的情况：交易状态不会改变，需要调用taobao.logistics.online.confirm确认发货后交易状态才会变成卖家已发货。
        如果输入运单号的情况发货：交易订单状态会直接变成卖家已发货 。'''
        request = TOPRequest('taobao.logistics.online.send')
        request['tid'] = tid
        request['company_code'] = company_code
        for k, v in kwargs.iteritems():
            if k not in ('out_sid', 'sender_id', 'cancel_id', 'feature') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), fields=['shipping', ], models={'shipping':Shipping})
        return self.shipping
    

class Orders(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(Orders, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'shippings':Shipping}
        self.fields = ['shippings', 'total_results']
    
    def detail_get(self, session, fields=[], **kwargs):
        '''taobao.logistics.orders.detail.get 批量查询物流订单,返回详细信息
        ===================================
        查询物流订单的详细信息，涉及用户隐私字段。（注：该API主要是提供给卖家查询物流订单使用，买家查询物流订单，建议使用taobao.logistics.trace.search）'''
        request = TOPRequest('taobao.logistics.orders.detail.get')
        if not fields:
            shipping = Shipping()
            fields = shipping.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('tid', 'buyer_nick', 'status', 'seller_confirm', 'receiver_name', 'start_created', 'end_created', 'freight_payer', 'type', 'page_no', 'page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.shippings
    
    def get(self, session, fields=[], **kwargs):
        '''taobao.logistics.orders.get 批量查询物流订单
        ===================================
        批量查询物流订单。（注：该API主要是提供给卖家查询物流订单使用，买家查询物流订单，建议使用taobao.logistics.trace.search）'''
        request = TOPRequest('taobao.logistics.orders.get')
        if not fields:
            shipping = Shipping()
            fields = shipping.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('tid', 'buyer_nick', 'status', 'seller_confirm', 'receiver_name', 'start_created', 'end_created', 'freight_payer', 'type', 'page_no', 'page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.shippings
    

class LogisticsTrace(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        super(LogisticsTrace, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'trace_list':TransitStepInfo}
        self.fields = ['out_sid','company_name','tid','status','trace_list']
    
    def search(self, tid, seller_nick):
        '''taobao.logistics.trace.search 物流流转信息查询
        ===================================
        用户根据淘宝交易号查询物流流转信息，如2010-8-10 15：23：00到达杭州集散地'''
        request = TOPRequest('taobao.logistics.address.add')
        request['tid'] = tid
        request['seller_nick'] = seller_nick
        self.create(self.execute(request))
        return self
    

class TopatsDelivery(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''运费模板结构'''
        super(TopatsDelivery, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models ={'task':Task}
        self.fields = ['task',]
        
    def send(self, tids, session, **kwargs):
        '''taobao.topats.delivery.send 异步批量物流发货api
        ===================================
        使用指南：http://open.taobao.com/dev/index.php/ATS%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97 1.提供异步批量物流发货功能 2.一次最多发货40个订单 3.提交任务会进行初步任务校验，如果成功会返回任务号和创建时间，如果失败就报错 4.可以接收淘宝发出的任务完成消息，也可以过一段时间来取结果。获取结果接口为taobao.topats.result.get 5.此api执行完成发送的通知消息格式为{"task":{"task_id":123456,"created":"2010-8-19"}}'''
        request = TOPRequest('taobao.postage.add')
        request['tids'] = tids
        for k, v in kwargs.iteritems():
            if k not in ('company_codes', 'out_sids', 'seller_name', 'seller_area_id', 'seller_address', 'seller_zip', 'seller_phone', 'seller_mobile', 'order_types', 'memos') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.task
    
