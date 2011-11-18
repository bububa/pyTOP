#!/usr/bin/env python
# encoding: utf-8
"""
trade.py

Created by 徐 光硕 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class PromotionDetail(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''交易的优惠信息详情'''
        super(PromotionDetail, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['id','promotion_name','discount_fee','gift_item_name']
    

class OrderAmount(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''子订单的帐务数据结构'''
        super(OrderAmount, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['payment','oid','title','sku_properties_name','num','price','discount_fee','adjust_fee','promotion_name','num_iid','sku_id']
    

class Order(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''订单结构'''
        super(Order, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'modified':TOPDate}
        self.fields = ['total_fee','discount_fee','adjust_fee','payment','modified','item_meal_id','status']
    
    def ordersku_update(self, oid, sku_id=None, sku_props=None):
        '''taobao.trade.ordersku.update 更新交易订单的销售属性
        ==============================
        需要商家或以上权限才可调用此接口，可重复调用本接口更新交易备注，本接口同时具有添加备注的功能'''
        request = TOPRequest('taobao.trade.ordersku.update')
        request['oid'] = oid
        if sku_id!=None: request['sku_id'] = sku_id
        if sku_props!=None: request['sku_props'] = sku_props
        self.create(self.execute(request)['order'])
        return self
    

class TradeAmount(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''交易订单的帐务信息详情'''
        super(TradeAmount, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate, 'pay_time':TOPDate, 'end_time':TOPDate, 'promotion_details':PromotionDetail, 'order_amounts':OrderAmount}
        self.fields = ['buyer_cod_fee','seller_cod_fee','express_agency_fee','tid','alipay_no','created','pay_time','end_time','total_fee','post_fee','cod_fee','payment','commission_fee','buyer_obtain_point_fee','promotion_details','order_amounts']
    
    def get(self, tid, session, fields=[]):
        '''taobao.trade.amount.get 交易订单帐务查询
        ==============================
        卖家查询该笔交易订单的资金帐务相关的数据； 
        1. 只供卖家使用，买家不可使用 
        2. 可查询所有的状态的订单，但不同状态时订单的相关数据可能会有不同'''
        request = TOPRequest('taobao.trade.amount.get')
        request['tid'] = tid
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request, session)['trade_amount'])
        return self
    

class TradeAccountDetail(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''淘宝卖家绑定的支付宝账户的财务明细'''
        super(TradeAccountDetail, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['type','memo','taobao_tid','alipay_tid','date','account_balance','income','expense','trade_partner','trade_locale','item_name']
    

class Task(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''批量异步任务结果'''
        super(Task, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'subtasks':Subtask, 'created':TOPDate}
        self.fields = ['download_url','task_id','status','subtasks','method','created']
    
    def get(self, task_id):
        '''taobao.topats.result.get 获取异步任务结果
        ==============================
        使用指南：http://open.taobao.com/doc/detail.htm?id=30 1.此接口用于获取异步任务处理的结果，传入的task_id必需属于当前的appKey才可以 2.此接口只返回执行完成的任务结果，未执行完的返回结果里面不包含任务结果，只有任务id，执行状态 3.执行完成的每个task的子任务结果内容与单个任务的结果结构一致。如：taobao.topats.trades.fullinfo.get返回的子任务结果就会是Trade的结构体。'''
        request = TOPRequest('taobao.topats.result.get')
        request['task_id'] = task_id
        self.create(self.execute(request)['task'])
        return self
    
    def accountreport_get(self, start_created, end_created, session, fields=[]):
        '''taobao.topats.trade.accountreport.get 异步获取淘宝卖家绑定的支付宝账户的财务明细
        ==============================
        1.提供异步下载用户支付宝对账信息接口 
        2.一次调用最多支持下载3个月的对账信息 
        3.仅能获取2010年6月10日以后的信息 
        4.提交任务会进行初步任务校验，如果成功会返回任务号和创建时间，如果失败就报错 
        5.可以接收淘宝发出的任务完成消息，也可以过一段时间来取结果。获取结果接口为taobao.topats.result.get 
        6.支付宝证书签名方法见文档：“http://open.taobao.com/dev/index.php/如何数字证书签名” 
        7.此api执行完成发送的通知消息格式为{"task":{"task_id":123456,"created":"2010-8-19"}} 
        8.此任务是大数据任务，获取任务结果时只能得到下载url 
        9.子任务结果解析见TradeAccountDetail结构体说明 
        10.此接口执行任务时间段为：00:00:00-09:30:00;11:00:00-14:00:00;17:00:00-20:00:00;22:30:00-23:59:59，只有在这段时间内才能返回查询结果'''
        request = TOPRequest('taobao.topats.trade.accountreport.get')
        request['start_created'] = start_created
        request['end_created'] = end_created
        if not fields:
            tradeAccountDetail = TradeAccountDetail()
            fields = tradeAccountDetail.fields
        request['fields'] = fields
        self.create(self.execute(request, session)['task'])
        return self
    
    def fullinfo_get(self, tids, session, fields=[]):
        '''taobao.topats.trades.fullinfo.get 异步批量获取交易订单详情api
        ==============================
        使用指南：http://open.taobao.com/dev/index.php/ATS%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97 1.提供异步批量获取订单详情功能 2.一次调用最多支持40个订单 3.提交任务会进行初步任务校验，如果成功会返回任务号和创建时间，如果失败就报错 4.可以接收淘宝发出的任务完成消息，也可以过一段时间来取结果。获取结果接口为taobao.topats.result.get 5.此api执行完成发送的通知消息格式为{"task":{"task_id":123456,"created":"2010-8-19"}}果'''
        request = TOPRequest('taobao.topats.trades.fullinfo.get')
        request['tids'] = tids
        if not fields:
            trade = Trade()
            fields = trade.fields
        request['fields'] = fields
        self.create(self.execute(request, session)['task'])
        return self
    

class Trade(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''交易结构'''
        super(Trade, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'pay_time':TOPDate, 'end_time':TOPDate, 'modified':TOPDate, 'created':TOPDate, 'consign_time':TOPDate, 'orders':Order, 'promotion_details':PromotionDetail}
        self.fields = ['end_time','buyer_message','shipping_type','buyer_cod_fee','seller_cod_fee','express_agency_fee','adjust_fee','status','buyer_memo','seller_memo','pay_time','modified','buyer_obtain_point_fee','cod_fee','buyer_flag','seller_flag','trade_from','alipay_warn_msg','alipay_id','cod_status','buyer_area','can_rate','seller_nick','buyer_nick','title','type','created','iid','price','pic_path','num','tid','alipay_no','payment','discount_fee','snapshot_url','snapshot','seller_rate','buyer_rate','trade_memo','point_fee','real_point_fee','total_fee','post_fee','buyer_alipay_no','receiver_name','receiver_state','receiver_city','receiver_district','receiver_address','receiver_zip','receiver_mobile','receiver_phone','consign_time', 'buyer_email','commission_fee','seller_alipay_no','seller_mobile','seller_phone','seller_name','seller_email','available_confirm_fee','has_post_fee','received_payment','is_3D','orders','num_iid','promotion','promotion_details', 'invoice_name', 'alipay_url']
    
    def close(self, tid, close_reason, session):
        '''taobao.trade.close 卖家关闭一笔交易
        ==============================
        关闭一笔订单，可以是主订单或子订单。'''
        request = TOPRequest('taobao.trade.close')
        request['tid'] = tid
        request['close_reason'] = close_reason
        self.create(self.execute(request, session)['trade'])
        return self
    
    def fullinfo_get(self, tid, session, fields=[]):
        '''taobao.trade.fullinfo.get 获取单笔交易的详细信息
        ==============================
        获取单笔交易的详细信息 
        1.只有在交易成功的状态下才能取到交易佣金，其它状态下取到的都是零或空值 
        2.只有单笔订单的情况下Trade数据结构中才包含商品相关的信息 
        3.获取到的Order中的payment字段在单笔子订单时包含物流费用，多笔子订单时不包含物流费用 注：包含以下字段的返回会增加TOP的后台压力，请仅在确实需要的情况下才去获取：commission_fee, buyer_alipay_no, seller_alipay_no, buyer_email, seller_mobile, seller_phone, seller_name, seller_email, timeout_action_time, item_memo, trade_memo, title, available_confirm_fee'''
        request = TOPRequest('taobao.trade.fullinfo.get')
        request['tid'] = tid
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request, session)['trade'])
        return self
    
    def get(self, tid, session, fields=[]):
        '''taobao.trade.get 获取单笔交易的部分信息(性能高)
        ==============================
        获取单笔交易的部分信息'''
        request = TOPRequest('taobao.trade.get')
        request['tid'] = tid
        if not fields:
            fields = self.fields
        request['fields'] = fields
        self.create(self.execute(request, session)['trade'])
        return self
    
    def memo_add(self, tid, memo, session, flag=None):
        '''taobao.trade.memo.add 对一笔交易添加备注
        ==============================
        根据登录用户的身份（买家或卖家），自动添加相应的交易备注,不能重复调用些接口添加备注，需要更新备注请用taobao.trade.memo.update'''
        request = TOPRequest('taobao.trade.memo.add')
        request['tid'] = tid
        request['memo'] = memo
        if flag!=None: request['flag'] = flag
        self.create(self.execute(request, session)['trade'])
        return self
    
    def memo_update(self, tid, session, memo=None, flag=None, reset=None):
        '''taobao.trade.memo.update 修改一笔交易备注
        ==============================
        需要商家或以上权限才可调用此接口，可重复调用本接口更新交易备注，本接口同时具有添加备注的功能'''
        request = TOPRequest('taobao.trade.memo.update')
        request['tid'] = tid
        if memo!=None: request['memo'] = memo
        if flag!=None: request['flag'] = flag
        if reset!=None: request['reset'] = reset
        self.create(self.execute(request, session)['trade'])
        return self
    
    def postage_update(self, tid, post_fee, session):
        '''taobao.trade.postage.update 修改订单邮费价格
        ==============================
        修改订单邮费接口，通过传入订单编号和邮费价格，修改订单的邮费，返回修改时间modified,邮费post_fee,总费用total_fee。'''
        request = TOPRequest('taobao.trade.postage.update')
        request['tid'] = tid
        request['post_fee'] = post_fee
        self.create(self.execute(request, session)['trade'])
        return self
    
    def receivetime_delay(self, tid, days, session):
        '''taobao.trade.receivetime.delay 延长交易收货时间
        ==============================
        延长交易收货时间'''
        request = TOPRequest('taobao.trade.receivetime.delay')
        request['tid'] = tid
        request['days'] = days
        self.create(self.execute(request, session)['trade'])
        return self
    
    def shippingaddress_update(self, tid, session, **kwargs):
        '''taobao.trade.shippingaddress.update 更改交易的收货地址'''
        request = TOPRequest('taobao.trade.shippingaddress.update')
        request['tid'] = tid
        for k, v in kwargs.iteritems():
            if k not in ('receiver_name','receiver_phone','receiver_mobile','receiver_state','receiver_city','receiver_district','receiver_address','receiver_zip') or v==None: continue
            request[k] = v
        self.create(self.execute(request, session)['trade'])
        return self
    
    def snapshot_get(self, tid, session, fields=['snapshot', ]):
        '''taobao.trade.snapshot.get 交易快照查询
        ==============================
        交易快照查询 目前只支持类型为“旺店标准版(600)”或“旺店入门版(610)”的交易 对于“旺店标准版”类型的交易，返回的snapshot字段为交易快照编号 对于“旺店入门版”类型的交易，返回的snapshot字段为JSON结构的数据(其中的shopPromotion包含了优惠，积分等信息）'''
        request = TOPRequest('taobao.trade.snapshot.get')
        request['tid'] = tid
        request['fields'] = fields
        self.create(self.execute(request, session)['trade'])
        return self
    

class Trades(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''批量异步任务的子任务结果'''
        super(Trades, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'trades':Trade}
        self.fields = ['trades','total_results','has_next']
    
    def bought_get(self, session, fields=[], **kwargs):
        '''taobao.trades.bought.get 搜索当前会话用户作为买家达成的交易记录
        ==============================
        搜索当前会话用户作为买家达成的交易记录(目前只能查询三个月以内的订单)'''
        request = TOPRequest('taobao.trades.bought.get')
        if not fields:
            trade = Trade()
            fields = trade.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('start_created','end_created','status','seller_nick','type','page_no','page_size','rate_status') or v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.trades
    
    def sold_get(self, session, fields=[], **kwargs):
        '''taobao.trades.sold.get 搜索当前会话用户作为卖家已卖出的交易数据
        ==============================
        搜索当前会话用户作为卖家已卖出的交易数据(只能获取到三个月以内的交易信息)'''
        request = TOPRequest('taobao.trades.sold.get')
        if not fields:
            trade = Trade()
            fields = trade.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('start_created','end_created','status','buyer_nick','type','page_no','page_size','rate_status','tag') or v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.trades
    
    def sold_increment_get(self, session, fields=[], **kwargs):
        '''taobao.trades.sold.increment.get 搜索当前会话用户作为卖家已卖出的增量交易数据
        ==============================
        1. 搜索当前会话用户作为卖家已卖出的增量交易数据 
        2. 只能查询时间跨度为一天的增量交易记录：start_modified：2011-7-1 16:00:00 end_modified： 2011-7-2 15:59:59（注意不能写成16:00:00） 
        3. 返回数据结果为创建订单时间的倒序 
        4. 只能查询3个月内修改过的数据，超过这个时间的数据无法通过taobao.trade.fullinfo.get获取详情。'''
        request = TOPRequest('taobao.trades.sold.increment.get')
        if not fields:
            trade = Trade()
            fields = trade.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('start_modified','end_modified','status','use_has_next','type','page_no','page_size','tag') or v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.trades
    

class Subtask(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''批量异步任务的子任务结果'''
        super(Subtask, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['sub_task_request','sub_task_result','is_success']
    

class TradeConfirmFee(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''确认收货费用结构'''
        super(TradeConfirmFee, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['confirm_fee','confirm_post_fee','is_last_order']
    
    def get(self, tid, is_detail, session):
        '''taobao.trade.confirmfee.get 获取交易确认收货费用
        ==============================
        获取交易确认收货费用 可以获取主订单或子订单的确认收货费用'''
        request = TOPRequest('taobao.trade.confirmfee.get')
        request['tid'] = tid
        request['is_detail'] = is_detail
        self.create(self.execute(request, session)['trade_confirm_fee'])
        return self
    

class TradeRate(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''评价列表'''
        super(TradeRate, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'created':TOPDate}
        self.fields = ['valid_score','tid','oid','role','nick','result','created','rated_nick','item_title','item_price','content','reply']
    
    def add(self, tid, result, role, session, oid=None, content=None, anony=None):
        '''taobao.traderate.add 新增单个评价
        ==============================
        新增单个评价(注：在评价之前需要对订单成功的时间进行判定（end_time）,如果超过15天，不能再通过该接口进行评价)'''
        request = TOPRequest('taobao.traderate.add')
        request['tld'] = tld
        request['result'] = result
        request['role'] = role
        if oid!=None: request['oid'] = oid
        if content!=None: request['content'] = content
        if anony!=None: request['anony'] = anony
        self.create(self.execute(request, session)['trade_rate'])
        return self
    
    def list_add(self, tid, result, role, session, oid=None, content=None, anony=None):
        '''taobao.traderate.list.add 针对父子订单新增批量评价
        ==============================
        针对父子订单新增批量评价(注：在评价之前需要对订单成功的时间进行判定（end_time）,如果超过15天，不用再通过该接口进行评价)'''
        request = TOPRequest('taobao.traderate.list.add')
        request['tld'] = tld
        request['result'] = result
        request['role'] = role
        if oid!=None: request['oid'] = oid
        if content!=None: request['content'] = content
        if anony!=None: request['anony'] = anony
        self.create(self.execute(request, session)['trade_rate'])
        return self
    

class TradRates(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        '''确认收货费用结构'''
        super(TradRates, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'trade_rates':TradeRate}
        self.fields = ['trade_rates','total_results']
    
    def get(self, rate_type, role, session, fields=[], **kwargs):
        '''taobao.traderates.get 搜索评价信息
        ==============================
        搜索评价信息，只能获取距今180天内的评价记录'''
        request = TOPRequest('taobao.traderates.get')
        request['rate_type'] = rate_type
        request['role'] = role
        if not fields:
            trade = Trade()
            fields = trade.fields
        request['fields'] = fields
        for k, v in kwargs.iteritems():
            if k not in ('result','page_no','page_size','start_date','end_date','tld') or v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.trade_rates
    
    def search(self, num_iid, seller_nick, page_no=None, page_size=None):
        '''taobao.traderates.search 商品评价查询接口
        ==============================
        通过商品id查询对应的评价信息'''
        request = TOPRequest('taobao.traderates.search')
        request['num_iid'] = num_iid
        request['seller_nick'] = seller_nick
        if page_no!=None: request['page_no'] = page_no
        if page_size!=None: request['page_size'] = page_size
        self.create(self.execute(request, session))
        return self.trade_rates
    



