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
HTTPCACHE_MONGODB_STORAGE_HOST = '127.0.0.1'
HTTPCACHE_MONGODB_STORAGE_PORT = 27017
HTTPCACHE_MONGODB_USERNAME = None
HTTPCACHE_MONGODB_PASSWORD = None
HTTPCACHE_MONGODB_AUTH_DB = None
HTTPCACHE_MONGODB_STORAGE_DB = MONGODB_DATABASE
HTTPCACHE_MONGODB_STORAGE_COLL = 'cache'
HTTPCACHE_MONGODB_CONNECTION_POOL_KWARGS = {}

BANNED_STORAGE = 'scrapy_httpcache.extensions.banned_storage.MongoBannedStorage'

REQUEST_ERROR_STORAGE = 'scrapy_httpcache.extensions.request_error_storage.MongoRequestErrorStorage'