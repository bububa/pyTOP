.. pyTOP documentation master file, created by
   sphinx-quickstart on Tue Nov 22 17:55:49 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyTOP: Taobao Open Platform API python Wrapper
===============================================

pyTOP is an ISC Licensed Taobao Open Platform API library, written in Python.


Features
--------

- 用户 API
- 类目 API
- 商品 API
- 店铺 API
- 交易 API
- 店铺会员管理 API
- 子账号管理 API
- 旺旺 API
- 物流 API
- 评价 API
- 收藏夹 API
- 系统时间 API
- 分销 API
- 淘客 API
- 主动通知业务 API
- 在线订购 API
- insight API
- campagin API


Requirements
------------

- Requests (https://github.com/kennethreitz/requests)
- Urllib3 (http://code.google.com/p/urllib3/)
- Dateutil (http://labix.org/python-dateutil)

Installation
------------

To install pyTOP, simply: ::

   $ pip install pyTOP

Or, if you absolutely must: ::
   
   $ easy_install pyTOP
   
Or, download the source file and run: ::

   $ python setup.py install


Usage
-----

You could setup API KEY and APP SECRET in system environment (~/.bash_profile)
::
    
    # TOP ENVIRONMENT
    TOP_ENVIRONMENT = product # or sandbox
    # PRODUCT VARS
    TOP_PRODUCT_API_KEY = 12345678
    TOP_PRODUCT_APP_SECRET = 9f127588ceb726905e078b64ab88a362
    TOP_PRODUCT_API_URL = http://gw.api.taobao.com/router/rest
    # SANDBOX VARS
    TOP_SANDBOX_API_KEY = 12345678
    TOP_SANDBOX_APP_SECRET = sandbox8ceb726905e078b64ab88a362
    TOP_SANDBOX_API_URL = http://gw.api.tbsandbox.com/router/rest

::

   >>> user = User()
   >>> user.get('bububa')
   >>> print user
   <User: user_id=180018765, uid=520be25d2ae9de5ea1d6a784e67d6edf, nick=bububa, buyer_credit=<UserCredit: level=0, score=0, total_num=0, good_num=0>, seller_credit=<UserCredit: level=0, score=0, total_num=0, good_num=0>, created=2011-11-21 15:11:47, last_visit=2011-11-21 15:12:07, type=C, has_shop=False, is_lightning_consignment=False>
   ...


API Document
------------
.. toctree::
   :maxdepth: 2

   api


Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. There is a Contributor Friendly tag for issues that should be ideal for people who are not very familiar with the codebase yet.
#. Fork `the repository`_ on Github to start making your changes to the **develop** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/bububa/pyTOP
.. _AUTHORS: http://github.com/bububa/pyTOP/blob/master/AUTHORS

