====================
Scrapy-HTTPCache
====================

.. image:: https://img.shields.io/pypi/v/scrapy-httpcache.svg
   :target: https://pypi.python.org/pypi/scrapy-httpcache
   :alt: PyPI Version

.. image:: https://img.shields.io/travis/xiaowangwindow/scrapy-httpcache/master.svg
   :target: http://travis-ci.org/xiaowangwindow/scrapy-httpcache
   :alt: Build Status

Overview
========

scrapy-httpcache is a scrapy middleware to save http cache in mongodb.
Besides, scrapy-httpcache contains two extra storage plugin,
including request_error_storage and banned_storage.
request_error_storage can save Request which occur error.
banned_storage can save Banned Request whose block_checker can be override.


Requirements
============

* Python 3.3+
* Works on Linux, Windows, Mac OSX, BSD

Install
=======

The quick way::

    pip install scrapy-httpcache

OR copy this middleware to your scrapy project.

Documentation
=============

In settings.py, for example::

    # -----------------------------------------------------------------------------
    # SCRAPY HTTPCACHE SETTINGS
    # -----------------------------------------------------------------------------
    DOWNLOADER_MIDDLEWARES.update({
        'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
        'scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware': 900,
    })

    HTTPCACHE_ENABLED = True
    HTTPCACHE_IGNORE_HTTP_CODES = [301, 302, 500, 503]
    HTTPCACHE_STORAGE = 'scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage'
    HTTPCACHE_MONGODB_STORAGE_URI = 'mongodb://127.0.0.1:27017'
    HTTPCACHE_MONGODB_STORAGE_DB = MONGODB_DATABASE
    HTTPCACHE_MONGODB_STORAGE_COLL = 'cache'

    # -----------------------------------------------------------------------------
    # SCRAPY HTTPCACHE BANNED SETTINGS (optional)
    # -----------------------------------------------------------------------------
    BANNED_STORAGE = 'scrapy_httpcache.extensions.banned_storage.MongoBannedStorage'
    BANNED_MONGODB_STORAGE_URI = 'mongodb://127.0.0.1:27017'
    BANNED_MONGODB_STORAGE_DB = MONGODB_DATABASE

    # -----------------------------------------------------------------------------
    # SCRAPY HTTPCACHE REQUEST ERROR SETTINGS (optional)
    # -----------------------------------------------------------------------------
    REQUEST_ERROR_STORAGE = 'scrapy_httpcache.extensions.request_error_storage.MongoRequestErrorStorage'
    REQUEST_ERROR_MONGODB_STORAGE_URI = 'mongodb://127.0.0.1:27017'
    REQUEST_ERROR_MONGODB_STORAGE_DB = MONGODB_DATABASE
