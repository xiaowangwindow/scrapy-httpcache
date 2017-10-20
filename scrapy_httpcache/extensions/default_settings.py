# DOWNLOADER_MIDDLEWARES = {}
# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': None,
#     'scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware': 900,
# })

HTTPCACHE_STORAGE = 'scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage'
HTTPCACHE_MONGODB_STORAGE_URI = 'mongodb://10.255.0.0:27017'
HTTPCACHE_MONGODB_STORAGE_DB = 'cache_storage'
HTTPCACHE_MONGODB_STORAGE_COLL = 'cache'
HTTPCACHE_MONGODB_STORAGE_COLL_INDEX = [[('fingerprint', 1)]]

BANNED_STORAGE = 'scrapy_httpcache.extensions.banned_storage.MongoBannedStorage'
BANNED_MONGODB_STORAGE_URI = 'mongodb://10.255.0.0:27017'
BANNED_MONGODB_STORAGE_DB = 'banned_storage'
BANNED_MONGODB_STORAGE_COLL = 'banned'
BANNED_MONGODB_STORAGE_COLL_INDEX = [[('fingerprint', 1)]]

REQUEST_ERROR_STORAGE = 'scrapy_httpcache.extensions.request_error_storage.MongoRequestErrorStorage'
REQUEST_ERROR_MONGODB_STORAGE_URI = 'mongodb://10.255.0.0:27017'
REQUEST_ERROR_MONGODB_STORAGE_DB = 'request_error_storage'
REQUEST_ERROR_MONGODB_STORAGE_COLL = 'request_error'
REQUEST_ERROR_MONGODB_STORAGE_COLL_INDEX = [[('fingerprint', 1)]]

