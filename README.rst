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
    HTTPCACHE_MONGODB_HOST = '127.0.0.1'
    HTTPCACHE_MONGODB_PORT = 27017
    HTTPCACHE_MONGODB_USERNAME = 'root'
    HTTPCACHE_MONGODB_PASSWORD = 'password'
    HTTPCACHE_MONGODB_AUTH_DB = 'admin'
    HTTPCACHE_MONGODB_DB = 'cache_storage'
    HTTPCACHE_MONGODB_COLL = 'cache'

    # -----------------------------------------------------------------------------
    # SCRAPY HTTPCACHE BANNED SETTINGS (optional)
    # -----------------------------------------------------------------------------
    BANNED_STORAGE = 'scrapy_httpcache.extensions.banned_storage.MongoBannedStorage'

    # -----------------------------------------------------------------------------
    # SCRAPY HTTPCACHE REQUEST ERROR SETTINGS (optional)
    # -----------------------------------------------------------------------------
    REQUEST_ERROR_STORAGE = 'scrapy_httpcache.extensions.request_error_storage.MongoRequestErrorStorage'

If you want to remove banned response, use `send_catch_log_deferred` to send signal to `scrapy_httpcache.signals.remove_banned`
with kwargs contains (spider, response, exception), which callback function return a Deferred.
