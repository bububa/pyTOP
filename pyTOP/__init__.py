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
from .item import Item, Items, Sku, Skus, ItemImg, PropImg, Video, ItemCategory, ProductPropImg, ProductImg, AfterSale, ItemTemplate, ItemTemplates, ItemSearch, Product, Products
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
# 物流 API
from .logistics import TransitStepInfo, Area, DeliveryTemplate, DeliveryTemplates, PartnerDetail, LogisticsCompany, LogisticsCompanies, PostageMode, Shipping, TopFee, Postage, Postages, AddressResult, LogisticsPartner, LogisticsPartners, LogisticsAddress, LogisticsDummy, LogisticsOffline, LogisticsOnline, Orders, LogisticsTrace, TopatsDelivery
# 收藏夹 API
from .favorite import CollectItem, Favorite
# 评价 API
from .traderate import TradeRate, TradeRates
# 系统十佳 API
from .systime import SysTime
# 分销 API
from .fenxiao import Discount, Discounts, DiscountDetail, FenxiaoSku, FenxiaoItemRecord, Cooperation, FenxiaoGrade, FenxiaoGrades, Receiver, LoginUser, Distributor, Distributors, PurchaseOrder, FenxiaoProduct, FenxiaoProducts, SubPurchaseOrder, ProductCat, ProductCats, FenxiaoOrder, FenxiaoOrders
# 淘客 API
from .taobaoke import TaobaokeReportMember, TaobaokeReport, TaobaokeItemDetail, TaobaokeItem, TaobaokeShop, TaobaokeShops, Taobaoke
# 主动通知业务 API
from .increment import NotifyRefund, NotifyItem, NotifyTrade, AppCustomer, Increment
# insight API
from .insight import INWordBase, INCategoryBase, INWordAnalysis, INCategoryAnalysis, INCategoryProperties, INCategory, INWordCategory, INRecordBase, INCategoryAnalysisTop, INCategoryChildTop, INCategoryTop, INWordAnalysisTop, WordBase, CatsBase, WordAnalysis, CatsAnalysis, CatsForecast, CatsTopWord, CatsRelatedWord, WordsCats, Cats, TopLevelCats, CreativeIDs, AdGroupIDs, KeywordIDs, CatMatchedIDs
# Campagin API
from .campaign import AreaOption, ChannelOption, Campaign, Campaigns, CampaignArea, CampaignBudget, CampaignPlatform, CampaignSchedule, ADGroups, ADGroup, ADGroupCatmatch, Creative, Creatives, CreativeRecord, Keyword, Keywords, AccountRecord, RecommendWord, RankedItem, ADGroupPage, RecommendWordPage, Result, Customers, Account, Tools
# Customize Exceptions
from .errors import TOPException