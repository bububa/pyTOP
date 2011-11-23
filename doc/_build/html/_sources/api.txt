.. _api:

pyTOP's API Document
=========================

Contents:

This part of the documentation covers all the interfaces of pyTOP.  For
parts where Requests depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Basic API
--------------

All of pyTOP's functionality can be accessed by these 3 methods.
They all return an instance of the :class:`TOP <TOP>` object.

.. module:: api

.. autoclass:: TOP
   :inherited-members:

.. autoclass:: TOPRequest
  :inherited-members:

.. autoclass:: TOPDate
  :inherited-members:

---------------------


.. _exceptions:

Exceptions
--------------
.. module:: errors

.. autoexception:: TOPException

---------------------


API
--------------

.. toctree::
   :maxdepth: 2

   user
   category
   item
   shop
   trade
   crm
   sellercenter
   wangwang
   logistics
   favorite
   traderate
   systime
   fenxiao

---------------------


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


