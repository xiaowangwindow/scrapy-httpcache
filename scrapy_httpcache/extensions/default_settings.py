# DOWNLOADER_MIDDLEWARES = {}
# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
#     'scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware': 900,
# })

HTTPCACHE_STORAGE = 'scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage'
HTTPCACHE_MONGODB_HOST = '127.0.0.1'
HTTPCACHE_MONGODB_PORT = 27017
HTTPCACHE_MONGODB_USERNAME = None
HTTPCACHE_MONGODB_PASSWORD = None
HTTPCACHE_MONGODB_AUTH_DB = None
HTTPCACHE_MONGODB_DB = 'cache_storage'
HTTPCACHE_MONGODB_COLL = 'cache'
HTTPCACHE_MONGODB_COLL_INDEX = [[('fingerprint', 1)]]
HTTPCACHE_MONGODB_CONNECTION_POOL_KWARGS = {}

BANNED_STORAGE = 'scrapy_httpcache.extensions.banned_storage.MongoBannedStorage'
BANNED_MONGODB_COLL = 'banned'
BANNED_MONGODB_COLL_INDEX = [[('fingerprint', 1)]]

REQUEST_ERROR_STORAGE = 'scrapy_httpcache.extensions.request_error_storage.MongoRequestErrorStorage'
REQUEST_ERROR_MONGODB_COLL = 'request_error'
REQUEST_ERROR_MONGODB_COLL_INDEX = [[('fingerprint', 1)]]

