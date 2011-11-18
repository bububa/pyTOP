#!/usr/bin/env python
# encoding: utf-8
"""
api.py

Created by 徐 光硕 on 2011-11-14.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import time
import datetime
from dateutil.parser import *
try :  
    import json  
except ImportError :  
    import simplejson as json  
import urllib
from hashlib import md5  
import base64

from errors import TOPException
import requests
from pprint import pprint

class TOPDate:
    def create(self, date_str):
        try:
            return parse(date_str)
        except:
            return date_str
    

class TOPRequest :
    def __init__(self, method_name) :  
        self.method_name = method_name  
        self.api_params = {}  
    def get_api_params(self) : return self.api_params  
    def get_method_name(self) : return self.method_name  
    def __setitem__(self, param_name, param_value) : self.api_params[param_name] = param_value

class TOP(object):
    def __init__(self, API_KEY=None, APP_SECRET=None, ENVIRONMENT='sandbox'):
        self.PRODUCT_API_KEY = '12422885'
        self.PRODUCT_APP_SECRET = '9f127588ceb726905e078b64ab88a361'
        self.SANDBOX_API_KEY = '12422885'
        self.SANDBOX_APP_SECRET = 'sandbox8ceb726905e078b64ab88a361'
        self.API_URL = 'http://gw.api.taobao.com/router/rest' #淘宝正式环境
        self.SANDBOX_URL = 'http://gw.api.tbsandbox.com/router/rest' #淘宝测试环境
        self.ENVIRONMENT = ENVIRONMENT # or product
        self.FORMAT = 'json'  
        self.SIGN_METHOD = 'md5'  
        self.API_VERSION = '2.0'  
        self.SDK_VERSON = 'pyTOP_0.1.0'
        if self.ENVIRONMENT == 'sandbox':
            if API_KEY:
                self.SANDBOX_API_KEY = API_KEY
            if APP_SECRET:
                self.SANDBOX_APP_SECRET = APP_SECRET
            self.GATEWAY = self.SANDBOX_URL
            self.API_KEY = self.SANDBOX_API_KEY
            self.APP_SECRET = self.SANDBOX_APP_SECRET
        elif self.ENVIRONMENT == 'product':
            if API_KEY:
                self.PRODUCT_API_KEY = API_KEY
            if APP_SECRET:
                self.PRODUCT_APP_SECRET = APP_SECRET
            self.GATEWAY = self.API_URL
            self.API_KEY = self.PRODUCT_API_KEY
            self.APP_SECRET = self.PRODUCT_APP_SECRET
        else:
            raise TOPException(0);
        self.AUTH_URL = 'http://container.api.taobao.com/container?appkey=%s' % self.API_KEY
    
    def set_format(self, format):
        if format in ('json','xml'): self.FORMAT = format
    
    def _sign(self,params):
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
    
    def execute(self, request, session=None):
        '''
        request -- TOPRequest instance
        '''
        params = {
            'app_key' : self.API_KEY,  
            'v'       : self.API_VERSION,
            'format'  : self.FORMAT,
            #'sign_method' : self.SIGN_METHOD,
            'partner_id'  : self.SDK_VERSON
        }
        api_params = request.get_api_params()
        params['timestamp'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %X")
        params['method'] = request.get_method_name()
        if session is not None :
            params['session'] = session
        params.update(api_params)
        params['sign'] = self._sign(params)
        #print params
        #form_data = urllib.urlencode(params)
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
    

        
        