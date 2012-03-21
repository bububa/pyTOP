#!/usr/bin/env python
# encoding: utf-8
"""
insight.py

Created by 徐 光硕 on 2011-11-21.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class INWordBase(TOP):
    '''词基础数据对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INWordBase, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['word','in_record_Base_list']
    

class INCategoryBase(TOP):
    '''类目基础数据对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryBase, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['category_id','category_name','category_pv','in_record_Base_list']
    

class INWordAnalysis(TOP):
    '''词数据分析对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INWordAnalysis, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['word','word_area_per','word_source_per','word_hp_price']
    

class INCategoryAnalysis(TOP):
    '''类目数据分析对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryAnalysis, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['category_id','category_name','category_area_per','category_source_per','category_hp_price']
    

class INCategoryProperties(TOP):
    '''类目属性对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryProperties, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['properties_id','properties_desc']

class INCategory(TOP):
    '''类目属性对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategory, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'category_properties_list':INCategoryProperties, 'child_category_list':INCategory}
        self.fields = ['category_id','category_name','category_desc','category_properties_list','child_category_list']
    

class INWordCategory(TOP):
    '''词和类目数据对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategory, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'date':TOPDate}
        self.fields = ['category_id','word','pv','click','avg_price','competition','date']
    

class INRecordBase(TOP):
    '''数据信息对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INRecordBase, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'date':TOPDate}
        self.fields = ['pc','click','avg_price','competition','date']
    

class INCategoryAnalysisTop(TOP):
    '''类目数据分析对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryAnalysisTop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['category_id','category_name','category_area_per','category_source_per','category_hp_price']
    

class INCategoryChildTop(TOP):
    '''类目对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryChildTop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'category_properties_list':INCategoryProperties}
        self.fields = ['category_id','category_name','category_desc','category_properties_list']
    

class INCategoryTop(TOP):
    '''类目对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INCategoryTop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'category_properties_list':INCategoryProperties, 'child_category_list':INCategory}
        self.fields = ['category_id','category_name','category_desc','category_properties_list','child_category_list']
    

class INWordAnalysisTop(TOP):
    '''词数据分析对象'''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(INWordAnalysisTop, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['word','word_area_pers','word_source_pers','word_hp_prices']
    

class WordsBase(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(WordsBase, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':INWordBase}
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, session, words, time='DAY|WEEK|MONTH|3MONTH', aFilter='PV|CLICK|AVGCPC|COMPETITION', nick=None):
        '''taobao.simba.insight.wordsbase.get
        ===================================
        词基础数据查询'''
        request = TOPRequest('taobao.simba.insight.wordsbase.get')
        request['words'] = words
        request['time'] = time
        request['filter'] = aFilter
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request, session))
        return self.result
    

class CatsBase(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CatsBase, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':INCategoryBase}
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, category_ids, time, aFilter='PV|CLICK|AVGCPC|COMPETITION', nick=None):
        '''taobao.simba.insight.catsbase.get
        ===================================
        类目基础数据查询'''
        request = TOPRequest('taobao.simba.insight.catsbase.get')
        request['category_ids'] = category_ids
        request['time'] = time
        request['filter'] = aFilter
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class WordsAnalysis(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(WordsAnalysis, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':INWordAnalysis}
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, session, words, stu='area|source|hpprice', nick=None):
        '''taobao.simba.insight.wordsanalysis.get
        ===================================
        词分析数据查询'''
        request = TOPRequest('taobao.simba.insight.wordsanalysis.get')
        request['words'] = words
        request['stu'] = stu
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request, session))
        return self.result
    

class CatsAnalysis(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CatsAnalysis, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':INCategoryAnalysis}
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, category_ids, stu='area|source|hpprice', nick=None):
        '''taobao.simba.insight.catsanalysis.get
        ===================================
        类目分析数据查询'''
        request = TOPRequest('taobao.simba.insight.catsbase.get')
        request['category_ids'] = category_ids
        request['stu'] = stu
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class CatsForecast(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CatsForecast, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':INCategory}
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, words, nick=None):
        '''taobao.simba.insight.catsforecast.get
        ===================================
        类目属性预测'''
        request = TOPRequest('taobao.simba.insight.catsforecast.get')
        request['words'] = words
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class CatsTopWord(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CatsTopWord, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, category_ids, result_num=100, nick=None):
        '''taobao.simba.insight.catstopword.get
        ===================================
        类目TOP词查询'''
        request = TOPRequest('taobao.simba.insight.catstopword.get')
        request['category_ids'] = category_ids
        request['result_num'] = result_num
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class CatsRelatedWord(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CatsRelatedWord, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, words, result_num=100, nick=None):
        '''taobao.simba.insight.catsrelatedword.get
        ===================================
        类目相关词查询'''
        request = TOPRequest('taobao.simba.insight.catsrelatedword.get')
        request['words'] = words
        request['result_num'] = result_num
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class WordsCats(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(WordsCats, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':INWordCategory}
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, wordCategories, aFilter='PV|CLICK|AVGCPC|COMPETITION', nick=None):
        '''taobao.simba.insight.wordscats.get
        ===================================
        词和类目查询'''
        request = TOPRequest('taobao.simba.insight.wordscats.get')
        request['wordCategories'] = wordCategories
        request['filter'] = aFilter
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class Cats(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(Cats, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':INCategory}
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, category_ids, nick=None):
        '''taobao.simba.insight.cats.get
        ===================================
        得到类目信息'''
        request = TOPRequest('taobao.simba.insight.cats.get')
        request['category_ids'] = category_ids
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class TopLevelCats(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(TopLevelCats, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'result':INCategory}
        self.fields = ['success','result','result_code','result_message']
    
    def get(self, session, nick=None):
        '''taobao.simba.insight.toplevelcats.get
        ===================================
        得到一级类目'''
        request = TOPRequest('taobao.simba.insight.toplevelcats.get')
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request, session))
        return self.result
    

class CreativeIDs(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CreativeIDs, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','result_code','result_message']
    
    def changed_get(self, start_time, nick=None, page_size=200, page_no=1):
        '''taobao.simba.creativeids.changed.get
        ===================================
        获取修改的创意ID'''
        request = TOPRequest('taobao.simba.creativeids.changed.get')
        request['start_time'] = start_time
        request['page_size'] = page_size
        request['page_no'] = page_no
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request), models={'result':INCategory})
        return self.result
    
    def deleted_get(self, start_time, nick=None, page_size=200, page_no=1):
        '''taobao.simba.creativeids.deleted.get
        ===================================
        获取删除的创意ID'''
        request = TOPRequest('taobao.simba.creativeids.deleted.get')
        request['start_time'] = start_time
        request['page_size'] = page_size
        request['page_no'] = page_no
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class AdGroupIDs(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(AdGroupIDs, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','result_code','result_message']
    
    def changed_get(self, start_time, nick=None, page_size=200, page_no=1):
        '''taobao.simba.adgroupids.changed.get
        ===================================
        获取修改的推广组ID'''
        request = TOPRequest('taobao.simba.adgroupids.changed.get')
        request['start_time'] = start_time
        request['page_size'] = page_size
        request['page_no'] = page_no
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    
    def deleted_get(self, start_time, nick=None, page_size=200, page_no=1):
        '''taobao.simba.adgroupids.deleted.get
        ===================================
        获取删除的推广组ID'''
        request = TOPRequest('taobao.simba.adgroupids.deleted.get')
        request['start_time'] = start_time
        request['page_size'] = page_size
        request['page_no'] = page_no
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class KeywordIDs(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(KeywordIDs, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','result_code','result_message']
    
    def changed_get(self, start_time, nick=None, page_size=200, page_no=1):
        '''taobao.simba.keywordids.changed.get
        ===================================
        获取修改的词ID'''
        request = TOPRequest('taobao.simba.keywordids.changed.get')
        request['start_time'] = start_time
        request['page_size'] = page_size
        request['page_no'] = page_no
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    
    def deleted_get(self, start_time, nick=None, page_size=200, page_no=1):
        '''taobao.simba.keywordids.deleted.get
        ===================================
        获取删除的词ID'''
        request = TOPRequest('taobao.simba.keywordids.deleted.get')
        request['start_time'] = start_time
        request['page_size'] = page_size
        request['page_no'] = page_no
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    

class CatMatchedIDs(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        super(CatMatchedIDs, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['success','result','result_code','result_message']
    
    def changed_get(self, start_time, nick=None, page_size=200, page_no=1):
        '''taobao.simba.catmatchids.changed.get
        ===================================
        获取更改过的类目出价ID'''
        request = TOPRequest('taobao.simba.catmatchids.changed.get')
        request['start_time'] = start_time
        request['page_size'] = page_size
        request['page_no'] = page_no
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    
    def deleted_get(self, start_time, nick=None, page_size=200, page_no=1):
        '''taobao.simba.catmatchids.deleted.get
        ===================================
        获取删除的类目出价ID'''
        request = TOPRequest('taobao.simba.catmatchids.deleted.get')
        request['start_time'] = start_time
        request['page_size'] = page_size
        request['page_no'] = page_no
        if nick!=None: request['nick'] = nick
        self.create(self.execute(request))
        return self.result
    
