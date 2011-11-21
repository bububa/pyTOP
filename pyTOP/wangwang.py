#!/usr/bin/env python
# encoding: utf-8
"""
wangwang.py

Created by 徐 光硕 on 2011-11-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from api import TOP, TOPRequest, TOPDate

class EService(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''wangwang.eservice'''
        super(EService, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'waiting_time_list_on_days':WaitingTimesOnDay, 'msgs':Msg, 'chatpeers':Chatpeer, 'staff_eval_details':EvalDetail, 'staff_eval_stat_on_days':StaffEvalStatOnDay, 'group_member_list':GroupMember, 'loginlogs':LoginLog, 'non_reply_stat_on_days':NonReplyStatOnDay,'online_times_list_on_days':OnlineTimesOnDay,'reply_stat_list_on_days':ReplyStatOnDay,'staff_stream_weights':StreamWeight}
        self.fields = ['waiting_time_list_on_days','msgs','ret','count', 'chatpeers', 'log_file_url', 'staff_eval_details', 'result_code','result_count', 'staff_eval_stat_on_days', 'group_member_list', 'user_id', 'loginlogs','non_reply_stat_on_days','online_times_list_on_days','reply_stat_list_on_days', 'staff_stream_weights','result_code','result_count','total_weight']
    
    def avgwaittime_get(self, service_staff_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.avgwaittime.get 平均等待时长
        ===================================
        根据客服ID和日期，获取该客服"当日接待的所有客户的平均等待时长"。 备注：1、如果是操作者ID=被查者ID，返回被查者ID的"当日接待的所有客户的平均等待时长"。 2、如果操作者是组管理员，他可以查询他的组中的所有子帐号的"当日接待的所有客户的平均等待时长"。 3、如果操作者是主账户，他可以查询所有子帐号的"当日接待的所有客户的平均等待时长"。 4、被查者ID可以是多个，用 "," 隔开，id数不能超过30。 5、开始时间与结束时间之间的间隔不能超过7天 6、不能查询90天以前的数据 7、不能查询当天的记录'''
        request = TOPRequest('taobao.wangwang.eservice.avgwaittime.get')
        request['service_staff_id'] = service_staff_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.waiting_time_list_on_days
    
    def chatlogs_get(self, chat_id, start_date, end_date, charset, session):
        '''taobao.wangwang.eservice.chatpeers.get 获取聊天对象列表，查询时间段<=7天,只支持xml返回
        ===================================
        获取聊天对象列表，查询时间段<=7天,只支持xml返回'''
        request = TOPRequest('taobao.wangwang.eservice.chatlog.get')
        request['chat_id'] = chat_id
        request['charset'] = charset
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.chatpeers
    
    def chatpeers_get(self, from_id, to_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.chatpeers.get 获取聊天对象列表，查询时间段<=7天,只支持xml返回'''
        request = TOPRequest('taobao.wangwang.eservice.chatpeers.get')
        request['from_id'] = from_id
        request['to_id'] = to_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.msgs
    
    def chatrecord_get(self, service_staff_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.chatrecord.get 聊天记录查询
        ===================================
        该接口会返回一个聊天记录的下载地址。 请于5分钟以后使用该链接下载(因为文件大小的不同，生成日志的时间会延长到50分钟),该链接有如下限制： 1.该链接的有效期为3个小时，逾期作废。 2.同一链接只能使用一次。 用户点击地址，下载聊天记录压缩包（压缩包中含有1个文件或多个文件，查询了几个用户的聊天记录，就含有几个文本文件）。 备注：1、如果是操作者ID=被查者ID，返回被查者ID的"聊天记录"。 2、如果操作者是组管理员，他可以查询他的组中的所有子帐号的"聊天记录"。 3、如果操作者是主账户，他可以查询所有子帐号的"聊天记录"。 4、被查者ID可以是多个，用 "," 隔开，id数不能超过30。 5、开始时间与结束时间之间的间隔不能超过7天 6、不能查询30天以前的记录 7、不能查询当天的数据'''
        request = TOPRequest('taobao.wangwang.eservice.chatrecord.get')
        request['service_staff_id'] = service_staff_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.log_file_url
    
    def evals_get(self, service_staff_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.evals.get 获取评价详细
        ===================================
        根据用户id查询用户对应的评价详细情况， 主账号id可以查询店铺内子账号的评价 组管理员可以查询组内账号的评价 非管理员的子账号可以查自己的评价'''
        request = TOPRequest('taobao.wangwang.eservice.evals.get')
        request['service_staff_id'] = service_staff_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.staff_eval_details
    
    def evaluation_get(self, service_staff_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.evaluation.get 客服评价统计
        ===================================
        根据操作者ID，返回被查者ID指定日期内每个帐号每日的"客服评价统计" 备注：1、如果是操作者ID=被查者ID，返回被查者ID的"客服评价统计"。 2、如果操作者是组管理员，他可以查询他的组中的所有子帐号的"客服评价统计"。 3、如果操作者是主账户，他可以查询所有子帐号的"客服评价统计"。 4、被查者ID可以是多个，用 "," 隔开，id数不能超过30。 5、开始时间与结束时间之间的间隔不能超过7天 6、不能查询90天以前的数据 7、不能查询当天的记录'''
        request = TOPRequest('taobao.wangwang.eservice.evaluation.get')
        request['service_staff_id'] = service_staff_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.staff_eval_stat_on_days
    
    def groupmember_get(self, manager_id, session):
        '''taobao.wangwang.eservice.groupmember.get 获取组成员列表
        ===================================
        用某个组管理员账号查询，返回该组组名、和该组所有组成员ID（E客服的分流设置）。 用旺旺主帐号查询，返回所有组的组名和该组所有组成员ID。 返回的组成员ID可以是多个，用 "," 隔开。 被查者ID只能传入一个。 组成员中排名最靠前的ID是组管理员ID'''
        request = TOPRequest('taobao.wangwang.eservice.groupmember.get')
        request['manager_id'] = manager_id
        self.create(self.execute(request, session))
        return self.group_member_list
    
    def loginlogs_get(self, service_staff_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.loginlogs.get 获取登录日志
        ===================================
        通过用户id查询用户自己或者子账户的登录日志： 主账号可以查询自己和店铺子账户的登录日志 组管理员可以查询自己和组内子账号的登录日志 非组管理员的子账户只能查询自己的登录日志'''
        request = TOPRequest('taobao.wangwang.eservice.loginlogs.get')
        request['service_staff_id'] = service_staff_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.loginlogs
    
    def noreplynum_get(self, service_staff_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.noreplynum.get 客服未回复人数
        ===================================
        根据操作者ID，返回被查者ID指定日期内每个帐号每日的"未回复情况" 备注：1、如果是操作者ID=被查者ID，返回被查者ID的"未回复情况"（未回复人数、未回复的ID）。 2、如果操作者是组管理员，他可以查询他的组中的所有子帐号的"未回复情况"。 3、如果操作者是主账户，他可以查询所有子帐号的"未回复情况"。 4、被查者ID可以是多个，用 "," 隔开，id数不能超过30。 5、开始时间与结束时间之间的间隔不能超过7天 6、不能查询90天以前的数据 7、不能查询当天的记录'''
        request = TOPRequest('taobao.wangwang.eservice.noreplynum.get')
        request['service_staff_id'] = service_staff_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.non_reply_stat_on_days
    
    def onlinetime_get(self, service_staff_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.onlinetime.get 日累计在线时长
        ===================================
        描述：根据客服ID和日期，获取该客服"当日在线时长"。 备注：1、如果是操作者ID=被查者ID，返回被查者ID的"当日在线时长"。 2、如果操作者是组管理员，他可以查询他的组中的所有子帐号的"当日在线时长"。 3、如果操作者是主账户，他可以查询所有子帐号的"当日在线时长"。 4、被查者ID可以是多个，用 "," 隔开，id数不能超过30。 5、日累计在线时长定义：当日该用户累计的旺旺在线时长 6、开始时间与结束时间之间的间隔不能超过7天 7、不能查询90天以前的数据 8、不能查询当天的记录'''
        request = TOPRequest('taobao.wangwang.eservice.onlinetime.get')
        request['service_staff_id'] = service_staff_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.online_times_list_on_days
    
    def receivenum_get(self, service_staff_id, start_date, end_date, session):
        '''taobao.wangwang.eservice.receivenum.get 客服接待数
        ===================================
        根据操作者ID，返回被查者ID指定时间段内每个帐号的"已接待人数" 备注：1、如果是操作者ID=被查者ID，返回被查者ID的"已接待人数"。 2、如果操作者是组管理员，他可以查询他的组中的所有子帐号的"已接待人数"。 3、如果操作者是主账户，他可以查询所有子帐号的"已接待人数"。 4、被查者ID可以是多个，用 "," 隔开，id数不能超过30。 5、规则：某客服在1天内和同一个客户交流了多次，已回复人数算1。 6、"已接待人数"定义：买家、卖家彼此发过至少1条消息 ，不论谁先发都可以。 4、被查者ID可以是多个，用 "," 隔开，id数不能超过30。 7、开始时间与结束时间之间的间隔不能超过7天 8、不能查询90天以前的数据 9、不能查询当天的记录'''
        request = TOPRequest('taobao.wangwang.eservice.receivenum.get')
        request['service_staff_id'] = service_staff_id
        request['start_date'] = start_date
        request['end_date'] = end_date
        self.create(self.execute(request, session))
        return self.reply_stat_list_on_days
    
    def streamweigths_get(self, session):
        '''taobao.wangwang.eservice.streamweigths.get 获取分流权重接口
        ===================================
        获取当前登录用户自己的店铺内的分流权重设置'''
        request = TOPRequest('taobao.wangwang.eservice.streamweigths.get')
        self.create(self.execute(request, session))
        return self.staff_stream_weights
    

class WaitingTimesOnDay(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''客户等待（客服）平均时长列表'''
        super(WaitingTimesOnDay, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'waiting_date':TOPDate, 'waiting_time_by_ids':WaitingTimeById}
        self.fields = ['waiting_date','waiting_time_by_ids']

class NonReplyStatOnDay(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''未回复统计列表(按天)'''
        super(NonReplyStatOnDay, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'nonreply_date':TOPDate, 'nonreply_stat_by_ids':NonreplyStatById}
        self.fields = ['nonreply_date','nonreply_stat_by_ids']
    

class StaffEvalStatOnDay(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''客服评价统计列表(按天)'''
        super(StaffEvalStatOnDay, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'eval_date':TOPDate, 'staff_eval_stat_by_ids':StaffEvalStatById}
        self.fields = ['eval_date','staff_eval_stat_by_ids']
    

class OnlineTimesOnDay(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''某天的客服在线时长列表'''
        super(OnlineTimesOnDay, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'online_date':TOPDate, 'online_time_by_ids':OnlineTimeById}
        self.fields = ['online_date','online_time_by_ids']
    

class Msg(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''聊天消息内容'''
        super(Msg, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['direction','time','content']
    

class NonreplyStatById(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''客服未回复统计'''
        super(NonreplyStatById, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['service_staff_id','non_reply_num','non_reply_customId']
    

class StaffEvalStatById(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''客服评价统计'''
        super(StaffEvalStatById, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'evaluations':Evaluation}
        self.fields = ['service_staff_id','evaluations']
    

class ReplyStatOnDay(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''(某天)回复统计列表'''
        super(ReplyStatOnDay, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'reply_date':TOPDate, 'reply_stat_by_ids':ReplyStatById}
        self.fields = ['reply_date','reply_stat_by_ids']
    

class Evaluation(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''客服评价'''
        super(Evaluation, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['evaluation_name','evaluation_num']
    

class OnlineTimeById(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''在线时长'''
        super(OnlineTimeById, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['service_staff_id','online_times']
    

class WaitingTimeById(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''平均等待时长'''
        super(WaitingTimeById, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['service_staff_id','avg_waiting_times']
    

class ReplyStatById(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''客服回复统计'''
        super(ReplyStatById, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['user_id','reply_num']
    

class LoginLog(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''登录日志'''
        super(LoginLog, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['time','type']
    

class EvalDetail(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''评价详细'''
        super(EvalDetail, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.models = {'send_time':TOPDate, 'eval_time':TOPDate}
        self.fields = ['eval_sender','eval_recer','send_time','eval_time','eval_code']
    

class StreamWeight(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''分流权重'''
        super(StreamWeight, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['user','weight']
    

class Chatpeer(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''聊天对象ID列表'''
        super(Chatpeer, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['uid','date']
    

class GroupMember(TOP):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        '''组及其成员列表'''
        super(GroupMember, self).__init__( API_KEY, APP_SECRET, ENVIRONMENT )
        self.fields = ['group_name','member_list','group_id']
    















