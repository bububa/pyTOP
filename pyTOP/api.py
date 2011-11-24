#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by 徐 光硕 on 2011-11-14.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
from os import getenv
import time
import datetime
from dateutil.parser import parse as date_parse
try :  
    import json  
except ImportError:  
    import simplejson as json  
import urllib
from hashlib import md5  
import base64

from errors import TOPException
import requests
#from pprint import pprint

class TOPDate:
    '''
    pyTOP Date Object
    '''
    def create(self, date_str):
        '''
        Convert string to datetime.datetime
        '''
        try:
            return date_parse(date_str)
        except:
            return date_str
    

class TOPRequest :
    '''
    pyTOP Request Object
    '''
    def __init__(self, method_name) :
        self.method_name = method_name  
        self.api_params = {}  
    def get_api_params(self) : return self.api_params  
    def get_method_name(self) : return self.method_name  
    def __setitem__(self, param_name, param_value) : self.api_params[param_name] = param_value

class TOP(object):
    '''
    Basic API class. All the API models are inherited from this class
    '''
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT=None):
        #淘宝正式环境
        #self.PRODUCT_API_KEY = '12422885'
        #self.PRODUCT_APP_SECRET = '9f127588ceb726905e078b64ab88a361'
        self.PRODUCT_API_KEY = getenv('TOP_PRODUCT_API_KEY')
        self.PRODUCT_APP_SECRET = getenv('TOP_PRODUCT_APP_SECRET')
        self.PRODUCT_API_URL = getenv('TOP_PRODUCT_API_URL') if getenv('TOP_PRODUCT_API_URL') else 'http://gw.api.taobao.com/router/rest'
        self.PRODUCT_LOGIN_URL = 'http://container.api.taobao.com/container?appkey='
        self.LOGOUT_URL = 'http://container.api.taobao.com/container/logoff'
        self.TaobaoID_URL = 'http://container.api.taobao.com/container/identify'
        #淘宝测试环境
        #self.SANDBOX_API_KEY = '12422885'
        #self.SANDBOX_APP_SECRET = 'sandbox8ceb726905e078b64ab88a361'
        self.SANDBOX_API_KEY = getenv('TOP_SANDBOX_API_KEY')
        self.SANDBOX_APP_KEY = getenv('TOP_SANDBOX_APP_SECRET')
        self.SANDBOX_API_URL = getenv('TOP_SANDBOX_API_URL') if getenv('TOP_SANDBOX_API_URL') else 'http://gw.api.tbsandbox.com/router/rest'
        self.SANDBOX_LOGIN_URL = 'http://container.api.tbsandbox.com/container?appkey='
        self.SANDBOX_USER_REGISTER_WITHOUT_VALIDATE = 'http://mini.tbsandbox.com/minisandbox/user/register.htm'
        
        self.REFRESH_TOKEN_URL = 'http://container.open.taobao.com/container/refresh'
        self.ENVIRONMENT = ENVIRONMENT if ENVIRONMENT else (getenv('TOP_ENVIRONMENT') if getenv('TOP_ENVIRONMENT') else 'sandbox')
        self.FORMAT = 'json'  
        self.SIGN_METHOD = 'md5'  
        self.API_VERSION = '2.0'  
        self.SDK_VERSON = 'pyTOP_0.1.0'
        
        if self.ENVIRONMENT == 'sandbox':
            if API_KEY:
                self.SANDBOX_API_KEY = API_KEY
            if APP_SECRET:
                self.SANDBOX_APP_SECRET = APP_SECRET
            self.GATEWAY = self.SANDBOX_API_URL
            self.LOGIN_URL = self.SANDBOX_LOGIN_URL
            self.API_KEY = self.SANDBOX_API_KEY
            self.APP_SECRET = self.SANDBOX_APP_SECRET
        elif self.ENVIRONMENT == 'product':
            if API_KEY:
                self.PRODUCT_API_KEY = API_KEY
            if APP_SECRET:
                self.PRODUCT_APP_SECRET = APP_SECRET
            self.GATEWAY = self.PRODUCT_API_URL
            self.LOGIN_URL = self.PRODUCT_LOGIN_URL
            self.API_KEY = self.PRODUCT_API_KEY
            self.APP_SECRET = self.PRODUCT_APP_SECRET
        else:
            raise TOPException(0);
        self.AUTH_URL = 'http://container.api.taobao.com/container?appkey=%s' % self.API_KEY
    
    def set_format(self, format):
        if format in ('json','xml'): self.FORMAT = format
    
    def _sign(self,params):
        '''
        Generate API sign code
        '''
        for k, v in params.iteritems():
            if type(v) == int: v = str(v)
            elif type(v) == float: v = '%.2f'%v
            elif type(v) in (list, set): 
                v = ','.join([str(i) for i in v])
            elif type(v) == bool: v = 'true' if v else 'false'
            elif type(v) == datetime.datetime: v = v.strftime('%Y-%m-%d %X')
            if type(v) == unicode:
                params[k] = v.encode('utf-8')
            else:
                params[k] = v
        src = self.APP_SECRET + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems())])
        return md5(src).hexdigest().upper()
    
    def decode_params(top_parameters) :  
        params = {}  
        param_string = base64.b64decode(top_parameters)  
        for p in param_string.split('&') :  
            key, value = p.split('=')  
            params[key] = value  
        return params
    
    def _get_timestamp(self):
        #gmtimefix = 28800
        #stime = time.gmtime(time.time() - time.timezone + gmtimefix)
        if(time.timezone == 0):
            gmtimefix = 28800
            stime = time.gmtime(gmtimefix + time.time())
        else:
            stime = time.localtime()
        strtime = time.strftime('%Y-%m-%d %X', stime)
        return strtime
    
    def execute(self, request, session=None, method='post'):
        '''
        pyTOP.API -- TOPRequest instance
        '''
        params = {
            'app_key' : self.API_KEY,  
            'v'       : self.API_VERSION,
            'format'  : self.FORMAT,
            #'sign_method' : self.SIGN_METHOD,
            'partner_id'  : self.SDK_VERSON
        }
        api_params = request.get_api_params()
        params['timestamp'] = self._get_timestamp()
        params['method'] = request.get_method_name()
        if session is not None :
            params['session'] = session
        params.update(api_params)
        params['sign'] = self._sign(params)
        #print params
        method = method.lower()
        if method == 'get':
            form_data = urllib.urlencode(params)
            rsp = requests.get('%s?%s'%(self.GATEWAY, form_data))
        elif method == 'post':
            rsp = requests.post(self.GATEWAY, data=params)
        rsp = json.loads(rsp.content)
        if rsp.has_key('error_response'):
            error_code = rsp['error_response']['code']
            if 'sub_msg' in rsp['error_response']:
                msg = rsp['error_response']['sub_msg']
            else:
                msg = rsp['error_response']['msg']
            raise TOPException(error_code, msg)
        else:
            #pprint(rsp)
            rsp = rsp[request.get_method_name().replace('.','_')[7:] + '_response']
            if not rsp: return None
            return rsp
    
    def create(self, data, fields=[], models={}):
        '''
        Create model attributes
        '''
        if not fields: fields = self.fields
        if not models and hasattr(self, 'models'): models = self.models
        for field in fields:
            setattr(self,field,None)
        if not data: return None
        for k, v in data.iteritems():
            if type(v) in (str, unicode):
                v = v.strip()
            if models and k in models:
                if type(v) == dict:
                    lists = []
                    for k2, v2 in v.iteritems():
                        if type(v2) == list:
                            for d in v2:
                                model = models[k]()
                                lists.append(model.create(d))
                    if not lists:
                        model = models[k]()
                        v = model.create(v)
                    else:
                        v = lists
                else:
                    model = models[k]()
                    v = model.create(v)
            setattr(self,k,v)
        return self
    
    def __str__(self):
        attrs = []
        for field in self.fields:
            if hasattr(self, field):
                v = getattr(self, field)
                if v==None: continue
                if type(v) == unicode: v = v.encode('utf-8')
                attrs.append('%s=%s'%(field, v))
        return "<%s: %s>" %(self.__class__.__name__, ', '.join(attrs))
    
    __repr__ = __str__

        
        