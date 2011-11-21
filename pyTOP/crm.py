#!/usr/bin/env python
# encoding: utf-8
"""
crm.py

Created by 徐 光硕 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class GroupDomain(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''分组简单定义'''
        super(GroupDomain, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['group_id','group_name']
    

class BasicMember(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''表示会员关系的基本信息字段，用于会员列表的基本查询'''
        super(BasicMember, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'last_trade_time':TOPDate}
        self.fields = ['buyer_nick','status','grade','trade_count','trade_amount','last_trade_time','close_trade_count','close_trade_amount','item_num','group_ids','relation_source','biz_order_id','buyer_id']
    

class GradePromotion(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''卖家设置的等级优惠信息'''
        super(GradePromotion, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['cur_grade','cur_grade_name','discount','next_upgrade_amount','next_upgrade_count']
    

class RuleData(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''规则相关信息'''
        super(RuleData, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'grouplist':GroupDomain,'start_trade_time':TOPDate,'end_trade_time':TOPDate}
        self.fields = ['rule_id','seller_id','rule_name','grouplist','start_trade_time','end_trade_time','min_avg_price','max_avg_price','min_trade_count','max_trade_count','min_item_count','max_item_count','min_close_trade_count','max_close_trade_count','min_trade_amount','max_trade_amount','relation_source','province','grade']
    

class CrmMember(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''会员信息对象'''
        super(CrmMember, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['buyer_nick','status','grade','trade_count','trade_amount','close_trade_count','close_trade_amount','item_num','biz_order_id','group_ids','province','city','avg_price','relation_source','last_trade_time','item_close_count','buyer_id']
    

class Group(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''描述分组的数据结构'''
        super(Group, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'group_create':TOPDate, 'group_modify':TOPDate}
        self.fields = ['group_id','group_name','group_create','group_modify','status','member_count']
    
    def add(self, group_name, session):
        '''taobao.crm.group.add 卖家创建一个分组
        ===================================
        卖家创建一个新的分组，接口返回一个创建成功的分组的id'''
        request = TOPRequest('taobao.crm.group.add')
        request['group_name'] = group_name
        self.create(self.execute(request, session), fields=['is_success', 'group_id'])
        return self.is_success, self.group_id
    
    def append(self, from_group_id, to_group_id, session):
        '''taobao.crm.group.append 将一个分组添加到另外一个分组
        ===================================
        将某分组下的所有会员添加到另一个分组,注：
        1.该操作为异步任务，建议先调用taobao.crm.grouptask.check 确保涉及分组上没有任务；
        2.若分组下某会员分组数超最大限额，则该会员不会被添加到新分组，同时不影响其余会员添加分组，接口调用依然返回成功。'''
        request = TOPRequest('taobao.crm.group.append')
        request['from_group_id'] = from_group_id
        request['to_group_id'] = to_group_id
        self.create(self.execute(request, session), fields=['is_success',])
        return self.is_success
    
    def delete(self, group_id, session):
        '''taobao.crm.group.delete 删除分组
        ===================================
        将该分组下的所有会员移除出该组，同时删除该分组。注：删除分组为异步任务，必须先调用taobao.crm.grouptask.check 确保涉及属性上没有任务。'''
        request = TOPRequest('taobao.crm.group.delete')
        request['group_id'] = group_id
        self.create(self.execute(request, session), fields=['is_success',])
        return self.is_success
    
    def move(self, from_group_id, to_group_id, session):
        '''taobao.crm.group.move 分组移动
        ===================================
        将一个分组下的所有会员移动到另一个分组，会员从原分组中删除 注：移动属性为异步任务建议先调用taobao.crm.grouptask.check 确保涉及属性上没有任务。'''
        request = TOPRequest('taobao.crm.group.move')
        request['from_group_id'] = from_group_id
        request['to_group_id'] = to_group_id
        self.create(self.execute(request, session), fields=['is_success',])
        return self.is_success
    
    def update(self, group_id, new_group_name, session):
        '''taobao.crm.group.update 修改一个已经存在的分组
        ===================================
        修改一个已经存在的分组，接口返回分组的修改是否成功'''
        request = TOPRequest('taobao.crm.group.update')
        request['group_id'] = group_id
        request['new_group_name'] = new_group_name
        self.create(self.execute(request, session), fields=['is_success',])
        return self.is_success
    

class Groups(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Groups, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'groups':Group}
        self.fields = ['groups', 'total_result']
    
    def get(self, page_size, current_page, session):
        '''taobao.crm.groups.get 查询卖家的分组
        ===================================
        查询卖家的分组，返回查询到的分组列表，分页返回分组'''
        request = TOPRequest('taobao.crm.groups.get')
        request['page_size'] = page_size
        request['current_page'] = current_page
        self.create(self.execute(request, session))
        return self.groups
    

class GroupTask(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(GroupTask, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['is_finished']
    
    def check(self, group_id, session):
        '''taobao.crm.grouptask.check 查询分组任务是否完成
        ===================================
        检查一个分组上是否有异步任务,异步任务包括
        1.将一个分组下的所有用户添加到另外一个分组
        2.将一个分组下的所有用户移动到另外一个分组
        3.删除某个分组 若分组上有任务则该属性不能被操作。'''
        request = TOPRequest('taobao.crm.grouptask.check')
        request['group_id'] = group_id
        self.create(self.execute(request, session))
        return self.is_finished
    

class MemberInfo(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(MemberInfo, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['is_success']
    
    def update(self, buyer_nick, status, session, grade=None, province=None, city=None):
        '''taobao.crm.memberinfo.update 编辑会员资料
        ===================================
        检查一个分组上是否有异步任务,异步任务包括
        1.将一个分组下的所有用户添加到另外一个分组
        2.将一个分组下的所有用户移动到另外一个分组
        3.删除某个分组 若分组上有任务则该属性不能被操作。'''
        request = TOPRequest('taobao.crm.memberinfo.update')
        request['buyer_nick'] = buyer_nick
        request['status'] = status
        if grade!=None: request['grade'] = grade
        if province!=None: request['province'] = province
        if city!=None: request['city'] = city
        self.create(self.execute(request, session))
        return self.is_success
    

class Members(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Members, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'members':BasicMember}
        self.fields = ['members', 'total_result']
    
    def get(self, current_page, session, **kwargs):
        '''taobao.crm.members.get 获取卖家的会员（基本查询）
        ===================================
        查询卖家的会员，进行基本的查询，返回符合条件的会员列表'''
        request = TOPRequest('taobao.crm.members.get')
        request['current_page'] = current_page
        for k, v in kwargs.iteritems():
            if k not in ('buyer_nick', 'grade', 'min_trade_amount', 'max_trade_amount', 'min_trade_count', 'max_trade_count', 'min_last_trade_time', 'max_last_trade_time', 'page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.members
    
    def group_batchadd(self, buyer_ids, group_ids, session):
        '''taobao.crm.members.group.batchadd 给一批会员添加一个分组
        ===================================
        为一批会员添加分组，接口返回添加是否成功,如至少有一个会员的分组添加成功，接口就返回成功，否则返回失败，如果当前会员已经拥有当前分组，则直接跳过'''
        request = TOPRequest('taobao.crm.members.group.batchadd')
        request['buyer_ids'] = buyer_ids
        request['group_ids'] = group_ids
        self.create(self.execute(request, session), fields=['is_success', ])
        return self.is_success
    
    def groups_batchdelete(self, buyer_ids, group_ids, session):
        '''taobao.crm.members.groups.batchdelete 批量删除分组
        ===================================
        批量删除多个会员的公共分组，接口返回删除是否成功，该接口只删除多个会员的公共分组，不是公共分组的，不进行删除。如果入参只输入一个会员，则表示删除该会员的某些分组。'''
        request = TOPRequest('taobao.crm.members.groups.batchdelete')
        request['buyer_ids'] = buyer_ids
        request['group_ids'] = group_ids
        self.create(self.execute(request, session), fields=['is_success', ])
        return self.is_success
    
    def increment_get(self, current_page, session, **kwargs):
        '''taobao.crm.members.increment.get 增量获取卖家会员）
        ===================================
        增量获取会员列表，接口返回符合查询条件的所有会员。任何状态更改都会返回'''
        request = TOPRequest('taobao.crm.members.increment.get')
        request['current_page'] = current_page
        for k, v in kwargs.iteritems():
            if k not in ('grade', 'start_modify', 'end_modify', 'page_size') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.members
    
    def search(self, current_page, session, **kwargs):
        '''taobao.crm.members.search 获取卖家会员（高级查询））
        ===================================
        会员列表的高级查询，接口返回符合条件的会员列表'''
        request = TOPRequest('taobao.crm.members.search')
        request['current_page'] = current_page
        for k, v in kwargs.iteritems():
            if k not in ('buyer_nick', 'grade', 'min_trade_amount', 'max_trade_amount', 'min_trade_count', 'max_trade_count', 'min_last_trade_time', 'max_last_trade_time', 'relation_source', 'min_item_num', 'min_avg_price', 'min_close_trade_num', 'province', 'city', 'group_id', 'page_size', 'order', 'max_avg_price', 'max_item_num', 'max_close_trade_num', 'sort') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session), models={'members':CrmMember})
        return self.members
    

class Grade(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Grade, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'grade_promotions':GradePromotion}
        self.fields = ['grade_promotions']
    
    def get(self, session):
        '''taobao.crm.grade.get 卖家查询等级规则
        ===================================
        卖家查询等级规则，包括普通会员、高级会员、VIP会员、至尊VIP会员四个等级的信息'''
        request = TOPRequest('taobao.crm.grade.get')
        self.create(self.execute(request, session))
        return self.grade_promotions

class Rule(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Rule, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['is_success', 'rule_id']
    
    def add(self, rule_name, session, **kwargs):
        '''taobao.crm.rule.add 分组规则添加
        ===================================
        添加分组规则，规则可用于筛选一定条件的会员。过滤条件可以选择客户来源、会员级别 、交易笔数、交易额、上次交易时间、平均客单价、宝贝件数、省份、关闭交易数等，新建规则时必须至少选择一个以上筛选条件。如果输入的规则的筛选条件不正确则不会进行处理，可以将某些分组挂在这个规则下，对被挂在该规则下的分组，系统对现有满足规则的客户都划分到这个分组（异步任务），若某些会员分组数或规则数超最大限额，则该会员不被操作，同时不影响其余会员操作，接口调用依然返回成功。每个规则可以应用到多个分组，一个用户的规则上限为5个。'''
        request = TOPRequest('taobao.crm.rule.add')
        request['rule_name'] = rule_name
        for k, v in kwargs.iteritems():
            if k not in ('relation_source', 'grade', 'min_trade_amount', 'max_trade_amount', 'min_trade_count', 'max_trade_count', 'min_last_trade_time', 'max_last_trade_time', 'min_item_num', 'min_avg_price', 'min_close_trade_num', 'province', 'group_ids', 'max_avg_price', 'max_item_num', 'max_close_trade_num') and v==None: continue
            request[k] = v
        self.create(self.execute(request, session))
        return self.is_success, self.rule_id
    
    def delete(self, rule_id, session):
        '''taobao.crm.rule.delete 分组规则删除
        ===================================
        分组规则删除'''
        request = TOPRequest('taobao.crm.rule.delete')
        request['rule_id'] = rule_id
        self.create(self.execute(request, session))
        return self.is_success
    
    def group_set(self, rule_id, session, add_groups=None, delete_groups=None):
        '''taobao.crm.rule.group.set 设置规则适用的分组
        ===================================
        将规则应用或取消应用到分组上，add_groups和delete_groups，两个参数最少填写一个。'''
        request = TOPRequest('taobao.crm.rule.delete')
        request['rule_id'] = rule_id
        if add_groups!=None: request['add_groups'] = add_groups
        if delete_groups!=None: request['delete_groups'] = delete_groups
        self.create(self.execute(request, session))
        return self.is_success
    

class Rules(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Rules, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'rule_list':RuleData}
        self.fields = ['rule_list', 'total_result']
    
    def get(self, current_page, session, page_size=None):
        '''taobao.crm.rules.get 获取规则
        ===================================
        获取现有的规则列表'''
        request = TOPRequest('taobao.crm.rules.get')
        request['current_page'] = current_page
        if page_size!=None: request['page_size'] = page_size
        self.create(self.execute(request, session))
        return self.rule_list
    

class ShopVip(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ShopVip, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['is_success', ]
    
    def cancel(self, session):
        '''taobao.crm.shopvip.cancel 卖家取消店铺vip的优惠
        ===================================
        此接口用于取消VIP优惠'''
        request = TOPRequest('taobao.crm.shopvip.cancel')
        self.create(self.execute(request, session))
        return self.is_success
    
