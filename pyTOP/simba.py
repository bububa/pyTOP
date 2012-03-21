#!/usr/bin/env python
# encoding: utf-8
"""
campaign.py

Created by 徐 光硕 on 2011-11-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class INCategoryAnalysis(TOP):
    '''类目数据分析对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryAnalysis, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['category_id','category_name','category_area_per','category_source_per','category_hp_price']
    

class INWordAnalysis(TOP):
    '''词数据分析对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INWordAnalysis, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['word','word_area_per','word_source_per','word_hp_price']
    

class INCategoryTop(TOP):
    '''类目对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryTop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'category_properties_list':INCategoryProperties, 'category_child_top_list':INCategoryChildTop}
        self.fields = ['category_id','category_name','category_desc','category_properties_list','category_child_top_list']
    

class INWordCategory(TOP):
    '''词和类目数据对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategory, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'date':TOPDate}
        self.fields = ['category_id','word','pv','click','avg_price','competition','date', 'ctr']
    
    
class CampaignBudget(TOP):
    '''推广计划的日限额'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CampaignBudget, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['is_smooth', 'nick','campaign_id','budget','old_value','create_time','modified_time']
    
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
    

class INWordBase(TOP):
    '''词基础数据对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INWordBase, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'in_record_base_list':INRecordBase}
        self.fields = ['word','in_record_base_list']
    

class CampaignArea(TOP):
    '''推广计划的投放地域'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CampaignArea, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['nick','campaign_id','area','create_time','modified_time']
    
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
    

class RecommendWord(TOP):
    '''推荐词'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(RecommendWord, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['word','quality_score','pv','average_price','pertinence']
    

class INRecordBase(TOP):
    '''数据信息对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INRecordBase, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'date':TOPDate}
        self.fields = ['pc','click','avg_price','competition','date', 'ctr']
    

class CampaignSchedule(TOP):
    '''推广计划的分时折扣设置'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CampaignSchedule, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['nick','campaign_id','schedule','create_time','modified_time']
    
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
    

class INCategoryBase(TOP):
    '''类目基础数据对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryBase, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'in_record_base_list':INRecordBase}
        self.fields = ['category_id','category_name','category_pv','in_record_base_list']
    

class CreativeRecord(TOP):
    '''创意修改记录，只记录最后一次修改'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CreativeRecord, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate, 'modify_time':TOPDate}
        self.fields = ['nick','creative_id','title','old_title','img_url','old_img_url','audit_status','audit_desc','modify_time','create_time','modified_time']
    

class Keyword(TOP):
    '''关键词'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Keyword, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['qscore', 'nick','campaign_id','adgroup_id','keyword_id','word','max_price','is_default_price','audit_status','audit_desc','is_garbage','create_time','modified_time']
    

class ADGroupCatmatch(TOP):
    '''推广组类目出价'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ADGroupCatmatch, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['qscore', 'nick','campaign_id','adgroup_id','catmatch_id','max_price','is_default_price','online_status','create_time','last_update_time', 'modified_time']
    
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
    

class INCategoryProperties(TOP):
    '''类目属性对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryProperties, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['properties_id','properties_desc', 'properties_name']
    

class Creative(TOP):
    '''创意'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Creative, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['nick','campaign_id','adgroup_id','creative_id','title','img_url','audit_status','audit_desc','create_time','modified_time']
    
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
    

class ChannelOption(TOP):
    '''推广计划可选择的投放频道'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ChannelOption, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['channel_id','name','traffic_type','traffic_name','is_search','is_nonsearch']
    
    def get(self):
        '''xxxxx.xxxxx.campaign.channeloptions.get
        ===================================
        取得推广计划的可设置投放频道列表'''
        request = TOPRequest('xxxxx.xxxxx.campaign.channeloptions.get')
        self.create(self.execute(request), fields=['success','result'], models={'result':ChannelOption})
        return self.result
    

class INCategoryChildTop(TOP):
    '''类目对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryChildTop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'category_properties_list':INCategoryProperties}
        self.fields = ['category_id','category_name','category_desc','category_properties_list']
    

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
    

class RankedItem(TOP):
    '''关键词排名推广商品信息'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(RankedItem, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['nick','order','max_price','title','link_url','rank_score']
    

class ADGroup(TOP):
    '''推广组'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(ADGroup, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['nick','campaign_id','adgroup_id','category_id','num_iid','default_price','nonsearch_max_price','is_nonsearch_default_price','online_status','offline_type','reason','create_time','modified_time'] 
    
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
    

class Campaign(TOP):
    '''推广计划'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Campaign, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['nick','campaign_id','title','is_smooth','online_status','settle_status','settle_reason','create_time','modified_time']
    
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
    

class CampaignPlatform(TOP):
    '''推广计划的投放平台'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CampaignPlatform, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'create_time':TOPDate, 'modified_time':TOPDate}
        self.fields = ['nick','campaign_id','search_channels','nonsearch_channels','outside_discount','create_time','modified_time']
    
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
    
