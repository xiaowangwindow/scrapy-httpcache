# Enable and configure HTTP caching (disabled by default)
# See
# http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
MONGODB_DATABASE = ''
DOWNLOADER_MIDDLEWARES = {}
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

BANNED_STORAGE = 'scrapy_httpcache.extensions.banned_storage.MongoBannedStorage'
BANNED_MONGODB_STORAGE_URI = 'mongodb://127.0.0.1:27017'
BANNED_MONGODB_STORAGE_DB = MONGODB_DATABASE

REQUEST_ERROR_STORAGE = 'scrapy_httpcache.extensions.request_error_storage.MongoRequestErrorStorage'
REQUEST_ERROR_MONGODB_STORAGE_URI = 'mongodb://127.0.0.1:27017'
REQUEST_ERROR_MONGODB_STORAGE_DB = MONGODB_DATABASE
