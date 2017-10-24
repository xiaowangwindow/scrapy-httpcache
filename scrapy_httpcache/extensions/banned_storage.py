
import datetime

from scrapy import Spider
from scrapy.http import Request, Response
from twisted.internet import defer
from scrapy_httpcache.extensions.base_storage import BaseStorage
from scrapy_httpcache.utils import request_util

class MongoBannedStorage(BaseStorage):

    def __init__(self, settings):
        super().__init__(
            settings,
            'BANNED')

    @defer.inlineCallbacks
    def save_banned(self, spider, request, response):
        key = request_util.fingerprint(request)
        data = {
            'status': response.status,
            'url': response.url,
            'meta': request.meta,
            'headers': request_util.convert_header(response.headers),
            'body': response.body,
            'update_time': datetime.datetime.now()
        }
        yield self._coll.update_one(
            {'fingerprint': key},
            {'$set': data},
            upsert=True
        )
