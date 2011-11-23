pyTOP: Taobao Open Platform API python Wrapper
=========================

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
- insight API
- campagin API


Requirements
------------

- Requests (https://github.com/kennethreitz/requests)
- Urllib3 (http://code.google.com/p/urllib3/)
- Dateutil (http://labix.org/python-dateutil)

Installation
------------

To install pyTOP, first download the files then simply: ::

    $ python setup.py install


Usage
-----

::

    >>> user = User()
    >>> user.get('bububa')
    >>> print user
    <User: user_id=180018765, uid=520be25d2ae9de5ea1d6a784e67d6edf, nick=bububa, buyer_credit=<UserCredit: level=0, score=0, total_num=0, good_num=0>, seller_credit=<UserCredit: level=0, score=0, total_num=0, good_num=0>, created=2011-11-21 15:11:47, last_visit=2011-11-21 15:12:07, type=C, has_shop=False, is_lightning_consignment=False>
    ...


Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. There is a Contributor Friendly tag for issues that should be ideal for people who are not very familiar with the codebase yet.
#. Fork `the repository`_ on Github to start making your changes to the **develop** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/bububa/pyTOP
.. _AUTHORS: http://github.com/bububa/pyTOP/blob/master/AUTHORS
