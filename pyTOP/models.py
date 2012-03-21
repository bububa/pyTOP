#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by 徐 光硕 on 2012-02-06.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Sequence, Integer, String, Text, MetaData, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.sql import and_, or_, not_

SQLBase = declarative_base()


def sqlite_engine(db_path, echo=False):
    #db_path = 'sqlite:////Users/syd/Desktop/taobao.sqlite'
    engine = create_engine(db_path, echo=echo)
    return engine

def postgres_engine(echo=False):
    engine = create_engine('postgresql://syd:00320398@127.0.0.1:5432/test', echo=echo)
    return engine

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

    
keyword_categories = Table('keyword_categories', SQLBase.metadata, Column('category_id', Integer, ForeignKey('categories.id', onupdate="cascade", ondelete="cascade"), primary_key=True ), Column('keyword_id', Integer, ForeignKey('keywords.id', onupdate="cascade", ondelete="cascade"), primary_key=True))

class Category(SQLBase):
    __tablename__ = 'categories'
    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    cid = Column(String(12), unique=True)
    name = Column(String(30))
    level = Column(Integer)
    pid = Column(Integer, ForeignKey('categories.id'))
    children = relationship("Category", backref=backref('parent', remote_side=[id]) )
    keywords = relationship("Keyword", secondary=keyword_categories, backref="categories")
    
    def __init__(self, cid, name, level, pid):
        self.cid = cid
        self.name = name
        self.level = level
        self.pid = pid
    
    def __repr__(self):
        return "<Category('%s','%s', %d, '%s')>" % (self.cid.encode('utf-8'), self.name.encode('utf-8'), self.level, self.pid)
    

class Keyword(SQLBase):
    __tablename__ = 'keywords'
    id = Column(Integer, Sequence('keyword_id_seq'), primary_key=True)
    name = Column(String, unique=True)
    #categories = relationship("Category", secondary=keyword_categories, backref="keywords")
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Keyword('%s')>" % (self.name)
    

    
