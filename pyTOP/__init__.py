#!/usr/bin/env python
# encoding: utf-8
"""
pyTOP
~~~~~~~~

:copyright: (c) 2011 by Prof Syd Xu.
:license: ISC, see LICENSE for more details.

"""

__title__ = 'pyTOP'
__version__ = '0.1.0'
__build__ = 0x000800
__author__ = 'Prof Syd Xu'
__license__ = 'ISC'
__copyright__ = 'Copyright 2011 Prof Syd Xu'

# basic API
from .api import TOP, TOPDate, TOPRequest
# 用户 API
from .user import User, Location, UserCredit, Users
# 类目 API
from .category import PropValue, SellerAuthorize, ItemCat, ItemProps, ItemPropValues
# 商品 API
from .item import Item, Items, Sku, Skus, ItemImg, PropImg, Video, ItemCategory, ProductPropImg, ProductImg, AfterSale, ItemTemplate, ItemTelplates, ItemSearch, Product, Products
# 店铺 API
from .shop import ShopCat, ShopCats, ShopScore, SellerCat, SellerCats, Shop
# 交易 API
from .trade import PromotionDetail, OrderAmount, Order, TradeAmount, TradeAccountDetail, Task, Trade, Trades, Subtask, TradeConfirmFee, TradeRate, TradRates
# 店铺会员管理 API
from .crm import GroupDomain, BasicMember, GradePromotion, RuleData, CrmMember, Group, Groups, GroupTask, MemberInfo, Members, Grade, Rule, Rules, ShopVip
# 子账号管理 API
from .sellercenter import SubUserInfo, SubUsers
# 旺旺 API
from .wangwang import EService, WaitingTimesOnDay, NonReplyStatOnDay, StaffEvalStatOnDay, OnlineTimesOnDay, Msg, NonreplyStatById, StaffEvalStatById, ReplyStatOnDay, Evaluation, OnlineTimeById, WaitingTimeById, ReplyStatById, LoginLog, EvalDetail, StreamWeight, Chatpeer, GroupMember
# 收藏夹 API
from .favorite import CollectItem, Favorite
# Customize Exceptions
from .errors import TOPException