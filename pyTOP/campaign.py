#!/usr/bin/env python
# encoding: utf-8
"""
campaign.py

Created by 徐 光硕 on 2011-11-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class AreaOption(TOP):
    '''推广计划可选择的投放地域'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(AreaOption, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['area_id','parent_id','name','level']
    
    def get(self):
        '''xxxxx.xxxxx.campaign.areaoptions.get
        ===================================
        取得推广计划的可设置投放地域列表'''
        request = TOPRequest('xxxxx.xxxxx.campaign.areaoptions.get')
        self.create(self.execute(request), fields=['success','result'], models={'result':AreaOption})
        return self.result
    

class ChannelOption(TOP):
    '''推广计划可选择的投放频道'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ChannelOption, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['channel_id','name','traffic_type','traffic_type_name','is_search','is_nonsearch']
    
    def get(self):
        '''xxxxx.xxxxx.campaign.channeloptions.get
        ===================================
        取得推广计划的可设置投放频道列表'''
        request = TOPRequest('xxxxx.xxxxx.campaign.channeloptions.get')
        self.create(self.execute(request), fields=['success','result'], models={'result':ChannelOption})
        return self.result

class Campaign(TOP):
    '''推广计划'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Campaign, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','title','is_smooth','online_status','settle_status','settle_reason','create_time','last_update_time']
    
    def add(self, title, nick=None):
        '''xxxxx.xxxxx.campaign.add
        ===================================
        创建一个推广计划'''
        request = TOPRequest('xxxxx.xxxxx.campaign.add')
        request['title'] = title
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':Campaign})
        return self.result
    
    def update(self, campaign_id, title, is_smooth, online_status, nick=None):
        '''xxxxx.xxxxx.campaign.update
        ===================================
        更新一个推广计划，可以设置推广计划名字、是否平滑消耗，只有在设置了日限额后平滑消耗才会产生作用。'''
        request = TOPRequest('xxxxx.xxxxx.campaign.update')
        request['campaign_id'] = campaign_id
        request['title'] = title
        request['is_smooth'] = is_smooth
        request['online_status'] = online_status
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':Campaign})
        return self.result
    

class Campaigns(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Campaigns, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':Campaign}
        self.fields = ['success','result','success','result_code','result_message']
    
    def get(self, nick=None):
        '''xxxxx.xxxxx.campaigns.get
        ===================================
        取得一个客户的推广计划，或者根据一个推广计划id列表取得一组推广计划；
        如果同时提供了客户的昵称和推广计划id列表，则优先使用客户参数；'''
        request = TOPRequest('xxxxx.xxxxx.campaigns.get')
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class CampaignArea(TOP):
    '''推广计划的投放地域'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CampaignArea, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','area','create_time','last_update_time']
    
    def get(self, campaign_id, nick=None):
        '''xxxxx.xxxxx.campaign.area.get
        ===================================
        取得一个推广计划的投放地域设置'''
        request = TOPRequest('xxxxx.xxxxx.campaign.area.get')
        request['campaign_id'] = campaign_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':CampaignArea})
        return self.result
    
    def update(self, campaign_id, area, nick=None):
        '''xxxxx.xxxxx.campaign.area.update
        ===================================
        更新一个推广计划的投放地域'''
        request = TOPRequest('xxxxx.xxxxx.campaign.area.update')
        request['campaign_id'] = campaign_id
        request['area'] = area
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':CampaignArea})
        return self.result

class CampaignBudget(TOP):
    '''推广计划的日限额'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CampaignBudget, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','budget','old_value','create_time','last_update_time']
    
    def get(self, campaign_id, nick=None):
        '''xxxxx.xxxxx.campaign.budget.get
        ===================================
        取得一个推广计划的日限额'''
        request = TOPRequest('xxxxx.xxxxx.campaign.budget.get')
        request['campaign_id'] = campaign_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':CampaignBudget})
        return self.result
    
    def update(self, campaign_id, budget, nick=None):
        '''xxxxx.xxxxx.campaign.budget.update
        ===================================
        更新一个推广计划的日限额'''
        request = TOPRequest('xxxxx.xxxxx.campaign.budget.update')
        request['campaign_id'] = campaign_id
        request['budget'] = budget
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':CampaignBudget})
        return self.result
    

class CampaignPlatform(TOP):
    '''推广计划的投放平台'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CampaignPlatform, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','search_channels','nonsearch_channels','outside_discount','create_time','last_update_time']
    
    def get(self, campaign_id, nick=None):
        '''xxxxx.xxxxx.campaign.platform.get
        ===================================
        取得一个推广计划的投放平台设置'''
        request = TOPRequest('xxxxx.xxxxx.campaign.platform.get')
        request['campaign_id'] = campaign_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':CampaignPlatform})
        return self.result
    
    def update(self, campaign_id, search_channels, nonsearch_channels, outside_discount, nick=None):
        '''xxxxx.xxxxx.campaign.platform.update
        ===================================
        取得一个推广计划的投放平台设置'''
        request = TOPRequest('xxxxx.xxxxx.campaign.platform.update')
        request['campaign_id'] = campaign_id
        request['search_channels'] = search_channels
        request['nonsearch_channels'] = nonsearch_channels
        request['outside_discount'] = outside_discount
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':CampaignPlatform})
        return self.result
    

class CampaignSchedule(TOP):
    '''推广计划的分时折扣设置'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CampaignSchedule, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','schedule','create_time','last_update_time']
    
    def get(self, campaign_id, nick=None):
        '''xxxxx.xxxxx.campaign.schedule.get
        ===================================
        取得一个推广计划的分时折扣设置'''
        request = TOPRequest('xxxxx.xxxxx.campaign.schedule.get')
        request['campaign_id'] = campaign_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':CampaignSchedule})
        return self.result
    
    def update(self, campaign_id, schedule, nick=None):
        '''xxxxx.xxxxx.campaign.schedule.update
        ===================================
        更新一个推广计划的分时折扣设置'''
        request = TOPRequest('xxxxx.xxxxx.campaign.schedule.update')
        request['campaign_id'] = campaign_id
        request['schedule'] = schedule
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':CampaignSchedule})
        return self.result
    

class ADGroups(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ADGroups, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','success','result_code','result_message']
    
    def get(self, page_size, page_no=1, campaign_id=None, adgroup_ids=None, nick=None):
        '''xxxxx.xxxxx.adgroups.get
        ===================================
        取得一个推广计划的所有推广组，或者根据一个推广组Id列表取得一组推广组；
        如果同时提供了推广计划Id和推广组id列表，则优先使用推广计划Id，当使用
        推广计划ID获取数据时，返回的结果是有分页的。如果是用推广组ID列表作查询
        则将一次返回所有查询的结果。'''
        request = TOPRequest('xxxxx.xxxxx.adgroups.get')
        request['page_size'] = page_size
        request['page_no'] = page_no
        if campaign_id!=None: request['campaign_id'] = campaign_id
        if adgroup_ids!=None: request['adgroup_ids'] = adgroup_ids
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), models = {'result':ADGroup})
        return self.result
    
    def item_exist(self, campaign_id, item_id, nick=None):
        '''xxxxx.xxxxx.adgroups.item.exist
        ===================================
        判断在一个推广计划中是否已经推广了一个商品'''
        request = TOPRequest('xxxxx.xxxxx.adgroups.item.exist')
        request['campaign_id'] = campaign_id
        request['item_id'] = item_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class ADGroup(TOP):
    '''推广组'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ADGroup, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','adgroup_id','category_id','item_id','default_price','nonsearch_price','is_nonsearch_default_price','online_status','offline_type','offline_reason','create_time','last_update_time'] 
       
    def add(self, campaign_id, item_id, default_price, title, img_url, nick=None):
        '''xxxxx.xxxxx.adgroup.add
        ===================================
        创建一个推广组'''
        request = TOPRequest('xxxxx.xxxxx.adgroup.add')
        request['campaign_id'] = campaign_id
        request['item_id'] = item_id
        request['default_price'] = default_price
        request['title'] = title
        request['img_url'] = img_url
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':ADGroup})
        return self.result
    
    def delete(self, group_id, nick=None):
        '''xxxxx.xxxxx.adgroup.delete
        ===================================
        删除一个推广组'''
        request = TOPRequest('xxxxx.xxxxx.adgroup.delete')
        request['group_id'] = group_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':ADGroup})
        return self.result
    
    def update(self, adgroup_id, default_price, nonsearch_max_price, is_nonsearch_default_price, online_status, campaign_id, nick=None):
        '''xxxxx.xxxxx.adgroup.update
        ===================================
        更新一个推广组的信息，可以设置默认出价、是否上线、非搜索出价、非搜索是否使用默认出价'''
        request = TOPRequest('xxxxx.xxxxx.adgroup.update')
        request['adgroup_id'] = adgroup_id
        request['default_price'] = default_price
        request['nonsearch_max_price'] = nonsearch_max_price
        request['is_nonsearch_default_price'] = is_nonsearch_default_price
        request['online_status'] = online_status
        request['campaign_id'] = campaign_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':ADGroup})
        return self.result
    

class ADGroupCatmatch(TOP):
    '''推广组类目出价'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ADGroupCatmatch, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','adgroup_id','catmatch_id','max_price','is_default_price','online_status','create_time','last_update_time']
    
    def get(self, adgroup_id, nick=None):
        '''xxxxx.xxxxx.adgroup.catmatch.get
        ===================================
        取得一个推广组的类目出价'''
        request = TOPRequest('xxxxx.xxxxx.adgroup.catmatch.get')
        request['adgroup_id'] = adgroup_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':ADGroupCatmatch})
        return self.result
    
    def update(self, adgroup_id, catmatch_id, max_price, is_default_price, online_status, nick=None):
        '''xxxxx.xxxxx.adgroup.catmatch.update
        ===================================
        更新一个推广组的类目出价，可以设置类目出价、是否使用默认出价、是否打开类目出价'''
        request = TOPRequest('xxxxx.xxxxx.adgroup.catmatch.update')
        request['adgroup_id'] = adgroup_id
        request['catmatch_id'] = catmatch_id
        request['max_price'] = max_price
        request['is_default_price'] = is_default_price
        request['online_status'] = online_status
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models={'result':ADGroupCatmatch})
        return self.result
    

class Creative(TOP):
    '''创意'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Creative, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','adgroup_id','creative_id','title','img_url','audit_status','audit_desc','create_time','last_update_time']
    
    def add(self, adgroup_id, title, img_url, nick=None):
        '''xxxxx.xxxxx.creative.add
        ===================================
        创建一个创意'''
        request = TOPRequest('xxxxx.xxxxx.creative.add')
        request['adgroup_id'] = adgroup_id
        request['title'] = title
        request['img_url'] = img_url
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models = {'result':Creative})
        return self.result
    
    def delete(self, creative_id, nick=None):
        '''xxxxx.xxxxx.creative.delete
        ===================================
        删除一个创意'''
        request = TOPRequest('xxxxx.xxxxx.creative.delete')
        request['creative_id'] = creative_id
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models = {'result':Creative})
        return self.result
    
    def update(self, adgroup_id, creative_id, title, img_url, nick=None):
        '''xxxxx.xxxxx.creative.update
        ===================================
        更新一个创意的信息，可以设置创意标题、创意图片'''
        request = TOPRequest('xxxxx.xxxxx.creative.update')
        request['adgroup_id'] = adgroup_id
        request['creative_id'] = creative_id
        request['title'] = title
        request['img_url'] = img_url
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), fields=['success','result','success','result_code','result_message'], models = {'result':CreativeRecord})
        return self.result
    

class Creatives(TOP):
    '''创意'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Creatives, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','success','result_code','result_message']
    
    def record_get(self, creative_ids, nick=None):
        '''xxxxx.xxxxx.creatives.record.get
        ===================================
        根据一个创意Id列表取得创意对应的修改记录'''
        request = TOPRequest('xxxxx.xxxxx.creatives.record.get')
        request['creative_ids'] = creative_ids
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), models = {'result':CreativeRecord})
        return self.result
    
    def get(self, adgroup_id=None, creative_ids=None, nick=None):
        '''xxxxx.xxxxx.creatives.get
        ===================================
        取得一个推广组的所有创意或者根据一个创意Id列表取得一组创意；
        如果同时提供了推广组Id和创意id列表，则优先使用推广组Id；'''
        request = TOPRequest('xxxxx.xxxxx.creatives.get')
        if adgroup_id!=None: request['adgroup_id'] = adgroup_id
        if creative_ids!=None: request['creative_ids'] = creative_ids
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), models = {'result':Creative})
        return self.result
    

class CreativeRecord(TOP):
    '''创意修改记录，只记录最后一次修改'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CreativeRecord, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate, 'modify_time':TOPDate}
        self.fields = ['nick','creative_id','title','old_title','img_url','old_img_url','audit_status','audit_desc','modify_time','create_time','last_update_time']
    

class Keyword(TOP):
    '''关键词'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Keyword, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'last_update_time':TOPDate}
        self.fields = ['nick','campaign_id','adgroup_id','keyword_id','word','max_price','is_default_price','audit_status','audit_desc','is_garbage','create_time','last_update_time']
    

class Keywords(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Keywords, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','success','result_code','result_message']
    
    def add(self, adgroup_id, keyword_prices, nick=None):
        '''xxxxx.xxxxx.keywords.add
        ===================================
        创建一批关键词'''
        request = TOPRequest('xxxxx.xxxxx.keywords.add')
        request['adgroup_id'] = adgroup_id
        request['keyword_prices'] = keyword_prices
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), models = {'result':Keyword})
        return self.result
    
    def delete(self, adgroup_id, keyword_ids, nick=None):
        '''xxxxx.xxxxx.keywords.delete
        ===================================
        删除一批关键词'''
        request = TOPRequest('xxxxx.xxxxx.keywords.delete')
        request['adgroup_id'] = adgroup_id
        request['keyword_ids'] = keyword_ids
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), models = {'result':Keyword})
        return self.result
    
    def price_set(self, adgroup_id, keywordId_prices, nick=None):
        '''xxxxx.xxxxx.keywords.price.set
        ===================================
        设置一批关键词的出价'''
        request = TOPRequest('xxxxx.xxxxx.keywords.price.set')
        request['adgroup_id'] = adgroup_id
        request['keywordId_prices'] = keywordId_prices
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    
    def get(self, adgroup_id=None, keyword_ids=None, nick=None):
        '''xxxxx.xxxxx.keywords.get
        ===================================
        取得一个推广组的所有关键词或者根据一个关键词Id列表取得一组关键词；
        如果同时提供了推广组Id和关键词id列表，则优先使用推广组Id；'''
        request = TOPRequest('xxxxx.xxxxx.keywords.get')
        if adgroup_id!=None: request['adgroup_id'] = adgroup_id
        if keyword_ids!=None: request['keyword_ids'] = keyword_ids
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), models = {'result':Keyword})
        return self.result
    
    def recommend_get(self, adgroup_id, **kwargs):
        '''xxxxx.xxxxx.keywords.recommend.get
        ===================================
        取得一个推广组的推荐关键词列表'''
        request = TOPRequest('xxxxx.xxxxx.keywords.recommend.get')
        request['adgroup_id'] = adgroup_id
        for k, v in kwargs.iteritems():
            if k not in ('nick', 'order_by', 'search', 'pertinence', 'page_size', 'page_no') and v==None: continue
            request[k] = v
        self.create(self.execute(request), models = {'result':RecommendWordPage})
        return self.result
    

class AccountRecord(TOP):
    '''帐户记录'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(AccountRecord, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'date':TOPDate}
        self.fields = ['date','type','amount','balance']
    

class RecommendWord(TOP):
    '''推荐词'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(RecommendWord, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['word','quality_score','pv','average_price','pertinence']
    

class RankedItem(TOP):
    '''关键词排名推广商品信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(RankedItem, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['nick','order','maxPrice','title','linkUrl','rankScore','calcScore']
    

class ADGroupPage(TOP):
    '''一页ADGroup列表'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ADGroupPage, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'adgroup_list':ADGroup}
        self.fields = ['page_size','page_no','total_item','adgroup_list']
    

class RecommendWordPage(TOP):
    '''一页推荐词列表'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(RecommendWordPage, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'recommend_word_list':RecommendWord}
        self.fields = ['page_size','page_no','total_item','recommend_word_list']
    

class Result(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Result, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','error_code','error_message','result']
    

class Customers(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Customers, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','success','result_code','result_message']
    
    def authorized_get(self):
        '''xxxxx.xxxxx.customers.authorized.get
        ===================================
        取得当前登录用户的授权账户列表'''
        request = TOPRequest('xxxxx.xxxxx.customers.authorized.get')
        self.create(self.execute(request))
        return self.result
    

class Account(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Account, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','success','result_code','result_message']
    
    def balance_get(self, nick):
        '''xxxxx.xxxxx.account.balance.get
        ===================================
        取得当前登录用户的授权账户列表'''
        request = TOPRequest('xxxxx.xxxxx.account.balance.get')
        request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    
    def records_get(self, nick, start_time=None, end_time=None):
        '''xxxxx.xxxxx.account.records.get
        ===================================
        获取账户财务记录'''
        request = TOPRequest('xxxxx.xxxxx.account.records.get')
        request['nick'] = nick
        if start_time!=None: request['start_time'] = start_time
        if end_time!=None: request['end_time'] = end_time
        self.create(self.execute(request), models={'result':AccountRecord})
        return self.result
    

class Tools(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Tools, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','success','result_code','result_message']
    
    def items_top_get(self, keyword, nick=None):
        '''xxxxx.xxxxx.tools.items.top.get
        ===================================
        取得当前登录用户的授权账户列表'''
        request = TOPRequest('xxxxx.xxxxx.tools.items.top.get')
        request['keyword'] = keyword
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), models={'result':RankedItem})
        return self.result
    
