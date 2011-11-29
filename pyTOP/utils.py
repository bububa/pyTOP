#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by 徐 光硕 on 2011-11-28.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from operator import itemgetter
import threading
import Queue
import traceback

try: 
    from cStringIO import StringIO 
except ImportError: 
    from StringIO import StringIO

def Traceback():
    try:
        s = StringIO() 
        traceback.print_exc(file=s) 
        return s.getvalue()
    except:
        return ''

def sort_dict(self, data, key):
    '''Sort a list of dictionaries by dictionary key'''
    return sorted(data, key=itemgetter(key)) if data else []

class ThreadPool:
    '''ThreadPool Utility'''
    def __init__(self,maxWorkers = 10):
        self.tasks = Queue.Queue()
        self.workers = 0
        self.working = 0
        self.responses = []
        self.maxWorkers = maxWorkers
        self.allKilled = threading.Event()
        self.countLock = threading.RLock()
        self.allKilled.set()
    
    def run(self, target, callback=None, *args, **kargs):
        self.countLock.acquire()
        if not self.workers:
            self.addWorker()
        self.countLock.release()
        self.tasks.put((target,callback,args,kargs))
    
    def setMaxWorkers(self,num):
        self.countLock.acquire()
        self.maxWorkers = num
        if self.workers > self.maxWorkers:
            self.killWorker(self.workers - self.maxWorkers)
        self.countLock.release()
    
    def addWorker(self,num = 1):
        for x in xrange(num):
            self.countLock.acquire()
            self.workers += 1
            self.allKilled.clear()
            self.countLock.release()        
            t = threading.Thread(target = self.__workerThread)
            t.setDaemon(True)
            t.start()
    
    def killWorker(self,num = 1):
        self.countLock.acquire()
        if num > self.workers:
            num = self.workers
        self.countLock.release()
        for x in xrange(num):
            self.tasks.put("exit")  
    
    def killAllWorkers(self, wait=None):
        self.countLock.acquire()
        self.killWorker(self.workers)
        self.countLock.release()
        self.allKilled.wait(wait)
        responses = self.responses
        self.responses = []
        return responses
    
    def __workerThread(self):
        while True:
            try:
                task = self.tasks.get(timeout=2)
            except:
                break
            # exit is "special" tasks to kill thread
            if task == "exit":
                break
            
            self.countLock.acquire()
            self.working += 1
            if (self.working >= self.workers) and (self.workers < self.maxWorkers): # create thread on demand
                self.addWorker()
            self.countLock.release()
            
            fun,cb,args,kargs = task
            try:
                ret = fun(*args,**kargs)
                if cb:
                    self.responses.append(cb(ret))
                else:
                    self.responses.append(ret)
            except Exception, err:
                print Traceback()
            self.countLock.acquire()
            self.working -= 1
            self.countLock.release()
        
        self.countLock.acquire()
        self.workers -= 1
        if not self.workers:
            self.allKilled.set()
        self.countLock.release()
    
