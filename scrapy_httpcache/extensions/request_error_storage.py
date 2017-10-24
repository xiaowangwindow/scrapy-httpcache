import datetime

from scrapy import Spider, Request
from scrapy.settings import Settings
from twisted.internet import defer
from scrapy_httpcache.utils import request_util
from scrapy_httpcache.extensions.base_storage import BaseStorage


class MongoRequestErrorStorage(BaseStorage):
    def __init__(self, settings):
        super().__init__(
            settings,
            'REQUEST_ERROR')

    @defer.inlineCallbacks
    def save_request_error(self, spider, request, exception):
        key = request_util.fingerprint(request)
        data = {
            'url': request.url,
            'exception': str(exception),
            'meta': request.meta,
            'update_time': datetime.datetime.now()
        }
        yield self._coll.update_one(
            {'fingerprint': key},
            {'$set': data},
            upsert=True
        )
