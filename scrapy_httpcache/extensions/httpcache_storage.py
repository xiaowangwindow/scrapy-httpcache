import datetime

import six
import txmongo
from scrapy import Spider, Request
from scrapy.settings import Settings

from scrapy.responsetypes import responsetypes
from scrapy.http import Headers, Response
from twisted.internet.defer import returnValue

from scrapy_httpcache.utils import request_util
from txmongo.filter import sort
from twisted.internet import defer

from scrapy_httpcache.extensions.base_storage import BaseStorage
from scrapy_httpcache.utils import request_util


def _convert_header(header):
    if isinstance(header, dict):
        return {_convert_header(k): _convert_header(v) for k, v in header.items()}
    elif isinstance(header, list):
        return [_convert_header(v) for v in header]
    elif isinstance(header, bytes):
        return header.decode('utf8')
    else:
        return header


class MongoDBCacheStorage(BaseStorage):
    def __init__(self, settings):
        super(MongoDBCacheStorage, self).__init__(
            settings,
            'HTTPCACHE')
        self.expiration_secs = settings.getint('HTTPCACHE_EXPIRATION_SECS')
        self.db_client = None

    @defer.inlineCallbacks
    def retrieve_response(self, spider, request):
        data = yield self._read_data(spider, request)
        if not data:
            if six.PY2:
                returnValue()
            else:
                return None
        url = data['url']
        status = data['status']
        headers = Headers(data['headers'])
        body = data['body']
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body, request=request)
        if six.PY2:
            returnValue(response)
        else:
            return response


    @defer.inlineCallbacks
    def remove_response(self, spider, request, response):
        key = request_util.fingerprint(request)
        yield self._coll.delete_one(
            {'fingerprint': key}
        )

    @defer.inlineCallbacks
    def store_response(self, spider, request, response):
        key = request_util.fingerprint(request)
        data = {
            'status': response.status,
            'url': response.url,
            'headers': _convert_header(response.headers),
            'body': response.body,
            'update_time': datetime.datetime.now()
        }
        yield self._coll.update_one(
            {'fingerprint': key},
            {'$set': data},
            upsert=True
        )

    @defer.inlineCallbacks
    def _read_data(self, spider, request):
        key = request_util.fingerprint(request)
        data = yield self._coll.find_one({'fingerprint': key})
        if not data:
            if six.PY2:
                returnValue()
            else:
                return
        if 0 < self.expiration_secs < (datetime.datetime.now - data['update_time']).seconds:
            yield self._coll.delete_one({'fingerprint': key})
            if six.PY2:
                returnValue()
            else:
                return
        if six.PY2:
            returnValue(data)
        else:
            return data

